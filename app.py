from datetime import datetime

import requests
import streamlit as st
from bs4 import BeautifulSoup
from markdownify import markdownify


# Common filtering options
DEFAULT_FILTER_CLASSES = [
    "nav",
    "navbar",
    "navigation",
    "menu",
    "sidebar",
    "breadcrumb",
    "pagination",
    "toc",
    "table-of-contents",
    "header-nav",
    "footer-nav",
    "social-nav",
    "utility-nav",
    "site-nav",
    "main-nav",
    "sub-nav",
    "mobile-nav",
]

DEFAULT_FILTER_ELEMENTS = [
    "nav",
    "header",
    "footer",
    "aside",
    "menu",
    "dialog",
    "sidebar",
    "complementary",
    "banner",
]


def filter_elements(soup, filter_classes=None, filter_elements=None):
    """
    Filter elements from soup using find_all and remove specified tags

    :param soup: BeautifulSoup object
    :param filter_classes: List of CSS classes to filter
    :param filter_elements: List of tag names to filter and remove
    """
    if not soup:
        return soup

    # Normalize inputs
    filter_classes = filter_classes or []
    filter_elements = filter_elements or []

    # Convert single strings to lists
    filter_classes = (
        [filter_classes] if isinstance(filter_classes, str) else filter_classes
    )
    filter_elements = (
        [filter_elements] if isinstance(filter_elements, str) else filter_elements
    )

    try:
        # Remove specified elements
        if filter_elements:
            for tag in filter_elements:
                for element in soup.find_all(tag):
                    element.decompose()

        # Remove elements with specified classes
        if filter_classes:
            for element in soup.find_all(class_=True):
                element_classes = element.get("class", [])
                if any(cls in element_classes for cls in filter_classes):
                    element.decompose()

    except Exception as e:
        st.error(f"Filtering error: {str(e)}")
        raise

    return soup


# Configure the app for wide mode
st.set_page_config(layout="wide")

# Initialize session state variables if they don't exist
if "urls" not in st.session_state:
    st.session_state.urls = []
if "original_markdown" not in st.session_state:
    st.session_state.original_markdown = ""

# Streamlit app title
st.title("Page to Markdown")

# Sidebar: URL management and controls
with st.sidebar:
    st.header("Document Sources")

    st.subheader("Content Filtering")

    # Filter by class
    filter_classes = st.multiselect(
        "Filter out elements with these classes",
        options=DEFAULT_FILTER_CLASSES,
        help="Elements with these classes will be removed. Leave empty to keep all.",
    )

    # Filter by element type
    filter_elements = st.multiselect(
        "Filter out these HTML elements (including children)",
        options=DEFAULT_FILTER_ELEMENTS,
        help="These elements and all their children will be removed. Leave empty to keep all.",
    )

    # Optional: Paragraph length filtering
    st.markdown("**Paragraph Filtering**")
    paragraph_filter = st.selectbox(
        "Filter paragraphs by length",
        ["None", "Remove Long Paragraphs", "Remove Short Paragraphs"],
        help="Filter paragraphs based on text length",
    )

    st.markdown("---")

    # URL input and management
    url = st.text_input("Enter URL", placeholder="https://example.com")
    col1_btn, col2_btn = st.columns(2)

    with col1_btn:
        if st.button("Add URL"):
            if url:
                if url not in st.session_state.urls:
                    st.session_state.urls.append(url)
                    st.success(f"Added URL: {url}")
                else:
                    st.warning("URL already in list")
            else:
                st.warning("Please enter a valid URL")

    with col2_btn:
        if st.button("Clear All"):
            st.session_state.urls = []
            st.session_state.original_markdown = ""
            st.success("Cleared all URLs")

    # URL List
    st.write("**URL List:**")
    for i, url in enumerate(st.session_state.urls):
        col1_url, col2_url = st.columns([3, 1])
        with col1_url:
            st.text(url)
        with col2_url:
            if st.button("Remove", key=f"remove_{i}"):
                st.session_state.urls.pop(i)
                st.rerun()

    # Process URLs button
    if st.button("Process URLs"):
        if st.session_state.urls:
            combined_markdown = ""

            # Process each URL
            for url in st.session_state.urls:
                try:
                    with st.spinner(f"Fetching {url}..."):
                        response = requests.get(url, timeout=10)  # 10 second timeout
                        response.raise_for_status()  # Handle HTTP errors
                        soup = BeautifulSoup(response.content, "html.parser")
                        # Apply filtering
                        if filter_classes or filter_elements:
                            soup = filter_elements(
                                soup, filter_classes, filter_elements
                            )

                        # Apply paragraph filtering if selected
                        if paragraph_filter == "Remove Long Paragraphs":
                            for p in soup.find_all("p"):
                                if len(p.text.strip()) > 200:
                                    p.decompose()
                        elif paragraph_filter == "Remove Short Paragraphs":
                            for p in soup.find_all("p"):
                                if len(p.text.strip()) < 50:
                                    p.decompose()
                        markdown_text = markdownify(str(soup))
                        combined_markdown += (
                            f"\n\n## Content from {url}\n\n{markdown_text}"
                        )
                except requests.exceptions.Timeout:
                    st.error(
                        f"Timeout error fetching {url}. The request took too long to complete."
                    )
                except requests.exceptions.RequestException as e:
                    st.error(f"Error fetching {url}: {str(e)}")

            if combined_markdown:
                st.session_state.original_markdown = combined_markdown
                st.success("URLs processed successfully!")
        else:
            st.warning("Please add URLs to the list first")

# Main content: Markdown preview and actions
st.header("Markdown Preview")
if st.session_state.original_markdown:
    # Preview the markdown
    st.markdown(st.session_state.original_markdown)

    # Actions
    col1_action, col2_action, col3_action = st.columns(3)

    # Copy to clipboard button
    with col1_action:
        if st.button("Copy to Clipboard"):
            st.write(
                "<script>navigator.clipboard.writeText(`"
                + st.session_state.original_markdown.replace("`", "\\`")
                + "`);</script>",
                unsafe_allow_html=True,
            )
            st.success("Copied to clipboard!")

    # Download button
    with col2_action:
        st.download_button(
            label="Download Markdown",
            data=st.session_state.original_markdown,
            file_name=f"page_to_markdown_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown",
        )

    # Chat link
    with col3_action:
        st.link_button("Chat with Content", "Chat")

else:
    st.info("Process some URLs to see the markdown preview.")
