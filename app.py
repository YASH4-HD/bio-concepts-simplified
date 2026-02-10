import streamlit as st
import pandas as pd
from Bio.Seq import Seq
from Bio.Restriction import Analysis, AllEnzymes
import io

# --- PAGE CONFIG ---
st.set_page_config(page_title="Wilson Walker Digital Lab", layout="wide")

# --- LOAD KNOWLEDGE FROM CSV ---
@st.cache_data # This keeps the app fast
def load_knowledge():
    try:
        # Load the CSV file you created
        df = pd.read_csv("knowledge.csv")
        return df
    except:
        # Fallback if file is missing
        return pd.DataFrame({"Topic": ["N/A"], "Section": ["0.0"], "Explanation": ["Please upload knowledge.csv"]})

knowledge_df = load_knowledge()

# --- SIDEBAR: DYNAMIC NAVIGATOR ---
with st.sidebar:
    st.title("📚 Book Navigator")
    st.write("Data loaded from `knowledge.csv`")
    
    # Create a dropdown from the "Topic" column of your CSV
    selected_topic = st.selectbox("Select a Topic:", knowledge_df["Topic"].unique())
    
    # Filter the CSV for the selected topic
    topic_info = knowledge_df[knowledge_df["Topic"] == selected_topic].iloc[0]
    
    st.success(f"**Section {topic_info['Section']}**")
    st.write(topic_info['Explanation'])
    st.divider()
    st.caption("PhD Project: Data-Driven Education")

# --- MAIN INTERFACE ---
st.title("🔬 Wilson & Walker: Interactive Molecular Lab")

tab1, tab2, tab3 = st.tabs(["🧬 Sequence Analyzer", "📦 Vector Selector", "🧪 PCR Optimizer"])

# --- TAB 1: SEQUENCE ANALYZER ---
with tab1:
    st.header("Restriction Mapping")
    uploaded_file = st.file_uploader("Upload DNA File (.txt / .fasta)", type=["txt", "fasta"])
    
    final_seq = ""
    if uploaded_file:
        content = uploaded_file.getvalue().decode("utf-8")
        lines = content.splitlines()
        final_seq = "".join(lines[1:]) if lines[0].startswith(">") else "".join(lines)
    
    clean_seq = "".join(final_seq.split()).upper()
    
    if st.button("Analyze") and clean_seq:
        my_seq = Seq(clean_seq)
        analysis = Analysis(AllEnzymes, my_seq)
        results = analysis.full()
        
        st.metric("Length", f"{len(my_seq)} bp")
        for enz, sites in results.items():
            if sites:
                st.write(f"✅ **{enz}**: Cut at {sites}")

# --- TAB 2: VECTOR SELECTOR ---
with tab2:
    st.header("Vector Selection Logic")
    size = st.number_input("Insert Size (kb)", 0.1, 2000.0, 1.0)
    if size < 10: st.success("Standard Plasmid (Ref: 4.12.1)")
    elif 10 <= size <= 23: st.success("Bacteriophage λ (Ref: 4.12.2)")
    else: st.warning("BAC or YAC (Ref: 4.12.4)")

# --- TAB 3: PCR OPTIMIZER ---
with tab3:
    st.header("PCR Troubleshooting")
    issue = st.selectbox("Gel Result:", ["No Bands", "Smearing", "Non-specific bands"])
    # You could also move these solutions to a CSV!
    solutions = {"No Bands": "Lower Ta", "Smearing": "Reduce cycles", "Non-specific bands": "Increase Ta"}
    st.error(f"Solution: {solutions[issue]}")
