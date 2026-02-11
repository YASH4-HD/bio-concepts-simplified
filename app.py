import streamlit as st
import pandas as pd
import os
import easyocr
from deep_translator import GoogleTranslator
import requests
import wikipedia
import datetime
import plotly.express as px
import datetime
import pytz
# ==========================================
# 1. MODERN DESIGN & ANIMATION (EXIFA STYLE)
# ==========================================
st.set_page_config(page_title="Bio-Tech Smart Textbook", layout="wide")

def inject_modern_design():
    st.markdown("""
    <style>
    /* Dark Background with subtle gradient */
    .stApp {
        background: linear-gradient(180deg, #0e1117 0%, #10141b 100%);
        color: #ffffff;
    }
    
    /* Floating Bio-Particles Background */
    .particle {
      color: rgba(0, 255, 255, 0.15); /* Very subtle cyan */
      font-size: 22px;
      position: fixed;
      top: -10%;
      z-index: 0;
      user-select: none;
      pointer-events: none;
      animation: fall 12s linear infinite, shake 3s ease-in-out infinite;
    }
    @keyframes fall { 0% { top: -10%; } 100% { top: 100%; } }
    @keyframes shake { 0%, 100% { transform: translateX(0); } 50% { transform: translateX(40px); } }
    
    .p1 { left: 10%; animation-delay: 0s; }
    .p2 { left: 30%; animation-delay: 4s; }
    .p3 { left: 50%; animation-delay: 2s; }
    .p4 { left: 70%; animation-delay: 7s; }
    .p5 { left: 85%; animation-delay: 1s; }

    /* Glassmorphism Sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(15px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Modern Bio-Card for Content */
    .bio-card {
        background: rgba(255, 255, 255, 0.04);
        padding: 25px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }

    /* Style for the DNA Tags */
    .bio-tag {
        background-color: rgba(1, 87, 155, 0.3);
        color: #81d4fa;
        padding: 4px 12px;
        border-radius: 15px;
        margin-right: 8px;
        font-size: 0.8rem;
        font-weight: bold;
        border: 1px solid #01579b;
    }
    </style>
    
    <div aria-hidden="true">
      <div class="particle p1">🧬</div>
      <div class="particle p2">●</div>
      <div class="particle p3">○</div>
      <div class="particle p4">🧬</div>
      <div class="particle p5">●</div>
    </div>
    """, unsafe_allow_html=True)

inject_modern_design()

# =========================
# 2. OCR & DATA INITIALIZATION
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
        except: return ""
    return ""

@st.cache_data
def load_knowledge_base():
    for file in ["knowledge_base.csv", "knowledge.csv"]:
        if os.path.exists(file):
            try:
                df = pd.read_csv(file)
                df.columns = df.columns.str.strip()
                return df.dropna(how='all')
            except: continue
    return pd.DataFrame(columns=["Topic", "Section", "Explanation", "Image", "Ten_Points", "Detailed_Explanation"])

knowledge_df = load_knowledge_base()

if "page_index" not in st.session_state:
    st.session_state.page_index = 0

