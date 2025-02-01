# Project: Page to Markdown Converter

## Overview & Core Features
- Multiple URL Processing:
  - Users can add multiple URLs for conversion
  - Simple interface for managing URLs (add/remove)
  - Batch processing of all URLs
- HTML to Markdown Conversion:
  - Scrape HTML content from URLs using BeautifulSoup
  - Convert HTML to markdown using markdownify
  - Live preview of generated markdown
- Interactive Chat Interface:
  - Chat with processed markdown content
  - Context-aware responses using Ollama
  - Streaming responses for better UX
- Export Options:
  - Copy to clipboard functionality
  - Download as markdown file
  - Timestamp-based file naming

## Technical Stack & Architecture
- **Frontend**: 
  - Streamlit for web interface
  - Two-column layout for efficient workflow
  - Real-time markdown preview
  - Chat interface with streaming responses
- **Backend**: 
  - Python for core functionality
  - Ollama for LLM capabilities
- **Libraries**:
  - `streamlit`: UI components and interface
  - `requests`: URL content fetching
  - `beautifulsoup4`: HTML parsing
  - `markdownify`: HTML to markdown conversion
  - `langchain`: LLM integration and chat handling
  - `ollama`: Local LLM support

## Data Flow
1. Document Collection:
   - User adds URLs through input interface
   - Validate URLs and manage list state
2. Content Processing:
   - Fetch HTML content from each URL
   - Convert to markdown format
   - Combine markdown documents
3. Chat Integration:
   - Initialize Langchain with processed markdown
   - Handle user queries through chat interface
   - Stream contextual responses from Ollama
4. Output Options:
   - Preview markdown in real-time
   - Chat with content for clarification
   - Copy entire content to clipboard
   - Download as markdown file

## Decisions & Clarifications
- [2/1/2025] Separated from chat functionality:
  - Focused solely on HTML to markdown conversion
  - Simplified UI for better user experience
  - Added clipboard functionality
  - Maintained core URL processing features
