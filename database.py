import psycopg2
import streamlit as st

conn = psycopg2.connect(
    host=st.secrets["DB_HOST"],
    port=st.secrets["DB_PORT"],
    database=st.secrets["DB_NAME"],
    user=st.secrets["DB_USER"],
    password=st.secrets["DB_PASSWORD"],
    sslmode="require"
)

cursor = conn.cursor()
