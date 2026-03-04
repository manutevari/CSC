from database import store_vector
from crawler import crawl_website


def add_knowledge(input_data):

    if input_data.startswith("http"):
        pages = crawl_website(input_data)
        return f"{pages} pages added from website"

    store_vector(input_data, source="manual")

    return "Knowledge added successfully"
