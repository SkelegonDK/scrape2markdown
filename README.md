# Scrape2Markdown

A streamlined tool for converting web pages to markdown format, designed specifically for collecting documentation for RAG (Retrieval-Augmented Generation) systems and AI agents.

## Features
- Process multiple URLs simultaneously
- Convert HTML content to clean markdown format
- Real-time markdown preview
- Flexible content filtering options (class-based and element-based)
- Export options (clipboard copy and file download)
- Simple and intuitive two-column interface

## Installation

### Prerequisites
- Python 3.x
- pip package manager

### Setup
1. Create a virtual environment:
```bash
python -m venv Scrape2Markdown
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
```

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Using the Application:
   - Add URLs through the left sidebar interface
   - Manage URL list (add, remove, clear all)
   - Use filtering options to customize content extraction
   - Preview generated markdown in real-time
   - Export using clipboard copy or download as file with timestamp

### Content Filtering
- Class-based filtering with multiselect options
- Element-based filtering with multiselect options
- Customizable content extraction

### Export Options
- Copy entire content to clipboard
- Download as markdown file with timestamp
- Clean markdown export (removes URL headers)

## Project Documentation

### Development Workflow
The project maintains several key documentation files:

#### todo.md
- Tracks current implementation status and progress
- Lists prioritized goals and upcoming tasks
- Documents completed features with timestamps
- Requires explicit approval for modifying developer tasks
- Must be updated before and after any development work

#### design.md
- Contains project vision and technical architecture
- Documents feature specifications
- Tracks architectural decisions and rationale

#### documentation.md
- Technical documentation
- API references
- Library dependencies
- Setup instructions

## Technical Stack
- **Frontend**: Streamlit web interface
- **Backend**: Python-based processing pipeline
- **Core Libraries**:
  - `streamlit`: Web application framework
  - `beautifulsoup4`: HTML parsing
  - `requests`: HTTP requests
  - `markdownify`: HTML to markdown conversion
  - `pyperclip`: Cross-platform clipboard operations

## Data Flow
1. Document Collection:
   - URL validation and management
   - Duplicate prevention
2. Content Processing:
   - HTML content fetching
   - Content filtering
   - Markdown conversion
3. Output Generation:
   - Real-time preview
   - Export options
