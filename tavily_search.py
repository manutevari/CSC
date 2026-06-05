import requests

from guardrails import allowed_domains, is_allowed_url, setting
from service_catalog import service_urls


TAVILY_ENDPOINT = "https://api.tavily.com/search"


def _tavily_key():

    return setting("TAVILY_API_KEY") or setting("TAVILY_KEY")


def _fallback_urls(query, limit):

    terms = [term.strip(".,:;?!()[]{}") for term in (query or "").lower().split()]
    terms = [term for term in terms if len(term) >= 4]
    ranked = []

    for url in service_urls():
        score = sum(1 for term in terms if term and term in url.lower())
        ranked.append((score, url))

    ranked.sort(key=lambda item: item[0], reverse=True)
    urls = [url for score, url in ranked if score > 0]
    urls.extend([url for _, url in ranked if url not in urls])

    return urls[:limit]


def suggested_csc_urls(query, max_results=5):

    return _fallback_urls(query, max_results)


def tavily_csc_search(query, max_results=5):

    key = _tavily_key()
    if not key:
        return {
            "context": "",
            "urls": _fallback_urls(query, max_results),
            "error": "Live search is not available.",
        }

    payload = {
        "query": query,
        "topic": "general",
        "search_depth": "advanced",
        "max_results": max_results,
        "include_answer": False,
        "include_raw_content": True,
        "include_domains": list(allowed_domains()),
    }
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "User-Agent": "CSC-AI-Assistant/1.0",
    }

    try:
        response = requests.post(TAVILY_ENDPOINT, json=payload, headers=headers, timeout=25)
        if response.status_code in {401, 403}:
            legacy_payload = dict(payload)
            legacy_payload["api_key"] = key
            response = requests.post(
                TAVILY_ENDPOINT,
                json=legacy_payload,
                headers={"Content-Type": "application/json", "User-Agent": "CSC-AI-Assistant/1.0"},
                timeout=25,
            )
        response.raise_for_status()
        data = response.json()
    except Exception:
        return {
            "context": "",
            "urls": _fallback_urls(query, max_results),
            "error": "Tavily search failed.",
        }

    blocks = []
    urls = []

    for item in data.get("results", []):
        url = str(item.get("url", "")).strip()
        if not is_allowed_url(url):
            continue

        title = str(item.get("title", "")).strip()
        content = str(item.get("content", "") or item.get("raw_content", "") or "").strip()
        raw = str(item.get("raw_content", "") or "").strip()
        text = raw or content
        if not text:
            continue

        urls.append(url)
        blocks.append(
            "Source: {url}\nTitle: {title}\nCSC page text:\n{text}".format(
                url=url,
                title=title or url,
                text=text[:3500],
            )
        )

    if not blocks:
        return {
            "context": "",
            "urls": _fallback_urls(query, max_results),
            "error": "No Tavily result matched the CSC allowlist.",
        }

    return {"context": "\n\n".join(blocks), "urls": urls, "error": ""}
