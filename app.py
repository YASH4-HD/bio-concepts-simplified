import streamlit as st
import pandas as pd
import os
from deep_translator import GoogleTranslator
import easyocr

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Bio-Tech Smart Textbook",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# OCR INITIALIZATION
# =========================
@st.cache_resource
def load_ocr():
    return easyocr.Reader(['en'])

reader = load_ocr()

# =========================
# LOAD KNOWLEDGE BASE
# =========================
@st.cache_data
def load_knowledge_base():
    # Looks for your CSV file
    for file in ["knowledge.csv", "knowledge_base.csv"]:
        if os.path.exists(file):
            df = pd.read_csv(file)
            df.columns = df.columns.str.strip()
            return df
    # Fallback if no file exists
    return pd.DataFrame({"Topic": ["Sample"], "Explanation": ["Upload a CSV to begin."], "Ten_Points": ["Point 1"]})

knowledge_df = load_knowledge_base()

# =========================
# DYNAMIC HINGLISH ENGINE (IMPROVED)
# =========================
def generate_dynamic_hinglish(hindi_text, original_english):
    # 1. Phonetic Transliteration (Hindi to Roman)
    roman_hindi = transliterate(hindi_text, sanscript.DEVANAGARI, sanscript.ITRANS).lower()
    
    # 2. Fix common phonetic artifacts to make it look like "Chat Hindi"
    fixes = {
        "shha": "sh", "aa": "a", "haim": "hain", "mam": "mein", 
        "upayoga": "use", "karake": "karke", "lie": "liye", "vishi": "specific",
        "jyam": "jaan", "bhai": "bhi", "dvara": "ke through"
    }
    for old, new in fixes.items():
        roman_hindi = roman_hindi.replace(old, new)

    # 3. KEYWORD PROTECTION (The "Dynamic" Fix)
    # Extract words that look like scientific terms from original English
    # (Words in ALL CAPS or words longer than 5 letters)
    keywords = re.findall(r'\b[A-Z]{2,}\b|\b\w{5,}\b', original_english)
    
    for word in set(keywords):
        # If a version of the English word exists in the transliteration, swap it back
        # This prevents "DNA" from becoming "die-en-e"
        pattern = re.compile(re.escape(word[:3]), re.IGNORECASE) 
        roman_hindi = pattern.sub(word, roman_hindi)
    
    return roman_hindi.strip().capitalize()

def get_dynamic_tips(text):
    all_tips = {
        "dna": "DNA extraction ke liye cold ethanol zaroori hai precipitation ke liye.",
        "pcr": "PCR mein 3 main steps hote hain: Denaturation, Annealing, aur Extension.",
        "enzyme": "Enzymes temperature sensitive hote hain, hamesha ice par rakhen.",
        "taq": "Taq Polymerase Thermus aquaticus bacteria se isolate kiya jata hai.",
        "gel": "Agarose gel electrophoresis mein DNA negative charge ki wajah se anode (+) ki taraf jata hai."
    }
    found = [tip for key, tip in all_tips.items() if key in text.lower()]
    return found if found else ["Exam Tip: Focus on diagrams and bold technical terms."]

# =========================
# SESSION STATE
# =========================
if "page_index" not in st.session_state:
    st.session_state.page_index = 0

# =========================
# MAIN UI
# =========================
st.title("🧬 Bio-Tech Smart Textbook")

tabs = st.tabs(["📖 Reader", "🧠 10 Points", "🔬 DNA Lab", "🔍 Search", "📊 Data", "🇮🇳 Hinglish Helper"])

