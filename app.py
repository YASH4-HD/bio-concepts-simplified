import streamlit as st

# --- CONFIG ---
st.set_page_config(page_title="Bio-Mastery Engine", layout="wide")

# --- KNOWLEDGE DATABASE (The "Mapping") ---
# In a real app, this could be a CSV or JSON file.
cross_book_data = {
    "Protein Folding": {
        "Lehninger": "Focuses on Thermodynamics (ΔG). Folding is driven by the Hydrophobic Effect and Chaperones (Hsp70).",
        "Watson": "Focuses on the Ribosome's role and how the mRNA sequence determines the folding speed (Codon usage).",
        "Wilson_Walker": "Techniques: Circular Dichroism (CD) to measure alpha-helices and X-ray Crystallography for final structure.",
        "Interactive_Tool": "Folding_Sim"
    },
    "PCR (Polymerase Chain Reaction)": {
        "Lehninger": "The role of Mg2+ ions as cofactors for DNA Polymerase and the stability of H-bonds at high temperatures.",
        "Watson": "The chemical mechanism of phosphodiester bond formation and primer annealing logic.",
        "Wilson_Walker": "Protocol design: How to calculate Tm, choosing between Taq (speed) and Pfu (accuracy) polymerases.",
        "Interactive_Tool": "PCR_Cycle_Sim"
    },
    "ATP Synthase": {
        "Lehninger": "The 'Rotary Engine' model. How the proton gradient (pH) turns the F0F1 stalk to create ATP.",
        "Watson": "Evolutionary conservation of the genes encoding the ATPase subunits across species.",
        "Wilson_Walker": "Using Chemiosmotic assays and Oxygen electrodes to measure the rate of oxidative phosphorylation.",
        "Interactive_Tool": "Proton_Gradient_Sim"
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
