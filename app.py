import streamlit as st
from bs4 import BeautifulSoup
import requests
from markdownify import markdownify

# Streamlit app title
st.title("HTML to Markdown Converter")

# Left column for URL input
with st.container():
    col1, col2 = st.columns(2)

    with col1:
        url = st.text_input("Enter URL", placeholder="https://example.com")
        if st.button("Convert"):
            if url:
                try:
                    response = requests.get(url)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.content, "html.parser")
                    markdown_text = markdownify(str(soup))

                    # Update the right column with markdown preview and word count
                    col2.markdown("**Markdown Preview:**")
                    col2.markdown(markdown_text)

                    # Word count token counter
                    word_count = len(markdown_text.split())
                    col2.write(f"**Word Count: {word_count}**")
                except requests.exceptions.RequestException as e:
                    st.error(f"Error fetching the URL: {e}")
            else:
                st.warning("Please enter a valid URL.")
