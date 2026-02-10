import streamlit as st
import pandas as pd
from Bio.Seq import Seq
from Bio.Restriction import Analysis, AllEnzymes
import io

# --- PAGE CONFIG ---
st.set_page_config(page_title="Wilson Walker Digital Lab", layout="wide")

# --- SIDEBAR: KNOWLEDGE LOADER ---
with st.sidebar:
    st.title("📚 Book Navigator")
    
    # NEW: Manual Upload for the Knowledge CSV
    uploaded_knowledge = st.file_uploader("Upload knowledge.csv", type="csv")
    
    if uploaded_knowledge is not None:
        knowledge_df = pd.read_csv(uploaded_knowledge)
        st.success("Knowledge Base Loaded!")
        
        # Create the dropdown from the CSV
        selected_topic = st.selectbox("Select a Topic:", knowledge_df["Topic"].unique())
        
        # Show info
        topic_info = knowledge_df[knowledge_df["Topic"] == selected_topic].iloc[0]
        st.markdown(f"### Section {topic_info['Section']}")
        st.write(topic_info['Explanation'])
    else:
        st.warning("Please upload your `knowledge.csv` file above to see the book data.")
        # Default empty data so the app doesn't crash
        knowledge_df = pd.DataFrame()

    st.divider()
    st.caption("PhD Project: Data-Driven Education")

# --- REST OF THE CODE (Tabs) ---
st.title("🔬 Wilson & Walker: Interactive Molecular Lab")
tab1, tab2, tab3 = st.tabs(["🧬 Sequence Analyzer", "📦 Vector Selector", "🧪 PCR Optimizer"])

# ... (Keep the rest of your tab code the same)
