import streamlit as st
from Bio.Seq import Seq
from Bio.Restriction import Analysis, AllEnzymes

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Wilson Walker Digital Lab", page_icon="🧬", layout="wide")

# --- KNOWLEDGE DATABASE (Free Alternative to AI) ---
# We store the book's wisdom in a Python Dictionary
KNOWLEDGE_BASE = {
    "Restriction Enzymes": "Section 4.6: Enzymes that cut DNA at specific palindromic sequences. Type II are most useful for cloning as they cut within the recognition site.",
    "PCR Principles": "Section 4.10: Uses Taq polymerase, primers, and thermal cycling (Denaturation, Annealing, Extension) to amplify DNA.",
    "Plasmids": "Section 4.12.1: Small, circular extrachromosomal DNA used for cloning inserts <10kb. Often contain antibiotic resistance genes.",
    "Transformation": "Section 4.13: The process of introducing foreign DNA into a host cell, often using heat-shock or electroporation.",
    "Genomic Libraries": "Section 4.15: A collection of total genomic DNA from a single organism, stored in a population of vector-carrying cells."
}

# --- SIDEBAR: FREE CONCEPT NAVIGATOR ---
with st.sidebar:
    st.title("📚 Concept Navigator")
    st.markdown("Select a topic to see the Wilson & Walker explanation (Free & Offline).")
    
    topic = st.selectbox("Choose a Concept:", list(KNOWLEDGE_BASE.keys()))
    st.info(KNOWLEDGE_BASE[topic])
    
    st.markdown("---")
    st.caption("PhD Project: Interactive Textbook")

# --- MAIN INTERFACE ---
st.title("🔬 Wilson & Walker: Interactive Molecular Lab")

tab1, tab2, tab3 = st.tabs(["🧬 Sequence Analyzer", "📦 Vector Selector", "🧪 PCR Optimizer"])

# --- TAB 1: SEQUENCE ANALYZER ---
with tab1:
    st.header("Restriction Mapping (Section 4.6)")
    raw_seq = st.text_area("Paste DNA Sequence:", "GAATTCGCTAGCTAGCTAGGGATCC", height=100)
    clean_seq = "".join(raw_seq.split()).upper()
    
    if st.button("Analyze Sequence"):
        if clean_seq:
            my_seq = Seq(clean_seq)
            analysis = Analysis(AllEnzymes, my_seq)
            results = analysis.full()
            
            c1, c2 = st.columns(2)
            c1.metric("Length", f"{len(my_seq)} bp")
            c2.metric("GC Content", f"{round((clean_seq.count('G')+clean_seq.count('C'))/len(clean_seq)*100, 1)}%")
            
            for enz, sites in results.items():
                if sites:
                    with st.expander(f"Enzyme: {enz}"):
                        st.write(f"**Cut Positions:** {sites}")
                        st.code(f"Seq: {clean_seq}\nCut: {' ' * (sites[0]-1)}^")
        else:
            st.error("Please enter a sequence.")

# --- TAB 2: VECTOR SELECTOR ---
with tab2:
    st.header("Vector Selection (Table 4.4)")
    size = st.number_input("Insert Size (kb)", 0.1, 2000.0, 1.0)
    
    if size < 10:
        st.success("**Standard Plasmid** (Ref: 4.12.1)")
    elif 10 <= size <= 23:
        st.success("**Bacteriophage λ** (Ref: 4.12.2)")
    elif 100 <= size <= 300:
        st.success("**BAC (Bacterial Artificial Chromosome)** (Ref: 4.12.4)")
    else:
        st.warning("**YAC (Yeast Artificial Chromosome)** (Ref: 4.12.5)")

# --- TAB 3: PCR OPTIMIZER ---
with tab3:
    st.header("PCR Troubleshooting (Section 4.10)")
    issue = st.selectbox("Gel Result:", ["No Bands", "Smearing", "Non-specific bands"])
    
    solutions = {
        "No Bands": "Lower Annealing Temp, increase MgCl2.",
        "Smearing": "Reduce cycles, check DNA template purity.",
        "Non-specific bands": "Increase Annealing Temp, use Hot Start."
    }
    st.error(f"**Wilson & Walker Solution:** {solutions[issue]}")
