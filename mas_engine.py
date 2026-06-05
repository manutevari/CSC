import os
import re

import requests
import streamlit as st

from builtin_guides import builtin_service_context
from database import vector_search
from guardrails import allowed_domains_label
from tavily_search import suggested_csc_urls, tavily_csc_search


TRUE_VALUES = {"1", "true", "yes", "on"}
FALSE_VALUES = {"0", "false", "no", "off"}

PERSONAL_DATA_PATTERNS = (
    ("AADHAAR", re.compile(r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}\b")),
    ("PAN", re.compile(r"\b[A-Z]{5}\d{4}[A-Z]\b", re.IGNORECASE)),
    ("EMAIL", re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)),
    ("PHONE", re.compile(r"(?<!\d)(?:\+91[\s-]?)?[6-9]\d{9}(?!\d)")),
    ("IFSC", re.compile(r"\b[A-Z]{4}0[A-Z0-9]{6}\b", re.IGNORECASE)),
    ("ACCOUNT", re.compile(r"\b(?:account|a/c|acct)[\s:.-]*(?:no\.?|number)?[\s:.-]*\d{9,18}\b", re.IGNORECASE)),
    ("DOB", re.compile(r"\b(?:dob|date of birth)[\s:.-]*\d{1,2}[\s/-]\d{1,2}[\s/-]\d{2,4}\b", re.IGNORECASE)),
)

CHILD_DATA_MARKERS = re.compile(
    r"\b(child|children|minor|student|school|class\s*[1-9]\d?|roll\s*(?:no|number)|guardian|parent)\b",
    re.IGNORECASE,
)

DEVANAGARI_PATTERN = re.compile(r"[\u0900-\u097F]")
HINDI_REQUEST_PATTERN = re.compile(r"\b(hindi|hindee|हिंदी|हिन्दी|हिंदि|हिन्दि)\b", re.IGNORECASE)


def _language(query, response_language="auto"):

    if response_language == "hi":
        return "hi"
    if response_language == "en":
        return "en"
    if DEVANAGARI_PATTERN.search(query or "") or HINDI_REQUEST_PATTERN.search(query or ""):
        return "hi"

    return "en"


def _is_hindi(query, response_language="auto"):

    return _language(query, response_language) == "hi"


def _secret(name, default=""):

    try:
        value = st.secrets.get(name, None)
    except Exception:
        value = None

    if value:
        return str(value).strip()

    return os.getenv(name, default).strip()


def _flag(name, default=False):

    value = _secret(name, "true" if default else "false").lower()
    if value in TRUE_VALUES:
        return True
    if value in FALSE_VALUES:
        return False

    return default


def _redact_personal_data(text):

    if not _flag("DPDP_REDACTION_ENABLED", True):
        return text

    redacted = text or ""
    for label, pattern in PERSONAL_DATA_PATTERNS:
        redacted = pattern.sub(f"[REDACTED_{label}]", redacted)

    return redacted


def _has_personal_data(text):

    return any(pattern.search(text or "") for _, pattern in PERSONAL_DATA_PATTERNS)


def _has_child_data(text):

    return bool(CHILD_DATA_MARKERS.search(text or ""))


def _sentiment_prefix(query, response_language="auto"):

    text = query or ""
    lower = text.lower()
    frustrated_terms = ("not working", "wrong", "bad", "issue", "problem", "angry", "frustrated", "urgent", "help")
    letters = [ch for ch in text if ch.isalpha()]
    caps_ratio = sum(1 for ch in letters if ch.isupper()) / max(1, len(letters))

    if any(term in lower for term in frustrated_terms) or (len(letters) >= 12 and caps_ratio > 0.65):
        if _is_hindi(query, response_language):
            return "समझ गया। मैं CSC/आधिकारिक स्रोतों की सीमा में रहते हुए सीधे उपयोगी उत्तर दे रहा हूं।\n\n"
        return "I understand. Let me give you the useful answer directly, while staying inside CSC-approved sources.\n\n"

    return ""


def _chat_endpoint(base_url):

    base = base_url.rstrip("/")
    if base.endswith("/chat/completions"):
        return base

    return f"{base}/chat/completions"


