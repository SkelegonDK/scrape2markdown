from datetime import datetime
import re
import requests
import streamlit as st
import pyperclip
from bs4 import BeautifulSoup
from markdownify import markdownify


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


def filter_html_elements(
    soup: BeautifulSoup,
    filter_classes: list[str] | str | None = None,
    filter_elements: list[str] | str | None = None,
) -> BeautifulSoup | None:
    """
    Filter elements from soup using find_all and remove specified tags

    Args:
        soup: BeautifulSoup object to filter
        filter_classes: List of CSS classes or single class to filter out
        filter_elements: List of HTML tag names or single tag to filter out

    Returns:
        BeautifulSoup: Filtered soup object
    """
    if not soup:
        return soup

    # Convert inputs to lists
    if filter_classes is None:
        filter_classes = []
    elif isinstance(filter_classes, str):
        filter_classes = [filter_classes]

    if filter_elements is None:
        filter_elements = []
    elif isinstance(filter_elements, str):
        filter_elements = [filter_elements]

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


def get_all_classes(soup: BeautifulSoup) -> list[str]:
    """
    Extract all unique class names from a BeautifulSoup object

    Args:
        soup: BeautifulSoup object to analyze

    Returns:
        list[str]: Sorted list of unique class names
    """
    classes = set()
    for element in soup.find_all(class_=True):
        classes.update(element.get("class", []))
    return sorted(classes)


# Initialize session state variables if they don't exist
if "urls" not in st.session_state:
    st.session_state.urls = []
if "original_markdown" not in st.session_state:
    st.session_state.original_markdown = ""
if "available_classes" not in st.session_state:
    st.session_state.available_classes = []

# Streamlit app title


# Sidebar: URL management and controls
with st.sidebar:
    st.title("Page2Markdown")
    st.subheader("Content Filtering")

    # Analyze Classes button

    # Filter by class
    selected_filter_classes = st.multiselect(
        "Filter out elements with these classes",
        options=st.session_state.available_classes,
        help="Elements with these classes will be removed. Click 'Analyze Classes' to update the list.",
    )

    # Filter by element type
    selected_filter_elements = st.multiselect(
        "Filter out these HTML elements (including children)",
        options=DEFAULT_FILTER_ELEMENTS,
        help="These elements and all their children will be removed. Leave empty to keep all.",
    )

    st.markdown("---")

    # URL input and management
    url = st.text_input("Enter URL", placeholder="https://example.com")
    col1_btn, col2_btn, col3_btn = st.columns(3)

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
            st.session_state.available_classes = []
            st.success("Cleared all URLs and analyzed classes")

    with col3_btn:
        if st.button("Analyze Classes"):
            if st.session_state.urls:
                all_classes = set()
                with st.spinner("Analyzing classes in URLs..."):
                    for url in st.session_state.urls:
                        try:
                            response = requests.get(url, timeout=10)
                            response.raise_for_status()
                            soup = BeautifulSoup(response.content, "html.parser")
                            all_classes.update(get_all_classes(soup))
                        except Exception as e:
                            st.error(f"Error analyzing {url}: {str(e)}")

                    st.session_state.available_classes = sorted(all_classes)
                    st.success(f"Found {len(all_classes)} unique classes")
            else:
                st.warning("Please add URLs to analyze")

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
                        if selected_filter_classes or selected_filter_elements:
                            filtered_soup = filter_html_elements(
                                soup, selected_filter_classes, selected_filter_elements
                            )
                            if filtered_soup is not None:
                                soup = filtered_soup

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

                # Clean markdown by removing URL headers
                clean_markdown = re.sub(
                    r"\n*## Content from https?://[^\n]*\n*",
                    "\n",
                    st.session_state.original_markdown,
                )
                # Download button
                st.download_button(
                    label="Download Markdown",
                    data=clean_markdown,
                    file_name=f"page_to_markdown_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                    mime="text/markdown",
                )
                # Copy to clipboard button
                if st.button("Copy to Clipboard"):
                    try:
                        pyperclip.copy(st.session_state.original_markdown)
                        st.success("Text copied successfully!")
                    except Exception as e:
                        st.error(f"Failed to copy to clipboard: {str(e)}")
        else:
            st.warning("Please add URLs to the list first")

# Main content: Markdown preview and actions
st.header("Markdown Preview")
if st.session_state.original_markdown:
    # Preview the markdown
    st.markdown(st.session_state.original_markdown)

    # Copy to clipboard button
    # if st.button("Copy to Clipboard"):
    #     try:
    #         pyperclip.copy(st.session_state.original_markdown)
    #         st.success("Text copied successfully!")
    #     except Exception as e:
    #         st.error(f"Failed to copy to clipboard: {str(e)}")

else:
    st.info("Process some URLs to see the markdown preview.")
