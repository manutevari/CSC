def vector_search(query, top_k=5):
    embedding = get_embedding(query)

    cursor.execute(
        """
        SELECT content
        FROM documents
        ORDER BY embedding <=> %s::vector
        LIMIT %s
        """,
        (embedding, top_k)
    )

    results = cursor.fetchall()
    return [r[0] for r in results]
