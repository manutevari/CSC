import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

def clean_text(soup):

    # remove unwanted tags
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text_parts = []

    for tag in soup.find_all(["h1","h2","h3","h4","p","li"]):
        text = tag.get_text(strip=True)
        if text:
            text_parts.append(text)

    return " ".join(text_parts)


def crawl_website(start_url, max_pages=5):

    visited = set()
    to_visit = [start_url]

    pages = []

    domain = urlparse(start_url).netloc

    while to_visit and len(pages) < max_pages:

        url = to_visit.pop(0)

        if url in visited:
            continue

        visited.add(url)

        try:

            r = requests.get(
                url,
                headers=HEADERS,
                timeout=10,
                allow_redirects=True,
                verify=True
            )

            if "text/html" not in r.headers.get("Content-Type",""):
                continue

            soup = BeautifulSoup(r.text, "html.parser")

            content = clean_text(soup)

            pages.append({
                "url": url,
                "content": content
            })

            # find internal links
            for link in soup.find_all("a", href=True):

                absolute = urljoin(url, link["href"])
                link_domain = urlparse(absolute).netloc

                if domain in link_domain and absolute not in visited:
                    to_visit.append(absolute)

        except Exception as e:
            print("Crawler error:", e)

    return pages
