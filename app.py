import streamlit as st
from mas_engine import ask
from knowledge import add_knowledge

st.set_page_config(page_title="CSC AI Assistant")

st.title("CSC AI Assistant")

# Chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:

    st.header("Privacy")
    cloud_consent = st.checkbox(
        "Allow cloud AI processing",
        value=False,
        help="When off, questions and retrieved knowledge stay local in this app.",
    )
    st.caption("Cloud AI uses Hugging Face first, then OpenRouter, then Grok after redaction.")
    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()

    st.header("Add Knowledge")

    text_input = st.text_area("Paste knowledge")
    url_input = st.text_input("Paste URL")

    if st.button("Add Knowledge"):

        if text_input:
            status = add_knowledge(text_input, cloud_consent=cloud_consent)
            if cloud_consent and "unavailable" not in status.lower() and "missing" not in status.lower() and "could not" not in status.lower():
                st.success(status)
            else:
                st.warning(status)

        elif url_input:
            status = add_knowledge(url_input, cloud_consent=cloud_consent)
            if cloud_consent and "failed" not in status.lower() and "unavailable" not in status.lower() and "missing" not in status.lower():
                st.success(status)
            else:
                st.warning(status)

# Chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input
query = st.chat_input("Ask CSC related question")

if query:

    st.session_state.messages.append({
        "role": "user",
        "content": query
    })

    with st.chat_message("user"):
        st.write(query)

    answer = ask(query, cloud_consent=cloud_consent)

    with st.chat_message("assistant"):
        st.write(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
