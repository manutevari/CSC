import psycopg2
from openai import OpenAI

# connect database
conn = psycopg2.connect(
    host="aws-1-ap-south-1.pooler.supabase.com",
    port=6543,
    database="postgres",
    user="postgres",
    password="YOUR_PASSWORD",
    sslmode="require"
)

cursor = conn.cursor()

client = OpenAI()

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


def search_similar(query, top_k=5):

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

    return [r[0] for r in cursor.fetchall()]