def _provider_chain():

    return [
        {
            "name": "Hugging Face",
            "key": _secret("HF_TOKEN") or _secret("HF_API_KEY") or _secret("HUGGINGFACE_API_KEY") or _secret("HUGGINGFACEHUB_API_TOKEN"),
            "base_url": _secret("HF_BASE_URL", "https://router.huggingface.co/v1"),
            "model": _secret("HF_MODEL", "Qwen/Qwen2.5-7B-Instruct"),
        },
        {
            "name": "OpenRouter",
            "key": _secret("OPENROUTER_API_KEY"),
            "base_url": _secret("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
            "model": _secret("OPENROUTER_MODEL", "meta-llama/llama-3.1-8b-instruct:free"),
        },
        {
            "name": "Grok",
            "key": _secret("GROK_API_KEY") or _secret("XAI_API_KEY"),
            "base_url": _secret("GROK_BASE_URL", "https://api.x.ai/v1"),
            "model": _secret("GROK_MODEL", "grok-2-latest"),
        },
    ]


def _llm_answer(provider, query, context, history=None, response_language="auto"):

    lang = _language(query, response_language)
    language_rule = (
        "Respond in Hindi using clear Devanagari Hindi. Keep official service names and URLs unchanged."
        if lang == "hi"
        else "Respond in English."
    )

    messages = [
        {
            "role": "system",
            "content": (
                "You are a CSC guardrailed chatbot. Answer only from retrieved CSC-approved website knowledge. "
                f"{language_rule} "
                f"Allowed source domains are: {allowed_domains_label()}. "
                "Do not use general knowledge, memory, assumptions, or non-CSC sources. "
                "If the retrieved knowledge does not answer the question, say: "
                "'I can answer only from approved CSC website data, and this was not found in the indexed CSC data.' "
                "Do not ask for Aadhaar, PAN, phone, bank, password, OTP, or child/minor personal data in chat. "
                "Explain like a Class 8 student can understand: short sentences, simple words, and numbered steps. "
                "Avoid legal/technical jargon unless the source uses the exact word, and explain that word simply. "
                "For form-filling help, give a VLE-friendly guide with: service/form name, official source URL, "
                "who can apply if stated, documents/prerequisites if stated, field-by-field filling guidance if stated, "
                "submission/verification steps if stated, mistakes to avoid, and DPDP privacy notes. "
                "Tell users to enter personal identifiers only inside the official CSC/service portal, not in this chat. "
                "If the source text does not contain a field, document, fee, eligibility rule, or step, say it is not found in the indexed CSC data. "
                "If the user's tone is frustrated or urgent, acknowledge briefly and then give the steps. "
                "Conversation history is only for continuity; it is not evidence."
            ),
        },
    ]

    for item in history or []:
        role = item.get("role", "user")
        content = item.get("content", "")
        if role in {"user", "assistant"} and content:
            messages.append({"role": role, "content": content[:1500]})

    user_content = f"Question:\n{query}"
    if context:
        user_content += f"\n\nRetrieved CSC-approved knowledge:\n{context}"
    else:
        user_content += "\n\nRetrieved CSC-approved knowledge: none available."

    messages.append({"role": "user", "content": user_content})
    payload = {
        "model": provider["model"],
        "messages": messages,
        "temperature": 0.2,
        "max_tokens": 700,
    }
    headers = {
        "Authorization": f"Bearer {provider['key']}",
        "Content-Type": "application/json",
        "User-Agent": "CSC-AI-Assistant/1.0",
    }
    if provider["name"] == "OpenRouter":
        headers["X-Title"] = "CSC AI Assistant"

    response = requests.post(
        _chat_endpoint(provider["base_url"]),
        json=payload,
        headers=headers,
        timeout=45,
    )
    response.raise_for_status()
    data = response.json()

    try:
        return data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, TypeError):
        return ""


def _format_urls(urls, response_language="auto"):

    if not urls:
        return ""

    lines = "\n".join(f"- {url}" for url in urls[:5])
    if response_language == "hi":
        return f"\n\nOfficial links जो मदद कर सकते हैं:\n{lines}"

    return f"\n\nOfficial links that may help:\n{lines}"


