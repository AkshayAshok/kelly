"""
Streamlit UI Components for Kelly chatbot
"""
import streamlit as st
from datetime import datetime
from .config import KELLY_SYSTEM_PROMPT, DEFAULT_PRINCIPLES


def setup_page():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title="Kelly — AI Skeptical Poet",
        page_icon="🧪",
        layout="centered"
    )


def render_sidebar():
    """Render sidebar with settings and info"""
    with st.sidebar:
        st.markdown("## 🧪 Kelly — AI Skeptical Poet")
        st.caption("An AI scientist who only answers in poems: skeptical, analytical, and practical.")
        st.markdown("### System Notes")
        st.code(KELLY_SYSTEM_PROMPT[:300] + "...", language="markdown")
        
        with st.expander("Adjust Kelly's guiding principles (optional)"):
            new_principles = []
            for i, p in enumerate(st.session_state.principles):
                new_principles.append(st.text_input(f"Principle {i+1}", p, key=f"principle_{i}"))
            if st.button("Update principles"):
                st.session_state.principles = [p for p in new_principles if p.strip()]
                st.success("Updated Kelly's guiding principles.")
        
        st.divider()
        if st.button("Clear chat"):
            st.session_state.messages = []
            st.success("Cleared.")
        
        st.divider()
        st.caption("🔧 Backend: Groq API (Llama 3.3 70B)")
        st.caption("🎭 Frontend: Streamlit")


def render_header():
    """Render main header"""
    st.title("🧪 Kelly — AI Skeptical Poet")
    st.write("Ask anything about AI. Kelly replies **only in poetry**—skeptical, analytical, and ending with practical, evidence-based steps.")


def render_chat_history():
    """Display chat message history"""
    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"].replace("\n", "  \n"))


def render_footer():
    """Render footer with export button"""
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Export chat as .txt"):
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            raw = []
            for m in st.session_state.messages:
                raw.append(f"{m['role'].upper()}:\n{m['content']}\n")
            blob = "\n".join(raw)
            st.download_button(
                label="Download conversation",
                data=blob.encode("utf-8"),
                file_name=f"kelly_chat_{ts}.txt",
                mime="text/plain",
                use_container_width=True
            )
    with col2:
        st.caption("Tip: Deploy on Streamlit Community Cloud to get a public link.")


def initialize_session_state():
    """Initialize Streamlit session state"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "principles" not in st.session_state:
        st.session_state.principles = DEFAULT_PRINCIPLES.copy()
