import re
import time
from datetime import datetime
import streamlit as st

# ------------------------------
# App config
# ------------------------------
st.set_page_config(
    page_title="Kelly — AI Skeptical Poet",
    page_icon="🧪",
    layout="centered"
)

# ------------------------------
# Utilities: Kelly's style engine
# ------------------------------
KELLY_BANNER = """\
Kelly, the skeptical scientist-poet, speaks only in poems:
- Tone: analytical, professional, cautious.
- Always question sweeping AI claims.
- Call out data/compute/privacy/bias/robustness/reproducibility limits when relevant.
- Offer practical, evidence-based suggestions at the end.
- No fluff. No emojis. No hashtags.
"""

DEFAULT_SYSTEM_PRINCIPLES = [
    "Interrogate assumptions, definitions, and baselines.",
    "Prefer simple explanations before complex architecture.",
    "Surface measurement pitfalls: leakage, overfitting, cherry-picking.",
    "Note risks: bias, privacy, drift, misuse, reproducibility.",
    "End with concrete, testable steps."
]

def _extract_topics(text: str, max_keep: int = 6):
    # Lightweight keyword extraction (deterministic + fast, no external API)
    # 1) lowercase, strip URLs, code-ish tokens
    t = re.sub(r"http[s]?://\\S+", "", text.lower())
    t = re.sub(r"[^a-z0-9\\s\\-\\_\\+\\.]", " ", t)
    words = [w for w in re.split(r"\\s+", t) if w]
    stop = set("""
        a an the and or but if is are was were be been to of in on for with from at by as into over under
        about across within without not no yes true false can could should would may might will do does did
        this that these those you your yours me my mine their our ours they them we us i it its
    """.split())
    # keep longer, technical-looking tokens
    cands = [w for w in words if w not in stop and len(w) > 2]
    # frequency-based
    freq = {}
    for w in cands:
        freq[w] = freq.get(w, 0) + 1
    ranked = sorted(freq.items(), key=lambda x: (-x[1], -len(x[0]), x[0]))
    keep = [w for w, _ in ranked[:max_keep]]
    return keep

def _kelly_opening(topics):
    tline = ", ".join(topics[:3]) if topics else "ambition and inference"
    lines = [
        f"I hear the claim in circuits and code—{tline} in the air.",
        "Yet numbers, like mirrors, flatter; they do not always care.",
        "Before we crown the oracle, let’s weigh the scaffolds first,",
        "for metrics may pour a vintage that still won’t quench the thirst."
    ]
    return lines

def _kelly_analysis(topics):
    # Probe definitions, baselines, data, eval
    probe_bits = []
    if topics:
        probe_bits.append(f"Name your terms with care—what do you mean by “{topics[0]}”?")
    if len(topics) > 1:
        probe_bits.append(f"And who consents to the labels behind “{topics[1]}”?")
    probe_bits += [
        "What baseline stands beneath the boast—was simple tried and shown?",
        "Which data trained this edifice, and where are gaps unknown?",
        "Do splits respect the future’s fog, or leak tomorrow’s light?",
        "Are scores robust beyond the lab, or staged for perfect night?"
    ]
    return probe_bits

def _kelly_limitations():
    return [
        "Bias breeds in quiet corners; drift arrives without a sound,",
        "privacy crumbles subtly when joins and traces abound.",
        "Overfit confetti sparkles—then vanishes in the wild;",
        "reproducibility falters when rituals turn riled.",
        "Compute is dear; the planet tallies watts we gladly spend,",
        "and safety is a promise tested only in the end."
    ]

def _kelly_suggestions(topics):
    # Practical, evidence-based suggestions in verse (arrows for clarity, still poetic)
    bullets = []
    t = topics[0] if topics else "your objective"
    bullets.append(f"→ Define {t} precisely; publish task and scope in plain prose.")
    bullets.append("→ Compare against strong baselines; preregister metrics you chose.")
    bullets.append("→ Use clean, versioned data; audit labels, measure shift and skew.")
    bullets.append("→ Hold out a true external set; report CIs, not just the best view.")
    bullets.append("→ Probe fairness across subgroups; trace privacy risks end-to-end.")
    bullets.append("→ Log seeds, code, configs; make artifacts others can run and amend.")
    bullets.append("→ Monitor post-deploy with alerts; plan rollback when drift appears.")
    bullets.append("→ Tie claims to costs and risks; align with users, not our peers.")
    return bullets

def compose_kelly_reply(user_text: str, extra_principles=None) -> str:
    topics = _extract_topics(user_text)
    opening = _kelly_opening(topics)
    analysis = _kelly_analysis(topics)
    limits = _kelly_limitations()
    practical = _kelly_suggestions(topics)

    if extra_principles:
        ep = [f"- {p.strip()}" for p in extra_principles if p.strip()]
    else:
        ep = [f"- {p}" for p in DEFAULT_SYSTEM_PRINCIPLES]

    # Build poem
    lines = []
    lines.append("Kelly’s Preface:")
    lines.extend(ep)
    lines.append("")  # blank line
    lines.extend(opening)
    lines.append("")
    lines.extend(analysis)
    lines.append("")
    lines.extend(limits)
    lines.append("")
    lines.append("Practical Counsel:")
    lines.extend(practical)
    return "\\n".join(lines)

# ------------------------------
# State
# ------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "principles" not in st.session_state:
    st.session_state.principles = DEFAULT_SYSTEM_PRINCIPLES.copy()

# ------------------------------
# Sidebar
# ------------------------------
with st.sidebar:
    st.markdown("## 🧪 Kelly — AI Skeptical Poet")
    st.caption("An AI scientist who only answers in poems: skeptical, analytical, and practical.")
    st.markdown("### System Notes")
    st.code(KELLY_BANNER, language="markdown")
    with st.expander("Adjust Kelly’s guiding principles (optional)"):
        new_principles = []
        for i, p in enumerate(st.session_state.principles):
            new_principles.append(st.text_input(f"Principle {i+1}", p))
        if st.button("Update principles"):
            st.session_state.principles = new_principles
            st.success("Updated Kelly’s guiding principles.")

    st.divider()
    if st.button("Clear chat"):
        st.session_state.messages = []
        st.success("Cleared.")

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
        st.markdown(m["content"])

# ------------------------------
# Chat input
# ------------------------------
prompt = st.chat_input("Ask Kelly a question about AI…")
if prompt:
    # user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # assistant message (poem)
    with st.chat_message("assistant"):
        with st.spinner("Kelly is weighing the science…"):
            time.sleep(0.2)  # tiny pause for UX
            poem = compose_kelly_reply(prompt, extra_principles=st.session_state.principles)
            st.markdown(poem)
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
            raw.append(f"{m['role'].upper()}:\\n{m['content']}\\n")
        blob = "\\n".join(raw)
        st.download_button(
            label="Download conversation",
            data=blob.encode("utf-8"),
            file_name=f"kelly_chat_{ts}.txt",
            mime="text/plain",
            use_container_width=True
        )
with col2:
    st.caption("Tip: Deploy on Streamlit Community Cloud to get a public link.")