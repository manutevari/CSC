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

    st.header("Add Knowledge")

    text_input = st.text_area("Paste knowledge")

    url_input = st.text_input("Paste URL")

    if st.button("Add Knowledge"):

        if text_input:
            add_knowledge(text_input)
            st.success("Knowledge added")

        elif url_input:
            add_knowledge(url_input)
            st.success("URL added")


# Chat history
for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.write(msg["content"])


# Chat input
query = st.chat_input("Ask CSC related question")

if query:

    st.session_state.messages.append({
        "role":"user",
        "content":query
    })

    with st.chat_message("user"):
        st.write(query)

    answer = ask(query)

    with st.chat_message("assistant"):
        st.write(answer)

    st.session_state.messages.append({
        "role":"assistant",
        "content":answer
    })
