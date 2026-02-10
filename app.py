import streamlit as st
import pandas as pd
from Bio.Seq import Seq
from Bio.Restriction import Analysis, AllEnzymes
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Wilson Walker Digital Lab",
    page_icon="🧬",
    layout="wide"
)

# --- DATA LOADING (Automatic/Public) ---
@st.cache_data
def load_knowledge_base():
    file_path = "knowledge.csv"
    if os.path.exists(file_path):
        # We use quotechar to handle commas inside the book text
        return pd.read_csv(file_path, quotechar='"')
    return None

knowledge_df = load_knowledge_base()

# --- SIDEBAR: NAVIGATION ---
with st.sidebar:
    st.title("📚 Book Navigator")
    
    if knowledge_df is not None:
        st.success("✅ Database Online")
        # Dropdown for all users to see
        selected_topic = st.selectbox("Search Topic:", knowledge_df["Topic"].unique())
        
        # Get data for the selected topic
        topic_info = knowledge_df[knowledge_df["Topic"] == selected_topic].iloc[0]
        
        st.divider()
        st.markdown(f"**Current Section:** {topic_info['Section']}")
        
        # Small sidebar preview of the image
        if "Image" in topic_info and pd.notna(topic_info['Image']):
            img_path = str(topic_info['Image'])
            if os.path.exists(img_path):
                st.image(img_path)
    else:
        st.error("❌ 'knowledge.csv' not found.")
        st.info("Please ensure your CSV file is in the same folder as this script.")

    st.divider()
    st.caption("PhD Project: Interactive Molecular Education")

# --- MAIN INTERFACE ---
st.title("🔬 Wilson & Walker: Interactive Molecular Lab")

# Create Tabs
tab0, tab1, tab2, tab3 = st.tabs(["🏠 Home Dashboard", "🧬 Sequence Analyzer", "📦 Vector Selector", "🧪 PCR Optimizer"])

# --- TAB 0: HOME DASHBOARD (Visible to everyone) ---
with tab0:
    if knowledge_df is not None:
        st.header(selected_topic)
        col_text, col_diag = st.columns([1, 1])
        
        with col_text:
            st.subheader(f"Textbook Context: Section {topic_info['Section']}")
            st.write(topic_info['Explanation'])
            st.info("💡 Select a different topic in the sidebar to update this page.")
            
        with col_diag:
            if "Image" in topic_info and pd.notna(topic_info['Image']):
                img_path = str(topic_info['Image'])
                if os.path.exists(img_path):
                    st.image(img_path, use_container_width=True, caption=f"Diagram: {selected_topic}")
                else:
                    st.warning(f"Image file '{img_path}' missing from server.")
            else:
                st.info("No diagram available for this specific topic.")
    else:
        st.header("Welcome to the Digital Lab")
        st.warning("Database is missing. Please upload 'knowledge.csv' to the repository.")

# --- TAB 1: SEQUENCE ANALYZER ---
with tab1:
    st.header("Restriction Mapping Tool")
    dna_file = st.file_uploader("Upload DNA Sequence (.txt or .fasta)", type=["txt", "fasta"])
    
    if dna_file:
        content = dna_file.getvalue().decode("utf-8")
        lines = content.splitlines()
        raw_seq = "".join(lines[1:]) if lines[0].startswith(">") else "".join(lines)
        clean_seq = "".join(raw_seq.split()).upper()
        
        if st.button("Analyze Sequence"):
            my_seq = Seq(clean_seq)
            analysis = Analysis(AllEnzymes, my_seq)
            results = analysis.full()
            
            st.metric("Sequence Length", f"{len(my_seq)} bp")
            cols = st.columns(2)
            for i, (enz, sites) in enumerate(results.items()):
                if sites:
                    with cols[i % 2].expander(f"Enzyme: {enz}"):
                        st.write(f"Cut positions: {sites}")
                        st.code(f"Cut site count: {len(sites)}")

# --- TAB 2: VECTOR SELECTOR ---
with tab2:
    st.header("Vector Selection (Table 4.4)")
    kb_size = st.number_input("Enter DNA Insert Size (kb):", 0.1, 2000.0, 1.0)
    
    if kb_size < 10:
        st.success("**Recommended: Plasmid** (Ref: Section 4.12.1)")
    elif 10 <= kb_size <= 23:
        st.success("**Recommended: Bacteriophage λ** (Ref: Section 4.12.2)")
    elif 100 <= kb_size <= 300:
        st.success("**Recommended: BAC** (Ref: Section 4.12.4)")
    else:
        st.warning("**Recommended: YAC** (Ref: Section 4.12.5)")

# --- TAB 3: PCR OPTIMIZER ---
with tab3:
    st.header("PCR Troubleshooting")
    problem = st.selectbox("Identify Gel Issue:", ["No Bands", "Smearing", "Non-specific Bands"])
    
    advice = {
        "No Bands": "Lower Annealing Temperature, increase MgCl2, check template.",
        "Smearing": "Reduce cycle number, check template purity.",
        "Non-specific Bands": "Increase Annealing Temperature, use Hot Start Taq."
    }
    st.error(f"Wilson & Walker Solution: {advice[problem]}")

st.divider()
st.caption("PhD Research Project | Integrating Digital Tools with Biochemistry Education")
