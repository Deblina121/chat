import google.generativeai as genai
import streamlit as st
import sqlite3
from datetime import datetime

# ---------------- Configure Gemini ----------------
genai.configure(api_key="AIzaSyB7986dsKfXWd5vLDH-XH2kepuh3AwhiQM")   # ⚠️ Replace with your API Key
model = genai.GenerativeModel("gemini-1.5-flash")

# ---------------- Database Setup ----------------
conn = sqlite3.connect("chat_history.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
    CREATE TABLE IF NOT EXISTS chats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        sender TEXT,
        message TEXT
    )
""")
conn.commit()

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

# ---------------- Chat Input ----------------
user_input = st.chat_input("💬 Type your message...")

if user_input:
    # Save user message
    c.execute("INSERT INTO chats (timestamp, sender, message) VALUES (?, ?, ?)",
              (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "You", user_input))
    conn.commit()

    # Gemini response
    try:
        response = model.generate_content(user_input)
        bot_reply = response.text if response.text else "⚠️ No response from Gemini."
    except Exception as e:
        bot_reply = f"⚠️ Error: {str(e)}"

    # Save bot reply
    c.execute("INSERT INTO chats (timestamp, sender, message) VALUES (?, ?, ?)",
              (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Gemini ⚡", bot_reply))
    conn.commit()

# ---------------- Display Chat ----------------
st.markdown("<div class='chat-box'>", unsafe_allow_html=True)

# Load history from DB
c.execute("SELECT id, sender, message FROM chats ORDER BY id ASC")
rows = c.fetchall()

for msg_id, sender, msg in rows:
    bubble_class = "user-bubble" if sender == "You" else "bot-bubble"

    cols = st.columns([12, 1])  # message + delete button

    with cols[0]:
        st.markdown(
            f"<div class='{bubble_class}'><b>{sender}:</b> {msg}</div>",
            unsafe_allow_html=True
        )

    with cols[1]:
        if msg != "🗑 This message was deleted":  # show delete only if not already deleted
            if st.button("🗑", key=f"del_{msg_id}"):
                c.execute("UPDATE chats SET message=? WHERE id=?",
                          ("🗑 This message was deleted", msg_id))
                conn.commit()
                st.rerun()

st.markdown("</div>", unsafe_allow_html=True)