def _hindi_reason(reason):

    known = {
        "No approved source context is available for this question.": "इस प्रश्न के लिए अभी approved official source data उपलब्ध नहीं है।",
        "Possible child/minor personal data was detected.": "बच्चे/नाबालिग से जुड़ा संभावित personal data मिला है, इसलिए मैं केवल सुरक्षित सामान्य guidance दे सकता हूं।",
        "Verified source data is available, but live AI processing is not enabled.": "Verified source data उपलब्ध है, इसलिए मैं सुरक्षित local guidance दे रहा हूं।",
        "Live AI response is unavailable, so I am showing verified source guidance.": "Live AI response उपलब्ध नहीं है, इसलिए मैं verified source guidance दिखा रहा हूं।",
    }

    if reason in known:
        return known[reason]
    if reason == "Live search is not available.":
        return "Live search अभी उपलब्ध नहीं है।"
    if reason == "Tavily search failed.":
        return "Live official-source search सफल नहीं हुआ।"
    if reason == "No Tavily result matched the CSC allowlist.":
        return "Approved official source में matching result नहीं मिला।"

    return reason


def _public_reason(reason, response_language="auto"):

    if response_language == "hi":
        if reason in {"Live search is not available.", "Tavily search failed.", "No Tavily result matched the CSC allowlist."}:
            return "इस समय मुझे इस exact service/form की verified official detail नहीं मिल पा रही है।"
        return "इस exact service/form की पूरी verified detail मेरे पास अभी उपलब्ध नहीं है।"

    if reason in {"Live search is not available.", "Tavily search failed.", "No Tavily result matched the CSC allowlist."}:
        return "I cannot get verified official details for this exact service/form right now."

    return "I do not have enough verified details for this exact service/form yet."


def _guardrail_refusal(reason, urls=None, query="", response_language="auto"):

    if _is_hindi(query, response_language):
        return (
            _sentiment_prefix(query, response_language)
            + f"{_public_reason(reason, 'hi')}\n\n"
            "कृपया service/form का exact नाम लिखें, या नीचे दिए official links पर details check करें।"
            f"{_format_urls(urls or [], 'hi')}"
        )

    return (
        _sentiment_prefix(query, response_language)
        + f"{_public_reason(reason, 'en')}\n\n"
        "Please share the exact service name, or check the official links below for the service details."
        f"{_format_urls(urls or [], 'en')}"
    )


