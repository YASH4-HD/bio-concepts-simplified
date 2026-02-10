import streamlit as st
import pandas as pd
import os
from deep_translator import GoogleTranslator
import easyocr

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Bio-Tech Smart Textbook", layout="wide")

# --- INITIALIZE OCR ---
@st.cache_resource
def load_ocr():
    return easyocr.Reader(['en'])

reader = load_ocr()

# --- OPTIMIZED OCR CACHING ---
# This function reads the image ONCE and remembers the text
@st.cache_data
def get_text_from_image(img_path):
    if img_path and os.path.exists(img_path):
        try:
            results = reader.readtext(img_path, detail=0)
            return " ".join(results).lower()
        except:
            return ""
    return ""

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

# --- APP LOGIC ---
if knowledge_df is not None:
    
    tab_list = ["📖 Reader", "🔬 DNA Lab", "🔍 Search", "📊 Data Analysis", "🇮🇳 Hinglish Helper"]
    tabs = st.tabs(tab_list)

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
                st.info("No diagram for this section.")

    # --- TAB 1: DNA LAB ---
    with tabs[1]:
        st.header("🔬 DNA Analysis")
        seq = st.text_area("Paste DNA Sequence:", "ATGC").upper().strip()
        if st.button("Analyze Sequence"):
            if seq:
                gc = (seq.count('G') + seq.count('C')) / len(seq) * 100
                st.metric("GC Content", f"{gc:.2f}%")

    # --- TAB 2: SMART SEARCH (OPTIMIZED) ---
    with tabs[2]:
        st.header("🔍 AI Search (Text + Images)")
        query = st.text_input("Search for any word (even inside diagrams):").lower().strip()
        
        if query:
            with st.spinner("Searching through text and diagrams..."):
                all_indices = []
                image_matches = []

                for idx, row in knowledge_df.iterrows():
                    # 1. Check Text
                    topic = str(row.get('Topic', '')).lower()
                    expl = str(row.get('Explanation', '')).lower()
                    
                    if query in topic or query in expl:
                        all_indices.append(idx)
                    else:
                        # 2. Check Image (Now lightning fast due to caching)
                        img_file = str(row.get('Image', ''))
                        img_text = get_text_from_image(img_file)
                        if query in img_text:
                            all_indices.append(idx)
                            image_matches.append(idx)

                # Remove duplicates and sort
                all_indices = sorted(list(set(all_indices)))

                if all_indices:
                    st.success(f"Found {len(all_indices)} matches!")
                    for i in all_indices:
                        row = knowledge_df.iloc[i]
                        with st.expander(f"📖 {row['Topic']} (Page {i+1})"):
                            if i in image_matches:
                                st.info("📍 Word found inside the diagram on this page.")
                            st.write(row['Explanation'][:200] + "...")
                            
                            # FIX: Instant jump button
                            if st.button(f"Go to Page {i+1}", key=f"search_btn_{i}"):
                                st.session_state.page_index = i
                                st.success(f"Loaded Page {i+1}! Click the 'Reader' tab.")
                                st.rerun()
                else:
                    st.warning("No matches found.")

    # --- TAB 3: DATA ANALYSIS ---
    with tabs[3]:
        st.header("📊 Lab Data")
        up = st.file_uploader("Upload CSV", type="csv")
        if up:
            st.dataframe(pd.read_csv(up))

        # --- TAB 4: HINDI & HINGLISH HELPER ---
    with tabs[4]:
        st.header("🇮🇳 Language Support Center")
        st.write("Understand complex Biotech concepts in your preferred language.")
        
        # User input
        to_translate = st.text_area("Paste English sentence or paragraph here:", 
                                   placeholder="e.g., Restriction enzymes are used to cut DNA at specific locations.",
                                   height=100)
        
        if st.button("Explain Concept"):
            if to_translate:
                with st.spinner("Processing..."):
                    # 1. Get Pure Hindi Translation
                    hindi_text = GoogleTranslator(source='auto', target='hi').translate(to_translate)
                    
                    # 2. Create Hinglish Version 
                    # (We keep technical English words but use Hindi grammar)
                    hinglish_text = hindi_text
                    # Logic: We replace some common Hindi translations back to English for scientific clarity
                    replacements = {
                        "प्रतिबंध एंजाइम": "Restriction Enzymes",
                        "अनुक्रम": "Sequence",
                        "अणु": "Molecule",
                        "क्लोनिंग": "Cloning",
                        "पुनर्संयोजक": "Recombinant"
                    }
                    for hi_word, en_word in replacements.items():
                        hinglish_text = hinglish_text.replace(hi_word, en_word)

                    # --- DISPLAY RESULTS IN COLUMNS ---
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("📝 Pure Hindi (शुद्ध हिंदी)")
                        st.markdown(f"""
                        <div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px; border-left: 5px solid #ff4b4b;">
                        {hindi_text}
                        </div>
                        """, unsafe_allow_html=True)
                        st.caption("Best for Hindi medium exam answers.")

                    with col2:
                        st.subheader("🗣️ Smart Hinglish")
                        st.markdown(f"""
                        <div style="background-color: #e1f5fe; padding: 15px; border-radius: 10px; border-left: 5px solid #03a9f4;">
                        {hinglish_text}
                        </div>
                        """, unsafe_allow_html=True)
                        st.caption("Best for understanding the logic.")

                    # --- 3. KEY TERMS BREAKDOWN ---
                    st.divider()
                    st.subheader("🔬 Vocabulary Breakdown (शब्दकोश)")
                    
                    # Logic to show definitions of specific biotech terms
                    terms_found = []
                    term_definitions = {
                        "enzyme": "**Enzyme (एंजाइम):** Biological molecules jo reaction fast karte hain.",
                        "dna": "**DNA:** Hamara genetic blueprint (आनुवंशिक ब्लूप्रिंट).",
                        "sequence": "**Sequence (अनुक्रम):** DNA mein bases ka order.",
                        "restriction": "**Restriction:** Limit karna ya specific jagah par rokna.",
                        "palindromic": "**Palindromic:** Aise words jo aage aur peeche se same read hote hain (जैसे: जहाज)."
                    }

                    t_cols = st.columns(len(term_definitions))
                    for i, (term, definition) in enumerate(term_definitions.items()):
                        if term in to_translate.lower():
                            st.info(definition)
            else:
                st.warning("Please enter some English text first.")


else:
    st.error("CSV File not found. Please ensure 'knowledge.csv' is in your GitHub folder.")
