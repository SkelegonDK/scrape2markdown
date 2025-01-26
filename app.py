import os
from datetime import datetime
import streamlit as st
from bs4 import BeautifulSoup
import requests
from markdownify import markdownify
from langchain_core.prompts import ChatPromptTemplate

from langchain_ollama.llms import OllamaLLM
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.callbacks.base import BaseCallbackHandler

# Configure the app for wide mode
st.set_page_config(layout="wide")


# Initialize session state variables if they don't exist
if "urls" not in st.session_state:
    st.session_state.urls = []
if "original_markdown" not in st.session_state:
    st.session_state.original_markdown = ""
if "refined_markdown" not in st.session_state:
    st.session_state.refined_markdown = ""
if "chunk_size" not in st.session_state:
    st.session_state.chunk_size = 4000
if "chunk_overlap" not in st.session_state:
    st.session_state.chunk_overlap = 200


class StreamHandler(BaseCallbackHandler):
    """Callback handler for streaming LLM responses to Streamlit"""

    def __init__(self, container):
        self.container = container
        self.text = ""

    def on_llm_new_token(self, token: str, **kwargs):
        """Callback for new tokens from the LLM"""
        self.text += token
        self.container.markdown(self.text)


def process_with_deepseek(text):
    """Process markdown text with deepseek model for refinement using Langchain"""
    try:
        # Create text splitter for handling large documents
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=st.session_state.chunk_size,
            chunk_overlap=st.session_state.chunk_overlap,
            length_function=len,
        )

        # Split text into chunks
        chunks = text_splitter.split_text(text)

        # Create Ollama model instance with LangChain
        llm = OllamaLLM(
            model="deepseek-r1:32b",
            temperature=0.7,
        )

        # Create prompt template
        prompt = ChatPromptTemplate.from_template(
            """Please refine and clean up this markdown documentation to make it more concise and clear, while preserving all important information:

{text}

Focus on:
1. Removing redundant information
2. Improving clarity and readability
3. Maintaining technical accuracy
4. Preserving all important details
5. Ensuring proper markdown formatting"""
        )

        # Create a placeholder for streaming output
        output_placeholder = st.empty()
        stream_handler = StreamHandler(output_placeholder)

        # Process each chunk and combine results
        refined_text = ""
        progress_bar = st.progress(0)

        for i, chunk in enumerate(chunks):
            # Update progress
            progress = (i + 1) / len(chunks)
            progress_bar.progress(progress)

            # Process chunk with model using LangChain
            chain = prompt | llm
            response = chain.invoke(
                {"text": chunk}, config={"callbacks": [stream_handler]}
            )

            refined_text += response + "\n\n"

        progress_bar.empty()
        return refined_text

    except Exception as e:
        st.error(f"Error processing with AI: {str(e)}")
        return None


# Streamlit app title
st.title("HTML to Markdown Converter")

# Main container with columns
with st.container():
    col1, col2 = st.columns(2)

    with col1:
        # URL input and add button
        url = st.text_input("Enter URL", placeholder="https://example.com")
        col1_buttons = st.columns(3)

        with col1_buttons[0]:
            if st.button("Add URL"):
                if url:
                    if url not in st.session_state.urls:
                        st.session_state.urls.append(url)
                        st.success(f"Added URL: {url}")
                    else:
                        st.warning("URL already in list")
                else:
                    st.warning("Please enter a valid URL")

        with col1_buttons[1]:
            if st.button("Clear All"):
                st.session_state.urls = []
                st.session_state.original_markdown = ""
                st.session_state.refined_markdown = ""
                st.success("Cleared all URLs")

        # Display list of URLs with remove buttons
        st.write("**URL List:**")
        for i, url in enumerate(st.session_state.urls):
            col1_url = st.columns([3, 1])
            with col1_url[0]:
                st.text(url)
            with col1_url[1]:
                if st.button("Remove", key=f"remove_{i}"):
                    st.session_state.urls.pop(i)
                    st.rerun()

        # Context window controls
        st.write("---")
        st.write("**Context Window Settings**")
        st.session_state.chunk_size = st.slider(
            "Chunk Size",
            min_value=1000,
            max_value=8000,
            value=st.session_state.chunk_size,
            step=500,
            help="Size of text chunks to process (in characters)",
        )
        st.session_state.chunk_overlap = st.slider(
            "Chunk Overlap",
            min_value=0,
            max_value=1000,
            value=st.session_state.chunk_overlap,
            step=50,
            help="Overlap between chunks to maintain context",
        )

        # Convert button for batch processing
        if st.button("Convert All"):
            if st.session_state.urls:
                combined_markdown = ""
                total_word_count = 0

                # Process each URL
                for url in st.session_state.urls:
                    try:
                        with st.spinner(f"Fetching {url}..."):
                            response = requests.get(url)
                            response.raise_for_status()
                            soup = BeautifulSoup(response.content, "html.parser")
                            markdown_text = markdownify(str(soup))
                            combined_markdown += (
                                f"\n\n## Content from {url}\n\n{markdown_text}"
                            )
                            total_word_count += len(markdown_text.split())
                    except requests.exceptions.RequestException as e:
                        st.error(f"Error fetching {url}: {e}")

                if combined_markdown:
                    st.session_state.original_markdown = combined_markdown
                    st.session_state.original_word_count = total_word_count
            else:
                st.warning("Please add URLs to the list first")

        # AI Refinement button
        if st.session_state.original_markdown:
            if st.button("Refine with AI"):
                with st.spinner("Processing with AI..."):
                    refined_text = process_with_deepseek(
                        st.session_state.original_markdown
                    )
                    if refined_text:
                        st.session_state.refined_markdown = refined_text
                        refined_word_count = len(refined_text.split())
                        st.session_state.refined_word_count = refined_word_count

    with col2:
        # Display original markdown if available
        if st.session_state.original_markdown:
            st.write("**Original Markdown Preview:**")
            st.markdown(st.session_state.original_markdown)
            st.write(f"**Word Count: {st.session_state.original_word_count}**")

        # Display refined version if available
        if st.session_state.refined_markdown:
            st.write("**Refined Markdown Preview:**")
            st.markdown(st.session_state.refined_markdown)
            st.write(f"**Refined Word Count: {st.session_state.refined_word_count}**")
            st.write(
                f"**Word Count Reduction: {st.session_state.original_word_count - st.session_state.refined_word_count} words**"
            )

            # File saving section
            if st.session_state.original_markdown or st.session_state.refined_markdown:
                st.write("---")
                st.write("**Save to File**")
                default_filename = (
                    f"documentation_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                )
                filename = st.text_input(
                    "File name (without extension)", value=default_filename
                )

                save_cols = st.columns(2)
                with save_cols[0]:
                    if st.button("Save Original"):
                        if st.session_state.original_markdown:
                            filepath = f"{filename}_original.md"
                            with open(filepath, "w") as f:
                                f.write(st.session_state.original_markdown)
                            st.success(f"Saved original markdown to {filepath}")

                with save_cols[1]:
                    if st.button("Save Refined"):
                        if st.session_state.refined_markdown:
                            filepath = f"{filename}_refined.md"
                            with open(filepath, "w") as f:
                                f.write(st.session_state.refined_markdown)
                            st.success(f"Saved refined markdown to {filepath}")