# 1. READER TAB
with tabs[0]:
    col1, col2, col3 = st.columns([1, 2, 1])
    if col1.button("⬅ Previous"):
        st.session_state.page_index = max(0, st.session_state.page_index - 1)
        st.rerun()
    col2.markdown(f"<h3 style='text-align:center;'>Page {st.session_state.page_index + 1} / {len(knowledge_df)}</h3>", unsafe_allow_html=True)
    if col3.button("Next ➡"):
        st.session_state.page_index = min(len(knowledge_df) - 1, st.session_state.page_index + 1)
        st.rerun()
    
    st.divider()
    row = knowledge_df.iloc[st.session_state.page_index]
    left, right = st.columns([2, 1])
    with left:
        st.header(row.get("Topic", "Untitled"))
        st.write(row.get("Explanation", "No content available."))
    with right:
        img = str(row.get("Image", ""))
        if img and os.path.exists(img):
            st.image(img, use_container_width=True)
        else:
            st.info("No diagram available for this topic.")

# 2. 10 POINTS TAB
with tabs[1]:
    st.header("🧠 Quick Revision Points")
    points = row.get("Ten_Points", "")
    if pd.isna(points) or points == "":
        st.write("No revision points available.")
    else:
        for p in str(points).split("\n"):
            if p.strip(): st.info(f"• {p.strip()}")

# 3. DNA LAB
with tabs[2]:
    st.header("🔬 DNA Sequence Analyzer")
    seq = st.text_area("Enter DNA Sequence (A, T, G, C):", "ATGCATGC").upper()
    if st.button("Analyze Sequence"):
        if all(base in "ATGC" for base in seq):
            gc = (seq.count('G') + seq.count('C')) / len(seq) * 100
            st.metric("GC Content", f"{gc:.2f}%")
            st.progress(gc/100)
        else:
            st.error("Invalid DNA sequence! Use only A, T, G, C.")

# 4. SEARCH
with tabs[3]:
    st.header("🔍 Search Knowledge Base")
    query = st.text_input("Enter topic name...")
    if query:
        results = knowledge_df[knowledge_df['Topic'].str.contains(query, case=False, na=False)]
        for i, r in results.iterrows():
            with st.expander(r['Topic']):
                st.write(r['Explanation'])
                if st.button("Open Page", key=f"btn_{i}"):
                    st.session_state.page_index = i
                    st.rerun()

# 5. DATA MANAGEMENT
with tabs[4]:
    st.header("📊 Upload New Content")
    uploaded_file = st.file_uploader("Upload CSV (Must have Topic, Explanation, Ten_Points columns)", type="csv")
    if uploaded_file:
        new_df = pd.read_csv(uploaded_file)
        st.write("Preview:", new_df.head())
        if st.button("Save Data"):
            new_df.to_csv("knowledge_base.csv", index=False)
            st.success("Data Saved! Please refresh the app.")

# 6. HINGLISH HELPER (THE DYNAMIC FIX)
with tabs[5]:
    st.header("🇮🇳 Smart Hinglish Translator")
    st.write("Paste complex English text to get a 'Chat-style' Hinglish explanation.")
    
    user_input = st.text_area("English Input:", height=150, placeholder="Example: DNA is a double helical structure discovered by Watson and Crick.")

    if st.button("Convert to Hinglish"):
        if user_input.strip():
            with st.spinner("Processing dynamic translation..."):
                # Step 1: Translate to Hindi
                hindi_trans = GoogleTranslator(source="auto", target="hi").translate(user_input)
                
                # Step 2: Convert to Smart Hinglish
                hinglish_trans = generate_dynamic_hinglish(hindi_trans, user_input)
                
                # Step 3: Get Contextual Tips
                tips = get_dynamic_tips(user_input)

                c1, c2 = st.columns(2)
                with c1:
                    st.subheader("📝 Hindi")
                    st.markdown(f'<div style="background-color:#f9f9f9; padding:15px; border-radius:10px; color:#333;">{hindi_trans}</div>', unsafe_allow_html=True)
                
                with c2:
                    st.subheader("🗣 Smart Hinglish")
                    st.markdown(f'<div style="background-color:#e8f4f8; padding:15px; border-radius:10px; color:#000; border-left:5px solid #2196f3;">{hinglish_trans}</div>', unsafe_allow_html=True)
                    st.code(hinglish_trans, language="text")

                st.divider()
                st.subheader("💡 Exam Strategy")
                for tip in tips:
                    st.warning(tip)
        else:
            st.warning("Please enter some text first.")
