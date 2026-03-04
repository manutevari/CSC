import streamlit as st
import psycopg2
from openai import OpenAI

# Database connection
conn = psycopg2.connect(
    host=st.secrets["DB_HOST"],
    port=st.secrets["DB_PORT"],
    database=st.secrets["DB_NAME"],
    user=st.secrets["DB_USER"],
    password=st.secrets["DB_PASSWORD"],
    sslmode="require"
)

cursor = conn.cursor()

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


def store_vector(text, source="manual"):

    emb = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    ).data[0].embedding

    vector = "[" + ",".join(map(str, emb)) + "]"

    cursor.execute(
        """
        INSERT INTO documents (content, embedding, source)
        VALUES (%s, %s, %s)
        """,
        (text, vector, source)
    )

    conn.commit()


def vector_search(query, top_k=5):

    emb = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    ).data[0].embedding

    vector = "[" + ",".join(map(str, emb)) + "]"

    cursor.execute(
        """
        SELECT content
        FROM documents
        ORDER BY embedding <-> %s::vector
        LIMIT %s
        """,
        (vector, top_k)
    )

    return "\n".join([r[0] for r in cursor.fetchall()])
