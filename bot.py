import google.generativeai as genai
import streamlit as st

# ---------------- Configure Gemini ----------------
genai.configure(api_key="AIzaSyB7986dsKfXWd5vLDH-XH2kepuh3AwhiQM")   # ⚠️ Replace with your API Key
model = genai.GenerativeModel("gemini-1.5-flash")

# ---------------- Streamlit Page ----------------
st.set_page_config(page_title="⚡ Gemini AI Chatbot", page_icon="🤖", layout="centered")

st.markdown(
    """
    <style>
    body {
        background: linear-gradient(135deg, #141E30, #243B55);
        color: white;
    }
    .title {
        font-size: 32px;
        font-weight: bold;
        text-align: center;
        padding: 15px;
        color: #FFD700;
        text-shadow: 0px 0px 15px #FFD700;
    }
    .chat-box {
        max-height: 500px;
        overflow-y: auto;
        padding: 15px;
        border-radius: 12px;
        background-color: rgba(255, 255, 255, 0.05);
        margin-bottom: 15px;
    }
    .user-bubble {
        background: linear-gradient(135deg, #2193b0, #6dd5ed);
        color: white;
        padding: 12px;
        border-radius: 12px;
        margin: 5px;
        text-align: right;
        box-shadow: 0px 0px 12px rgba(33,147,176,0.5);
    }
    .bot-bubble {
        background: linear-gradient(135deg, #8E2DE2, #FF6B6B);
        color: white;
        padding: 12px;
        border-radius: 12px;
        margin: 5px;
        text-align: left;
        box-shadow: 0px 0px 12px rgba(142,45,226,0.5);
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<div class='title'>⚡ Gemini AI Powered Chatbot ⚡</div>", unsafe_allow_html=True)

# ---------------- Chat History ----------------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- Chat Input ----------------
user_input = st.chat_input("💬 Type your message...")

if user_input:
    # Save user message
    st.session_state.history.append(("You", user_input))

    # Gemini response
    try:
        response = model.generate_content(user_input)
        bot_reply = response.text if response.text else "⚠️ No response from Gemini."
    except Exception as e:
        bot_reply = f"⚠️ Error: {str(e)}"

    # Save bot reply
    st.session_state.history.append(("Gemini ⚡", bot_reply))

# ---------------- Display Chat with Delete Option ----------------
st.markdown("<div class='chat-box'>", unsafe_allow_html=True)

# Iterate in reverse order so delete works safely
for i in range(len(st.session_state.history) - 1, -1, -1):
    sender, msg = st.session_state.history[i]
    cols = st.columns([10, 1])

    with cols[0]:
        if sender == "You":
            st.markdown(f"<div class='user-bubble'><b>{sender}:</b> {msg}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='bot-bubble'><b>{sender}:</b> {msg}</div>", unsafe_allow_html=True)

    with cols[1]:
        if st.button("❌", key=f"del_{i}"):
            st.session_state.history.pop(i)
            st.rerun()

