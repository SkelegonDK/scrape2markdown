# Documentation for Scrape2Markdown

## Frontend
- Streamlit web interface
- Two-column layout:
  - Left sidebar: URL management and filtering controls
  - Right main area: Content preview
- Support for multiple URL processing
- Real-time markdown preview
- Export options in sidebar

## Backend
- Python-based processing pipeline
- HTML scraping and markdown conversion
- Content filtering system
- File saving capabilities

## APIs
- BeautifulSoup for HTML parsing
- Markdownify for HTML to markdown conversion

## Libraries and packages
### Required Libraries
- `streamlit`: Web application framework
  - Provides UI components and state management
  - Handles file downloads
- `beautifulsoup4`: HTML parsing
  - Extracts content from web pages
  - Supports element and class-based filtering
- `requests`: HTTP requests
  - Fetches content from URLs
  - Handles timeouts and errors
- `markdownify`: HTML to markdown conversion
  - Converts HTML content to clean markdown
  - Preserves important formatting
- `pyperclip`: Cross-platform clipboard operations
  - Provides native clipboard functionality
  - Handles copying text to system clipboard

## Virtual Environments
It's recommended to use a virtual environment for this project:

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- On macOS/Linux:
```bash
source venv/bin/activate
```
- On Windows:
```bash
.\venv\Scripts\activate
```

3. Install required packages:
```bash
pip install streamlit beautifulsoup4 requests markdownify pyperclip
