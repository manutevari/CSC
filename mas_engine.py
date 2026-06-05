import os
import re

import requests
import streamlit as st

from database import vector_search


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


def _llm_answer(provider, query, context, history=None):

    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful CSC AI chatbot. Be conversational, practical, and concise. "
                "Use retrieved knowledge when it is provided. If no retrieved knowledge is available, "
                "answer from general CSC/service-center knowledge and clearly say when the user should verify locally. "
                "Do not ask for Aadhaar, PAN, phone, bank, password, OTP, or child/minor personal data in chat."
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
        user_content += f"\n\nRetrieved knowledge:\n{context}"
    else:
        user_content += "\n\nRetrieved knowledge: none available."

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


def _local_chatbot_answer(query, context, reason):

    if context:
        return f"""I found this saved knowledge and can use it locally:

{context}

{reason}
"""

    setup_hint = (
        "To enable full AI chat, add `HF_TOKEN` in Streamlit secrets and turn on `Allow cloud AI processing`. "
        "OpenRouter and Grok are still fallbacks if their keys are configured."
    )

    return (
        "I am running in DPDP privacy-safe local mode right now, so I will not send this chat to a cloud LLM. "
        f"{reason}\n\n"
        f"{setup_hint}\n\n"
        "You can ask me about CSC app setup, privacy settings, knowledge upload, database configuration, or deployment troubleshooting."
    )


def ask(query, cloud_consent=False, history=None):

    context = vector_search(query)

    sensitive_text = f"{query}\n{context}"

    if _has_child_data(sensitive_text) and _has_personal_data(sensitive_text) and not _flag("DPDP_ALLOW_CHILD_DATA_CLOUD", False):
        return _local_chatbot_answer(
            query,
            context,
            "Cloud LLM processing is off because possible child/minor personal data was detected.",
        )

    if not cloud_consent:
        return _local_chatbot_answer(
            query,
            context,
            "Cloud LLM processing is off because DPDP cloud-processing consent was not granted.",
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
            answer = _llm_answer(provider, safe_query, safe_context, history=safe_history)
        except Exception:
            continue

        if answer:
            return answer

    return _local_chatbot_answer(
        query,
        context,
        "No configured cloud LLM responded successfully.",
    )
