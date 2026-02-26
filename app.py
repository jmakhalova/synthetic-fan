"""
Synthetic Fan — Idea Testing Chat Interface
Powered by Claude (Anthropic API)
"""

import streamlit as st
import anthropic
import os
from pathlib import Path

# --- Page config ---
st.set_page_config(
    page_title="SYNTHETIC FAN",
    page_icon="🔴",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# --- Custom CSS: Studio Linear-inspired — white, red, pixelated type ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Silkscreen:wght@400;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

    /* Hide Streamlit chrome */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* White base */
    .stApp {
        background-color: #ffffff;
    }

    /* Override Streamlit defaults to white bg */
    [data-testid="stAppViewContainer"],
    [data-testid="stHeader"],
    [data-testid="stToolbar"] {
        background-color: #ffffff !important;
    }

    /* Title block */
    .app-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.8rem;
        font-weight: 700;
        color: #E60000;
        letter-spacing: -0.02em;
        text-transform: uppercase;
        padding: 2rem 0 0.15rem 0;
        margin: 0;
        line-height: 1;
    }
    .app-subtitle {
        font-family: 'Silkscreen', monospace;
        font-size: 0.7rem;
        color: #999;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        padding: 0 0 1.5rem 0;
        margin: 0;
        border-bottom: 2px solid #E60000;
        margin-bottom: 1.5rem;
    }

    /* Mode buttons */
    .stButton > button {
        font-family: 'Silkscreen', monospace !important;
        font-size: 0.6rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
        border-radius: 0 !important;
        border: 2px solid #000 !important;
        background-color: #fff !important;
        color: #000 !important;
        padding: 0.4rem 0.5rem !important;
        transition: all 0.15s ease !important;
    }
    .stButton > button:hover {
        background-color: #E60000 !important;
        color: #fff !important;
        border-color: #E60000 !important;
    }
    .stButton > button[kind="primary"] {
        background-color: #E60000 !important;
        color: #fff !important;
        border-color: #E60000 !important;
    }

    /* Chat messages */
    .stChatMessage {
        background-color: transparent !important;
        border: none !important;
        padding: 0.75rem 0 !important;
    }
    .stChatMessage [data-testid="stMarkdownContainer"] {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 0.9rem !important;
        color: #1a1a1a !important;
        line-height: 1.6 !important;
    }

    /* User messages */
    [data-testid="stChatMessage"][data-testid-type="user"] {
        border-left: 3px solid #E60000;
        padding-left: 1rem !important;
    }

    /* Chat input */
    .stChatInputContainer {
        background-color: #ffffff !important;
    }
    .stChatInputContainer textarea {
        font-family: 'Space Grotesk', sans-serif !important;
        border: 2px solid #000 !important;
        border-radius: 0 !important;
    }
    .stChatInputContainer textarea:focus {
        border-color: #E60000 !important;
        box-shadow: none !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #f5f5f5;
        border-right: 2px solid #E60000;
    }
    [data-testid="stSidebar"] .stMarkdown {
        font-family: 'Space Grotesk', sans-serif;
        color: #1a1a1a;
    }

    /* Selectbox and inputs */
    .stSelectbox label, .stTextInput label {
        font-family: 'Silkscreen', monospace !important;
        font-size: 0.65rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
        color: #666 !important;
    }

    /* Password page styling */
    .stTextInput input {
        font-family: 'Space Grotesk', sans-serif !important;
        border: 2px solid #000 !important;
        border-radius: 0 !important;
        background-color: #fff !important;
    }
    .stTextInput input:focus {
        border-color: #E60000 !important;
        box-shadow: none !important;
    }

    /* System info in sidebar */
    .sidebar-info {
        font-family: 'Silkscreen', monospace;
        font-size: 0.55rem;
        color: #999;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        line-height: 1.8;
    }

    /* Red dividers */
    hr {
        border-color: #E60000 !important;
    }

    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 4px;
    }
    ::-webkit-scrollbar-track {
        background: #fff;
    }
    ::-webkit-scrollbar-thumb {
        background: #E60000;
    }
