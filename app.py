import streamlit as st
from mas_engine import ask
from knowledge import add_knowledge, index_csc_service_guides
from guardrails import allowed_domains_label

st.set_page_config(page_title="CSC AI Assistant")

st.title("CSC AI Assistant")

# Chat memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:

    st.header("Privacy")
    cloud_consent = st.checkbox(
        "Allow Tavily search and cloud AI for chatbot",
        value=False,
        help="When off, questions stay local and only the built-in CSC URL catalog is suggested.",
    )
    st.caption("Live mode uses Tavily for CSC/official service URLs, then Hugging Face/OpenRouter/Grok after redaction.")
    st.caption(f"CSC data guardrail: {allowed_domains_label()}")
    response_language = st.selectbox("Response language", ["Auto", "English", "Hindi"], index=0)
    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()

    st.header("Add Knowledge")

    url_input = st.text_input("Paste CSC or official service URL")

    if st.button("Add Knowledge"):

        if url_input:
            status = add_knowledge(url_input, cloud_consent=cloud_consent)
            if cloud_consent and "failed" not in status.lower() and "unavailable" not in status.lower() and "missing" not in status.lower():
                st.success(status)
            else:
                st.warning(status)
        else:
            st.warning("Paste an allowed CSC or official service URL first.")

    if st.button("Index CSC service guides"):
        status = index_csc_service_guides(cloud_consent=cloud_consent)
        if cloud_consent and "failed" not in status.lower() and "not indexed" not in status.lower():
            st.success(status)
        else:
            st.warning(status)

    st.caption("Try: Explain all Digital Seva service forms in Class 8 level. How do I fill the PAN card form?")

# Chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input
query = st.chat_input("Ask CSC related question")

if query:

    history = st.session_state.messages[-8:]

    st.session_state.messages.append({
        "role": "user",
        "content": query
    })

    with st.chat_message("user"):
        st.write(query)

    language_map = {"Auto": "auto", "English": "en", "Hindi": "hi"}
    answer = ask(query, cloud_consent=cloud_consent, history=history, response_language=language_map[response_language])

    with st.chat_message("assistant"):
        st.write(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
