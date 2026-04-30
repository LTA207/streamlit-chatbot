import random
import time
from datetime import datetime

import streamlit as st
import html


st.set_page_config(
    page_title="PulseCare Chat",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def fake_bot_reply(user_text: str) -> str:
    """Simple local responder for UI demo without external API."""
    text = user_text.lower().strip()

    if any(word in text for word in ["xin chao", "hello", "hi", "chao"]):
        return "Xin chao! Minh la PulseCare Chat, san sang ho tro ban ngay bay gio."

    if "thoi gian" in text or "gio" in text:
        return f"Bay gio la {datetime.now().strftime('%H:%M:%S')} ."

    if "streamlit" in text:
        return (
            "Streamlit rat hop de xay chatbot nhanh: co st.chat_message, st.chat_input "
            "va session_state de luu hoi thoai."
        )

    suggestions = [
        "Ban co the mo ta ro hon muc tieu de minh goi y chinh xac hon.",
        "Neu can, minh co the tao tiep backend ket noi OpenAI/Gemini cho giao dien nay.",
        "Mau giao dien nay co the mo rong them upload file, voice input va lich su chat.",
    ]
    return random.choice(suggestions)


def init_state() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "history" not in st.session_state:
        st.session_state.history = []
    if "active_history_index" not in st.session_state:
        st.session_state.active_history_index = None
    if "conversation_dirty" not in st.session_state:
        st.session_state.conversation_dirty = False


init_state()

# ChatGPT-like visual style with a centered conversation column.
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Public+Sans:wght@400;500;600;700&display=swap');

    :root {
        --bg-main: radial-gradient(circle at 10% 10%, #2a2b31 0%, #1e1f22 45%, #17181b 100%);
        --panel-bg: #202126;
        --panel-border: #3a3b45;
        --text-strong: #ececf1;
        --text-soft: #a1a1aa;
        --assistant-bubble: #202126;
        --user-bubble: #2b2c34;
        --input-bg: #2a2b31;
        --input-border: #41424d;
        --button-bg: #10a37f;
        --button-bg-hover: #0d8a6d;
    }

    html, body, [class*="css"] {
        font-family: 'Public Sans', sans-serif;
        color: var(--text-strong);
    }

    .stApp {
        background: var(--bg-main);
    }

    .block-container {
        max-width: 860px;
        padding-top: 5rem;
        padding-bottom: 1.5rem;
    }

    section[data-testid="stSidebar"] {
        background: #17181b;
        border-right: 1px solid var(--panel-border);
        padding-top: 0 !important;
        margin-top: 0 !important;
    }

    /* Take the collapse-button container out of normal flow so it doesn't push content down */
    [data-testid="stSidebarContent"] {
        position: relative !important;
        padding-top: 1.4rem !important;
        margin-top: 0 !important;
    }

    [data-testid="stSidebarContent"] > div:first-child {
        position: absolute !important;
        top: 0.35rem !important;
        right: -0.9rem !important;
        height: auto !important;
        width: auto !important;
        z-index: 200 !important;
    }

    /* Ensure the button inside is visible and positioned naturally inside its now-floating container */
    [data-testid="stSidebarContent"] > div:first-child > button {
        position: static !important;
        visibility: visible !important;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }

    section[data-testid="stSidebar"] > div > div {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }

    [data-testid="stChatMessage"] {
        border-radius: 12px;
        padding: 0.8rem 0.95rem;
        margin-bottom: 0.75rem;
        border: 1px solid transparent;
        box-shadow: none;
        animation: slideUp 300ms ease-out;
        max-width: 92%;
    }

    [data-testid="stChatMessage"][aria-label="user"] {
        background: var(--user-bubble);
        color: var(--text-strong);
        border-color: var(--panel-border);
        margin-left: auto;
        max-width: 66.5%;
    }

    .user-plain {
        background: var(--user-bubble);
        color: var(--text-strong);
        border: 1px solid var(--panel-border);
        border-radius: 12px;
        padding: 0.8rem 0.95rem;
        margin-bottom: 0.75rem;
        margin-left: auto;
        max-width: 66.5%;
        animation: slideUp 300ms ease-out;
    }

    [data-testid="stChatMessage"][aria-label="assistant"] {
        background: transparent;
        border-color: transparent;
        margin-right: auto;
    }

    [data-testid="stChatMessage"] p {
        line-height: 1.55;
    }

    [data-testid="stChatInput"] {
        background: var(--input-bg);
        border: 1px solid var(--input-border);
        border-radius: 14px;
        padding: 0.18rem;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.22);
    }

    [data-testid="stChatInput"] > div {
        background: transparent;
    }

    [data-testid="stChatInput"] textarea {
        font-size: 0.98rem;
    }

    .stButton button {
        width: 100%;
        border-radius: 10px;
        border: 1px solid #0f8c6f;
        background: var(--button-bg);
        color: #ffffff;
        font-weight: 600;
    }

    .stButton button:hover {
        background: var(--button-bg-hover);
        color: #ffffff;
    }

    .caps-label {
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--text-soft);
        font-size: 0.72rem;
        font-weight: 600;
        margin-bottom: 0.2rem;
    }

    .assistant-plain {
        max-width: 78%;
        margin-right: auto;
        color: var(--text-strong);
        padding: 0.2rem 0.25rem;
        font-size: 1rem;
    }

    .hero-title {
        max-width: 34rem;
        margin: 0 auto 1.4rem;
        text-align: center;
        font-size: clamp(2rem, 4vw, 3.4rem);
        line-height: 1.1;
        font-weight: 700;
        color: var(--text-strong);
    }

    [data-testid="stTextInput"] {
        background: var(--input-bg);
        border: 1px solid var(--input-border);
        border-radius: 16px;
        padding: 0.2rem 0.35rem;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.2);
    }

    .hero-input input {
        min-height: 3.4rem;
        font-size: 1.02rem;
        color: var(--text-strong);
    }

    .hero-input input::placeholder {
        color: rgba(161, 161, 170, 0.75);
    }

    /* top-brand removed: title now lives inside sidebar via .sidebar-title */

    .sidebar-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.75rem;
        margin: 2.5rem 0 0.9rem; /* Increased top margin for spacing */
    }

    .sidebar-title {
        font-size: 1rem;
        font-weight: 700;
        color: var(--text-strong);
        line-height: 1.2;
        margin: 0;
    }

    .sidebar-new-chat {
        margin: 0 0 1rem;
    }

    .sidebar-history-label {
        margin-top: 0.25rem;
    }

    [data-testid="stCaptionContainer"] {
        color: var(--text-soft);
    }

    @keyframes slideUp {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; transform: translateY(0); }
    }

    [data-testid="stToolbarActionButton"]:has-text("Deploy") {
        display: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Brand name is now shown inside sidebar via sidebar-title

st.markdown("""
<script>
    const observer = new MutationObserver(() => {
        const buttons = document.querySelectorAll('button');
        buttons.forEach(btn => {
            if (btn.textContent.includes('Deploy')) {
                btn.style.display = 'none';
            }
        });
    });
    observer.observe(document.body, { childList: true, subtree: true });
    document.querySelectorAll('button').forEach(btn => {
        if (btn.textContent.includes('Deploy')) {
            btn.style.display = 'none';
        }
    });
</script>
""", unsafe_allow_html=True)

def save_current_conversation() -> None:
    # Save current messages back into the active history entry, or append a new one.
    if not st.session_state.get("messages"):
        return

    snapshot = {
        "title": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "messages": [m.copy() for m in st.session_state.messages],
    }

    active_history_index = st.session_state.active_history_index
    if active_history_index is not None and 0 <= active_history_index < len(st.session_state.history):
        snapshot["title"] = st.session_state.history[active_history_index]["title"]
        st.session_state.history[active_history_index] = snapshot
    else:
        st.session_state.history.append(snapshot)

    st.session_state.conversation_dirty = False


def safe_rerun():
    """Rerun the Streamlit script to update UI."""
    st.rerun()


def handle_user_prompt(prompt: str) -> None:
    if not prompt.strip():
        return

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.conversation_dirty = True

    safe = html.escape(prompt)
    st.markdown(f"<div class=\"user-plain\">{safe}</div>", unsafe_allow_html=True)

    with st.spinner("PulseCare dang suy nghi..."):
        time.sleep(typing_speed)
        response = fake_bot_reply(prompt)

    safe = html.escape(response)
    st.markdown(f"<div class=\"assistant-plain\">{safe}</div>", unsafe_allow_html=True)

    st.session_state.messages.append({"role": "assistant", "content": response})


def queue_hero_prompt() -> None:
    prompt = st.session_state.get("hero_prompt", "").strip()
    if prompt:
        st.session_state.pending_hero_prompt = prompt
        st.session_state.hero_prompt = ""


with st.sidebar:
    st.markdown(
        "<div class='sidebar-header'><div class='sidebar-title'>PulseCare Chat</div></div>",
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sidebar-new-chat">', unsafe_allow_html=True)
    if st.button("+ New chat"):
        # Save current changes only when the user actually edited a loaded or active conversation.
        if st.session_state.get("messages") and st.session_state.conversation_dirty:
            save_current_conversation()
        st.session_state.messages = []
        st.session_state.active_history_index = None
        st.session_state.conversation_dirty = False
        safe_rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="caps-label sidebar-history-label">History</div>', unsafe_allow_html=True)

    if st.session_state.history:
        # show most recent first
        for i in range(len(st.session_state.history) - 1, -1, -1):
            convo = st.session_state.history[i]
            if st.button(convo["title"], key=f"hist_{i}"):
                # Keep the active history intact if it was edited; otherwise just load the selected one.
                if st.session_state.active_history_index == i:
                    safe_rerun()

                if st.session_state.get("messages") and st.session_state.conversation_dirty:
                    save_current_conversation()

                st.session_state.messages = [m.copy() for m in convo["messages"]]
                st.session_state.active_history_index = i
                st.session_state.conversation_dirty = False
                safe_rerun()
    else:
        st.markdown("_No previous chats_")

    # Fixed typing speed per user request
    typing_speed = 1.5

for message in st.session_state.messages:
    role = message.get("role", "assistant")
    content = message.get("content", "")
    if role == "user":
        # render user reply as plain paragraph without avatar
        safe = html.escape(content)
        st.markdown(f"<div class=\"user-plain\">{safe}</div>", unsafe_allow_html=True)
    else:
        # render assistant reply as plain paragraph without avatar
        safe = html.escape(content)
        st.markdown(f"<div class=\"assistant-plain\">{safe}</div>", unsafe_allow_html=True)

pending_hero_prompt = st.session_state.pop("pending_hero_prompt", "")
if pending_hero_prompt:
    handle_user_prompt(pending_hero_prompt)
    safe_rerun()

if not st.session_state.messages:
    st.markdown(
        "<div class='hero-title'>Hôm nay bạn cảm thấy sức khỏe thế nào?</div>",
        unsafe_allow_html=True,
    )
    st.markdown("<div class='hero-input'>", unsafe_allow_html=True)
    prompt = st.text_input(
        "",
        placeholder="Hỏi bất cứ điều gì",
        key="hero_prompt",
        on_change=queue_hero_prompt,
        label_visibility="collapsed",
    )
    st.markdown("</div>", unsafe_allow_html=True)
else:
    typed_prompt = st.chat_input("Hỏi bất cứ điều gì")
    if typed_prompt:
        handle_user_prompt(typed_prompt)
