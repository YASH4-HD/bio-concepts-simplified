import streamlit as st
import pandas as pd
from Bio.Seq import Seq
from Bio.Restriction import Analysis, AllEnzymes
import io

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Wilson Walker Digital Lab",
    page_icon="🧬",
    layout="wide"
)

# --- STYLING ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { 
        background-color: #e1e4e8; 
        border-radius: 5px; 
        padding: 8px 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: BOOK NAVIGATOR ---
with st.sidebar:
    st.title("📚 Book Navigator")
    st.write("Upload your book data to begin.")
    
    # Upload the knowledge.csv file
    uploaded_knowledge = st.file_uploader("Upload knowledge.csv", type="csv")
    
    knowledge_loaded = False
    if uploaded_knowledge is not None:
        try:
            knowledge_df = pd.read_csv(uploaded_knowledge)
            knowledge_loaded = True
            st.success("✅ Book Data Loaded")
            
            # Dropdown for topics
            selected_topic = st.selectbox("Select a Topic:", knowledge_df["Topic"].unique())
            
            # Filter and display info in sidebar
            topic_info = knowledge_df[knowledge_df["Topic"] == selected_topic].iloc[0]
            st.markdown(f"### Section {topic_info['Section']}")
            st.info(topic_info['Explanation'])
        except Exception as e:
            st.error(f"Error loading CSV: {e}")
    else:
        st.warning("⚠️ Please upload 'knowledge.csv' to activate the Navigator.")

    st.divider()
    st.caption("PhD Project: Interactive Molecular Education")

# --- MAIN INTERFACE ---
st.title("🔬 Wilson & Walker: Interactive Molecular Lab")
st.markdown("### *A Digital Companion for Biotechnology Students*")

# TABS (Home tab prevents the blank right-side issue)
tab0, tab1, tab2, tab3 = st.tabs(["🏠 Dashboard", "🧬 Sequence Analyzer", "📦 Vector Selector", "🧪 PCR Optimizer"])

# --- TAB 0: DASHBOARD (The Welcome Screen) ---
with tab0:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.header("Welcome to the Digital Lab")
        st.write("""
        This tool implements the techniques described in **Wilson & Walker's Principles and Techniques of Biochemistry and Molecular Biology**.
        
        ### Getting Started:
        1. **Check the Sidebar:** Upload your `knowledge.csv` to access textbook summaries.
        2. **Analyze DNA:** Go to the **Sequence Analyzer** to find restriction sites.
        3. **Select Vectors:** Use the **Vector Selector** to find the right tool for your insert size.
        4. **Troubleshoot:** Use the **PCR Optimizer** to fix failed experiments.
        """)
        
        if knowledge_loaded:
            st.subheader(f"Current Study Topic: {selected_topic}")
            st.write(topic_info['Explanation'])
        else:
            st.info("👈 Upload your knowledge file in the sidebar to see study notes here.")

    with col2:
        # Placeholder for a diagram/image
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/f/f0/DNA_Double_Helix.png/160px-DNA_Double_Helix.png", 
                 caption="DNA Analysis Tools")

# --- TAB 1: SEQUENCE ANALYZER ---
with tab1:
    st.header("Restriction Mapping (Section 4.6)")
    st.write("Upload a .txt or .fasta file to identify restriction enzyme cut sites.")
    
    up_file = st.file_uploader("Upload DNA File", type=["txt", "fasta"], key="dna_up")
    
    if up_file:
        content = up_file.getvalue().decode("utf-8")
        # Handle FASTA header
        lines = content.splitlines()
        final_seq = "".join(lines[1:]) if lines[0].startswith(">") else "".join(lines)
        clean_seq = "".join(final_seq.split()).upper()
        
        if st.button("Run Full Mapping"):
            try:
                my_seq = Seq(clean_seq)
                analysis = Analysis(AllEnzymes, my_seq)
                results = analysis.full()
                
                c1, c2 = st.columns(2)
                c1.metric("Sequence Length", f"{len(my_seq)} bp")
                c2.metric("GC Content", f"{round((clean_seq.count('G')+clean_seq.count('C'))/len(clean_seq)*100, 1)}%")
                
                st.subheader("Restriction Sites Found:")
                found = False
                for enz, sites in results.items():
                    if sites:
                        with st.expander(f"Enzyme: {enz}"):
                            st.write(f"**Cut Positions:** {sites}")
                            st.code(f"Sequence: {clean_seq[:60]}...\nCut:      {' ' * (sites[0]-1)}^")
                        found = True
                if not found:
                    st.info("No common restriction sites found.")
            except Exception as e:
                st.error(f"Error: {e}")

# --- TAB 2: VECTOR SELECTOR ---
with tab2:
    st.header("Vector Selection Decision Matrix")
    st.write("Based on Table 4.4: Selection of Cloning Vectors.")
    
    v_size = st.number_input("Insert Size (kb):", 0.1, 2000.0, 1.0)
    
    if v_size < 10:
        st.success("✅ **Recommended: Plasmid (e.g., pBR322, pUC19)**")
        st.write("**Features:** High copy number, easy to handle, antibiotic resistance markers.")
    elif 10 <= v_size <= 23:
        st.success("✅ **Recommended: Bacteriophage λ**")
        st.write("**Features:** High efficiency via in vitro packaging, ideal for cDNA libraries.")
    elif 100 <= v_size <= 300:
        st.success("✅ **Recommended: BAC (Bacterial Artificial Chromosome)**")
        st.write("**Features:** Stable maintenance of large genomic fragments in E. coli.")
    else:
        st.warning("⚠️ **Recommended: YAC (Yeast Artificial Chromosome)**")
        st.write("**Features:** Can hold up to 2000kb; used for mapping complex genomes.")

# --- TAB 3: PCR OPTIMIZER ---
with tab3:
    st.header("PCR Troubleshooting Guide")
    issue = st.selectbox("What is the result on your agarose gel?", 
                         ["No Bands", "Multiple Bands (Non-specific)", "Smearing", "Primer Dimers"])
    
    st.subheader("Recommended Action:")
    if issue == "No Bands":
        st.error("1. Decrease Annealing Temperature (Ta)\n2. Increase MgCl2 concentration\n3. Check DNA template quality.")
    elif issue == "Multiple Bands (Non-specific)":
        st.warning("1. Increase Annealing Temperature (Ta)\n2. Reduce Primer concentration\n3. Use 'Hot Start' polymerase.")
    elif issue == "Smearing":
        st.warning("1. Reduce number of cycles\n2. Decrease amount of template DNA\n3. Check for DNA degradation.")
    else:
        st.info("1. Redesign primers to avoid 3' complementarity\n2. Increase Annealing Temperature.")

st.divider()
st.caption("PhD Research Project | Integrating Digital Tools with Biochemistry Education")
