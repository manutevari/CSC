import streamlit as st
from database import store_vector
from crawler import crawl_website

def add_knowledge(input_data):

    # If URL
    if input_data.startswith("http"):
        pages = crawl_website(input_data)
        return f"Added {pages} pages"

    # If plain text
    store_vector(input_data, source="manual")
    return "Knowledge added"
