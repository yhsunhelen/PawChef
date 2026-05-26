import streamlit as st

_FONTS_URL = (
    "https://fonts.googleapis.com/css2?"
    "family=Instrument+Serif:ital@0;1"
    "&family=Geist:wght@400;500;600"
    "&family=JetBrains+Mono:wght@400;500"
    "&display=swap"
)

_TOKENS_CSS = """
:root {
  --bg:           #f5efe3;
  --bg-2:         #ede4d2;
  --paper:        #fbf7ee;
  --ink:          #2a241d;
  --ink-2:        #5b4f42;
  --muted:        #8d8073;
  --line:         #e2d6bf;
  --line-strong:  #c9b896;
  --primary:      #4f6b3a;
  --primary-ink:  #f5efe3;
  --primary-soft: #dfe6d0;
  --accent:       #c45a3a;
  --accent-soft:  #f1d3c4;
  --warn:         #b78a2f;
  --danger:       #a23a2a;
  --r-sm:  10px;
  --r:     16px;
  --r-lg:  24px;
  --r-xl:  32px;
  --r-pill:999px;
  --shadow-sm: 0 1px 2px rgba(58,44,25,.06),0 1px 3px rgba(58,44,25,.04);
  --shadow:    0 2px 4px rgba(58,44,25,.05),0 8px 24px rgba(58,44,25,.08);
  --shadow-lg: 0 8px 16px rgba(58,44,25,.08),0 24px 48px rgba(58,44,25,.12);
  --pad: 20px;
  --gap: 16px;
  --serif: "Instrument Serif","Iowan Old Style",Georgia,serif;
  --sans:  "Geist","Inter Tight",-apple-system,BlinkMacSystemFont,"Helvetica Neue",sans-serif;
  --mono:  "JetBrains Mono",ui-monospace,"SF Mono",Menlo,monospace;
}
"""

_STREAMLIT_OVERRIDES = """
/* ── hide Streamlit chrome ── */
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
/* Make header transparent instead of hidden — preserves sidebar toggle button */
header[data-testid="stHeader"] {
  background: transparent !important;
  border-bottom: none !important;
}
[data-testid="stToolbar"]    { visibility: hidden !important; }
[data-testid="stDecoration"] { display: none !important; }

/* ── global reset ── */
html, body, [data-testid="stAppViewContainer"] {
  background: var(--bg) !important;
  color: var(--ink) !important;
  font-family: var(--sans) !important;
  -webkit-font-smoothing: antialiased;
}

/* ── sidebar ── */
[data-testid="stSidebar"] {
  background: var(--paper) !important;
  border-right: 1px solid var(--line) !important;
}
[data-testid="stSidebarContent"] { padding-top: 24px !important; }

/* ── main content area ── */
[data-testid="stMain"] {
  background: var(--bg) !important;
}
.main .block-container {
  padding-top: 2rem !important;
  max-width: 1100px !important;
}

/* ── primary buttons ── */
[data-testid="stButton"] > button {
  background: var(--primary) !important;
  color: var(--primary-ink) !important;
  border: none !important;
  border-radius: var(--r-pill) !important;
  padding: 10px 22px !important;
  font-family: var(--sans) !important;
  font-weight: 500 !important;
  font-size: 15px !important;
  box-shadow: var(--shadow-sm) !important;
  transition: background 120ms ease, transform 120ms ease !important;
}
[data-testid="stButton"] > button:hover {
  background: #3e562e !important;
  transform: translateY(-1px) !important;
}
[data-testid="stButton"] > button:active {
  transform: translateY(1px) !important;
}

/* ── secondary / ghost buttons ── */
[data-testid="stButton"] > button[kind="secondary"] {
  background: transparent !important;
  color: var(--ink) !important;
  border: 1px solid var(--line-strong) !important;
}
[data-testid="stButton"] > button[kind="secondary"]:hover {
  background: var(--bg-2) !important;
}

/* ── inputs ── */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input,
[data-testid="stTextArea"] textarea {
  background: var(--paper) !important;
  color: var(--ink) !important;
  border: 1px solid var(--line-strong) !important;
  border-radius: var(--r-sm) !important;
  font-family: var(--sans) !important;
  font-size: 15px !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
  border-color: var(--primary) !important;
  box-shadow: 0 0 0 3px rgba(79,107,58,.18) !important;
}

/* ── selectbox ── */
[data-testid="stSelectbox"] > div > div {
  background: var(--paper) !important;
  border: 1px solid var(--line-strong) !important;
  border-radius: var(--r-sm) !important;
  color: var(--ink) !important;
}

/* ── metrics / stat boxes ── */
[data-testid="stMetric"] {
  background: var(--paper) !important;
  border: 1px solid var(--line) !important;
  border-radius: var(--r) !important;
  padding: 16px !important;
}
[data-testid="stMetricLabel"] {
  font-family: var(--mono) !important;
  font-size: 10px !important;
  letter-spacing: .12em !important;
  text-transform: uppercase !important;
  color: var(--muted) !important;
}
[data-testid="stMetricValue"] {
  font-family: var(--serif) !important;
  font-size: 28px !important;
  color: var(--ink) !important;
}

/* ── expanders ── */
[data-testid="stExpander"] {
  background: var(--paper) !important;
  border: 1px solid var(--line) !important;
  border-radius: var(--r-lg) !important;
  overflow: hidden !important;
}
[data-testid="stExpander"] summary {
  font-family: var(--serif) !important;
  font-size: 18px !important;
  color: var(--ink) !important;
}

/* ── divider ── */
hr { border-color: var(--line) !important; }

/* ── download / generic buttons ── */
[data-testid="stDownloadButton"] > button {
  background: transparent !important;
  color: var(--ink) !important;
  border: 1px solid var(--line-strong) !important;
  border-radius: var(--r-pill) !important;
}

/* ── pills ── */
[data-testid="stPills"] span {
  border-radius: var(--r-pill) !important;
  font-family: var(--sans) !important;
}

/* ── tabs ── */
[data-testid="stTabs"] [data-baseweb="tab"] {
  font-family: var(--mono) !important;
  font-size: 12px !important;
  letter-spacing: .08em !important;
  text-transform: uppercase !important;
}

/* ── alerts / info boxes ── */
[data-testid="stAlert"] {
  border-radius: var(--r) !important;
}

/* ── captions ── */
[data-testid="stCaptionContainer"] {
  font-family: var(--mono) !important;
  font-size: 11px !important;
  color: var(--muted) !important;
  letter-spacing: .04em !important;
}
"""