</style>
""", unsafe_allow_html=True)


# --- Password gate ---
def check_password():
    """Simple password check. Password is stored in Streamlit secrets or env var."""
    app_password = st.secrets.get("APP_PASSWORD", os.environ.get("APP_PASSWORD", ""))

    if not app_password:
        return True

    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False

    if st.session_state.password_correct:
        return True

    st.markdown('<p class="app-title">Synthetic Fan</p>', unsafe_allow_html=True)
    st.markdown('<p class="app-subtitle">Idea testing system &mdash; Armani White</p>', unsafe_allow_html=True)
    st.markdown("")

    password_input = st.text_input("Enter password to continue", type="password")

    if password_input:
        if password_input == app_password:
            st.session_state.password_correct = True
            st.rerun()
        else:
            st.error("Wrong password.")

    return False


if not check_password():
    st.stop()


# --- Load system prompt ---
@st.cache_data
def load_system_prompt():
    """Load the synthetic fan system prompt from the markdown file."""
    possible_paths = [
        Path(__file__).parent / "system_prompt.md",
        Path(__file__).parent / "synthetic-fan-system.md",
        Path("system_prompt.md"),
        Path("synthetic-fan-system.md"),
    ]

    for path in possible_paths:
        if path.exists():
            return path.read_text(encoding="utf-8")

    return """You are the Synthetic Fan idea testing system.
    The system prompt file (system_prompt.md) was not found in the app directory.
    Please place the synthetic-fan-system.md file in the same folder as app.py
    and rename it to system_prompt.md, then restart the app."""


SYSTEM_PROMPT = load_system_prompt()

# --- Mode definitions ---
MODES = {
    "quick": {
        "label": "Quick Test",
        "instruction": "Run a Quick Test (30 seconds). State the idea, pick the primary segment, score the Relevance Triangle, check triggers. Be concise.",
        "placeholder": "Describe your idea in one sentence...",
    },
    "full": {
        "label": "Full Test",
        "instruction": "Run a Full Test (2 minutes). Score all five segments on the Relevance Triangle. Check the Tension Map. Apply all Calibration Notes. Deliver a PROCEED / SHARPEN / RETHINK verdict.",
        "placeholder": "Describe your idea — I'll run it through all five segments...",
    },
    "ideate": {
        "label": "Ideation",
        "instruction": "Enter Ideation Mode. Ask which segment(s) to prioritize, then generate 3–5 idea directions that score LOCKED on the Triangle. Flag tensions and tradeoffs for each.",
        "placeholder": "What do you want to ideate around?",
    },
    "challenge": {
        "label": "Challenge",
        "instruction": "Enter Challenge Mode. Run the Full Test, then adopt the synthetic voice of the segment most likely to reject this idea. Argue against it specifically. Then offer one modification.",
        "placeholder": "What idea do you want stress-tested?",
    },
    "persona": {
        "label": "Persona",
        "instruction": "Enter Persona Mode. Ask which segment or individual fan type to inhabit, then respond entirely in that voice using their language, references, and evaluation criteria.",
        "placeholder": "Which fan perspective do you want to hear from?",
    },
    "open": {
        "label": "Open Chat",
        "instruction": "Respond naturally using the full Synthetic Fan system. The user may ask questions, explore ideas, or discuss strategy. Use the system flexibly — score when useful, speak as personas when asked, ideate when prompted. Don't force a mode unless the user signals one.",
        "placeholder": "Ask anything — test an idea, explore a tension, talk strategy...",
    },
}

# --- Session state ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_mode" not in st.session_state:
    st.session_state.current_mode = "open"

# API key: prefer secrets (for cloud deploy), fall back to env var, then sidebar input
api_key_default = st.secrets.get("ANTHROPIC_API_KEY", os.environ.get("ANTHROPIC_API_KEY", ""))
if "api_key" not in st.session_state:
    st.session_state.api_key = api_key_default

# --- Header ---
st.markdown('<p class="app-title">Synthetic Fan</p>', unsafe_allow_html=True)
st.markdown('<p class="app-subtitle">Idea testing system &mdash; Armani White &bull; 11 interviews &bull; 5 segments</p>', unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown("### Settings")

    if not api_key_default:
        api_key_input = st.text_input(
            "Anthropic API Key",
            value=st.session_state.api_key,
            type="password",
            help="Your API key from console.anthropic.com"
        )
        if api_key_input:
            st.session_state.api_key = api_key_input
    else:
        st.markdown('<p class="sidebar-info">API key loaded from secrets.</p>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Model")
    model = st.selectbox(
        "Claude model",
        ["claude-sonnet-4-5-20250929", "claude-opus-4-5-20251101", "claude-haiku-4-5-20251001"],
        index=0,
        help="Sonnet is fast and capable. Opus is deeper but slower and more expensive."
    )

    st.markdown("---")
    st.markdown("### System")
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown(
        '<p class="sidebar-info">Built from ethnographic research.<br>'
        '11 fan interviews · Feb 2026<br>'
        '5 segments · 6 fault lines · 4 calibration checks</p>',
        unsafe_allow_html=True,
    )

# --- Mode selector ---
cols = st.columns(len(MODES))
for i, (mode_key, mode_info) in enumerate(MODES.items()):
    with cols[i]:
        is_active = st.session_state.current_mode == mode_key
        if st.button(
            mode_info["label"],
            key=f"mode_{mode_key}",
            use_container_width=True,
            type="primary" if is_active else "secondary",
        ):
            st.session_state.current_mode = mode_key
            st.rerun()

st.markdown("<div style='height: 0.5rem'></div>", unsafe_allow_html=True)

# --- Display chat history ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Chat input ---
current_mode = MODES[st.session_state.current_mode]

if prompt := st.chat_input(current_mode["placeholder"]):
    if not st.session_state.api_key:
        st.error("Please add your Anthropic API key in the sidebar (click > arrow at top left).")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Build the messages for the API
    mode_instruction = current_mode["instruction"]

    api_messages = []
    for msg in st.session_state.messages:
        api_messages.append({"role": msg["role"], "content": msg["content"]})

    # Build system prompt with mode context + conciseness directive
    full_system = f"""{SYSTEM_PROMPT}

