# Status

- Discover other pages at the same level.
- Add URL validation
- run find relevant pages in the list of URLs, rather than just the current page. Change the button to "Find Relevant Pages"
- Add css class filtering by scanning the page for all classes, and then filtering by class.

## Current Goals
- Priority 1: Streamline URL collection and markdown conversion
- Priority 2: Add URLs based on links in URL
- Priority 3: Add LLM features for rewriting and filtering content.


## Developer Tasks (Require approval to modify)


## Completed
- [x] Separate page-to-markdown functionality from chat features
  - Removed all AI/chat related code
  - Simplified UI and improved user experience
  - Last updated: 2/1/2025, 8:39 PM
- [x] Enhance export options
  - Added copy to clipboard functionality
  - Maintained download feature with timestamps
  - Last updated: 2/1/2025, 8:39 PM
- [x] Core functionality
  - URL list management (add, remove, clear all)
  - Duplicate URL prevention
  - Batch processing of all URLs
  - Combined markdown preview
- [x] UI Improvements
  - Two-column layout (management left, preview right)
  - Real-time markdown preview
  - Improved error handling and user feedback
- [x] Add flexible content filtering options
  - Added class-based filtering with multiselect
  - Added element-based filtering with multiselect
  - Improved UI with clear section headers
  - Last updated: 2/1/2025, 10:07 PM

## Next Up
- [x] Update Copy to clipboard
  - Replaced JavaScript clipboard with pyperclip
  - Added error handling for clipboard operations
  - Last updated: 2/3/2025, 10:00 PM

- [x] Streamline core functionality
  - Remove paragraph filtering
  - Move download button to sidebar
  - Remove chat-related features
  - Improve UI organization
- [ ] Add URL validation improvements
- [ ] Add intelligent URL selector  ( based on URL context )
- [ ] Enhance markdown formatting with LLMs
