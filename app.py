"""
Kelly - AI Skeptical Poet Chatbot
Main application entry point
"""
import streamlit as st
from src.api_manager import load_api_key, display_api_key_error
from src.poem_generator import KellyPoetGenerator
from src.ui_components import (
    setup_page,
    initialize_session_state,
    render_sidebar,
    render_header,
    render_chat_history,
    render_footer
)


def main():
    """Main application function"""
    # Setup
    setup_page()
    initialize_session_state()
    
    # Load API key
    API_KEY = load_api_key()
    
    if not API_KEY:
        display_api_key_error()
        st.stop()
    
    # Initialize poem generator
    generator = KellyPoetGenerator(api_key=API_KEY)
    
    # Render UI
    render_sidebar()
    render_header()
    render_chat_history()
    
    # Chat input
    prompt = st.chat_input("Ask Kelly a question about AI…")
    if prompt:
        # User message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Assistant message (Backend API call)
        with st.chat_message("assistant"):
            with st.spinner("Kelly is weighing the science and crafting verses…"):
                # Generate poem
                poem = generator.generate_poem(
                    prompt, 
                    extra_principles=st.session_state.principles
                )
                st.markdown(poem.replace("\n", "  \n"))
        
        st.session_state.messages.append({"role": "assistant", "content": poem})
    
    # Footer
    render_footer()


if __name__ == "__main__":
    main()
