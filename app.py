import streamlit as st
import pandas as pd
import os
from deep_translator import GoogleTranslator
import easyocr

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Bio-Tech Smart Textbook",
    layout="wide"
)

# =========================
# OCR INITIALIZATION
# =========================
@st.cache_resource
def load_ocr():
    return easyocr.Reader(['en'])

reader = load_ocr()

@st.cache_data
def get_text_from_image(img_path):
    if img_path and os.path.exists(img_path):
        try:
            text = reader.readtext(img_path, detail=0)
            return " ".join(text).lower()
        except Exception:
            return ""
    return ""

# =========================
# LOAD KNOWLEDGE BASE
# =========================
@st.cache_data
def load_knowledge_base():
    for file in ["knowledge.csv", "knowledge_base.csv"]:
        if os.path.exists(file):
            df = pd.read_csv(file)
            df.columns = df.columns.str.strip()
            return df
    return None

knowledge_df = load_knowledge_base()

# =========================
# SESSION STATE
# =========================
if "page_index" not in st.session_state:
    st.session_state.page_index = 0

# =========================
# TOPIC DETECTION
# =========================
def detect_topic(text):
    t = text.lower()

    if any(k in t for k in ["phenol", "ethanol", "dnase", "rnase", "extraction"]):
        return "dna_extraction"
    if any(k in t for k in ["pcr", "taq", "thermal cycling"]):
        return "pcr"
    if any(k in t for k in ["restriction enzyme", "endonuclease"]):
        return "restriction"
    if any(k in t for k in ["huntington", "ptc518", "votoplam"]):
        return "neurogenetics"
    if any(k in t for k in ["immunotherapy", "cd40", "antibody"]):
        return "immunology"

    return "general"

# =========================
# SMART HINGLISH (DYNAMIC)
# =========================
def generate_hinglish(topic):
    data = {
        "dna_extraction": [
            "Cell se DNA nikalne ke baad proteins remove kiye jaate hain.",
            "RNase RNA ko degrade karta hai, DNase ko inactivate karna zaroori hota hai.",
            "Phenol–chloroform extraction proteins ko separate karta hai.",
            "Ethanol precipitation se DNA solution se bahar aata hai.",
            "EDTA DNase activity ko inhibit karta hai."
        ],
        "pcr": [
            "PCR ek technique hai jisme DNA ki multiple copies banti hain.",
            "Taq polymerase heat-stable hota hai.",
            "Thermal cycling mein denaturation, annealing aur extension steps hote hain."
        ],
        "restriction": [
            "Restriction enzymes DNA ko specific palindromic sites par cut karte hain.",
            "Ye molecular cloning ke liye important hote hain.",
            "Sticky ends ligation ko easy banaate hain."
        ],
        "neurogenetics": [
            "Huntington’s disease ek genetic neurodegenerative disorder hai.",
            "PTC518 (Votoplam) ek splicing modifier hai.",
            "Ye mutant huntingtin expression ko reduce karta hai."
        ],
        "immunology": [
            "Immunotherapy immune system ko activate karti hai.",
            "CD40 immune activation mein important role play karta hai.",
            "Antibody-based therapies targeted hoti hain."
        ],
        "general": [
            "Yeh biology ka ek important concept hai.",
            "Exam ke liye definition aur mechanism samajhna kaafi hota hai."
        ]
    }

    return "\n".join("• " + line for line in data[topic])

# =========================
# EXAM TIPS (DYNAMIC)
# =========================
def generate_exam_tips(topic):
    tips = {
        "dna_extraction": [
            "DNase DNA ko degrade karta hai, isliye EDTA use hota hai.",
            "RNase heat-stable hota hai, DNase nahi.",
            "Phenol–chloroform protein removal ke liye hota hai."
        ],
        "pcr": [
            "Taq polymerase Thermus aquaticus se milta hai.",
            "PCR exponential amplification dikhata hai.",
            "Annealing temperature primer-dependent hota hai."
        ],
        "restriction": [
            "Most restriction enzymes Type II hote hain.",
            "Recognition sites palindromic hoti hain.",
            "Sticky ends blunt ends se better hote hain."
        ],
        "neurogenetics": [
            "Huntington’s disease autosomal dominant hoti hai.",
            "CAG repeat expansion HTT gene mein hota hai.",
            "Splicing modifiers gene expression alter karte hain."
        ],
        "immunology": [
            "CD40–CD40L interaction immune activation ke liye important hai.",
            "Monoclonal antibodies targeted therapy hoti hain.",
            "Immunotherapy adaptive immunity ko activate karti hai."
        ],
        "general": [
            "Definition + mechanism + application exam ke liye enough hota hai."
        ]
    }
    return tips[topic]

