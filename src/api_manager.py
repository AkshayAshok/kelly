"""
API Key Management
"""
import os
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st


def load_api_key() -> str:
    """
    Load API key from multiple sources with fallback
    
    Priority:
    1. Streamlit secrets
    2. Environment variable
    3. Direct .env file reading
    
    Returns:
        API key string or None
    """
    # Get script directory
    script_dir = Path(__file__).parent.parent
    env_path = script_dir / '.env'
    
    # Load environment variables
    load_dotenv(dotenv_path=env_path)
    
    API_KEY = None
    
    # Method 1: Try Streamlit secrets
    try:
        API_KEY = st.secrets["Groq_API_KEY"]
    except Exception:
        pass
    
    # Method 2: Try environment variable
    if not API_KEY:
        API_KEY = os.getenv("Groq_API_KEY")
    
    # Method 3: Try reading .env file directly
    if not API_KEY:
        try:
            env_file = script_dir / '.env'
            if env_file.exists():
                with open(env_file, 'r') as f:
                    for line in f:
                        if line.startswith('Groq_API_KEY='):
                            API_KEY = line.split('=', 1)[1].strip()
                            break
        except Exception:
            pass
    
    return API_KEY


def display_api_key_error():
    """Display helpful error message when API key is not found"""
    st.error("⚠️ Groq_API_KEY not found. Please add it to .streamlit/secrets.toml or .env file.")
    st.write("**Debug info:**")
    st.write(f"- Environment variable 'Groq_API_KEY': {os.getenv('Groq_API_KEY')}")
    st.write(f"- Secrets available: {list(st.secrets.keys()) if hasattr(st, 'secrets') else 'No secrets'}")
    
    script_dir = Path(__file__).parent.parent
    st.write(f"- Script directory: {script_dir}")
    st.write(f"- .env file exists: {(script_dir / '.env').exists()}")
