from database import vector_search


def ask(query):

    context = vector_search(query)

    response = f"""
Relevant knowledge:

{context}

Answer:
"""

    return response
