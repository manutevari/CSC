def crawl_website(base_url, max_pages=10):

    visited = set()

    to_visit = [base_url]

    pages_added = 0

    while to_visit and pages_added < max_pages:

        url = to_visit.pop(0)

        if url in visited:
            continue

        visited.add(url)

        text = extract_page_text(url)

        if len(text) > 200:

            chunks = chunk_document(text)

            for c in chunks:
                store_vector(c, source=url)

            pages_added += 1

        try:

            links = get_internal_links(url)

            for l in links:

                if l not in visited:
                    to_visit.append(l)

        except:
            pass

    return pages_added

