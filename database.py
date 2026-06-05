import os

import psycopg2
import streamlit as st
from openai import OpenAI

from guardrails import is_allowed_source


DB_SECRET_NAMES = ("DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD")
EMBEDDING_MODEL = "text-embedding-3-small"


def _secret(name, default=""):

    try:
        value = st.secrets.get(name, None)
    except Exception:
        value = None

    if value:
        return str(value).strip()

    return os.getenv(name, default).strip()


def _safe_log(message):

    try:
        print(message)
    except Exception:
        pass


def _missing_secret_message(names):

    return "Missing required Streamlit secrets: " + ", ".join(names)


def _openai_client():

    key = _secret("OPENAI_API_KEY")
    if not key:
        return None, _missing_secret_message(["OPENAI_API_KEY"])

    return OpenAI(api_key=key), ""


def _db_connection():

    missing = [name for name in DB_SECRET_NAMES if not _secret(name)]
    if missing:
        return None, _missing_secret_message(missing)

    try:
        conn = psycopg2.connect(
            host=_secret("DB_HOST"),
            port=_secret("DB_PORT"),
            database=_secret("DB_NAME"),
            user=_secret("DB_USER"),
            password=_secret("DB_PASSWORD"),
            sslmode="require",
        )
    except psycopg2.OperationalError as exc:
        _safe_log(f"Database connection failed: {exc.__class__.__name__}")
        return None, "Knowledge database is unavailable. Check Supabase database secrets and network access."

    return conn, ""


def _embedding(text):

    client, error = _openai_client()
    if error:
        return None, error

    try:
        emb = client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=text,
        ).data[0].embedding
    except Exception as exc:
        _safe_log(f"Embedding failed: {exc.__class__.__name__}")
        return None, "Embedding service is unavailable. Check OPENAI_API_KEY and billing/access."

    return emb, ""


def store_vector(text, source="manual"):

    if not is_allowed_source(source):
        return False, "Blocked by CSC guardrail. Knowledge source must be an allowed CSC website URL."

    emb, error = _embedding(text)
    if error:
        return False, error

    conn, error = _db_connection()
    if error:
        return False, error

    vector = "[" + ",".join(map(str, emb)) + "]"

    try:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO documents (content, embedding, source)
                    VALUES (%s, %s, %s)
                    """,
                    (text, vector, source),
                )
    except psycopg2.Error as exc:
        _safe_log(f"Database insert failed: {exc.__class__.__name__}")
        return False, "Knowledge could not be stored. Check the documents table and pgvector setup."
    finally:
        conn.close()

    return True, "Knowledge added successfully"


def vector_search(query, top_k=5):

    emb, error = _embedding(query)
    if error:
        return ""

    conn, error = _db_connection()
    if error:
        return ""

    vector = "[" + ",".join(map(str, emb)) + "]"

    try:
        with conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT content, source
                    FROM documents
                    ORDER BY embedding <-> %s::vector
                    LIMIT %s
                    """,
                    (vector, top_k * 8),
                )
                rows = cursor.fetchall()
    except psycopg2.Error as exc:
        _safe_log(f"Vector search failed: {exc.__class__.__name__}")
        return ""
    finally:
        conn.close()

    allowed_rows = [(content, source) for content, source in rows if is_allowed_source(source)]
    allowed_rows = allowed_rows[:top_k]

    return "\n\n".join([f"Source: {source}\n{content}" for content, source in allowed_rows])
