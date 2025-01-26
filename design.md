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
  - Use LangChain with Ollama's deepseek-coder model
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
  - `ollama`: AI model integration

## Data Flow
1. URL Collection:
   - User adds URLs to list
   - Validate URLs and manage list state
2. Content Processing:
   - Fetch HTML content from each URL
   - Convert to markdown format
   - Combine markdown documents
3. AI Refinement:
   - Process combined content with deepseek-r1
   - Generate refined version
4. Output:
   - Save to markdown file
   - Display preview and statistics

## Decisions & Clarifications
- [1/26/2025] Chosen Streamlit for its simplicity and ease of use in creating web applications
- [1/26/2025] Selected BeautifulSoup for HTML parsing due to its robustness
- [1/26/2025] Decided to use markdownify for HTML to markdown conversion
- [1/26/2025] Selected deepseek-r1 model for its superior reasoning capabilities
- [1/26/2025] Implemented file output for persistent storage of refined documentation