def _local_chatbot_answer(query, context, reason, response_language="auto"):

    if context:
        is_builtin_form_guide = (
            "Class 8 level guide" in context
            or "CSC form-filling guide for PAN card" in context
            or "PAN card form भरने की CSC guide" in context
            or "Class 8 level guide:" in context
        )
        if is_builtin_form_guide:
            if _is_hindi(query, response_language):
                reason = _hindi_reason(reason)
                return f"""{_sentiment_prefix(query, response_language)}यह approved CSC/official service source के आधार पर आसान guide है।

DPDP सुरक्षा: Aadhaar, PAN number, bank details, OTP, password या बच्चे/नाबालिग का personal data इस chat में न डालें। ऐसी जानकारी केवल official CSC/service portal में ही भरें।

{context}

{reason}
"""

            return f"""{_sentiment_prefix(query, response_language)}Here is the simple guide from approved CSC/official service sources.

DPDP safety: Do not paste Aadhaar, PAN number, bank details, OTP, passwords, or child/minor personal data in this chat. Enter those only inside the official CSC/service portal.

{context}

{reason}
"""

        if _is_hindi(query, response_language):
            reason = _hindi_reason(reason)
            return f"""{_sentiment_prefix(query, response_language)}मुझे स्वीकृत CSC/आधिकारिक सेवा डेटा मिला है और मैं local privacy mode में रहकर उत्तर दे रहा हूं।

Class 8 जैसी आसान भाषा में समझें: form भरना मतलब सही service चुनना, citizen की सही जानकारी भरना, documents लगाना, submit करना, और receipt/reference number सुरक्षित रखना।

नीचे दिए गए source के आधार पर service form भरें। DPDP सुरक्षा के लिए Aadhaar, PAN number, bank details, OTP, password या बच्चे/नाबालिग का personal data इस chat में न डालें। ऐसी जानकारी केवल official CSC/service portal में ही भरें।

Form भरने की checklist:
1. Source से सही CSC service/form name confirm करें।
2. Eligibility, documents, fee और prerequisites source में जांचें।
3. केवल वही fields भरें जो official form मांगता है।
4. Applicant के documents के अनुसार name, date, ID और contact details match करें।
5. Consent, declaration, payment और final submission status official portal पर review करें।
6. अगर कोई required field या document source में नहीं दिख रहा है, तो submission से पहले official CSC/service portal पर verify करें।

प्राप्त CSC source text:
{context}

{reason}
"""

        return f"""{_sentiment_prefix(query, response_language)}I found approved CSC/official service data and will stay in local privacy mode.

Class 8 simple meaning: filling a form means choosing the right service, entering correct citizen details, attaching required documents, submitting, and saving the receipt/reference number.

Use the source text below to fill the service form. For DPDP safety, do not paste Aadhaar, PAN, bank details, OTP, passwords, or child/minor personal data in this chat. Enter those only inside the official CSC/service portal.

Form-filling checklist:
1. Confirm the exact CSC service/form name from the source.
2. Check eligibility, documents, fee, and prerequisites in the source.
3. Fill only fields that the official form asks for.
4. Match names, dates, IDs, and contact details with the applicant's official documents.
5. Review consent, declaration, payment, and final submission status on the official portal.
6. If any required field or document is not visible in the source, verify it on the official CSC portal before submission.

Retrieved CSC source text:
{context}

{reason}
"""

    setup_hint = (
        "Please use an official CSC/service URL or ask with the exact service name."
    )

    if _is_hindi(query, response_language):
        reason = _hindi_reason(reason)
        return (
            _sentiment_prefix(query, response_language)
            + "मैं CSC guardrail mode में हूं और non-CSC data का उपयोग नहीं करूंगा। "
            f"{reason}\n\n"
            "कृपया official CSC/service URL या exact service name के साथ पूछें।"
        )

    return (
        _sentiment_prefix(query, response_language)
        + "I am running in CSC guardrail mode and will not use non-CSC data. "
        f"{reason}\n\n"
        f"{setup_hint}"
    )


def ask(query, cloud_consent=False, history=None, response_language="auto"):

    context = vector_search(query)
    suggested_urls = []

    if not context:
        builtin_context = builtin_service_context(query, language=_language(query, response_language))
        if builtin_context:
            context = builtin_context

    if not context:
        if not cloud_consent:
            suggested_urls = suggested_csc_urls(query, max_results=5)
            return _guardrail_refusal(
                "No approved source context is available for this question.",
                urls=suggested_urls,
                query=query,
                response_language=response_language,
            )

        live = tavily_csc_search(_redact_personal_data(query), max_results=5)
        context = live.get("context", "")
        suggested_urls = live.get("urls", [])

        if not context:
            return _guardrail_refusal(
                live.get("error") or "No approved source context is available for this question.",
                urls=suggested_urls,
                query=query,
                response_language=response_language,
            )

    sensitive_text = f"{query}\n{context}"

    if _has_child_data(sensitive_text) and _has_personal_data(sensitive_text) and not _flag("DPDP_ALLOW_CHILD_DATA_CLOUD", False):
        return _local_chatbot_answer(
            query,
            context,
            "Possible child/minor personal data was detected.",
            response_language=response_language,
        )

    if not cloud_consent:
        return _local_chatbot_answer(
            query,
            context,
            "Verified source data is available, but live AI processing is not enabled.",
            response_language=response_language,
        )

    safe_query = _redact_personal_data(query)
    safe_context = _redact_personal_data(context)
    safe_history = [
        {
            "role": item.get("role", "user"),
            "content": _redact_personal_data(item.get("content", "")),
        }
        for item in (history or [])[-8:]
    ]

    for provider in _provider_chain():
        if not provider["key"]:
            continue

        try:
            answer = _llm_answer(provider, safe_query, safe_context, history=safe_history, response_language=response_language)
        except Exception:
            continue

        if answer:
            if suggested_urls:
                return answer + _format_urls(suggested_urls, _language(query, response_language))
            return answer

    return _local_chatbot_answer(
        query,
        context,
        "Live AI response is unavailable, so I am showing verified source guidance.",
        response_language=response_language,
    )