# =========================
# MAIN APP
# =========================
if knowledge_df is None:
    st.error("❌ Knowledge base CSV not found.")
    st.stop()

tabs = st.tabs([
    "📖 Reader",
    "🧠 10 Points",
    "🔬 DNA Lab",
    "🔍 Search",
    "📊 Data",
    "🇮🇳 Hinglish Helper"
])

# =========================
# TAB 1: READER
# =========================
with tabs[0]:
    col1, col2, col3 = st.columns([1, 2, 1])

    if col1.button("⬅ Previous"):
        st.session_state.page_index = max(0, st.session_state.page_index - 1)
        st.rerun()

    col2.markdown(
        f"<h3 style='text-align:center;'>Page {st.session_state.page_index + 1} of {len(knowledge_df)}</h3>",
        unsafe_allow_html=True
    )

    if col3.button("Next ➡"):
        st.session_state.page_index = min(len(knowledge_df) - 1, st.session_state.page_index + 1)
        st.rerun()

    st.divider()
    row = knowledge_df.iloc[st.session_state.page_index]

    left, right = st.columns([2, 1])
    with left:
        st.header(row.get("Topic", "Untitled"))
        st.write(row.get("Explanation", ""))

        with st.expander("📘 Read Detailed Explanation"):
            st.write(row.get("Detailed_Explanation", "No extra explanation available."))

    with right:
        img = str(row.get("Image", ""))
        if img and os.path.exists(img):
            with st.expander("🖼️ Show Diagram"):
                st.image(img, use_container_width=True)

# =========================
# TAB 2: 10 POINTS
# =========================
with tabs[1]:
    st.header("🧠 10 Key Exam Points")
    points = row.get("Ten_Points", "")
    if isinstance(points, str) and points.strip():
        for p in points.split("\n"):
            st.write("•", p.strip())
    else:
        st.info("No exam points available.")

# =========================
# TAB 3: DNA LAB
# =========================
with tabs[2]:
    st.header("🔬 DNA Analysis Tool")
    seq = st.text_area("Paste DNA sequence:", "ATGC").upper()
    if st.button("Analyze"):
        st.metric("GC Content", f"{(seq.count('G') + seq.count('C')) / len(seq) * 100:.2f}%")

# =========================
# TAB 4: SEARCH
# =========================
with tabs[3]:
    st.header("🔍 Smart Search")
    query = st.text_input("Search term").lower()
    for i, r in knowledge_df.iterrows():
        if query and query in str(r.get("Topic", "")).lower():
            with st.expander(r["Topic"]):
                st.write(r["Explanation"])
                if st.button("Go", key=i):
                    st.session_state.page_index = i
                    st.rerun()

# =========================
# TAB 5: DATA
# =========================
with tabs[4]:
    file = st.file_uploader("Upload CSV", type="csv")
    if file:
        st.dataframe(pd.read_csv(file))

# =========================
# TAB 6: HINGLISH HELPER (FINAL)
# =========================
with tabs[5]:
    st.header("🇮🇳 Hindi & Hinglish Helper")

    text = st.text_area("Paste English text here:", height=150)

    if st.button("Translate & Explain"):
        hindi = GoogleTranslator(source="auto", target="hi").translate(text)
        topic = detect_topic(text)
        hinglish = generate_hinglish(topic)
        exam_tips = generate_exam_tips(topic)

        c1, c2 = st.columns(2)
        with c1:
            st.subheader("📝 Pure Hindi")
            st.info(hindi)

        with c2:
            st.subheader("🗣 Smart Hinglish")
            st.code(hinglish, language="text")

        st.divider()
        st.subheader("🧠 Exam Tips")
        for tip in exam_tips:
            st.info("• " + tip)