---

CURRENT MODE: {current_mode['label']}
MODE INSTRUCTION: {mode_instruction}

OUTPUT RULES:
- Be direct and concise. No filler, no preamble, no restating the question.
- Lead with the verdict or score. Explain only what's needed.
- Use short paragraphs (2-3 sentences max per point).
- For Quick Tests: stay under 150 words.
- For Full Tests: stay under 400 words. Use segment labels and Triangle scores as structure, not long prose.
- Never use bullet points where a single sentence works.
- When citing fan evidence, drop the quote inline — don't introduce it with "as one fan said."
- Apply the vagueness tax. If any manifesto-style abstraction creeps into an idea, name it and cut it.
- Speak like a sharp strategist in a working session, not a report."""

    # Call Claude API
    try:
        client = anthropic.Anthropic(api_key=st.session_state.api_key)

        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""

            with client.messages.stream(
                model=model,
                max_tokens=2048,
                system=full_system,
                messages=api_messages,
            ) as stream:
                for text in stream.text_stream:
                    full_response += text
                    response_placeholder.markdown(full_response + "▊")

            response_placeholder.markdown(full_response)

        st.session_state.messages.append({"role": "assistant", "content": full_response})

    except anthropic.AuthenticationError:
        st.error("Invalid API key. Check your key in the sidebar.")
    except anthropic.RateLimitError:
        st.error("Rate limit reached. Wait a moment and try again.")
    except Exception as e:
        st.error(f"Error: {str(e)}")
