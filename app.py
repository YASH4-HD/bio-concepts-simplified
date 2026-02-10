import streamlit as st
import pandas as pd
import os
import google.generativeai as genai
import easyocr
import re

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Bio-Tech Smart AI Textbook",
    page_icon="🧬",
    layout="wide"
)

# =========================
# API SETUP (SECURE & ERROR-PROOF)
# =========================
# This looks for GEMINI_API_KEY in your Streamlit Cloud Secrets
if "GEMINI_API_KEY" in st.secrets:
    try:
        API_KEY = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=API_KEY)
        
        # Fallback Logic: Try Flash first, then Pro
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            # Test connection
            model.generate_content("test") 
        except Exception:
            model = genai.GenerativeModel('gemini-pro')
            
    except Exception as e:
        st.error(f"Failed to initialize Gemini: {e}")
else:
    st.error("🔑 API Key not found! Please add 'GEMINI_API_KEY' to Streamlit Secrets.")
    st.stop()

# =========================
# DATA LOADING
# =========================
@st.cache_data
def load_knowledge_base():
    file_path = "knowledge_base.csv"
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)
            df.columns = df.columns.str.strip() # Remove hidden spaces
            return df
        except Exception as e:
            st.error(f"Error reading CSV: {e}")
    
    # Default data if file is missing
    return pd.DataFrame({
        "Topic": ["Welcome to Bio-Tech AI"], 
        "Explanation": ["Please upload your knowledge_base.csv in the Data Management tab."], 
        "Ten_Points": ["1. Upload CSV\n2. Set API Key\n3. Start Learning"],
        "Image": [""]
    })

knowledge_df = load_knowledge_base()

def get_col_data(row, possible_names, default="Not Available"):
    for name in possible_names:
        if name in row:
            return str(row[name])
    return default

# =========================
# AI LOGIC
# =========================
def ask_gemini_hinglish(text):
    prompt = f"""
    Explain this Bio-Technology concept in 'Hinglish' (Natural mix of Hindi and English in Roman script).
    - Keep technical terms (DNA, PCR, CRISPR, Enzymes, etc.) in English.
    - Use a friendly, conversational 'Chat' style tone.
    - Explain like you are talking to a student.
    - Write Hindi words using English letters.
    
    Text to explain: {text}
    """
    try:
        response = model.generate_content(prompt)
        if response and response.text:
            return response.text
        else:
            return "AI was unable to generate a response. Please try again."
    except Exception as e:
        return f"AI Error: {str(e)}. Please check if your API key is active."

# =========================
# SESSION STATE
# =========================
if "page_index" not in st.session_state:
    st.session_state.page_index = 0

# =========================
# MAIN UI
# =========================
st.title("🧬 Bio-Tech Smart AI Textbook")

tabs = st.tabs(["📖 AI Reader", "🧠 10 Points", "🔬 DNA Lab", "🇮🇳 AI Hinglish Helper", "📊 Data Management"])

# Safety check for empty dataframe
if not knowledge_df.empty:
    row = knowledge_df.iloc[st.session_state.page_index]
else:
    st.error("Database is empty.")
    st.stop()

# --- TAB 1: AI READER ---
with tabs[0]:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("⬅ Previous"):
            st.session_state.page_index = max(0, st.session_state.page_index - 1)
            st.rerun()
    with col2:
        st.markdown(f"<h3 style='text-align:center;'>Page {st.session_state.page_index + 1} / {len(knowledge_df)}</h3>", unsafe_allow_html=True)
    with col3:
        if st.button("Next ➡"):
            st.session_state.page_index = min(len(knowledge_df) - 1, st.session_state.page_index + 1)
            st.rerun()
    
    st.divider()
    
    left, right = st.columns([1, 1])
    with left:
        topic = get_col_data(row, ["Topic", "topic", "Title"])
        expl = get_col_data(row, ["Explanation", "explanation", "Content"])
        
        st.header(topic)
        st.write(expl)
        
        if st.button("✨ AI Hinglish Explanation"):
            with st.spinner("Gemini is explaining..."):
                result = ask_gemini_hinglish(expl)
                st.info(result)

    with right:
        img_path = get_col_data(row, ["Image", "image", "Picture"], "")
        if img_path and os.path.exists(img_path):
            st.image(img_path, use_container_width=True)
        else:
            st.info("No diagram found for this topic.")

# --- TAB 2: 10 POINTS ---
with tabs[1]:
    topic = get_col_data(row, ["Topic", "topic"])
    st.header(f"Quick Revision: {topic}")
    
    points_text = get_col_data(row, ["Ten_Points", "Points", "ten_points", "Key Points"])
    
    if points_text != "Not Available":
        points_list = points_text.split('\n')
        for p in points_list:
            if p.strip():
                st.success(f"🔹 {p.strip()}")
    else:
        st.warning("No revision points found in CSV. Ensure you have a 'Ten_Points' column.")

# --- TAB 3: DNA LAB ---
with tabs[2]:
    st.header("🔬 DNA Sequence Analyzer")
    dna = st.text_input("Enter DNA Sequence:", "ATGCATGC").upper()
    if dna:
        # Basic Bio-informatics logic
        valid_dna = all(base in "ATGC" for base in dna)
        if valid_dna:
            gc = (dna.count('G') + dna.count('C')) / len(dna) * 100
            st.metric("GC Content", f"{gc:.2f}%")
            st.write(f"**Sequence Length:** {len(dna)} bp")
        else:
            st.error("Invalid Sequence! Please use only A, T, G, C.")

# --- TAB 4: AI HINGLISH HELPER ---
with tabs[3]:
    st.header("🇮🇳 Custom AI Translator")
    st.write("Paste any English text from your notes to get a Hinglish explanation.")
    user_text = st.text_area("Paste English Text here:", height=200)
    if st.button("Translate with AI"):
        if user_text.strip():
            with st.spinner("Processing..."):
                st.markdown("---")
                st.write(ask_gemini_hinglish(user_text))
        else:
            st.warning("Please paste some text first.")

# --- TAB 5: DATA MANAGEMENT ---
with tabs[4]:
    st.header("📊 Database Management")
    st.write("Detected Columns:", list(knowledge_df.columns))
    
    uploaded_file = st.file_uploader("Upload New knowledge_base.csv", type="csv")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        df.to_csv("knowledge_base.csv", index=False)
        st.success("File uploaded successfully! Please refresh the page to see changes.")
    
    st.divider()
    st.subheader("Current Data Preview")
    st.dataframe(knowledge_df)
