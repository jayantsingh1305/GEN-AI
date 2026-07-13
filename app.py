from dotenv import load_dotenv
load_dotenv()

import html as html_lib
import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="AI Chat Bot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── FULL CSS REDESIGN ────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp {
    background: #050510;
    min-height: 100vh;
}
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 80% 60% at 20% 10%,  rgba(99,102,241,0.18) 0%, transparent 60%),
        radial-gradient(ellipse 60% 50% at 80% 80%,  rgba(139,92,246,0.15) 0%, transparent 55%),
        radial-gradient(ellipse 50% 40% at 60% 30%,  rgba(236,72,153,0.10) 0%, transparent 50%),
        radial-gradient(ellipse 70% 60% at 10% 70%,  rgba(59,130,246,0.10) 0%, transparent 55%);
    animation: bgShift 12s ease-in-out infinite alternate;
    pointer-events: none;
    z-index: 0;
}
@keyframes bgShift {
    0%   { opacity:1; transform:scale(1)    rotate(0deg); }
    50%  { opacity:.8; transform:scale(1.05) rotate(1deg); }
    100% { opacity:1; transform:scale(1)    rotate(0deg); }
}
.stApp::after {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(99,102,241,0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(99,102,241,0.04) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
    z-index: 0;
}

[data-testid="stSidebar"] {
    background: rgba(8,8,20,0.92) !important;
    border-right: 1px solid rgba(99,102,241,0.2) !important;
    backdrop-filter: blur(20px);
    box-shadow: 4px 0 30px rgba(0,0,0,0.5);
}
[data-testid="stSidebar"] > div { padding-top: 1.5rem; }

.sb-brand {
    display:flex; align-items:center; gap:10px;
    padding:0 1rem 1rem;
    border-bottom:1px solid rgba(255,255,255,0.07);
    margin-bottom:1.5rem;
}
.sb-brand-icon {
    font-size:2rem;
    filter:drop-shadow(0 0 8px rgba(99,102,241,0.8));
    animation:pulse 3s ease-in-out infinite;
}
@keyframes pulse {
    0%,100%{ filter:drop-shadow(0 0 8px rgba(99,102,241,0.8)); }
    50%    { filter:drop-shadow(0 0 18px rgba(139,92,246,1)); }
}
.sb-brand-text { font-size:1.1rem; font-weight:700; color:#fff; }
.sb-brand-sub  { font-size:0.68rem; color:rgba(255,255,255,0.35); letter-spacing:1px; text-transform:uppercase; }

.mode-label {
    font-size:0.68rem; font-weight:600; letter-spacing:1.5px;
    text-transform:uppercase; color:rgba(255,255,255,0.3);
    padding:0 1rem; margin-bottom:0.5rem;
}
.mode-card {
    display:flex; align-items:center; gap:12px;
    padding:12px 16px; margin:0 0.5rem 6px;
    border-radius:14px; border:1px solid rgba(255,255,255,0.07);
    background:rgba(255,255,255,0.03);
    transition:all 0.25s cubic-bezier(0.4,0,0.2,1);
}
.mode-card:hover {
    background:rgba(99,102,241,0.1);
    border-color:rgba(99,102,241,0.35);
    transform:translateX(4px);
}
.mode-card.active {
    border-color:var(--mc) !important;
    background:linear-gradient(135deg,rgba(var(--mc-rgb),0.18),rgba(var(--mc-rgb),0.06));
    box-shadow:0 0 20px rgba(var(--mc-rgb),0.2),inset 0 0 20px rgba(var(--mc-rgb),0.04);
}
.mode-emoji { font-size:1.35rem; line-height:1; }
.mode-info  { flex:1; }
.mode-name  { font-size:0.88rem; font-weight:600; color:#f0f0ff; }
.mode-desc  { font-size:0.71rem; color:rgba(255,255,255,0.38); margin-top:2px; }
.mode-dot   {
    width:8px; height:8px; border-radius:50%;
    background:var(--mc); box-shadow:0 0 6px var(--mc);
    flex-shrink:0; opacity:0; transition:opacity 0.2s;
}
.mode-card.active .mode-dot { opacity:1; }

[data-testid="stSidebar"] button {
    background:rgba(239,68,68,0.08) !important;
    border:1px solid rgba(239,68,68,0.25) !important;
    color:#fca5a5 !important; border-radius:12px !important;
    font-weight:500 !important; font-size:0.85rem !important;
    transition:all 0.2s !important;
    margin-top:0 !important;
    height:36px !important;
    min-height:36px !important;
    padding:0 !important;
    visibility:hidden !important;
    position:absolute !important;
}

.clear-btn {
    display:flex; align-items:center; justify-content:center; gap:8px;
    width:calc(100% - 1rem); margin:0 0.5rem;
    padding:10px 16px; border-radius:12px;
    border:1px solid rgba(239,68,68,0.25);
    background:rgba(239,68,68,0.08);
    color:#fca5a5; font-size:0.85rem; font-weight:500;
    cursor:pointer; transition:all 0.2s;
    font-family:'Inter',sans-serif;
}
.clear-btn:hover {
    background:rgba(239,68,68,0.18);
    border-color:rgba(239,68,68,0.5);
    box-shadow:0 0 16px rgba(239,68,68,0.15);
}

.sb-footer {
    padding:1rem;
    border-top:1px solid rgba(255,255,255,0.07);
    margin-top:1rem;
    font-size:0.7rem; color:rgba(255,255,255,0.22);
    text-align:center; line-height:1.7;
}

.main-wrap { max-width:820px; margin:0 auto; padding:0 1rem; position:relative; z-index:1; }

.chat-header { text-align:center; padding:2rem 1rem 1rem; }
.chat-title {
    font-size:2.6rem; font-weight:800;
    background:linear-gradient(135deg,#818cf8 0%,#c084fc 45%,#f472b6 90%);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    background-clip:text; letter-spacing:-1px; line-height:1.1; margin:0 0 0.5rem;
}
.chat-subtitle { font-size:0.86rem; color:rgba(255,255,255,0.35); }
.mode-pill {
    display:inline-flex; align-items:center; gap:5px;
    padding:3px 12px 3px 8px; border-radius:999px;
    font-size:0.8rem; font-weight:600;
    border:1px solid; margin-left:4px; vertical-align:middle;
}

.chat-container {
    display:flex; flex-direction:column; gap:16px;
    padding:1rem 0 7rem;
}
.msg-row { display:flex; align-items:flex-end; gap:10px; animation:fadeUp 0.28s ease-out; }
@keyframes fadeUp { from{opacity:0;transform:translateY(10px)} to{opacity:1;transform:translateY(0)} }
.msg-row.user-row { flex-direction:row-reverse; }

.msg-avatar {
    width:34px; height:34px; border-radius:50%;
    display:flex; align-items:center; justify-content:center;
    font-size:1rem; flex-shrink:0; border:2px solid;
}
.user-avatar { background:rgba(99,102,241,0.2); border-color:rgba(99,102,241,0.5); }
.ai-avatar   { background:rgba(139,92,246,0.2);  border-color:rgba(139,92,246,0.5); }

.bubble { max-width:68%; padding:12px 16px; border-radius:18px; font-size:0.9rem; line-height:1.68; word-break:break-word; white-space:pre-wrap; }
.user-bubble {
    background:linear-gradient(135deg,#4f46e5,#7c3aed);
    color:#fff; border-bottom-right-radius:4px;
    box-shadow:0 4px 22px rgba(99,102,241,0.35);
}
.ai-bubble {
    background:rgba(255,255,255,0.055); color:#e4e4f4;
    border:1px solid rgba(255,255,255,0.09); border-bottom-left-radius:4px;
    backdrop-filter:blur(12px); box-shadow:0 4px 20px rgba(0,0,0,0.28);
}

[data-testid="stChatMessage"] { background:transparent !important; border:none !important; padding:0 !important; box-shadow:none !important; }

[data-testid="stBottom"],
[data-testid="stBottom"] > div,
.stBottom, .stBottom > div {
    background:rgba(5,5,16,0.92) !important;
    backdrop-filter:blur(24px) !important;
    border-top:1px solid rgba(99,102,241,0.18) !important;
}
section[data-testid="stBottom"] { background:rgba(5,5,16,0.92) !important; }
.stChatInputContainer, .stChatInputContainer > div { background:transparent !important; }
[data-testid="stChatInput"] {
    background:rgba(255,255,255,0.055) !important;
    border:1.5px solid rgba(99,102,241,0.28) !important;
    border-radius:16px !important;
    backdrop-filter:blur(10px);
    transition:border-color .2s,box-shadow .2s !important;
    max-width:820px !important; margin:0 auto !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color:#818cf8 !important;
    box-shadow:0 0 0 3px rgba(99,102,241,0.18),0 0 28px rgba(99,102,241,0.18) !important;
}
[data-testid="stChatInput"] textarea { color:#f0f0ff !important; font-family:'Inter',sans-serif !important; font-size:0.92rem !important; }
[data-testid="stChatInput"] textarea::placeholder { color:rgba(255,255,255,0.22) !important; }
[data-testid="stChatInput"] button {
    background:linear-gradient(135deg,#6366f1,#8b5cf6) !important;
    border-radius:10px !important; border:none !important;
    box-shadow:0 0 14px rgba(99,102,241,0.45) !important;
}

::-webkit-scrollbar { width:5px; }
::-webkit-scrollbar-track { background:transparent; }
::-webkit-scrollbar-thumb { background:rgba(99,102,241,0.38); border-radius:10px; }
::-webkit-scrollbar-thumb:hover { background:rgba(99,102,241,0.6); }

/* ── Force dark background on every Streamlit wrapper ── */
body, .main, [data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
[data-testid="stVerticalBlock"],
[data-testid="stBottom"],
[data-testid="stBottom"] > div,
.stChatFloatingInputContainer,
.stChatFloatingInputContainer > div,
.block-container {
    background: transparent !important;
}
body { background: #050510 !important; }

#MainMenu, footer, header, [data-testid="stToolbar"] { visibility:hidden !important; display:none !important; }

.empty-state { text-align:center; padding:4rem 2rem; }
.empty-icon {
    font-size:4rem; display:block; margin-bottom:1rem;
    filter:drop-shadow(0 0 20px rgba(99,102,241,0.5));
    animation:float 4s ease-in-out infinite;
}
@keyframes float { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-12px)} }
.empty-text { font-size:1.05rem; font-weight:600; color:rgba(255,255,255,0.3); }
.empty-sub  { font-size:0.82rem; color:rgba(255,255,255,0.18); margin-top:6px; }

.stSpinner > div { border-top-color:#818cf8 !important; }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_client():
    return Groq()
client = get_client()

MODES = {
    "😊 Helpful": {"prompt":"You are a helpful assistant.",
                   "color":"#818cf8","rgb":"129,140,248","desc":"Friendly & informative"},
    "😠 Angry":   {"prompt":"You are an angry assistant. You respond to the user in a very angry and aggressive manner.",
                   "color":"#f87171","rgb":"248,113,113","desc":"Aggressive & hot-headed"},
    "😂 Funny":   {"prompt":"You are a funny assistant. You respond to the user in a humorous and entertaining manner.",
                   "color":"#fbbf24","rgb":"251,191,36", "desc":"Hilarious & entertaining"},
    "😢 Sad":     {"prompt":"You are a sad assistant. You respond to the user in a melancholic and sorrowful manner.",
                   "color":"#60a5fa","rgb":"96,165,250", "desc":"Melancholic & sorrowful"},
}

if "selected_mode" not in st.session_state:
    st.session_state.selected_mode = "😊 Helpful"
if "messages" not in st.session_state:
    st.session_state.messages = [{"role":"system","content":MODES["😊 Helpful"]["prompt"]}]

with st.sidebar:
    st.markdown("""
    <div class="sb-brand">
        <span class="sb-brand-icon">🤖</span>
        <div>
            <div class="sb-brand-text">AI Chat Bot</div>
            <div class="sb-brand-sub">LLaMA 3.3 · 70B via Groq</div>
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="mode-label">Choose Mode</div>', unsafe_allow_html=True)
    for mode_name, cfg in MODES.items():
        emoji = mode_name.split()[0]
        label = " ".join(mode_name.split()[1:])
        is_active = st.session_state.selected_mode == mode_name
        ac = "active" if is_active else ""
        st.markdown(f"""
        <div class="mode-card {ac}" style="--mc:{cfg['color']};--mc-rgb:{cfg['rgb']};">
            <span class="mode-emoji">{emoji}</span>
            <div class="mode-info">
                <div class="mode-name">{label}</div>
                <div class="mode-desc">{cfg['desc']}</div>
            </div>
            <div class="mode-dot"></div>
        </div>""", unsafe_allow_html=True)
        if st.button(label, key=f"mb_{mode_name}", use_container_width=True):
            st.session_state.selected_mode = mode_name
            st.session_state.messages = [{"role":"system","content":cfg["prompt"]}]
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🗑️  Clear Conversation", use_container_width=True, key="clear"):
        mode = st.session_state.selected_mode
        st.session_state.messages = [{"role":"system","content":MODES[mode]["prompt"]}]
        st.rerun()

    st.markdown("""
    <div class="sb-footer">
        ⚡ Powered by <b>Groq</b><br>
        LLaMA 3.3 · 70B Versatile<br>
        <span style="opacity:.4;">───────────</span><br>
        AI Chat Bot &nbsp;v1.0
    </div>""", unsafe_allow_html=True)

mode = st.session_state.selected_mode
cfg  = MODES[mode]

st.markdown(f"""
<div class="main-wrap">
  <div class="chat-header">
    <div class="chat-title">🤖 AI Chat Bot</div>
    <div class="chat-subtitle">
      Talking to the
      <span class="mode-pill"
            style="color:{cfg['color']};border-color:rgba({cfg['rgb']},.4);background:rgba({cfg['rgb']},.1);">
        {mode}
      </span>
      assistant
    </div>
  </div>
</div>""", unsafe_allow_html=True)

history = [m for m in st.session_state.messages if m["role"] != "system"]

chat_html = '<div class="main-wrap"><div class="chat-container">'
if not history:
    chat_html += f"""
    <div class="empty-state">
        <span class="empty-icon">{mode.split()[0]}</span>
        <div class="empty-text">Start a conversation!</div>
        <div class="empty-sub">I am in <b style="color:{cfg['color']}">{mode}</b> mode — say hello 👋</div>
    </div>"""
else:
    import html as html_lib
    for msg in history:
        safe = html_lib.escape(msg["content"]).replace("\n","<br>")
        if msg["role"] == "user":
            chat_html += f"""
            <div class="msg-row user-row">
                <div class="bubble user-bubble">{safe}</div>
                <div class="msg-avatar user-avatar">🧑</div>
            </div>"""
        else:
            chat_html += f"""
            <div class="msg-row ai-row">
                <div class="msg-avatar ai-avatar">🤖</div>
                <div class="bubble ai-bubble">{safe}</div>
            </div>"""
chat_html += '</div></div>'
st.markdown(chat_html, unsafe_allow_html=True)

if prompt := st.chat_input(f"Message {mode} assistant..."):
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.spinner("Thinking..."):
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=st.session_state.messages,
            temperature=0.8,
            max_tokens=1024,
        )
        ai_content = response.choices[0].message.content
    st.session_state.messages.append({"role":"assistant","content":ai_content})
    st.rerun()
