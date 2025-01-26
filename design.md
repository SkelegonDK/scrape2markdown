# Project: Streamlit App for HTML to Markdown Conversion

## Overview & Core Features
- Multiple URL Processing:
  - Users can add multiple URLs containing API documentation
  - List interface for managing URLs (add/remove)
  - Batch processing of all URLs
- HTML to Markdown Conversion:
  - Scrape HTML content from URLs using BeautifulSoup
  - Convert HTML to markdown using markdownify
  - Preview of generated markdown documents
- AI-Powered Refinement:
  - Use LangChain with Ollama integration
  - Dynamic model selection from installed Ollama models
  - Split large documents into manageable chunks
  - Process with configurable context windows
  - Stream token-by-token output with progress tracking
  - Make documentation concise and clear
  - Display both original and refined versions
- File Output:
  - Save refined markdown to files
  - Automatic naming based on date/time
  - Option for custom filenames
  - Word count token counter

## Technical Stack & Architecture
- **Frontend**: 
  - Streamlit for web interface
  - Two-column layout with URL list and preview
- **Backend**: 
  - Python for core functionality
  - Ollama integration for AI refinement
- **Libraries**:
  - `streamlit`: UI components
  - `requests`: URL content fetching
  - `beautifulsoup4`: HTML parsing
  - `markdownify`: HTML to markdown conversion
  - `langchain-core`: Core LangChain functionality
  - `langchain-ollama`: Ollama integration through LangChain

## Data Flow
1. URL Collection:
   - User adds URLs to list
   - Validate URLs and manage list state
2. Content Processing:
   - Fetch HTML content from each URL
   - Convert to markdown format
   - Combine markdown documents
3. AI Refinement:
   - Split content into manageable chunks
   - Process each chunk with deepseek-coder through LangChain
   - Stream refined output with progress tracking
4. Output:
   - Save to markdown file
   - Display preview and statistics

## Decisions & Clarifications
- [1/26/2025] Added dynamic model selection:
  - Integrated Ollama API to fetch available models
  - Added model selector in sidebar
  - Moved AI settings to dedicated sidebar section
- [1/26/2025] Chosen Streamlit for its simplicity and ease of use in creating web applications
- [1/26/2025] Selected BeautifulSoup for HTML parsing due to its robustness
- [1/26/2025] Decided to use markdownify for HTML to markdown conversion
- [1/26/2025] Selected deepseek-coder:6.7b model for its superior code understanding capabilities
- [1/26/2025] Implemented file output for persistent storage of refined documentation
- [1/26/2025] Integrated LangChain for better AI orchestration and document handling:
  - Improved text splitting with RecursiveCharacterTextSplitter
  - Added configurable context window controls
  - Enhanced streaming with LangChain callbacks
