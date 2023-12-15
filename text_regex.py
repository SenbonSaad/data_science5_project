import streamlit as st
import re

def text_regex():
    st.title("Regex Text File Processor")

    # Option to choose between uploading a file or typing text
    option = st.radio("Choose an option", ["Upload a Text File", "Type Text"])

    if option == "Upload a Text File":
        uploaded_file = st.file_uploader("Choose a file", type=["txt"])
        if uploaded_file is not None:
            file_contents = uploaded_file.read().decode("utf-8")  # Decode the bytes to string
            st.text_area("File Contents", file_contents)
    else:
        st.subheader("Type or paste your text below:")
        file_contents = st.text_area("Text Input")

    # Input regex pattern
    regex_pattern = st.text_input("Enter Regex Pattern")

    # Apply regex
    if st.button("Apply Regex"):
        try:
            if not file_contents:
                st.warning("No text to process. Please upload a file or type text.")
            else:
                result = re.findall(regex_pattern, file_contents)
                st.write("Regex Match Result:")
                st.write(result)
        except re.error as e:
            st.error(f"Error in regex pattern: {e}")
