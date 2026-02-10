import streamlit as st

# --- CONFIG ---
st.set_page_config(page_title="Bio-Mastery Engine", layout="wide")

# --- KNOWLEDGE DATABASE (The "Mapping") ---
# In a real app, this could be a CSV or JSON file.
cross_book_data = {
    "Protein Folding": {
        "Lehninger": "The 'Thermodynamic' view: Focuses on ΔG, the Hydrophobic Effect, and how Chaperones (Hsp70/GroEL) prevent 'Energy Traps'.",
        "Watson": "The 'Sequence' view: How the Ribosome speed and 'Codon Usage' affect the co-translational folding of a nascent chain.",
        "Wilson_Walker": "The 'Structural' view: Using Circular Dichroism (CD) to track secondary structure and X-ray Crystallography for 3D atomic maps.",
        "Exam_Focus": "What is the Levinthal Paradox? How do disulfide bonds stabilize folding?",
        "Troubleshoot": "Protein is aggregating? Lower the temperature to 18°C or use a 'Chaperone-overexpressing' bacterial strain."
    },
    "Lac Operon": {
        "Lehninger": "Allosteric logic: How the inducer (Allo-lactose) changes the Repressor's conformation so it loses affinity for DNA.",
        "Watson": "Regulatory logic: Cis-acting elements (Operator/Promoter) vs Trans-acting factors (Repressor). The logic of 'Negative Regulation'.",
        "Wilson_Walker": "Reporter Assays: Using β-galactosidase activity (X-gal staining) to quantify gene expression levels.",
        "Exam_Focus": "Predict the phenotype of an I- or O-c mutation. (Constitutive vs Uninducible).",
        "Troubleshoot": "High background expression? Check for 'Leaky' promoters or glucose contamination in the media (Catabolite Repression)."
    },
    "CRISPR-Cas9": {
        "Lehninger": "Nuclease Chemistry: The mechanism of the RuvC and HNH domains cutting the DNA phosphodiester backbone.",
        "Watson": "RNA-Guided Logic: How the crRNA/tracrRNA complex scans the genome for a matching sequence and a PAM (NGG) motif.",
        "Wilson_Walker": "Genome Editing: Designing 'Guide RNAs' and verifying the 'In-del' mutations via the T7E1 Surveyor Assay.",
        "Exam_Focus": "What is the PAM sequence and why is it essential for Cas9 but not for the host?",
        "Troubleshoot": "Off-target effects? Use a 'High-Fidelity' Cas9 variant or improve the gRNA specificity score."
    },
    "Western Blotting": {
        "Lehninger": "Binding Affinity: The non-covalent interactions (Kd) between the primary antibody and the specific protein epitope.",
        "Watson": "Expression Proof: Proving that the 'Genetic Blueprint' was successfully translated into a functional 'Protein Machine'.",
        "Wilson_Walker": "The Protocol: SDS-PAGE separation -> Semi-dry Transfer -> Blocking (BSA/Milk) -> Chemiluminescent detection.",
        "Exam_Focus": "Why do we use a 'Loading Control' (like Actin or GAPDH)?",
        "Troubleshoot": "Multiple bands? Antibody is non-specific. No bands? Transfer failed (check with Ponceau S staining)."
    },
    "Oxidative Phosphorylation": {
        "Lehninger": "Bioenergetics: The 'Proton Motive Force' (Δp) and the rotary motor mechanism of the F0F1-ATP Synthase.",
        "Watson": "The Organelle Genome: Why the ETC subunits are encoded by Mitochondrial DNA and their unique evolutionary origin.",
        "Wilson_Walker": "Respirometry: Using a Clark-type Oxygen Electrode to measure the 'Oxygen Consumption Rate' (OCR).",
        "Exam_Focus": "How do uncouplers (like DNP) affect the P/O ratio and heat production?",
        "Troubleshoot": "Low ATP yield? Check for mitochondrial membrane leakage or inhibition by Cyanide/Azide."
    },
    "DNA Sequencing": {
        "Lehninger": "Nucleotide Chemistry: Why the absence of the 3'-OH group in ddNTPs acts as a 'Chain Terminator'.",
        "Watson": "The Information Age: How we convert physical DNA molecules into a digital string of A, T, C, and G.",
        "Wilson_Walker": "NGS Technology: The logic of 'Bridge Amplification' on a flow cell and 'Sequencing by Synthesis'.",
        "Exam_Focus": "Compare Sanger Sequencing (1 read/capillary) vs Illumina (millions of reads/flow cell).",
        "Troubleshoot": "Noisy sequence data? Primer dimer formation or poor DNA purity (A260/280 ratio < 1.8)."
    }
}

# --- UI LAYOUT ---
st.title("🌐 The Bio-Mastery Cross-Book Engine")
st.markdown("### *One Search. Three Perspectives. Total Mastery.*")

# Search Bar with Autocomplete
search_query = st.selectbox(
    "Select a core concept to master:",
    options=["Select a concept..."] + list(cross_book_data.keys())
)

if search_query != "Select a concept...":
    data = cross_book_data[search_query]
    
    st.divider()
    
    # Three-Column Display (The "Big Three")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.image("https://img.icons8.com/fluency/96/test-tube.png", width=60)
        st.subheader("Lehninger")
        st.info(f"**The Biochemistry:**\n\n{data['Lehninger']}")
        
    with col2:
        st.image("https://img.icons8.com/fluency/96/dna-helix.png", width=60)
        st.subheader("Watson")
        st.success(f"**The Genetic Logic:**\n\n{data['Watson']}")
        
    with col3:
        st.image("https://img.icons8.com/fluency/96/microscope.png", width=60)
        st.subheader("Wilson & Walker")
        st.warning(f"**The Lab Technique:**\n\n{data['Wilson_Walker']}")

    # --- THE "WHY NOT" & TROUBLESHOOTING SECTION ---
    st.divider()
    exp1, exp2 = st.columns(2)
    
    with exp1:
        with st.expander("🎓 Exam Perspective (Common Questions)"):
            if search_query == "Protein Folding":
                st.write("- What is the 'Levinthal Paradox'?")
                st.write("- How do disulfide bonds stabilize folding?")
            elif search_query == "PCR":
                st.write("- Why is MgCl2 concentration critical?")
                st.write("- Define 'Primer Dimers' and how to avoid them.")
                
    with exp2:
        with st.expander("🔬 Research Perspective (Troubleshooting)"):
            st.error("⚠️ What if the experiment fails?")
            if search_query == "Protein Folding":
                st.write("Problem: Protein is forming Inclusion Bodies (aggregates).")
                st.write("Solution: Lower the induction temperature to 18°C to slow down folding.")
            elif search_query == "PCR":
                st.write("Problem: Multiple non-specific bands.")
                st.write("Solution: Perform a 'Touchdown PCR' to increase specificity.")

# --- SIDEBAR PROGRESS ---
with st.sidebar:
    st.header("🎯 Mastery Tracker")
    st.write("Track your journey through the 'Big Three'.")
    progress = st.multiselect("Concepts Mastered:", list(cross_book_data.keys()))
    if progress:
        score = (len(progress) / len(cross_book_data)) * 100
        st.progress(score / 100)
        st.write(f"You are {int(score)}% of the way to becoming a Bio-Expert!")
