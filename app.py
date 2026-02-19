import streamlit as st
from agent import preview_organization, execute_organization
from rag_engine import index_documents, answer_question

st.title("🧠 Personal AI File Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "folder" not in st.session_state:
    st.session_state.folder = None

if "preview_data" not in st.session_state:
    st.session_state.preview_data = None


# ---------- Display Chat ----------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


user_input = st.chat_input("Ask or command...")


if user_input:

    st.session_state.messages.append({"role": "user", "content": user_input})
    lower = user_input.lower()

    # -------- Set Folder --------
    if lower.startswith("set folder"):
        folder = user_input.replace("set folder", "").strip()
        st.session_state.folder = folder
        index_documents(folder)
        reply = f"Folder set. I can now read and search your files."

    # -------- Preview Organize --------
    elif "organize" in lower:

        if not st.session_state.folder:
            reply = "Please set a folder first using: set folder <path>"

        else:
            with st.spinner("Analyzing files..."):
                preview = preview_organization(st.session_state.folder)
                st.session_state.preview_data = preview

            reply = "I prepared an organization plan. Review below and type **confirm** to proceed."

    # -------- Confirm Move --------
    elif lower == "confirm":

        if st.session_state.preview_data:
            execute_organization(st.session_state.folder, st.session_state.preview_data)
            st.session_state.preview_data = None
            reply = "Files organized successfully."
        else:
            reply = "No pending organization."

    # -------- RAG Question --------
    else:
        if not st.session_state.folder:
            reply = "Please set a folder first using: set folder <path>"
        else:
            reply = answer_question(user_input)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()


# ---------- Show Preview ----------
if st.session_state.preview_data:

    st.subheader("📊 Organization Preview")

    for item in st.session_state.preview_data:
        st.write("📄", item["file"])
        st.write("➡️", item["category"])
        st.write("💡", item["reason"])
        st.divider()