_UTILITY_CSS = """
/* ── chef design-system utility classes ── */
.chef-eyebrow {
  font-family: var(--mono);
  font-size: 11px;
  letter-spacing: .12em;
  text-transform: uppercase;
  color: var(--muted);
  display: block;
  margin-bottom: 6px;
}
.chef-display {
  font-family: var(--serif);
  font-size: clamp(36px, 5vw, 64px);
  line-height: 1;
  letter-spacing: -.02em;
  color: var(--ink);
  margin: 0;
}
.chef-display em { font-style: italic; color: var(--accent); }
.chef-h2 {
  font-family: var(--serif);
  font-size: 32px;
  line-height: 1.1;
  letter-spacing: -.01em;
  margin: 0;
}
.chef-h2 em { font-style: italic; color: var(--accent); }
.chef-h3 {
  font-family: var(--serif);
  font-size: 22px;
  line-height: 1.15;
  margin: 0;
}
.chef-lede {
  font-size: 18px;
  color: var(--ink-2);
  max-width: 52ch;
  margin: 12px 0 0;
}
.chef-card {
  background: var(--paper);
  border: 1px solid var(--line);
  border-radius: var(--r-lg);
  padding: 22px;
  box-shadow: var(--shadow);
}
.chef-tag {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  background: var(--bg-2);
  border-radius: var(--r-pill);
  padding: 3px 10px;
  font-size: 11px;
  color: var(--ink-2);
  font-family: var(--mono);
  letter-spacing: .04em;
}
.chef-tag-allergy {
  background: var(--accent-soft);
  color: var(--accent);
}
.chef-mono {
  font-family: var(--mono);
  font-size: 12px;
  letter-spacing: .06em;
  color: var(--muted);
  text-transform: uppercase;
}
"""


def inject_css() -> None:
    st.markdown(
        f'<link rel="preconnect" href="https://fonts.googleapis.com">'
        f'<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        f'<link href="{_FONTS_URL}" rel="stylesheet">',
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<style>{_TOKENS_CSS}{_STREAMLIT_OVERRIDES}{_UTILITY_CSS}</style>",
        unsafe_allow_html=True,
    )


def eyebrow(text: str) -> None:
    st.markdown(f'<span class="chef-eyebrow">{text}</span>', unsafe_allow_html=True)


def display(html: str) -> None:
    """Big serif display heading. Use <em> for italic terracotta emphasis."""
    st.markdown(f'<h1 class="chef-display">{html}</h1>', unsafe_allow_html=True)


def h2(html: str) -> None:
    st.markdown(f'<h2 class="chef-h2">{html}</h2>', unsafe_allow_html=True)


def h3(html: str) -> None:
    st.markdown(f'<h3 class="chef-h3">{html}</h3>', unsafe_allow_html=True)


def lede(text: str) -> None:
    st.markdown(f'<p class="chef-lede">{text}</p>', unsafe_allow_html=True)


def tag(text: str, allergy: bool = False) -> str:
    cls = "chef-tag chef-tag-allergy" if allergy else "chef-tag"
    return f'<span class="{cls}">{text}</span>'


def card_open() -> str:
    return '<div class="chef-card">'


def card_close() -> str:
    return '</div>'
