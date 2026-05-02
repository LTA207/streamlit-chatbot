import random
import time
from datetime import datetime

import streamlit as st
import html


st.set_page_config(
    page_title="PulseCare",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
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
    if "sidebar_collapsed" not in st.session_state:
        st.session_state.sidebar_collapsed = False


init_state()

sidebar_width = "4.6rem" if st.session_state.sidebar_collapsed else "20rem"
sidebar_panel_display = "none" if st.session_state.sidebar_collapsed else "block"
sidebar_rail_display = "flex" if st.session_state.sidebar_collapsed else "none"

st.markdown(
    f"""
    <style>
    [data-testid="stSidebar"] {{
        width: {sidebar_width} !important;
        min-width: {sidebar_width} !important;
        max-width: {sidebar_width} !important;
    }}

    [data-testid="collapsedControl"] {{
        display: none !important;
    }}

    [data-testid="stSidebarHeader"],
    [data-testid="stSidebarHeader"] button,
    [data-testid="stSidebarNav"],
    [data-testid="stSidebarNav"] button,
    [data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebarCollapseButton"] button {{
        display: none !important;
    }}

    [data-testid="collapsedControl"] button,
    button[aria-label*="Open sidebar" i],
    button[aria-label*="Close sidebar" i],
    button[title*="sidebar" i] {{
        display: none !important;
    }}

    button[title*="collapse" i],
    button[aria-label*="collapse" i],
    button[aria-label*="sidebar" i] {{
        display: none !important;
    }}

    .sidebar-panel {{
        display: {sidebar_panel_display};
    }}

    .sidebar-rail-only {{
        display: {sidebar_rail_display};
    }}

    .sidebar-rail-col {{
        min-height: calc(100vh - 2rem);
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ChatGPT-like visual style with a centered conversation column.
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Public+Sans:wght@400;500;600;700&display=swap');

    :root {
        --bg-main: radial-gradient(circle at top, #2b2c31 0%, #1b1c20 46%, #111114 100%);
        --panel-bg: #17181c;
        --panel-border: #31323a;
        --text-strong: #ececf1;
        --text-soft: #a1a1aa;
        --assistant-bubble: #202126;
        --user-bubble: #2b2c34;
        --input-bg: #2a2b31;
        --input-border: #41424d;
        --button-bg: #10a37f;
        --button-bg-hover: #0d8a6d;
        --sidebar-rail: #191a1e;
        --sidebar-accent: #23242a;
    }

    html, body, [class*="css"] {
        font-family: 'Public Sans', sans-serif;
        color: var(--text-strong);
    }

    .stApp {
        background: var(--bg-main);
    }

    .block-container {
        max-width: 920px;
        padding-top: 0rem;
        padding-bottom: 1.5rem;
    }

    [data-testid="stHeader"] {
        display: none !important;
    }

    [data-testid="stToolbar"] {
        display: none !important;
    }

    [data-testid="stDecoration"] {
        display: none !important;
    }

    header {
        display: none !important;
    }

    [data-testid="stSidebar"] {
        background: #131418;
        border-right: 1px solid var(--panel-border);
    }

    section[data-testid="stSidebar"] {
        background: #131418;
        padding-top: 0 !important;
        margin-top: 0 !important;
    }

    [data-testid="stSidebarContent"] {
        padding-top: 0.85rem !important;
        margin-top: 0 !important;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }

    section[data-testid="stSidebar"] > div > div {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }

    [data-testid="stSidebar"] [data-testid="column"] {
        padding-left: 0 !important;
        padding-right: 0 !important;
    }

    .sidebar-rail-col {
        background: var(--sidebar-rail);
        border-right: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 1rem;
        min-height: calc(100vh - 2rem);
        padding: 0.85rem 0.5rem;
    }

    .sidebar-rail-stack {
        min-height: calc(100vh - 3.75rem);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-between;
        gap: 0.75rem;
    }

    .rail-logo,
    .rail-user {
        width: 2rem;
        height: 2rem;
        border-radius: 999px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(180deg, #2a2b30, #1f2025);
        color: var(--text-strong);
        font-size: 0.8rem;
        font-weight: 700;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.04);
        margin: 0 auto;
    }

    .sidebar-panel {
        min-width: 0;
        padding-top: 0.15rem;
    }

    .sidebar-brand-block {
        margin: 0 0 1rem;
    }

    .sidebar-brand {
        margin: 0 0 1rem;
    }

    .sidebar-brand-name {
        font-size: 1.05rem;
        font-weight: 700;
        color: var(--text-strong);
        line-height: 1.2;
    }

    .sidebar-brand-subtitle {
        color: var(--text-soft);
        font-size: 0.76rem;
        margin-top: 0.12rem;
    }

    .sidebar-section {
        margin-top: 1rem;
    }

    .sidebar-section-title {
        margin: 0 0 0.5rem;
        color: var(--text-soft);
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-size: 0.71rem;
        font-weight: 700;
    }

    .sidebar-divider {
        height: 1px;
        background: rgba(255, 255, 255, 0.06);
        margin: 0.9rem 0;
    }

    .sidebar-empty {
        color: var(--text-soft);
        font-size: 0.92rem;
        padding: 0.45rem 0;
    }

    .sidebar-history-item button {
        text-align: left;
        border-radius: 14px;
        padding: 0.72rem 0.85rem;
        background: var(--sidebar-accent);
        border: 1px solid rgba(255, 255, 255, 0.05);
        color: var(--text-strong);
        font-size: 0.94rem;
        font-weight: 500;
    }

    .sidebar-history-item button:hover {
        background: #2c2d35;
        border-color: rgba(255, 255, 255, 0.09);
    }

    .sidebar-history-item button:focus {
        outline: none;
        box-shadow: 0 0 0 2px rgba(16, 163, 127, 0.35);
    }

    .sidebar-action button {
        width: 100%;
        border-radius: 14px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        background: linear-gradient(180deg, #23242a, #1f2025);
        color: var(--text-strong);
        font-weight: 600;
    }

    .sidebar-action button:hover {
        background: #292a31;
    }

    .sidebar-mini-button button {
        width: 2rem;
        min-width: 2rem;
        height: 2rem;
        padding: 0;
        border-radius: 999px;
        background: transparent;
        border: 1px solid rgba(255, 255, 255, 0.08);
        color: var(--text-strong);
        font-size: 0.95rem;
    }

    .sidebar-mini-button button:hover {
        background: rgba(255, 255, 255, 0.06);
    }

    .sidebar-toggle-wrap {
        margin: 0.5rem 0 0.75rem;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.35rem;
    }

    .sidebar-toggle-label {
        color: var(--text-soft);
        font-size: 0.68rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        text-align: center;
    }

    .sidebar-action-stack {
        display: flex;
        flex-direction: column;
        gap: 0.55rem;
    }

    /* Make action buttons visually neutral: transparent background, white text */
    [data-testid="stSidebar"] .stButton > button {
        background: transparent !important;
        color: var(--text-strong) !important;
        border: 1px solid rgba(255, 255, 255, 0.04) !important;
        box-shadow: none !important;
        padding: 0.7rem 0.85rem !important;
        text-align: left !important;
        border-radius: 12px !important;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(255,255,255,0.02) !important;
    }

    .sidebar-history-stack {
        display: flex;
        flex-direction: column;
        gap: 0.55rem;
    }

    /* history items: white text, no background; on hover text becomes light gray */
    .sidebar-history-stack button,
    .sidebar-empty button {
        background: transparent !important;
        border: none !important;
        color: var(--text-strong) !important;
        padding: 0.45rem 0 !important;
        text-align: left !important;
        font-size: 0.95rem !important;
    }

    .sidebar-history-stack button:hover {
        color: #d0d0d4 !important;
        background: transparent !important;
    }

    .sidebar-toggle button {
        width: 2.25rem;
        min-width: 2.25rem;
        height: 2.25rem;
        padding: 0;
        border-radius: 999px;
        background: #202126;
        border: 1px solid rgba(255, 255, 255, 0.08);
        color: var(--text-strong);
        font-size: 1rem;
        font-weight: 700;
        margin: 0 auto;
    }

    .sidebar-toggle button:hover {
        background: #2a2b31;
    }

    .sidebar-rail-button button {
        width: 2rem;
        min-width: 2rem;
        height: 2rem;
        padding: 0;
        border-radius: 999px;
        background: transparent;
        border: 1px solid rgba(255, 255, 255, 0.08);
        color: var(--text-strong);
        font-size: 0.95rem;
    }

    .sidebar-rail-button button:hover {
        background: rgba(255, 255, 255, 0.06);
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

    /* Bottom bar container that wraps chat input */
    [data-testid="stBottom"],
    [data-testid="stBottom"] > div,
    .stChatFloatingInputContainer,
    .stChatFloatingInputContainer > div {
        background: transparent !important;
        background-color: transparent !important;
        backdrop-filter: none !important;
        border-top: none !important;
        box-shadow: none !important;
    }

    /* ── Chat input container ── */
    [data-testid="stChatInput"],
    [data-testid="stChatInputContainer"] {
        background: var(--input-bg);
        border: 1px solid var(--input-border) !important;
        border-radius: 16px;
        padding: 0.2rem 0.35rem;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.2);
        outline: none !important;
    }

    /* Kill green focus ring – target BaseUI internal wrapper */
    [data-baseweb="base-input"],
    [data-baseweb="base-input"]:focus,
    [data-baseweb="base-input"]:focus-within,
    [data-baseweb="input"],
    [data-baseweb="input"]:focus-within {
        border-color: var(--input-border) !important;
        border-top-color: var(--input-border) !important;
        border-right-color: var(--input-border) !important;
        border-bottom-color: var(--input-border) !important;
        border-left-color: var(--input-border) !important;
        box-shadow: none !important;
        outline: none !important;
    }

    /* Also target wrapper divs at every depth */
    [data-testid="stChatInput"]:focus-within,
    [data-testid="stChatInputContainer"]:focus-within,
    [data-testid="stChatInput"] > div:focus-within,
    [data-testid="stChatInputContainer"] > div:focus-within,
    [data-testid="stTextInput"]:focus-within,
    [data-testid="stTextInput"] > div:focus-within {
        border-color: var(--input-border) !important;
        border-top-color: var(--input-border) !important;
        border-right-color: var(--input-border) !important;
        border-bottom-color: var(--input-border) !important;
        border-left-color: var(--input-border) !important;
        box-shadow: none !important;
        outline: none !important;
    }

    [data-testid="stChatInput"] > div,
    [data-testid="stChatInputContainer"] > div {
        background: transparent;
        outline: none !important;
        box-shadow: none !important;
    }

    [data-testid="stChatInput"] textarea,
    [data-testid="stChatInputContainer"] textarea {
        font-size: 1.02rem;
        min-height: 3.4rem;
        color: var(--text-strong);
        background: transparent;
        outline: none !important;
        box-shadow: none !important;
        border: none !important;
    }

    [data-testid="stChatInput"] textarea:focus,
    [data-testid="stChatInputContainer"] textarea:focus {
        outline: none !important;
        box-shadow: none !important;
        border: none !important;
    }

    [data-testid="stChatInput"] textarea::placeholder,
    [data-testid="stChatInputContainer"] textarea::placeholder {
        color: rgba(161, 161, 170, 0.75);
    }

    /* ── Hero text input (màn hình chào) ── */
    [data-testid="stTextInput"] input:focus,
    .hero-input input:focus {
        outline: none !important;
        box-shadow: none !important;
        border-color: var(--input-border) !important;
    }

    [data-testid="stTextInput"]:focus-within,
    .hero-input:focus-within {
        outline: none !important;
        box-shadow: none !important;
        border-color: var(--input-border) !important;
    }

    .stButton button {
        width: 100%;
        border-radius: 10px;
        border: none;
        background: transparent;
        color: #ffffff;
        font-weight: 600;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .stButton button:hover {
        background: rgba(255, 255, 255, 0.1);
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

st.markdown("""
<script>
    const hideControls = (btn) => {
        try {
            const txt = (btn.textContent || "").trim();
            const title = (btn.title || "").toLowerCase();
            const aria = (btn.getAttribute && (btn.getAttribute('aria-label') || "")).toLowerCase();

            // Hide the Deploy toolbar button (existing behaviour)
            if (txt.includes('Deploy')) {
                btn.style.display = 'none';
            }

            // Hide any Streamlit sidebar collapse/expand controls that may appear
            if (title.includes('collapse') || title.includes('expand') || aria.includes('collapse') || aria.includes('sidebar') || txt.includes('❯') || txt.includes('❮') ) {
                btn.style.display = 'none';
            }

            // Also hide the collapsedControl container if present
            const collapsed = document.querySelectorAll('[data-testid="collapsedControl"]');
            collapsed.forEach(el => { el.style.display = 'none'; });
        } catch (e) {
            // ignore
        }
    };

    const observer = new MutationObserver(() => {
        const buttons = document.querySelectorAll('button');
        buttons.forEach(hideControls);
    });
    observer.observe(document.body, { childList: true, subtree: true });

    // Run once immediately to catch existing controls
    document.querySelectorAll('button').forEach(hideControls);
</script>
""", unsafe_allow_html=True)

def get_conversation_title(messages: list, max_length: int = 20) -> str:
    """
    Lấy tiêu đề từ thông điệp đầu tiên của user.
    Giới hạn 1 dòng, nếu quá dài thì truncate với dấu '...'
    """
    # Tìm thông điệp user đầu tiên
    for msg in messages:
        if msg.get("role") == "user":
            title = msg.get("content", "").strip()
            if title:
                # Loại bỏ các ký tự xuống dòng và thay khoảng trắng liên tiếp bằng 1 khoảng
                title = " ".join(title.split())
                
                if len(title) > max_length:
                    return title[:max_length].strip() + "...."
                return title
    
    # Fallback nếu không có user message
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def save_current_conversation() -> None:
    # Save current messages back into the active history entry, or append a new one.
    if not st.session_state.get("messages"):
        return

    snapshot = {
        "title": get_conversation_title(st.session_state.messages),
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
    rail_col, panel_col = st.columns([1, 5], gap="small")

    with rail_col:
        st.markdown('<div class="sidebar-toggle-wrap sidebar-rail-only">', unsafe_allow_html=True)
        if st.button("☰" if st.session_state.sidebar_collapsed else "❮", key="sidebar_toggle", help="Mở hoặc thu gọn sidebar"):
            st.session_state.sidebar_collapsed = not st.session_state.sidebar_collapsed
            safe_rerun()
        st.markdown('</div>', unsafe_allow_html=True)


    with panel_col:
        if not st.session_state.sidebar_collapsed:
            st.markdown('<div class="sidebar-brand-block">', unsafe_allow_html=True)
            st.markdown("<div class='sidebar-brand-name'>PulseCare Chat</div>", unsafe_allow_html=True)
            st.markdown("<div class='sidebar-brand-subtitle'>AI assistant workspace</div>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="sidebar-action-stack">', unsafe_allow_html=True)
            if st.button("+ Đoạn chat mới", key="new_chat"):
                if st.session_state.get("messages") and st.session_state.conversation_dirty:
                    save_current_conversation()
                st.session_state.messages = []
                st.session_state.active_history_index = None
                st.session_state.conversation_dirty = False
                safe_rerun()

                # removed search/settings buttons per user request
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
            st.markdown('<div class="sidebar-section-title">History</div>', unsafe_allow_html=True)

            history_filter = st.text_input(
                "",
                placeholder="Tìm cuộc trò chuyện",
                key="history_filter",
                label_visibility="collapsed",
            )

            filtered_history = st.session_state.history
            if history_filter.strip():
                query = history_filter.strip().lower()
                filtered_history = [
                    convo
                    for convo in st.session_state.history
                    if query in convo.get("title", "").lower()
                    or any(query in msg.get("content", "").lower() for msg in convo.get("messages", []))
                ]

            if filtered_history:
                st.markdown('<div class="sidebar-history-stack">', unsafe_allow_html=True)
                for i in range(len(st.session_state.history) - 1, -1, -1):
                    convo = st.session_state.history[i]
                    if convo not in filtered_history:
                        continue

                    if st.button(convo["title"], key=f"hist_{i}"):
                        if st.session_state.active_history_index == i:
                            safe_rerun()

                        if st.session_state.get("messages") and st.session_state.conversation_dirty:
                            save_current_conversation()

                        st.session_state.messages = [m.copy() for m in convo["messages"]]
                        st.session_state.active_history_index = i
                        st.session_state.conversation_dirty = False
                        safe_rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="sidebar-empty">Chưa có cuộc trò chuyện nào</div>', unsafe_allow_html=True)

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
