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
  - Flexible content filtering options
- Export Options:
  - Copy to clipboard functionality
  - Download as markdown file with timestamp
  - Clean markdown export (removes URL headers)

## Technical Stack & Architecture
- **Frontend**: 
  - Streamlit for web interface
  - Two-column layout for efficient workflow
  - Real-time markdown preview
  - Sidebar for URL management and filtering
- **Backend**: 
  - Python for core functionality
  - Efficient HTML processing and conversion
- **Libraries**:
  - `streamlit`: UI components and interface
  - `requests`: URL content fetching
  - `beautifulsoup4`: HTML parsing
  - `markdownify`: HTML to markdown conversion

## Data Flow
1. Document Collection:
   - User adds URLs through input interface
   - Validate URLs and manage list state
2. Content Processing:
   - Fetch HTML content from each URL
   - Apply content filtering (classes and elements)
   - Convert to markdown format
   - Combine markdown documents
3. Output Options:
   - Preview markdown in real-time
   - Copy entire content to clipboard
   - Download clean markdown file

## Decisions & Clarifications
- [2/1/2025] Separated from chat functionality:
  - Focused solely on HTML to markdown conversion
  - Simplified UI for better user experience
  - Added clipboard functionality
  - Maintained core URL processing features
- [2/3/2025] Streamlined core functionality:
  - Removed paragraph filtering for simpler workflow
  - Moved download button to sidebar for better organization
  - Removed chat-related features to focus on conversion
  - Enhanced content filtering options
