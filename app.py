import streamlit as st
from image_api import generate_image
from styles import STYLE_MODES
from datetime import datetime
from io import BytesIO

# Page config
st.set_page_config(
    page_title="AstraMind Image AI",
    page_icon="🎨",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
    }

    .main-title {
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        margin-bottom: 0;
    }

    .main-subtitle {
        text-align: center;
        color: #a78bfa99;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }

    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        font-size: 1.1rem;
        font-weight: 600;
        padding: 0.6rem 2rem;
        transition: transform 0.2s, box-shadow 0.2s;
    }

    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 20px #667eea88;
        color: white;
    }

    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid #667eea55;
        border-radius: 10px;
        color: white;
        font-size: 1rem;
    }

    .stTextInput > div > div > input:focus {
        border: 1px solid #667eea;
        box-shadow: 0 0 10px #667eea44;
    }

    .stTextInput label p, .stRadio label p {
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        color: #a78bfa !important;
    }

    [data-testid="stRadio"] label {
        background: rgba(102, 126, 234, 0.08);
        border: 1px solid #667eea33;
        border-radius: 8px;
        padding: 8px 16px;
        margin-right: 8px;
    }

    img {
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
    }

    hr {
        border-color: #667eea33;
    }

    .stCaption {
        color: #667eea99 !important;
    }

    /* General text sizing */
    .stMarkdown, .stCaption, p {
        font-size: 1.05rem;
    }

    /* Subheader for each history entry */
    h3 {
        font-size: 1.6rem !important;
    }

    /* Radio button option text */
    [data-testid="stRadio"] label p {
        font-size: 1.05rem !important;
        color: white !important;
        font-weight: 500 !important;
    }

    /* Input placeholder text */
    .stTextInput input::placeholder {
        font-size: 1rem;
        opacity: 0.5;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">🎨 AstraMind Image AI</p>', unsafe_allow_html=True)
st.markdown('<p class="main-subtitle">Type a prompt. Choose a style. Watch AI create.</p>', unsafe_allow_html=True)

# Initialize session state
if "history" not in st.session_state:
    st.session_state["history"] = []

with st.sidebar:
    st.title("🎨 AstraMind Image AI")
    st.markdown("*Powered by FLUX.1-dev*")
    st.divider()

    st.markdown(f"**{len(st.session_state['history'])}** images generated")

    if st.session_state["history"]:
        st.caption(f"Last generated: {st.session_state['history'][-1]['timestamp']}")
        st.divider()
        st.markdown("**Recent Generations**")
        for entry in reversed(st.session_state["history"][-3:]):
            st.image(entry["image"], caption=entry["style"], width=150)

    st.divider()

    if st.button("🗑️ Clear Gallery", use_container_width=True):
        st.session_state["history"] = []
        st.rerun()

# Input section
user_input = st.text_input(
    "Enter your image prompt",
    placeholder="e.g. A futuristic Indian city at night"
)

style = st.radio(
    "Choose a style",
    list(STYLE_MODES.keys()),
    horizontal=True
)

generate = st.button("Generate Image ✨", use_container_width=True)

if generate:
    if user_input.strip() == "":
        st.warning("⚠️ Please enter a prompt before generating!")
    else:
        with st.spinner("Generating your image... this may take 20-30 seconds"):
            image, error = generate_image(user_input, style)

        if error:
            st.error(error)
        else:
            entry = {
                "prompt": user_input,
                "style": style,
                "image": image,
                "timestamp": datetime.now().strftime("%I:%M %p")
            }
            st.session_state["history"].append(entry)
            st.rerun()

# Display history
st.divider()

if len(st.session_state["history"]) == 0:
    st.info("👋 Your generated images will appear here.")
else:
    for entry in reversed(st.session_state["history"]):
        st.subheader(f"🖼️ {entry['prompt']} — {entry['style']}")
        st.caption(entry["timestamp"])
        st.image(entry["image"], width=500)

        buffer = BytesIO()
        entry["image"].save(buffer, format="PNG")
        image_bytes = buffer.getvalue()

        st.download_button(
            "⬇️ Download Image",
            data=image_bytes,
            file_name=f"astramind_{entry['timestamp'].replace(':', '-')}.png",
            mime="image/png",
            key=f"download_{entry['timestamp']}_{entry['prompt'][:10]}"
        )
        st.divider()