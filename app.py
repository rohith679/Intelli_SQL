import streamlit as st
import os
import sqlite3
import google.generativeai as genai

# Try to get API key from Streamlit Secrets (Streamlit Cloud)
api_key = st.secrets.get("API_KEY", None)

# Configure Gemini
genai.configure(api_key=api_key)


# Gemini Prompt
prompt = """
You are an expert in converting English questions to SQL query!
The SQL database is named STUDENTS and has the following columns:
NAME (VARCHAR), CLASS (VARCHAR), MARKS (INT), COMPANY (VARCHAR), CITY (VARCHAR), GRADUATION_YEAR (INT), INTERNSHIP_COMPLETED (BOOLEAN).

Example 1: How many students are present?
SELECT COUNT(*) FROM STUDENTS;

Example 2: List all BTech students from Mumbai.
SELECT * FROM STUDENTS WHERE CLASS="BTech" AND CITY="Mumbai";
"""

# Gemini Function
def get_response(que, prompt):
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content([prompt, que])
    return response.text

# SQL Runner
def read_query(sql, db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.commit()
    conn.close()
    return rows

# Page Config
st.set_page_config(page_title="IntelliSQL", page_icon="🧠", layout="wide")

# --- CSS Styling ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500&family=Roboto+Mono&display=swap');

html, body, .stApp {
    background: linear-gradient(135deg, #0d0d0d, #1a0000);
    color: white;
    font-family: 'Orbitron', sans-serif;
    scroll-behavior: smooth;
    transition: all 0.4s ease;
}

.main-title {
    font-size: 3rem;
    text-align: center;
    color: #ff1a1a;
    animation: flicker 1.5s infinite alternate;
    text-shadow: 0 0 10px red, 0 0 20px crimson, 0 0 30px darkred;
}
@keyframes flicker {
    0% { opacity: 1; }
    50% { opacity: 0.75; }
    100% { opacity: 1; }
}

.subtitle {
    text-align: center;
    font-size: 1.4rem;
    color: #ff9999;
    margin-bottom: 2rem;
    font-family: 'Roboto Mono', monospace;
    animation: slide-up 1.5s ease;
}
@keyframes slide-up {
    from { transform: translateY(20px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}

.description-box {
    background: rgba(255, 255, 255, 0.08);
    border-radius: 20px;
    padding: 1.5rem;
    backdrop-filter: blur(6px);
    box-shadow: 0 0 10px rgba(255, 0, 0, 0.4);
    margin-bottom: 2rem;
}

/* Larger input label styling */
.stTextInput > label {
    font-size: 1.4rem !important;
    font-weight: 600;
    color: #00ffff;
    margin-bottom: 0.3rem;
    font-family: 'Orbitron', sans-serif;
}

.stTextInput > div > input {
    background-color: rgba(0,0,0,0.5);
    color: #00ffff;
    border: 1px solid #00ffff;
    border-radius: 10px;
    padding: 0.6rem;
    transition: 0.3s;
}
.stTextInput > div > input:hover {
    box-shadow: 0 0 12px #00ffff;
}

.stButton button {
    background: linear-gradient(135deg, #ff0000, #990000);
    color: white;
    border: none;
    border-radius: 10px;
    font-weight: bold;
    padding: 0.6rem 1.5rem;
    transition: transform 0.3s;
}
.stButton button:hover {
    transform: scale(1.08);
    box-shadow: 0 0 12px red;
}
.stButton button:active {
    background: linear-gradient(135deg, #b30000, #660000);
    color: white;
}

.response {
    animation: glowFade 1s ease;
    background: rgba(255, 255, 255, 0.05);
    padding: 1rem;
    border-radius: 15px;
    box-shadow: 0 0 10px #ff4d4d;
    margin-top: 1rem;
}
@keyframes glowFade {
    from { transform: scale(0.95); opacity: 0; }
    to { transform: scale(1); opacity: 1; }
}

.footer {
    text-align: center;
    margin-top: 2rem;
    font-size: 0.9rem;
    opacity: 0;
    animation: fadeIn 3s forwards;
    color: #999;
}
.footer:hover {
    color: white;
    text-shadow: 0 0 10px #ff1a1a;
}
@keyframes fadeIn {
    to { opacity: 1; }
}

.schema {
    font-family: 'Roboto Mono', monospace;
    background-color: rgba(255, 255, 255, 0.07);
    padding: 1rem;
    border-radius: 12px;
    margin-top: 1rem;
    color: #66ffff;
    font-size: 0.9rem;
    border-left: 4px solid #ff1a1a;
}
</style>
""", unsafe_allow_html=True)

# --- Title & Subtitle ---
st.markdown("<h1 class='main-title'>IntelliSQL - Ask your Database</h1>", unsafe_allow_html=True)
st.markdown("<h3 class='subtitle'>Query your database like a pro – just by asking in English!</h3>", unsafe_allow_html=True)

# --- Description ---
st.markdown("""
<div class='description-box'>
<p><b>IntelliSQL</b> is a smart interface that converts your English questions into SQL queries and runs them on your database.</p>

<ul>
<li>🤖 Translates English to SQL instantly</li>
<li>📊 Runs directly on your local STUDENTS database</li>
<li>⚡ Powered by Gemini 2.0 Pro</li>
<li>🧠 Designed for students, analysts & developers</li>
</ul>

<div style="background-color: rgba(255, 50, 50, 0.15); border-left: 5px solid #ff4d4d; padding: 1rem; margin-top: 1.2rem; font-family: 'Roboto Mono', monospace; color: #66ccff; border-radius: 12px; box-shadow: 0 0 8px rgba(255, 0, 0, 0.3);">
🔔 <b>Note:</b> Please ask questions only based on the structure of our student database.<br><br>
Each record contains:
<ul style="margin-left: 1rem;">
<li><b>name</b></li>
<li><b>class</b> (e.g., BTech, MTech)</li>
<li><b>marks</b></li>
<li><b>company</b> (placement company)</li>
<li><b>city</b> (student's city)</li>
<li><b>graduation year</b></li>
<li><b>internship completed</b> (true/false)</li>
</ul>
</div>
</div>
""", unsafe_allow_html=True)

# --- Input ---
que = st.text_input("📝 Enter your English question here:")
submit = st.button("🚀 Generate SQL & Run")

# --- Processing ---
if submit and que:
    try:
        response = get_response(que, prompt)
        cleaned_sql = response.strip().replace("```sql", "").replace("```", "").strip()
        st.markdown(f"<h4>🔍 Generated SQL:</h4><code>{cleaned_sql}</code>", unsafe_allow_html=True)

        # Optional: Basic check
        if not cleaned_sql.lower().startswith("select"):
            st.error("❌ Invalid SQL generated. Please try rephrasing your question.")
        else:
            result = read_query(cleaned_sql, "data.db")
            if result:
                st.markdown("<div class='response'>", unsafe_allow_html=True)
                st.subheader("📥 Query Result:")
                st.table(result)
                st.markdown("</div>", unsafe_allow_html=True)
            else:
                st.warning("⚠️ No results found for this query.")

    except Exception as e:
        st.error(f"❌ Error occurred: {e}")

# --- Footer ---
st.markdown("<div class='footer'>Built with ❤️ using Streamlit, Gemini LLM, and SQLite</div>", unsafe_allow_html=True)
