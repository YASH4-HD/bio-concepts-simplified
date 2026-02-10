import streamlit as st
import pandas as pd
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Bio-Tech Smart Textbook", layout="wide")

# --- CUSTOM CSS FOR BETTER READING ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #007bff; color: white; }
    .stMarkdown { font-size: 1.1rem; line-height: 1.6; }
    .page-box { padding: 20px; background: white; border-radius: 15px; border: 1px solid #ddd; }
    </style>
    """, unsafe_allow_html=True)

# --- DATA LOADING ---
@st.cache_data
def load_data():
    # Replace 'knowledge_base.csv' with your actual file path
    if os.path.exists('knowledge_base.csv'):
        return pd.read_csv('knowledge_base.csv')
    else:
        # Dummy data for demonstration
        return pd.DataFrame({
            'Section': ['1.1', '1.2', '2.1'],
            'Topic': ['Structure of DNA', 'PCR Basics', 'Gel Electrophoresis'],
            'Explanation': [
                'DNA is a double helix made of nucleotides...',
                'Polymerase Chain Reaction (PCR) is used to amplify DNA...',
                'Gel electrophoresis separates DNA fragments by size...'
            ],
            'Image': ['dna.jpg', 'pcr.jpg', 'gel.jpg'] # Ensure these exist or use placeholders
        })

knowledge_df = load_data()

# --- INITIALIZE SESSION STATE FOR PAGE NAVIGATION ---
if 'page_index' not in st.session_state:
    st.session_state.page_index = 0

# --- APP LAYOUT ---
st.title("🧬 Wilson & Walker: Interactive Lab Guide")

tab0, tab1, tab2, tab3 = st.tabs(["📖 Interactive Reader", "🔬 DNA Lab Tools", "🤖 AI Research Assistant", "📊 Data Analysis"])

# --- TAB 0: THE INTERACTIVE READER (OPTION 1) ---
with tab0:
    st.subheader("Interactive Textbook Interface")
    
    # Navigation Row
    col_prev, col_page, col_next = st.columns([1, 2, 1])
    
    if col_prev.button("⬅️ Previous Page"):
        if st.session_state.page_index > 0:
            st.session_state.page_index -= 1
            st.rerun()

    with col_page:
        st.markdown(f"<h3 style='text-align: center;'>Page {st.session_state.page_index + 1} of {len(knowledge_df)}</h3>", unsafe_allow_html=True)

    if col_next.button("Next Page ➡️"):
        if st.session_state.page_index < len(knowledge_df) - 1:
            st.session_state.page_index += 1
            st.rerun()

    # Get current page data
    current_page = knowledge_df.iloc[st.session_state.page_index]

    # Content Display
    st.markdown("---")
    col_text, col_img = st.columns([3, 2])

    with col_text:
        st.markdown(f"## {current_page['Topic']}")
        st.markdown(f"**Section:** {current_page['Section']}")
        st.write(current_page['Explanation'])
        
        # Action Button to link with Lab
        if st.button("Apply this topic in DNA Lab 🔬"):
            st.info(f"Context for '{current_page['Topic']}' sent to Lab Tools!")

    with col_img:
        if pd.notna(current_page['Image']) and os.path.exists(str(current_page['Image'])):
            st.image(current_page['Image'], caption=current_page['Topic'], use_container_width=True)
        else:
            # Placeholder for missing images
            st.info("💡 Image/Diagram placeholder for " + current_page['Topic'])

# --- TAB 1: DNA LAB TOOLS ---
with tab1:
    st.header("Sequence Analysis Tools")
    seq = st.text_area("Enter DNA Sequence:", "ATGC...", height=150)
    
    c1, c2, c3 = st.columns(3)
    if c1.button("Calculate GC Content"):
        gc = (seq.count('G') + seq.count('C')) / len(seq) * 100
        st.metric("GC Content", f"{gc:.2f}%")
    
    if c2.button("Find Reverse Complement"):
        complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
        rev_comp = "".join(complement.get(base, base) for base in reversed(seq))
        st.code(rev_comp)

# --- TAB 2: AI RESEARCH ASSISTANT ---
with tab2:
    st.header("Ask the Wilson & Walker AI")
    user_query = st.text_input("Ask a question about the current section:")
    if user_query:
        st.write(f"**AI Response:** Based on Section {current_page['Section']}, the answer is...")
        st.caption("Note: Integrate OpenAI/Anthropic API here for real responses.")

# --- TAB 3: DATA ANALYSIS ---
with tab3:
    st.header("Experimental Data Upload")
    uploaded_file = st.file_uploader("Upload Lab Results (CSV)", type="csv")
    if uploaded_file:
        data = pd.read_csv(uploaded_file)
        st.line_chart(data)
