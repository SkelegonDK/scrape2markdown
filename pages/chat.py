import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOllama

# Configure the page
st.set_page_config(layout="wide")
st.title("Chat with Content")

# Check if there's markdown content to chat about
if (
    "original_markdown" not in st.session_state
    or not st.session_state.original_markdown
):
    st.warning(
        "Please process some URLs in the main page first to generate content for chat."
    )
    st.stop()

# Initialize chat-specific session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation" not in st.session_state:
    st.session_state.conversation = None

# Initialize Ollama and conversation chain if not already initialized
if st.session_state.conversation is None:
    llm = ChatOllama(model="llama2")
    template = """You are a helpful assistant that discusses the following content:

{context}

Current conversation:
{history}
Human: {input}
Assistant:"""

    prompt: PromptTemplate = PromptTemplate(
        input_variables=["context", "history", "input"], template=template
    )

    memory = ConversationBufferMemory(memory_key="history", input_key="input")

    st.session_state.conversation = LLMChain(
        llm=llm, prompt=prompt, memory=memory, verbose=True
    )

    # Add markdown content as context
    st.session_state.conversation.predict(
        context=st.session_state.original_markdown, input="Let's discuss this content."
    )

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("Ask about the content..."):
    # Display user message
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get and display assistant response
    with st.chat_message("assistant"):
        response = st.session_state.conversation.predict(
            context=st.session_state.original_markdown, input=prompt
        )
        st.write(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
