from crawler import crawl_website
from database import store_vector


def add_knowledge(input_data, cloud_consent=False):

    if not cloud_consent:
        return "Knowledge was not stored because DPDP cloud storage/embedding consent was not granted."

    if input_data.startswith("http"):
        pages = crawl_website(input_data)
        stored = 0
        failed = 0

        for page in pages:
            ok, _ = store_vector(page["content"], source=page["url"])
            if ok:
                stored += 1
            else:
                failed += 1

        return f"{stored} pages added from website. {failed} pages failed."

    ok, message = store_vector(input_data, source="manual")
    if not ok:
        return message

    return message
