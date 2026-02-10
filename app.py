import streamlit as st
import pandas as pd
import os
import easyocr
from deep_translator import GoogleTranslator

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Bio-Tech Smart Textbook",
    layout="wide"
)

# =========================
# OCR INITIALIZATION
# =========================
@st.cache_resource
def load_ocr():
    return easyocr.Reader(['en'])

reader = load_ocr()

@st.cache_data
def get_text_from_image(img_path):
    if img_path and os.path.exists(img_path):
        try:
            text = reader.readtext(img_path, detail=0)
            return " ".join(text).lower()
        except Exception:
            return ""
    return ""

# =========================
# LOAD KNOWLEDGE BASE
# =========================
@st.cache_data
def load_knowledge_base():
    # Try multiple filenames
    for file in ["knowledge_base.csv", "knowledge.csv"]:
        if os.path.exists(file):
            try:
                df = pd.read_csv(file)
                # Clean column names (remove hidden spaces)
                df.columns = df.columns.str.strip()
                # Remove rows that are completely empty
                df = df.dropna(how='all')
                return df
            except Exception as e:
                st.error(f"Error reading CSV: {e}")
    return None

knowledge_df = load_knowledge_base()

if knowledge_df is None:
    st.error("❌ Knowledge base CSV not found. Please ensure 'knowledge_base.csv' is in the folder.")
    st.stop()

# =========================
# SESSION STATE
# =========================
if "page_index" not in st.session_state:
    st.session_state.page_index = 0

# Sidebar Refresh (Crucial for CSV updates)
with st.sidebar:
    st.title("Settings")
    if st.button("🔄 Force Reload CSV Data"):
        st.cache_data.clear()
        st.rerun()

# =========================
# TABS
# =========================
tabs = st.tabs([
    "📖 Reader",
    "🧠 10 Points",
    "🔬 DNA Lab",
    "🔍 Search",
    "📊 Data",
    "🇮🇳 Hindi Helper",
])

# Get current row data
# Safety check to prevent index errors
if st.session_state.page_index >= len(knowledge_df):
    st.session_state.page_index = 0
row = knowledge_df.iloc[st.session_state.page_index]

# =========================
# TAB 1: READER
# =========================
with tabs[0]:
    col1, col2, col3 = st.columns([1, 2, 1])

    if col1.button("⬅ Previous"):
        st.session_state.page_index = max(0, st.session_state.page_index - 1)
        st.rerun()

    col2.markdown(
        f"<h3 style='text-align:center;'>Page {st.session_state.page_index + 1} / {len(knowledge_df)}</h3>",
        unsafe_allow_html=True
    )

    if col3.button("Next ➡"):
        st.session_state.page_index = min(len(knowledge_df) - 1, st.session_state.page_index + 1)
        st.rerun()

    st.divider()

    left, right = st.columns([2, 1])

    with left:
        st.header(row.get("Topic", "Untitled"))
        st.write(row.get("Explanation", "No explanation provided."))

        # Check for Detailed_Explanation column
        det_expl = row.get("Detailed_Explanation", "No additional details.")
        with st.expander("📘 Detailed Explanation"):
            st.write(det_expl)

    with right:
        img = str(row.get("Image", ""))
        if img and os.path.exists(img):
            with st.expander("🖼️ Show Diagram", expanded=True):
                st.image(img, use_container_width=True)
        else:
            st.info("No diagram available.")

# =========================
# TAB 2: 10 POINTS (FIXED LOGIC)
# =========================
with tabs[1]:
    st.header("🧠 10 Key Exam Points")
    
    # Check if the column exists
    if "Ten_Points" in knowledge_df.columns:
        points_raw = row.get("Ten_Points", "")
        
        # Check if cell is empty or NaN
        if pd.isna(points_raw) or str(points_raw).strip() == "":
            st.warning(f"No points found in the 'Ten_Points' column for: {row.get('Topic')}")
            st.info("Ensure your CSV has data in the same row as the topic.")
        else:
            # Split by newline (Excel Alt+Enter)
            points_list = str(points_raw).split("\n")
            for p in points_list:
                clean_p = p.strip()
                if clean_p:
                    # If the user already included numbers, don't double up
                    if clean_p[0].isdigit() and ('.' in clean_p[:3] or ')' in clean_p[:3]):
                        st.write(clean_p)
                    else:
                        st.write(f"• {clean_p}")
    else:
        st.error("❌ Column 'Ten_Points' not found in your CSV file.")
        st.write("Columns detected:", list(knowledge_df.columns))

# =========================
# TAB 3: DNA LAB
# =========================
with tabs[2]:
    st.header("🔬 DNA Analysis Tool")
    seq = st.text_area("Paste DNA sequence:", "ATGC").upper().strip()

    if st.button("Analyze"):
        if seq:
            try:
                gc = (seq.count("G") + seq.count("C")) / len(seq) * 100
                st.metric("GC Content", f"{gc:.2f}%")
            except ZeroDivisionError:
                st.error("Please enter a valid sequence.")

# =========================
# TAB 4: SEARCH (TEXT + OCR)
# =========================
with tabs[3]:
    st.header("🔍 Smart Search (Text + Diagrams)")
    query = st.text_input("Search term").lower().strip()

    if query:
        found_any = False
        for i, r in knowledge_df.iterrows():
            topic = str(r.get("Topic", "")).lower()
            expl = str(r.get("Explanation", "")).lower()
            img = str(r.get("Image", ""))

            found_in = []
            if query in topic or query in expl:
                found_in.append("Text")

            # OCR Search
            if img and os.path.exists(img):
                if query in get_text_from_image(img):
                    found_in.append("Diagram")

            if found_in:
                found_any = True
                with st.expander(f"📖 {r.get('Topic', 'Untitled')} (Page {i+1})"):
                    st.write(r.get("Explanation", ""))
                    if "Diagram" in found_in:
                        st.success("🎯 Found inside the diagram!")
                    if st.button(f"Go to Page {i+1}", key=f"search_go_{i}"):
                        st.session_state.page_index = i
                        st.rerun()

        if not found_any:
            st.warning("No matches found in text or diagrams.")

# =========================
# TAB 5: DATA
# =========================
with tabs[4]:
    st.header("📊 Knowledge Base Viewer")
    st.dataframe(knowledge_df)
    
    st.divider()
    st.subheader("Upload New Data")
    uploaded_file = st.file_uploader("Upload a new CSV", type="csv")
    if uploaded_file:
        new_df = pd.read_csv(uploaded_file)
        st.write("Preview of uploaded file:")
        st.dataframe(new_df)

# =========================
# TAB 6: HINDI HELPER
# =========================
with tabs[5]:
    st.header("🇮🇳 Hindi Explanation Helper")
    text_to_translate = st.text_area("Paste English text here:", height=150)

    if st.button("Translate to Hindi"):
        if not text_to_translate.strip():
            st.warning("Please enter text.")
        else:
            try:
                hindi_translation = GoogleTranslator(source="auto", target="hi").translate(text_to_translate)
                st.subheader("📝 Hindi Translation")
                st.info(hindi_translation)
            except Exception as e:
                st.error(f"Translation error: {e}")
