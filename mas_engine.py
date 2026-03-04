from database import vector_search
from knowledge import add_knowledge

def ask(query):

    context = vector_search(query)

    response = f"""
Relevant knowledge:

{context}

Answer:
"""

    return response
