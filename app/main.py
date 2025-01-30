"""
Streamlit-based Coding Assistant powered by Ollama's DeepSeek model-R1:1.5B

Features:
- Interactive chat interface with message history
- Adjustable model parameters via sidebar
- Server connectivity checks
- Error handling and user feedback
- Responsive design with dark mode support
"""

import streamlit as st
import ollama
from dotenv import load_dotenv
import time
from typing import Dict, List, Any

# Load environment variables from .env file
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="DeepChat",
    page_icon="⚡",
    layout="centered"
)

# Custom CSS for enhanced UI components
STYLE_CSS = """
<style>
    /* Chat input styling */
    .stChatInput input {
        background-color: #f0f2f6 !important;
        color: #1a1a1a !important;
        border: 1px solid #d0d0d0 !important;
        border-radius: 8px !important;
        padding: 12px !important;
    }
    
    /* Dark mode adaptation */
    @media (prefers-color-scheme: dark) {
        .stChatInput input {
            background-color: #2d2d2d !important;
            color: #ffffff !important;
            border-color: #404040 !important;
        }
    }

    /* Message styling */
    .stChatMessage { 
        padding: 1rem; 
        border-radius: 8px; 
        margin: 0.5rem 0; 
    }
    
    /* Loading spinner alignment */
    [data-testid="stSpinner"] { 
        margin: 0 auto; 
    }
    
    /* Error message styling */
    .error-box { 
        padding: 1rem; 
        background: #ffe6e6; 
        border-radius: 4px; 
        border: 1px solid #ffcccc;
    }
</style>
"""

st.markdown(STYLE_CSS, unsafe_allow_html=True)

def initialize_session() -> None:
    """Initialize session state with default values.
    
    Sets up:
    - Chat message history with initial assistant message
    - Default model parameters for text generation
    """
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "How can I help you today? 🚀"}
        ]
    if "params" not in st.session_state:
        st.session_state.params = {
            "temperature": 0.7,    # Controls randomness (0=deterministic, 1=creative)
            "top_p": 0.9,          # Nucleus sampling probability threshold
            "num_predict": 512,    # Maximum tokens to generate
            "repeat_penalty": 1.1  # Penalty for repeated content
        }

def settings_sidebar() -> None:
    """Create sidebar controls for model parameters and chat management."""
    with st.sidebar:
        st.header("⚙️ Model Parameters")
        
        # Temperature control
        st.session_state.params["temperature"] = st.slider(
            "Temperature (Creativity)", 0.0, 1.0, 
            st.session_state.params["temperature"],
            help="Lower values produce more focused outputs, higher values increase creativity"
        )
        
        # Top-P sampling control
        st.session_state.params["top_p"] = st.slider(
            "Top-P Sampling", 0.1, 1.0, 
            st.session_state.params["top_p"],
            help="Consider only the top tokens with cumulative probability >= top_p"
        )
        
        # Response length control
        st.session_state.params["num_predict"] = st.slider(
            "Max Response Length", 128, 2048, 
            st.session_state.params["num_predict"], step=128,
            help="Maximum number of tokens to generate in the response"
        )
        
        # Repetition penalty control
        st.session_state.params["repeat_penalty"] = st.slider(
            "Repeat Penalty", 1.0, 2.0, 
            st.session_state.params["repeat_penalty"],
            help="Penalty factor for repeated phrases (higher = less repetition)"
        )
        
        # Chat history management
        if st.button("🧹 Clear Chat History", use_container_width=True):
            st.session_state.messages = [
                {"role": "assistant", "content": "How can I help you with coding today? 🚀"}
            ]
            st.rerun()

def display_chat() -> None:
    """Render chat messages from session history."""
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

def handle_query() -> None:
    """Process user input and generate model response with error handling."""
    if prompt := st.chat_input("Enter your coding question..."):
        try:
            # Add user message to history
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Display user message immediately
            with st.chat_message("user"):
                st.markdown(prompt)

            response_container = st.empty()
            
            # Generate model response
            with st.spinner("🔍 Analyzing and generating response..."):
                response = ollama.chat(
                    model='deepseek-r1:1.5b',
                    messages=st.session_state.messages,
                    stream=False,
                    options={
                        "temperature": st.session_state.params["temperature"],
                        "top_p": st.session_state.params["top_p"],
                        "num_predict": st.session_state.params["num_predict"],
                        "repeat_penalty": st.session_state.params["repeat_penalty"]
                    }
                )
                
                # Validate response structure
                if 'message' not in response or 'content' not in response['message']:
                    raise ValueError("Invalid response format from Ollama API")
                
                reply = response['message']['content']

                # Display and store assistant response
                with response_container.chat_message("assistant"):
                    st.markdown(reply)
                
                st.session_state.messages.append({"role": "assistant", "content": reply})

        except Exception as e:
            # Error handling and user feedback
            st.markdown(f"""
            <div class="error-box">
                ⚠️ **Generation Error**  
                {str(e)}  
                *Last message has been removed from history*
            </div>
            """, unsafe_allow_html=True)
            # Remove failed interaction from history
            st.session_state.messages.pop()

def main() -> None:
    """Main application workflow."""
    st.title("DeepChat 🤖💬")
    st.caption("DeepChat: Powered by 🐋DeepSeek-R1:1.5B, Ollama & Streamlit | by faizy")
    
    # Phase 1: Server connectivity check
    try:
        server_status = ollama.list()
    except ollama.ClientError as e:
        st.error(f"""
        ## 🔌 Connection Error  
        Failed to connect to Ollama server:  
        `{str(e)}`  

        **Troubleshooting Steps:**  
        1. Verify Ollama service is running (`ollama serve`)  
        2. Check network connectivity  
        3. Review firewall/port settings  
        4. Ensure correct API endpoint configuration
        """)
        st.stop()
    except Exception as e:
        st.error(f"Unexpected connection error: {str(e)}")
        st.stop()

    # Phase 2: Model verification
    try:
        if 'models' not in server_status:
            st.error(f"""
            ## 📦 Unexpected Response Format  
            Received server response:  
            ```python
            {server_status}
            ```  
            Please verify your Ollama server version and configuration
            """)
            st.stop()

        # Check for required model availability
        model_found = any(
            m.get('model') == 'deepseek-r1:1.5b' or 
            m.get('name') == 'deepseek-r1:1.5b' 
            for m in server_status['models']
        )

        if not model_found:
            st.error(f"""
            ## 🚫 Model Not Found  
            Required model `deepseek-r1:1.5b` not installed.  

            **Installation Instructions:**  
            ```bash
            ollama pull deepseek-r1:1.5b
            ```  
            After installation, restart the application
            """)
            st.stop()

    except KeyError as e:
        st.error(f"Missing expected field in server response: {str(e)}")
        st.stop()

    # Phase 3: Application runtime
    initialize_session()
    settings_sidebar()
    display_chat()
    handle_query()

if __name__ == "__main__":
    main()