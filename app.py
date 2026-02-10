import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- PAGE CONFIG ---
st.set_page_config(page_title="Bio-Logic Framework Pro", layout="wide")

# --- CUSTOM CSS FOR CLEANER LOOK ---
st.markdown("""
    <style>
    .reportview-container { background: #f0f2f6; }
    .stMetric { background: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: GLOBAL MODES ---
with st.sidebar:
    st.title("🧠 Logic Engine")
    mode = st.radio("Select Perspective:", ["🎓 Exam Brain (The 'What')", "🔬 Research Brain (The 'Why/How')"])
    st.divider()
    complication = st.toggle("⚠️ Introduce Real-World Complications")
    st.divider()
    st.info("This tool simulates decision-making logic from Lehninger, Watson, and Wilson & Walker.")

# --- MODULE 1: ENZYME KINETICS (Lehninger) ---
st.header("🧬 Enzyme Systems: Beyond the Curve")

col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("Experimental Parameters")
    vmax = st.slider("Theoretical Vmax", 10, 100, 70)
    km = st.slider("Km (Affinity)", 5, 50, 20)
    
    inhibition = "None"
    if complication:
        inhibition = st.selectbox("Select Inhibition Type", ["None", "Competitive", "Non-Competitive", "Substrate Inhibition"])

with col2:
    s_range = np.linspace(0, 120, 500)
    
    # Logic for different inhibition modes
    if inhibition == "Competitive":
        # Km increases, Vmax stays same
        v_range = (vmax * s_range) / ((km * 2) + s_range)
        desc = "Km increased. You need more substrate to reach half-speed."
    elif inhibition == "Non-Competitive":
        # Vmax decreases, Km stays same
        v_range = ((vmax/2) * s_range) / (km + s_range)
        desc = "Vmax dropped. Adding more substrate won't help."
    elif inhibition == "Substrate Inhibition":
        # High substrate actually slows it down
        v_range = (vmax * s_range) / (km + s_range + (s_range**2 / 10))
        desc = "Excess substrate is blocking the active site!"
    else:
        v_range = (vmax * s_range) / (km + s_range)
        desc = "Normal Michaelis-Menten behavior."

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(s_range, v_range, color='#1f77b4', lw=3)
    ax.set_title(f"Kinetics: {inhibition} Mode")
    ax.set_xlabel("[Substrate]")
    ax.set_ylabel("Velocity")
    st.pyplot(fig)

# --- COMPARATIVE LOGIC LAYER ---
st.divider()
st.subheader("🧪 Technique Decision Tree (Wilson & Walker)")

goal = st.selectbox("Research Goal:", ["Determine Protein Molecular Weight", "Quantify DNA Concentration"])

if goal == "Determine Protein Molecular Weight":
    c1, c2 = st.columns(2)
    
    with c1:
        st.success("✅ **Recommended: SDS-PAGE**")
        st.write("**Logic:** Denatures proteins and coats them in SDS (negative charge) so they separate strictly by mass.")
        
        if mode == "🔬 Research Brain (The 'Why/How')":
            with st.expander("🔍 Troubleshooting: 'My band is in the wrong place'"):
                st.write("- **Post-translational modifications:** Glycosylation makes bands appear larger/fuzzy.")
                st.write("- **Incomplete reduction:** Disulfide bonds still intact (forgot β-mercaptoethanol).")
                st.write("- **Protein Degradation:** Multiple small bands (add protease inhibitors).")

    with c2:
        st.error("❌ **Why NOT others?**")
        st.markdown("""
        *   **Native PAGE:** Charge and shape interfere. A small round protein might move slower than a large thin one.
        *   **Size Exclusion Chromatography (SEC):** Good for native state, but lower resolution than a gel.
        *   **Mass Spec:** High cost. Overkill if you just need to check if your protein is ~50kDa.
        """)

# --- EXAM VS RESEARCH MODE TEXT ---
st.divider()
if mode == "🎓 Exam Brain (The 'What')":
    st.info("**Exam Focus:** Memorize the Michaelis-Menten equation and the definitions of Km/Vmax. Know that Competitive inhibitors increase Km.")
else:
    st.warning("**Research Focus:** In the lab, 'Pure' MM kinetics rarely exist. Always look for substrate inhibition, enzyme instability, or buffer interference. The 'Why Not' is as important as the 'Why'.")

# --- FOOTER ---
st.caption("PhD Portfolio Tool | Integrating Lehninger, Watson, and Wilson & Walker Logic")