# =========================
# 3. SIDEBAR: BIO-VERIFY & REPORT
# =========================
with st.sidebar:
    st.title("🛡️ Bio-Verify 2026")
    ist = pytz.timezone("Asia/Kolkata")
    today_dt = datetime.datetime.now(ist)
    st.subheader(f"📅 {today_dt.strftime('%d %b %Y').upper()}")
    
    st.divider()
    EXAMS = {"CSIR NET JUNE": datetime.date(2026, 6, 1), "GATE 2027": datetime.date(2027, 2, 2)}
    for exam, exam_date in EXAMS.items():
        days_left = (exam_date - today_dt.date()).days
        if days_left > 0: st.info(f"**{exam}**: {days_left} days left")
    
    st.divider()
    st.success("✅ API: Active | Verified Sources")
    
    # Profile Card
    st.markdown("""
        <div style="background: rgba(30, 70, 138, 0.4); padding: 20px; border-radius: 15px; text-align: center; border: 1px solid #1e468a;">
            <h3 style="margin:0; color:white;">Yashwant Nama</h3>
            <p style="font-size:0.9rem; opacity:0.8;">Developer & Researcher</p>
            <div style="display: flex; justify-content: center; gap: 5px; margin-top: 10px;">
                <span style="background: rgba(255,255,255,0.1); padding: 3px 8px; border-radius: 10px; font-size:0.7rem;">🧬 Genomics</span>
                <span style="background: rgba(255,255,255,0.1); padding: 3px 8px; border-radius: 10px; font-size:0.7rem;">🕸️ Networks</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.header("📋 My Research Report")
    if 'report_list' in st.session_state and st.session_state['report_list']:
        for idx, item in enumerate(st.session_state['report_list']):
            st.write(f"{idx+1}. {item['Topic']}")
        
        full_report = "BIO-RESEARCH REPORT\n" + "="*20 + "\n"
        for item in st.session_state['report_list']:
            full_report += f"TOPIC: {item['Topic']}\n{item['Notes']}\n\n"
            
        st.download_button("📥 Download Report", full_report, "Bio_Report.txt", use_container_width=True)
        if st.button("🗑️ Clear Report"):
            st.session_state.report_list = []; st.rerun()
    else:
        st.info("Report is empty.")

# =========================
# 4. MAIN TABS LOGIC
# =========================
st.markdown('<h1 style="color: #00d4ff; margin-bottom:0;">🧬 Bio-Tech Smart Textbook</h1>', unsafe_allow_html=True)
st.markdown('<p style="font-style: italic; opacity: 0.7;">Foundational reference for computational hypothesis generation.</p>', unsafe_allow_html=True)

tabs = st.tabs(["📖 Reader", "🧠 10 Points", "🧪 DNA Lab", "🔍 Search", "🌐 Global", "🇮🇳 Hindi", "🧬 Advanced Suite"])

# --- TAB 1: READER ---
with tabs[0]:
    if knowledge_df.empty:
        st.warning("Knowledge base empty.")
    else:
        st.progress((st.session_state.page_index + 1) / len(knowledge_df))
        c1, c2, c3, _ = st.columns([0.6, 0.8, 0.6, 4])
        if c1.button("⬅ PREV", disabled=st.session_state.page_index == 0):
            st.session_state.page_index -= 1; st.rerun()
        with c2: st.markdown(f"<div style='text-align:center; padding-top:5px;'><b>{st.session_state.page_index+1} / {len(knowledge_df)}</b></div>", unsafe_allow_html=True)
        if c3.button("NEXT ➡", disabled=st.session_state.page_index == len(knowledge_df)-1):
            st.session_state.page_index += 1; st.rerun()

        row = knowledge_df.iloc[st.session_state.page_index]
        st.session_state['selected_row'] = row
        
        st.markdown('<div class="bio-card">', unsafe_allow_html=True)
        left, right = st.columns([2, 1])
        with left:
            st.header(row.get("Topic", "Untitled"))
            # Auto-Tags
            bio_keywords = ["DNA", "RNA", "Protein", "CRISPR", "Gene", "Cell", "Enzyme"]
            found_tags = [t for t in bio_keywords if t.lower() in str(row.get("Explanation")).lower()]
            if found_tags:
                tag_html = "".join([f'<span class="bio-tag">🧬 {t}</span>' for t in found_tags])
                st.markdown(tag_html, unsafe_allow_html=True)
                st.write("")
            
            st.write(row.get("Explanation", ""))
            with st.expander("📘 Detailed Analysis"):
                st.write(row.get("Detailed_Explanation", "No extra details."))
            if st.button("➕ Add to Report"):
                if 'report_list' not in st.session_state: st.session_state['report_list'] = []
                st.session_state['report_list'].append({"Topic": row['Topic'], "Notes": row['Explanation']})
                st.toast("Added!")
        with right:
            with st.expander("🖼️ View Diagram", expanded=True):
                img = str(row.get("Image", ""))
                if os.path.exists(img): st.image(img, use_container_width=True)
                else: st.info("No diagram.")
        st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 2: 10 POINTS ---
with tabs[1]:
    if 'selected_row' in st.session_state:
        curr = st.session_state['selected_row']
        st.header(f"🧠 Key Points: {curr['Topic']}")
        study_mode = st.toggle("Enable Study Mode (Hide Notes)")
        pts = curr.get('Ten_Points') or "No points available."
        if study_mode:
            st.warning("🙈 Study Mode Active!")
            if st.button("👁️ Reveal Notes"): st.write(pts)
        else:
            st.success("📝 Full Notes:")
            st.write(pts)
        st.download_button("📥 Download Notes", str(pts), f"{curr['Topic']}_Notes.txt")
    else: st.warning("Select a topic in Reader first.")

# --- TAB 3: DNA LAB ---
with tabs[2]:
    st.header("🧪 DNA Interactive Lab")
    raw_input = st.text_area("Enter Raw DNA:", "atgc 123 gtatc")
    c1, c2, c3 = st.columns(3)
    cleaned = "".join([char for char in raw_input if char.upper() in "ATGC"]).upper()
    if c1.button("🧹 Clean"): st.success("Cleaned DNA:"); st.code(cleaned)
    if c2.button("🧬 Transcribe"): st.warning("mRNA:"); st.code(cleaned.replace("T", "U"))
    if c3.button("🎲 Mutate"):
        import random
        if cleaned:
            l = list(cleaned); idx = random.randint(0, len(l)-1)
            l[idx] = random.choice("ATGC"); st.error(f"Mutated at {idx}:"); st.code("".join(l))

# --- TAB 4: INTERNAL SEARCH (OCR INCLUDED) ---
with tabs[3]:
    st.header("🔍 Smart Search")
    query = st.text_input("Search term (Text or Diagram OCR):").lower()
    if query:
        for i, r in knowledge_df.iterrows():
            img_text = get_text_from_image(str(r.get('Image', '')))
            if query in str(r['Topic']).lower() or query in str(r['Explanation']).lower() or query in img_text:
                with st.expander(f"📖 {r['Topic']} (Page {i+1})"):
                    st.write(r['Explanation'][:200] + "...")
                    if st.button(f"Jump to Page {i+1}", key=f"jump_{i}"):
                        st.session_state.page_index = i; st.rerun()

# --- TAB 5: GLOBAL SEARCH ---
with tabs[4]:
    st.header("🌐 Global Bio-Intelligence")
    user_input = st.text_input("Wikipedia/NCBI Search:")
    if user_input:
        try:
            summary = wikipedia.summary(user_input, sentences=3)
            st.markdown(f"<div class='bio-card'><h3>📚 Wikipedia:</h3>{summary}</div>", unsafe_allow_html=True)
        except: st.error("Wikipedia search failed.")
        
        if st.button("Search NCBI"):
            res = requests.get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi", 
                               params={"db": "pubmed", "term": user_input, "retmode": "json"}).json()
            ids = res.get("esearchresult", {}).get("idlist", [])
            for rid in ids: st.write(f"✅ Record: https://www.ncbi.nlm.nih.gov/pubmed/{rid}")

# --- TAB 6: HINDI HELPER ---
with tabs[5]:
    st.header("🇮🇳 Hindi Helper")
    txt = st.text_area("English text to Hindi:")
    if st.button("Translate"):
        if txt.strip():
            st.info(GoogleTranslator(source="auto", target="hi").translate(txt))

# --- TAB 7: ADVANCED SUITE ---
with tabs[6]:
    st.header("🧬 Advanced Molecular Suite")
    raw_seq = st.text_area("DNA Sequence:", "ATGGCCATTGTAATGGGCCGCTGAAAGGGTACCCGATAG").upper().strip()
    if raw_seq:
        col1, col2, col3 = st.columns(3)
        col1.metric("Length", f"{len(raw_seq)} bp")
        gc = (raw_seq.count('G') + raw_seq.count('C')) / len(raw_seq) * 100
        col2.metric("GC Content", f"{gc:.1f}%")
        mw = (raw_seq.count('A')*313.2) + (raw_seq.count('T')*304.2) + (raw_seq.count('C')*289.2) + (raw_seq.count('G')*329.2)
        col3.metric("Mol. Weight", f"{mw:,.1f} Da")
        
        df = pd.DataFrame({'Nucleotide': ['A', 'T', 'G', 'C'], 'Count': [raw_seq.count(x) for x in 'ATGC']})
        st.plotly_chart(px.bar(df, x='Nucleotide', y='Count', color='Nucleotide', template="plotly_dark", height=300))
        
        c1, c2 = st.columns(2)
        with c1:
            with st.expander("🔗 Complement"):
                st.code("".join([{"A":"T","T":"A","G":"C","C":"G"}.get(b,"N") for b in raw_seq]))
        with c2:
            with st.expander("🧪 Translation"):
                codon_map = {'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M', 'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T', 'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K', 'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R', 'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L', 'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P', 'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q', 'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R', 'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V', 'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A', 'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E', 'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G', 'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S', 'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L', 'TAC':'Y', 'TAT':'Y', 'TAA':'_', 'TAG':'_', 'TGC':'C', 'TGT':'C', 'TGA':'_', 'TGG':'W'}
                prot = "".join([codon_map.get(raw_seq[i:i+3], '?') for i in range(0, len(raw_seq)-2, 3)])
                st.write(f"**Protein:** `{prot}`")
# =========================
# SIDEBAR: RESEARCH REPORT
# =========================
with st.sidebar:
    st.divider()
    st.header("📋 My Research Report")
    
    if 'report_list' in st.session_state and st.session_state['report_list']:
        for idx, item in enumerate(st.session_state['report_list']):
            st.write(f"{idx+1}. {item['Topic']}")
        
        if st.button("🗑️ Clear Report"):
            st.session_state['report_list'] = []
            st.rerun()
            
        # Create the download string
        full_report = "BIO-VERIFY RESEARCH REPORT\n" + "="*25 + "\n\n"
        for item in st.session_state['report_list']:
            full_report += f"TOPIC: {item['Topic']}\n{item['Notes']}\n\n" + "-"*20 + "\n"
            
        st.download_button(
            label="📥 Download Full Report",
            data=full_report,
            file_name="Bio_Research_Report.txt",
            mime="text/plain",
            use_container_width=True
        )
    else:
        st.info("Your report is empty. Add topics from the 'Reader' tab.")
# =========================
# SIDEBAR: RESEARCH TIP
# =========================
with st.sidebar:
    st.divider()
    st.markdown("### 💡 Research Tip")
    tips = [
        "Always verify GC content for primer design stability.",
        "Use NCBI BLAST to compare your sequences against known databases.",
        "CRISPR-Cas9 efficiency depends on the choice of Guide RNA (gRNA).",
        "Restriction enzymes work best at specific pH and temperature buffers."
    ]
    # This picks a different tip based on the day
    import datetime
    tip_index = datetime.datetime.now().day % len(tips)
    st.info(tips[tip_index])
    
    st.caption("© 2026 Bio-Verify | Developed for Genomic Research")
