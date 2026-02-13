import streamlit as st
from agent import preview_organization, execute_organization

st.title("🧠 AI File Organizer")

folder = st.text_input("Enter Folder Path")

if "preview_data" not in st.session_state:
    st.session_state.preview_data = None


if st.button("Preview Organization"):

    if folder:
        with st.spinner("Analyzing files..."):
            preview = preview_organization(folder)
            st.session_state.preview_data = preview


if st.session_state.preview_data:

    st.subheader("📊 Organization Preview")

    for item in st.session_state.preview_data:

        st.write("📄 File:", item["file"])
        st.write("➡️ Suggested Folder:", item["category"])
        st.write("💡 Reason:", item["reason"])
        st.divider()


if st.session_state.preview_data and st.button("Confirm and Organize Files"):

    execute_organization(folder, st.session_state.preview_data)

    st.success("Files Organized Successfully!")
    st.session_state.preview_data = None
