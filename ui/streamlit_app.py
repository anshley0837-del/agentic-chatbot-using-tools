# import os

# import requests
# import streamlit as st
# from dotenv import load_dotenv

# load_dotenv()

# BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:8000').rstrip('/')

# st.set_page_config(
#     page_title='Agentic Chatbot',
#     page_icon='🤖',
#     layout='centered',
# )

# st.title('🤖 Agentic Chatbot')
# st.caption('Streamlit UI -> FastAPI -> LangGraph Agent -> Tools -> Response')

# with st.sidebar:
#     st.subheader('Backend')
#     st.code(BACKEND_URL)
#     st.write('Tools: calculator, current time, weather')
#     if st.button('Clear chat'):
#         st.session_state.messages = []
#         st.rerun()

# if 'messages' not in st.session_state:
#     st.session_state.messages = []

# for message in st.session_state.messages:
#     with st.chat_message(message['role']):
#         st.markdown(message['content'])

# prompt = st.chat_input('Ask something...')

# if prompt:
#     with st.chat_message('user'):
#         st.markdown(prompt)

#     history = st.session_state.messages.copy()
#     st.session_state.messages.append({'role': 'user', 'content': prompt})

#     with st.chat_message('assistant'):
#         with st.spinner('Agent is working...'):
#             try:
#                 response = requests.post(
#                     f'{BACKEND_URL}/chat',
#                     json={'message': prompt, 'history': history},
#                     timeout=120,
#                 )
#                 response.raise_for_status()
#                 data = response.json()
#                 answer = data['answer']
#                 tool_calls = data.get('tool_calls', [])

#                 st.markdown(answer)
#                 if tool_calls:
#                     st.caption('Tools used: ' + ', '.join(tool_calls))

#                 st.session_state.messages.append(
#                     {'role': 'assistant', 'content': answer}
#                 )
#             except requests.RequestException as exc:
#                 st.error(f'Backend connection failed: {exc}')
#             except Exception as exc:
#                 st.error(f'Unexpected error: {exc}')

import os
import textwrap

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:8000').rstrip('/')

st.set_page_config(
    page_title='J.A.R.V.I.S | Agentic AI',
    page_icon='🤖',
    layout='wide',
)

