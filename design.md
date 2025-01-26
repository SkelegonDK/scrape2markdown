# Project: Streamlit App for HTML to Markdown Conversion

## Overview & Core Features
- The app will allow users to input URLs containing API documentation in HTML format.
- It will scrape the HTML content from these URLs and convert it into markdown using BeautifulSoup.
- A preview of the generated markdown document will be displayed on the right side of the app.
- A word count token counter will also be shown alongside the markdown preview.

## Technical Stack & Architecture
- **Frontend**: Streamlit for creating the web interface.
- **Backend**: Python for handling URL input, HTML scraping, and conversion to markdown.
- **Libraries**:
  - `streamlit`: For building the user interface.
  - `requests`: For fetching HTML content from URLs.
  - `beautifulsoup4`: For parsing HTML and converting it into markdown.
  - `markdownify`: For converting HTML to markdown.

## Data Models & API Design
- No specific data models are required as the app will primarily handle URL inputs and outputs.
- The app will not interact with any external APIs other than those specified by the user for fetching HTML content.

## Decisions & Clarifications
- [1/26/2025] Chosen Streamlit for its simplicity and ease of use in creating web applications.
- [1/26/2025] Selected BeautifulSoup for HTML parsing due to its robustness and ease of integration with Python.
- [1/26/2025] Decided to use `markdownify` for converting HTML to markdown as it provides a straightforward way to handle the conversion process.
