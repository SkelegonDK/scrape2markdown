# Project Brief: Scrape2Markdown

## Core Purpose
Scrape2Markdown is a streamlined tool for converting web pages to markdown format, specifically designed for collecting documentation for RAG (Retrieval-Augmented Generation) systems and AI agents.

## Core Requirements

### URL Processing
- Process multiple URLs simultaneously
- Validate and manage URL list (add, remove, clear)
- Prevent duplicate URLs
- Support batch processing of all URLs

### Content Processing
- Convert HTML content to clean markdown format
- Provide flexible content filtering options:
  - Class-based filtering
  - Element-based filtering
- Real-time markdown preview
- Maintain content structure and formatting

### Export Capabilities
- Copy to clipboard functionality
- Download as markdown file with timestamp
- Clean markdown export (removes URL headers)

### User Interface
- Simple and intuitive two-column interface
- Left sidebar for URL management and controls
- Right main area for content preview
- Real-time preview updates

## Technical Requirements
- Python 3.x environment
- Web-based interface using Streamlit
- Efficient HTML processing pipeline
- Cross-platform clipboard support
- Error handling and user feedback

## Project Goals
1. Streamline URL collection and markdown conversion
2. Add capability to process URLs based on page context
3. Integrate LLM features for content enhancement
4. Improve URL validation
5. Maintain clean, maintainable codebase

## Success Criteria
- Successful conversion of multiple web pages to markdown
- Clean, readable markdown output
- Intuitive user experience
- Reliable error handling
- Efficient processing pipeline
