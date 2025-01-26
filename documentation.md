# Documentation for Scrape2Markdown

## Frontend
- Streamlit web interface
- Two-column layout for URL management and content preview
- Support for multiple URL processing
- Markdown preview functionality
- Word count statistics

## Backend
- Python-based processing pipeline
- HTML scraping and markdown conversion
- AI-powered content refinement using Ollama
- File saving capabilities

## APIs
- LangChain for AI orchestration and model integration
- BeautifulSoup for HTML parsing
- Markdownify for HTML to markdown conversion

## Libraries and packages

### LangChain Integration
LangChain provides a framework for developing applications powered by language models, with built-in support for Ollama integration.

#### Prerequisites
1. Ollama Installation
   - Ollama must be installed and running on your system
   - Visit [Ollama.com](https://ollama.com) for installation instructions

2. Required Model
   - Pull the deepseek model: `ollama pull deepseek-coder:6.7b`
   - This model is used for markdown refinement in our application

#### Installation
```bash
pip install langchain-core langchain-ollama
```

#### Usage in Our Application
We use LangChain with Ollama for AI-powered markdown refinement:

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.callbacks.base import BaseCallbackHandler

def process_with_deepseek(text):
    """Process markdown text with deepseek model for refinement using Langchain"""
    try:
        # Create text splitter for handling large documents
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=4000,
            chunk_overlap=200,
            length_function=len,
        )

        # Split text into chunks
        chunks = text_splitter.split_text(text)

        # Create Ollama model instance with LangChain
        llm = OllamaLLM(
            model="deepseek-coder:6.7b",
            temperature=0.7,
        )

        # Create prompt template
        prompt = ChatPromptTemplate.from_template(
            """Please refine and clean up this markdown documentation..."""
        )

        # Process chunks with streaming
        chain = prompt | llm
        response = chain.invoke(
            {"text": chunk},
            config={"callbacks": [StreamHandler(output_placeholder)]}
        )

        return response

    except Exception as e:
        st.error(f"Error processing with AI: {str(e)}")
        return None
```

#### Key Features
- Text splitting for large documents
- Streaming token output
- Progress tracking
- Context window management
- Chunk overlap for better context preservation

### Other Required Libraries
- `streamlit`: Web application framework
- `beautifulsoup4`: HTML parsing
- `requests`: HTTP requests
- `markdownify`: HTML to markdown conversion

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
pip install streamlit beautifulsoup4 requests markdownify langchain-core langchain-ollama
