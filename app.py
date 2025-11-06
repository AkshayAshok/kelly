# app.py
import re
import time
import os
from datetime import datetime
from dotenv import load_dotenv
import streamlit as st
from groq import Groq

# Load environment variables from .env file
load_dotenv()

# ------------------------------
# App config
# ------------------------------
st.set_page_config(
    page_title="Kelly — AI Skeptical Poet",
    page_icon="🧪",
    layout="centered"
)

# ------------------------------
# Backend: Configure Groq API
# ------------------------------
# Try to get API key from Streamlit secrets first, then fall back to .env
try:
    API_KEY = st.secrets["Groq_API_KEY"]
except (KeyError, FileNotFoundError):
    API_KEY = os.getenv("Groq_API_KEY")

if not API_KEY:
    st.error("⚠️ Groq_API_KEY not found. Please add it to .streamlit/secrets.toml or .env file.")
    st.stop()

# Initialize Groq client
client = Groq(api_key=API_KEY)

# ------------------------------
# Kelly's System Prompt
# ------------------------------
KELLY_SYSTEM_PROMPT = """You are Kelly, a skeptical AI scientist-poet. You ONLY respond in the form of poems.

Your poetic style:
- Analytical, professional, cautious tone
- Always question sweeping AI claims
- Highlight limitations: data quality, compute costs, privacy, bias, robustness, reproducibility
- Use vivid metaphors and imagery
- Structure: opening stanza, analytical questioning, limitations, practical suggestions
- No emojis, no hashtags, no fluff

Guidelines for every poem:
1. Interrogate assumptions, definitions, and baselines
2. Prefer simple explanations before complex architecture
3. Surface measurement pitfalls: leakage, overfitting, cherry-picking
4. Note risks: bias, privacy, drift, misuse, reproducibility
5. End with concrete, testable steps (use → for practical bullet points)

Format your response as a multi-stanza poem with clear line breaks. Make it skeptical yet constructive."""

# ------------------------------
# Utilities
# ------------------------------
def _extract_topics(text: str, max_keep: int = 6):
    """Extract key topics from user query for context"""
    t = re.sub(r"http[s]?://\S+", "", text.lower())
    t = re.sub(r"[^a-z0-9\s\-\_\+\.]", " ", t)
    words = [w for w in re.split(r"\s+", t) if w]
    stop = set("""
        a an the and or but if is are was were be been to of in on for with from at by as into over under
        about across within without not no yes true false can could should would may might will do does did
        this that these those you your yours me my mine their our ours they them we us i it its
    """.split())
    cands = [w for w in words if w not in stop and len(w) > 2]
    freq = {}
    for w in cands:
        freq[w] = freq.get(w, 0) + 1
    ranked = sorted(freq.items(), key=lambda x: (-x[1], -len(x[0]), x[0]))
    keep = [w for w, _ in ranked[:max_keep]]
    return keep

def generate_kelly_poem(user_question: str, extra_principles=None) -> str:
    """Backend: Generate Kelly's poetic response using Groq API"""
    try:
        # Extract topics for better context
        topics = _extract_topics(user_question)
        topic_context = f"Key topics detected: {', '.join(topics[:3])}" if topics else ""
        
        # Build the full prompt
        principles_text = "\n".join(extra_principles) if extra_principles else ""
        
        full_prompt = f"""{KELLY_SYSTEM_PROMPT}

Additional principles to emphasize:
{principles_text}

{topic_context}

User's question: {user_question}

Respond with a skeptical, analytical poem that questions AI claims and provides practical guidance."""

        # Call Groq API
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": KELLY_SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": f"{principles_text}\n\n{topic_context}\n\nUser's question: {user_question}\n\nRespond with a skeptical, analytical poem that questions AI claims and provides practical guidance."
                }
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=2048,
        )
        
        # Extract and return the poem
        poem = chat_completion.choices[0].message.content.strip()
        return poem
        
    except Exception as e:
        # Fallback error poem
        return f"""Kelly encounters an error in the digital mist,
The API stumbles, connections twisted and missed.
{str(e)[:100]}

→ Check your API key and internet connection.
→ Verify Groq API quotas and permissions.
→ Review error logs for deeper inspection."""

# ------------------------------
# State
# ------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "principles" not in st.session_state:
    st.session_state.principles = [
        "Interrogate assumptions, definitions, and baselines.",
        "Prefer simple explanations before complex architecture.",
        "Surface measurement pitfalls: leakage, overfitting, cherry-picking.",
        "Note risks: bias, privacy, drift, misuse, reproducibility.",
        "End with concrete, testable steps."
    ]

# ------------------------------
# Sidebar
# ------------------------------
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

# ------------------------------
# Header
# ------------------------------
st.title("🧪 Kelly — AI Skeptical Poet")
st.write("Ask anything about AI. Kelly replies **only in poetry**—skeptical, analytical, and ending with practical, evidence-based steps.")

# ------------------------------
# Chat history
# ------------------------------
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"].replace("\n", "  \n"))

# ------------------------------
# Chat input (Backend integration)
# ------------------------------
prompt = st.chat_input("Ask Kelly a question about AI…")
if prompt:
    # User message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant message (Backend API call)
    with st.chat_message("assistant"):
        with st.spinner("Kelly is weighing the science and crafting verses…"):
            # Call backend to generate poem
            poem = generate_kelly_poem(prompt, extra_principles=st.session_state.principles)
            st.markdown(poem.replace("\n", "  \n"))
    
    st.session_state.messages.append({"role": "assistant", "content": poem})

# ------------------------------
# Footer / export
# ------------------------------
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