# ----------------------------------------------------------------------------
# GLASSMORPHISM / JARVIS THEME
# (CSS must have no blank lines and no leading indentation inside st.markdown)
# ----------------------------------------------------------------------------
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Inter:wght@300;400;500;600&display=swap');
:root {
  --cyan: #00e5ff;
  --blue: #3b82f6;
  --violet: #8b5cf6;
  --glass: rgba(255, 255, 255, 0.06);
  --glass-strong: rgba(255, 255, 255, 0.10);
  --border: rgba(255, 255, 255, 0.16);
}
html, body, [class*="css"], .stApp { font-family: 'Inter', sans-serif; }
.stApp {
  background: radial-gradient(circle at 15% 20%, #0b1a3a 0%, transparent 45%),
              radial-gradient(circle at 85% 80%, #2a0f4a 0%, transparent 45%),
              linear-gradient(135deg, #04060f 0%, #070b1c 50%, #05030d 100%);
  background-attachment: fixed;
  color: #e6f1ff;
}
.stApp::before {
  content: ''; position: fixed; inset: 0; pointer-events: none; z-index: 0;
  background-image: linear-gradient(rgba(0,229,255,0.04) 1px, transparent 1px),
                    linear-gradient(90deg, rgba(0,229,255,0.04) 1px, transparent 1px);
  background-size: 48px 48px;
  mask-image: radial-gradient(circle at center, black 30%, transparent 80%);
}
.orb { position: fixed; border-radius: 50%; filter: blur(90px); opacity: 0.35; z-index: 0; pointer-events: none; animation: float 14s ease-in-out infinite; }
.orb.o1 { width: 380px; height: 380px; background: var(--cyan); top: -80px; left: -80px; }
.orb.o2 { width: 420px; height: 420px; background: var(--violet); bottom: -120px; right: -100px; animation-delay: -6s; }
.orb.o3 { width: 260px; height: 260px; background: var(--blue); top: 45%; left: 55%; animation-delay: -3s; opacity: 0.2; }
@keyframes float { 0%,100% { transform: translate(0,0) scale(1); } 50% { transform: translate(40px,-50px) scale(1.15); } }
header[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer { visibility: hidden; }
.block-container { max-width: 980px; padding-top: 1.5rem; padding-bottom: 7rem; position: relative; z-index: 1; }
section[data-testid="stSidebar"] {
  background: rgba(8, 12, 30, 0.55) !important;
  backdrop-filter: blur(22px) saturate(160%);
  -webkit-backdrop-filter: blur(22px) saturate(160%);
  border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] * { color: #d6e6ff; }
.glass {
  background: var(--glass);
  backdrop-filter: blur(18px) saturate(170%);
  -webkit-backdrop-filter: blur(18px) saturate(170%);
  border: 1px solid var(--border);
  border-radius: 20px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.45), inset 0 1px 0 rgba(255,255,255,0.12);
}
.hero { display: flex; align-items: center; gap: 22px; padding: 20px 26px; margin-bottom: 18px; }
.reactor { position: relative; width: 78px; height: 78px; flex: 0 0 78px; }
.reactor .ring { position: absolute; inset: 0; border-radius: 50%; border: 2px solid transparent; }
.reactor .r1 { border-top-color: var(--cyan); border-bottom-color: var(--cyan); animation: spin 3s linear infinite; }
.reactor .r2 { inset: 9px; border-left-color: var(--blue); border-right-color: var(--blue); animation: spin 2s linear infinite reverse; }
.reactor .r3 { inset: 18px; border-top-color: var(--violet); border-bottom-color: var(--violet); animation: spin 1.4s linear infinite; }
.reactor .core { position: absolute; inset: 28px; border-radius: 50%; background: radial-gradient(circle, #fff 0%, var(--cyan) 45%, transparent 75%); box-shadow: 0 0 25px var(--cyan), 0 0 55px rgba(0,229,255,0.6); animation: pulse 2s ease-in-out infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
@keyframes pulse { 0%,100% { transform: scale(0.85); opacity: 0.8; } 50% { transform: scale(1.15); opacity: 1; } }
.hero h1 { font-family: 'Orbitron', sans-serif; font-weight: 900; font-size: 1.9rem; letter-spacing: 0.18em; margin: 0; background: linear-gradient(90deg, #fff, var(--cyan), var(--violet)); -webkit-background-clip: text; background-clip: text; color: transparent; }
.hero p { margin: 4px 0 0 0; color: #8fb2d9; font-size: 0.85rem; letter-spacing: 0.06em; }
.pill { display: inline-flex; align-items: center; gap: 8px; padding: 5px 14px; border-radius: 999px; font-size: 0.75rem; font-weight: 500; letter-spacing: 0.08em; background: var(--glass); border: 1px solid var(--border); }
.dot { width: 8px; height: 8px; border-radius: 50%; animation: blink 1.6s infinite; }
.dot.on { background: #22ff9c; box-shadow: 0 0 10px #22ff9c; }
.dot.off { background: #ff4d6d; box-shadow: 0 0 10px #ff4d6d; }
@keyframes blink { 50% { opacity: 0.35; } }
.hero .status { margin-left: auto; }
div[data-testid="stChatMessage"] {
  background: var(--glass);
  backdrop-filter: blur(16px) saturate(160%);
  -webkit-backdrop-filter: blur(16px) saturate(160%);
  border: 1px solid var(--border);
  border-radius: 18px;
  padding: 14px 18px;
  margin-bottom: 14px;
  box-shadow: 0 6px 24px rgba(0,0,0,0.35), inset 0 1px 0 rgba(255,255,255,0.10);
  animation: slideIn 0.45s cubic-bezier(.2,.8,.2,1);
}
div[data-testid="stChatMessage"]:has(img[alt="user avatar"]),
div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
  background: linear-gradient(135deg, rgba(59,130,246,0.22), rgba(139,92,246,0.18));
  border-color: rgba(139,180,255,0.35);
}
div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
  border-left: 3px solid var(--cyan);
}
@keyframes slideIn { from { opacity: 0; transform: translateY(14px) scale(0.98); } to { opacity: 1; transform: none; } }
div[data-testid="stChatMessage"] p, div[data-testid="stChatMessage"] li { color: #e6f1ff; line-height: 1.65; }
div[data-testid="stChatMessage"] code { background: rgba(0,0,0,0.4); color: var(--cyan); border-radius: 6px; padding: 2px 6px; }
div[data-testid="stBottom"] > div, div[data-testid="stBottomBlockContainer"] { background: transparent !important; }
div[data-testid="stChatInput"] {
  background: rgba(255,255,255,0.07) !important;
  backdrop-filter: blur(20px) saturate(170%);
  -webkit-backdrop-filter: blur(20px) saturate(170%);
  border: 1px solid rgba(0,229,255,0.35) !important;
  border-radius: 999px !important;
  box-shadow: 0 0 24px rgba(0,229,255,0.18), inset 0 1px 0 rgba(255,255,255,0.12);
  transition: box-shadow .3s, border-color .3s;
}
div[data-testid="stChatInput"]:focus-within { border-color: var(--cyan) !important; box-shadow: 0 0 34px rgba(0,229,255,0.45); }
div[data-testid="stChatInput"] textarea { color: #e6f1ff !important; background: transparent !important; }
div[data-testid="stChatInput"] textarea::placeholder { color: #7f9cc0 !important; }
.stButton > button {
  background: var(--glass) !important;
  color: #dff3ff !important;
  border: 1px solid var(--border) !important;
  border-radius: 14px !important;
  backdrop-filter: blur(14px);
  transition: all .25s ease;
  font-weight: 500;
}
.stButton > button:hover { transform: translateY(-2px); border-color: var(--cyan) !important; box-shadow: 0 0 20px rgba(0,229,255,0.35); color: #fff !important; }
.tool-badge { display: inline-block; margin: 8px 6px 0 0; padding: 4px 12px; font-size: 0.72rem; letter-spacing: 0.08em; text-transform: uppercase; color: var(--cyan); background: rgba(0,229,255,0.10); border: 1px solid rgba(0,229,255,0.4); border-radius: 999px; box-shadow: 0 0 12px rgba(0,229,255,0.2); }
.thinking { display: flex; align-items: center; gap: 12px; color: #8fdcff; font-size: 0.9rem; letter-spacing: 0.08em; }
.thinking .bars { display: flex; gap: 4px; align-items: flex-end; height: 22px; }
.thinking .bars span { width: 4px; background: linear-gradient(var(--cyan), var(--violet)); border-radius: 2px; animation: eq 1s ease-in-out infinite; }
.thinking .bars span:nth-child(2) { animation-delay: .12s; }
.thinking .bars span:nth-child(3) { animation-delay: .24s; }
.thinking .bars span:nth-child(4) { animation-delay: .36s; }
.thinking .bars span:nth-child(5) { animation-delay: .48s; }
@keyframes eq { 0%,100% { height: 5px; } 50% { height: 22px; } }
.welcome { padding: 34px; text-align: center; margin-bottom: 18px; }
.welcome h3 { font-family: 'Orbitron', sans-serif; letter-spacing: 0.12em; color: #fff; margin-bottom: 6px; }
.welcome p { color: #8fb2d9; margin: 0; }
.sb-title { font-family: 'Orbitron', sans-serif; font-size: 0.8rem; letter-spacing: 0.2em; color: var(--cyan); margin: 14px 0 8px 0; }
.sb-card { padding: 12px 14px; margin-bottom: 10px; font-size: 0.85rem; }
.sb-card code { color: var(--cyan) !important; background: rgba(0,0,0,0.35) !important; font-size: 0.75rem; word-break: break-all; }
.stat { display: flex; justify-content: space-between; padding: 4px 0; }
.stat b { color: var(--cyan); font-family: 'Orbitron', sans-serif; }
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-thumb { background: rgba(0,229,255,0.35); border-radius: 8px; }
</style>
<div class="orb o1"></div><div class="orb o2"></div><div class="orb o3"></div>
"""
st.markdown(CSS, unsafe_allow_html=True)


# ----------------------------------------------------------------------------
# HELPERS
# ----------------------------------------------------------------------------
@st.cache_data(ttl=15, show_spinner=False)
def backend_online(url: str) -> bool:
    """Any HTTP response below 500 means the backend is reachable."""
    try:
        return requests.get(f'{url}/health', timeout=2).status_code < 500
    except requests.RequestException:
        return False


def html(block: str) -> None:
    """Render raw HTML safely (dedent so Markdown doesn't treat it as code)."""
    st.markdown(textwrap.dedent(block).strip(), unsafe_allow_html=True)


def tool_badges(tool_calls) -> str:
    return ''.join(f'<span class="tool-badge">⚙ {t}</span>' for t in tool_calls)


def render_message(msg: dict) -> None:
    avatar = '🧑‍💻' if msg['role'] == 'user' else '🤖'
    with st.chat_message(msg['role'], avatar=avatar):
        st.markdown(msg['content'])
        if msg.get('tool_calls'):
            html(f'<div>{tool_badges(msg["tool_calls"])}</div>')


THINKING_HTML = (
    '<div class="thinking"><div class="bars">'
    '<span></span><span></span><span></span><span></span><span></span>'
    '</div>AGENT PROCESSING · REASONING · CALLING TOOLS...</div>'
)

# ----------------------------------------------------------------------------
# STATE
# ----------------------------------------------------------------------------
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'pending' not in st.session_state:
    st.session_state.pending = None

online = backend_online(BACKEND_URL)

# ----------------------------------------------------------------------------
# SIDEBAR
# ----------------------------------------------------------------------------
with st.sidebar:
    html('<div class="sb-title">◈ BACKEND LINK</div>')
    html(f'<div class="glass sb-card"><code>{BACKEND_URL}</code></div>')

    html('<div class="sb-title">◈ ACTIVE MODULES</div>')
    html(
        """
        <div class="glass sb-card">
        🧮 Calculator<br>🕒 Current Time<br>🌦️ Weather
        </div>
        """
    )

    total_tools = sum(len(m.get('tool_calls', [])) for m in st.session_state.messages)
    html('<div class="sb-title">◈ SESSION TELEMETRY</div>')
    html(
        f"""
        <div class="glass sb-card">
        <div class="stat"><span>Messages</span><b>{len(st.session_state.messages)}</b></div>
        <div class="stat"><span>Tool calls</span><b>{total_tools}</b></div>
        </div>
        """
    )

    if st.button('🗑  Clear chat', use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending = None
        st.rerun()

# ----------------------------------------------------------------------------
# HERO HEADER
# ----------------------------------------------------------------------------
status_dot = 'on' if online else 'off'
status_txt = 'SYSTEMS ONLINE' if online else 'BACKEND OFFLINE'
html(
    f"""
    <div class="glass hero">
      <div class="reactor">
        <div class="ring r1"></div><div class="ring r2"></div><div class="ring r3"></div>
        <div class="core"></div>
      </div>
      <div>
        <h1>J.A.R.V.I.S</h1>
        <p>Streamlit UI → FastAPI → LangGraph Agent → Tools → Response</p>
      </div>
      <div class="status"><span class="pill"><span class="dot {status_dot}"></span>{status_txt}</span></div>
    </div>
    """
)

# ----------------------------------------------------------------------------
# WELCOME + QUICK ACTIONS (only when chat is empty)
# ----------------------------------------------------------------------------
if not st.session_state.messages:
    html(
        """
        <div class="glass welcome">
          <h3>AT YOUR SERVICE</h3>
          <p>Ask me to calculate, check the time, or fetch the weather. Pick a quick command or type below.</p>
        </div>
        """
    )
    quick = [
        ('🧮 Calculate', 'What is (1234 * 56) / 7?'),
        ('🕒 Time now', 'What is the current time?'),
        ('🌦️ Weather', 'What is the weather in Indore right now?'),
    ]
    cols = st.columns(len(quick))
    for col, (label, text) in zip(cols, quick):
        if col.button(label, use_container_width=True, key=f'quick_{label}'):
            st.session_state.pending = text
            st.rerun()

# ----------------------------------------------------------------------------
# CHAT HISTORY
# ----------------------------------------------------------------------------
for message in st.session_state.messages:
    render_message(message)

# ----------------------------------------------------------------------------
# INPUT + BACKEND CALL
# ----------------------------------------------------------------------------
typed = st.chat_input('Command J.A.R.V.I.S ...')
prompt = typed or st.session_state.pending
st.session_state.pending = None

if prompt:
    render_message({'role': 'user', 'content': prompt})

    # Backend only needs role + content (same format as before)
    history = [
        {'role': m['role'], 'content': m['content']}
        for m in st.session_state.messages
    ]
    st.session_state.messages.append({'role': 'user', 'content': prompt})

    with st.chat_message('assistant', avatar='🤖'):
        placeholder = st.empty()
        placeholder.markdown(THINKING_HTML, unsafe_allow_html=True)
        try:
            response = requests.post(
                f'{BACKEND_URL}/chat',
                json={'message': prompt, 'history': history},
                timeout=120,
            )
            response.raise_for_status()
            data = response.json()
            answer = data['answer']
            tool_calls = data.get('tool_calls', [])

            placeholder.markdown(answer)
            if tool_calls:
                html(f'<div>{tool_badges(tool_calls)}</div>')

            st.session_state.messages.append(
                {'role': 'assistant', 'content': answer, 'tool_calls': tool_calls}
            )
        except requests.RequestException as exc:
            placeholder.empty()
            st.error(f'Backend connection failed: {exc}')
        except Exception as exc:
            placeholder.empty()
            st.error(f'Unexpected error: {exc}')