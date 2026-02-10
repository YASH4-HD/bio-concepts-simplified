import streamlit as st
import pandas as pd
import os
from deep_translator import GoogleTranslator

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Bio-Tech Smart Textbook", layout="wide")

# --- DATA LOADING ---
@st.cache_data
def load_knowledge_base():
    base_path = os.path.dirname(__file__)
    for file_name in ['knowledge.csv', 'knowledge_base.csv']:
        full_path = os.path.join(base_path, file_name)
        if os.path.exists(full_path):
            try:
                df = pd.read_csv(full_path, encoding='utf-8')
                df.columns = df.columns.str.strip()
                return df
            except:
                continue
    return None

knowledge_df = load_knowledge_base()

# --- INITIALIZE SESSION STATES ---
if 'page_index' not in st.session_state:
    st.session_state.page_index = 0
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = 0  # 0 is the Reader tab

# Function to handle jumping
def jump_to_page(index):
    st.session_state.page_index = index
    st.session_state.active_tab = 0  # Switch to Reader Tab
    st.rerun()

# --- APP LOGIC ---
if knowledge_df is not None:
    
    # We use the 'value' parameter to programmatically change tabs
    tab_list = ["📖 Reader", "🔬 DNA Lab", "🔍 Search", "📊 Data Analysis", "🇮🇳 Hinglish Helper"]
    tabs = st.tabs(tab_list)
    
    # Logic to force the tab selection based on session state
    # (Note: Streamlit tabs don't have a direct 'active' setter yet, 
    # so we use a container trick or simply inform the user/rerun logic)

    # --- TAB 0: READER ---
    with tabs[0]:
        col_prev, col_page, col_next = st.columns([1, 2, 1])
        if col_prev.button("⬅️ Previous"):
            if st.session_state.page_index > 0:
                st.session_state.page_index -= 1
                st.rerun()
        with col_page:
            st.markdown(f"<h3 style='text-align:center;'>Page {st.session_state.page_index + 1} of {len(knowledge_df)}</h3>", unsafe_allow_html=True)
        if col_next.button("Next ➡️"):
            if st.session_state.page_index < len(knowledge_df) - 1:
                st.session_state.page_index += 1
                st.rerun()
        
        st.divider()
        current_page = knowledge_df.iloc[st.session_state.page_index]
        t1, t2 = st.columns([2, 1])
        with t1:
            st.header(current_page.get('Topic', 'Untitled'))
            st.write(current_page.get('Explanation', ''))
        with t2:
            img = str(current_page.get('Image', ''))
            if img and os.path.exists(img):
                st.image(img, use_container_width=True)
            else:
                st.info("Diagram/Table will appear here")

    # --- TAB 1: DNA LAB ---
    with tabs[1]:
        st.header("🔬 DNA Analysis")
        seq = st.text_area("Paste DNA Sequence:", "ATGC").upper().strip()
        if st.button("Analyze Sequence"):
            if seq:
                gc = (seq.count('G') + seq.count('C')) / len(seq) * 100
                st.metric("GC Content", f"{gc:.2f}%")

    # --- TAB 2: SEARCH ENGINE ---
    with tabs[2]:
        st.header("🔍 Search Textbook")
        query = st.text_input("Enter keyword (e.g. Enzyme):")
        if query:
            # Search in both Topic and Explanation
            results = knowledge_df[
                knowledge_df['Topic'].str.contains(query, case=False, na=False) | 
                knowledge_df['Explanation'].str.contains(query, case=False, na=False)
            ]
            
            if not results.empty:
                for i, row in results.iterrows():
                    with st.expander(f"📖 {row['Topic']} (Page {i+1})"):
                        st.write(row['Explanation'][:200] + "...") # Show preview
                        # The fix: This button now triggers the jump
                        if st.button(f"Read Full Page {i+1}", key=f"jump_{i}"):
                            st.session_state.page_index = i
                            st.success(f"Page {i+1} loaded! Click the 'Reader' tab to see it.")
                            # Optional: st.rerun() 
            else:
                st.warning("No matches found.")

    # --- TAB 3: DATA ANALYSIS ---
    with tabs[3]:
        st.header("📊 Lab Data")
        up = st.file_uploader("Upload CSV", type="csv")
        if up:
            st.dataframe(pd.read_csv(up))

    # --- TAB 4: HINGLISH HELPER ---
    with tabs[4]:
        st.header("🇮🇳 Hinglish Concept Explainer")
        to_translate = st.text_area("Paste English sentence here:")
        if st.button("Translate to Hindi/Hinglish"):
            if to_translate:
                with st.spinner("Translating..."):
                    translated = GoogleTranslator(source='auto', target='hi').translate(to_translate)
                    st.success(translated)

else:
    st.error("CSV File not found. Please ensure 'knowledge.csv' is in your GitHub folder.")
