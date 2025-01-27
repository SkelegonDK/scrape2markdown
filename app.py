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
if "models" not in st.session_state:
    st.session_state.models = []
if "selected_model" not in st.session_state:
    st.session_state.selected_model = "llama3.2:latest"
if "context_info" not in st.session_state:
    st.session_state.context_info = {
        "max_context": 0,
        "chunk_size": 0,
        "chunk_overlap": 0,
        "total_tokens": 0,
        "num_chunks": 0,
    }


class StreamHandler(BaseCallbackHandler):
    """Callback handler for streaming LLM responses to Streamlit"""

    def __init__(self, container):
        self.container = container
        self.text = ""

    def on_llm_new_token(self, token: str, **kwargs):
        """Callback for new tokens from the LLM"""
        self.text += token
        self.container.markdown(self.text)


def get_ollama_models():
    """Fetch available models from Ollama API"""
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            models = [model["name"] for model in response.json()["models"]]
            if not models:  # If no models are found
                st.warning("No Ollama models found. Using default model.")
                return ["llama3.2:latest"]
            return models
        else:
            st.error("Failed to connect to Ollama API. Using default model.")
            return ["llama3.2:latest"]
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to Ollama. Please ensure Ollama is running.")
        return ["llama3.2:latest"]
    except Exception as e:
        st.error(f"Error fetching Ollama models: {str(e)}")
        return ["llama3.2:latest"]  # Fallback to default


def process_with_deepseek(text):
    """Process markdown text with deepseek model for refinement using Langchain"""
    try:
        # Create LLM instance with dynamic context
        llm = OllamaLLM(
            model=st.session_state.selected_model,
            temperature=0.7,
        )

        # Get max context and set optimal chunks
        max_context = llm.get_model_default_max_length() or 4096  # Fallback to 4096
        chunk_size = max_context - 1000  # Buffer for prompt
        chunk_overlap = int(chunk_size * 0.1)  # 10% overlap

        # Create text splitter with dynamic settings
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )

        # Split text into chunks
        chunks = text_splitter.split_text(text)

        # Update context info
        st.session_state.context_info = {
            "max_context": max_context,
            "chunk_size": chunk_size,
            "chunk_overlap": chunk_overlap,
            "total_tokens": len(text.split()),  # Approximate token count
            "num_chunks": len(chunks),
        }

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


# Fetch available models on app start
if not st.session_state.models:
    st.session_state.models = get_ollama_models()

# Streamlit app title
st.title("HTML to Markdown Converter")

with st.sidebar:
    st.header("AI Settings")

    # Model selection
    st.session_state.selected_model = st.selectbox(
        "Select Ollama Model",
        options=st.session_state.models,
        index=st.session_state.models.index(st.session_state.selected_model),
        help="Choose the Ollama model for markdown refinement",
    )

    # Context information display
    st.header("Context Information")
    if st.session_state.context_info["max_context"] > 0:
        st.metric(
            "Max Context Size", f"{st.session_state.context_info['max_context']} tokens"
        )
        st.metric("Chunk Size", f"{st.session_state.context_info['chunk_size']} tokens")
        st.metric(
            "Chunk Overlap", f"{st.session_state.context_info['chunk_overlap']} tokens"
        )
        st.metric("Number of Chunks", st.session_state.context_info["num_chunks"])

        # Calculate and display context utilization
        total_context_used = (
            st.session_state.context_info["chunk_size"]
            * st.session_state.context_info["num_chunks"]
        )
        context_utilization = (
            total_context_used / st.session_state.context_info["max_context"]
        ) * 100

        st.metric("Context Utilization", f"{context_utilization:.1f}%")

        # Show warning if high utilization
        if context_utilization > 90:
            st.warning(
                "High context utilization! Consider processing in smaller batches."
            )
    else:
        st.info("Context information will appear after processing text.")

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
