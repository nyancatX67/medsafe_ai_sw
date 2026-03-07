"""
MedSafe AI — Intelligent Medicine Safety Assistant
Main Streamlit Application (main.py)

Run with: streamlit run main.py

Educational use only. Not a substitute for professional medical advice.
"""

import json
import logging
import re
from datetime import datetime

import streamlit as st
from PIL import Image
from rapidfuzz import process, fuzz

from med_db import MED_DB, find_medicine, get_all_medicine_keys
from symptom import symptom_advice, get_all_symptoms
from ocr_utils import extract_text_from_image, parse_medicines_with_llm
from risk_engine import compute_risk, get_risk_recommendation

# ── Logging setup ────────────────────────────────────────────────────────────
logging.basicConfig(
    filename="medsafe_log.txt",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# ── Ollama LLM client ────────────────────────────────────────────────────────
try:
    from ollama import Client
    ollama = Client()
    LLM_AVAILABLE = True
except Exception:
    ollama = None
    LLM_AVAILABLE = False
    logger.warning("Ollama not available. AI features will use fallback mode.")


# ════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="MedSafe AI — Intelligent Medicine Safety Assistant",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #0d1117; color: #e6edf3; }

    /* Header */
    .medsafe-header {
        background: linear-gradient(135deg, #1a1f2e 0%, #0d1117 100%);
        border-bottom: 2px solid #21262d;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1.5rem;
        border-radius: 0 0 12px 12px;
    }
    .medsafe-title {
        font-size: 1.9rem;
        font-weight: 800;
        color: #e6edf3;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .medsafe-subtitle {
        color: #8b949e;
        font-size: 0.85rem;
        margin-top: 0.2rem;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #161b22;
        border-radius: 10px;
        padding: 4px;
        gap: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 8px;
        color: #8b949e;
        font-weight: 600;
        font-size: 0.85rem;
        padding: 8px 16px;
        border: none;
    }
    .stTabs [aria-selected="true"] {
        background-color: #21262d;
        color: #e6edf3;
    }

    /* Cards */
    .med-card {
        background: #161b22;
        border: 1px solid #21262d;
        border-radius: 12px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 1rem;
    }

    /* Risk gauge */
    .risk-gauge {
        text-align: center;
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid;
    }
    .risk-score-number {
        font-size: 4rem;
        font-weight: 900;
        line-height: 1;
    }

    /* Interaction flag */
    .interaction-flag {
        background: rgba(248, 81, 73, 0.1);
        border: 1px solid rgba(248, 81, 73, 0.3);
        border-left: 4px solid #f85149;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        color: #ffa198;
    }

    /* Safe badge */
    .safe-badge {
        background: rgba(63, 185, 80, 0.1);
        border: 1px solid rgba(63, 185, 80, 0.3);
        border-radius: 8px;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        color: #3fb950;
    }

    /* AI output box */
    .ai-box {
        background: rgba(56, 139, 253, 0.08);
        border: 1px solid rgba(56, 139, 253, 0.25);
        border-radius: 10px;
        padding: 1rem 1.2rem;
        margin-top: 1rem;
    }
    .ai-label {
        color: #388bfd;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }

    /* Disclaimer */
    .disclaimer {
        background: rgba(210, 153, 34, 0.08);
        border: 1px solid rgba(210, 153, 34, 0.3);
        border-radius: 8px;
        padding: 0.75rem 1rem;
        color: #d29922;
        font-size: 0.8rem;
        text-align: center;
        margin-top: 2rem;
    }

    /* Input fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: #161b22;
        border: 1px solid #30363d;
        color: #e6edf3;
        border-radius: 8px;
    }
    .stSelectbox > div > div {
        background-color: #161b22;
        border: 1px solid #30363d;
    }

    /* Buttons */
    .stButton > button {
        background-color: #21262d;
        border: 1px solid #30363d;
        color: #e6edf3;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        background-color: #30363d;
        border-color: #58a6ff;
        color: #58a6ff;
    }

    /* Metrics */
    .stMetric {
        background: #161b22;
        border: 1px solid #21262d;
        border-radius: 10px;
        padding: 0.8rem;
    }

    /* Hide Streamlit branding */
    #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# SESSION STATE INITIALISATION
# ════════════════════════════════════════════════════════════════════════════
def init_session_state():
    defaults = {
        "ocr_medicines":     [],
        "ocr_raw_text":      "",
        "ocr_parsed_json":   {},
        "interaction_log":   [],
        "side_effect_log":   [],
        "risk_results":      {},
        "last_ocr_filename": "",
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_session_state()


# ════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ════════════════════════════════════════════════════════════════════════════
def find_medicine_fuzzy(name: str, threshold: int = 65) -> str | None:
    """
    Fuzzy-match a user-typed medicine name against the database.
    Uses RapidFuzz for performance-optimized matching.
    Returns matched key or None.
    """
    candidates = get_all_medicine_keys()
    # Direct key match first
    direct = find_medicine(name)
    if direct:
        return direct
    # Fuzzy match
    result = process.extractOne(
        name.lower().strip(),
        candidates,
        scorer=fuzz.WRatio,
        score_cutoff=threshold,
    )
    return result[0] if result else None


def check_interactions(medicines: list[str]) -> list[dict]:
    """
    Cross-reference all medicine pairs for known interactions.
    Returns list of interaction dicts.
    """
    results = []
    med_keys = []
    for m in medicines:
        key = find_medicine_fuzzy(m)
        if key:
            med_keys.append(key)

    checked = set()
    for i, key_a in enumerate(med_keys):
        for key_b in med_keys[i + 1:]:
            pair = tuple(sorted([key_a, key_b]))
            if pair in checked:
                continue
            checked.add(pair)

            interactions = MED_DB[key_a].get("interactions", {})
            if key_b in interactions:
                results.append({
                    "med_a": MED_DB[key_a]["name"],
                    "med_b": MED_DB[key_b]["name"],
                    "warning": interactions[key_b],
                })
            elif key_a in MED_DB[key_b].get("interactions", {}):
                results.append({
                    "med_a": MED_DB[key_a]["name"],
                    "med_b": MED_DB[key_b]["name"],
                    "warning": MED_DB[key_b]["interactions"][key_a],
                })
    return results


def llama_short_warning(lines: list[str]) -> str:
    """
    Generate a concise AI safety summary using Ollama LLaMA 3.
    Falls back to a static message if LLM unavailable.
    """
    prompt = f"""Medicines safety note:
{chr(10).join(lines)}

Write 2-3 sentences: educational safety summary, non-diagnostic. 
End: 'Always consult your pharmacist or doctor.'"""

    if not LLM_AVAILABLE or ollama is None:
        return (
            "⚠️ AI model (Ollama) is not running. "
            "Please install Ollama and run 'ollama pull llama3' to enable AI summaries. "
            "Always consult your pharmacist or doctor for medication guidance."
        )
    try:
        response = ollama.chat(
            model="llama3",
            messages=[{"role": "user", "content": prompt}]
        )
        return response["message"]["content"].strip()
    except Exception as e:
        logger.error(f"LLaMA inference error: {e}")
        return "AI summary unavailable at this time. Please consult your pharmacist or doctor."


def log_side_effect(entry: dict):
    """Log a side-effect report to session state and file."""
    st.session_state.side_effect_log.append(entry)
    logger.info(f"SIDE_EFFECT_LOG: {json.dumps(entry)}")


# ════════════════════════════════════════════════════════════════════════════
# HEADER
# ════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="medsafe-header">
    <div class="medsafe-title">🩺 MedSafe AI – Intelligent Medicine Safety Assistant</div>
    <div class="medsafe-subtitle">Educational tool only · Not a substitute for professional medical advice</div>
</div>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# TABS
# ════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔴 Medicine Interaction Checker",
    "📋 Prescription OCR",
    "🔵 Symptom & Doubt Solver",
    "⚠️ Side-Effect Monitor",
    "🚨 Emergency Risk Predictor",
])


# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — MEDICINE INTERACTION CHECKER
# ════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("## 🔴 Medicine Interaction Checker")
    st.caption("Enter medicines to detect known drug–drug interactions. Uses fuzzy matching for accurate identification.")

    medicines_input = st.text_input(
        "Enter medicines :",
        placeholder="e.g. aspirin, warfarin, ibuprofen",
        help="Separate multiple medicines with commas. Spelling variations are handled automatically.",
        key="interaction_input",
    )

    col1, col2 = st.columns([1, 4])
    with col1:
        check_btn = st.button("Check Interactions", type="primary", use_container_width=True)

    if check_btn:
        if not medicines_input.strip():
            st.warning("⚠️ Please enter at least one medicine name.")
        else:
            raw_list = [m.strip() for m in medicines_input.split(",") if m.strip()]

            # Fuzzy match each medicine
            matched = {}
            unrecognized = []
            for m in raw_list:
                key = find_medicine_fuzzy(m)
                if key:
                    matched[m] = key
                else:
                    unrecognized.append(m)

            if unrecognized:
                st.warning(f"⚠️ Could not identify: **{', '.join(unrecognized)}**. "
                           f"Check spelling or try generic names.")

            if not matched:
                st.error("No medicines identified. Please check your input.")
            else:
                # Display matched medicines
                st.markdown("**✅ Medicines identified:**")
                cols = st.columns(min(len(matched), 4))
                for idx, (user_input, key) in enumerate(matched.items()):
                    with cols[idx % 4]:
                        info = MED_DB[key]
                        st.metric(
                            label=f"💊 {user_input}",
                            value=info["name"],
                            delta=info["salt"],
                            delta_color="off",
                        )

                st.divider()

                # Check interactions
                med_names = list(matched.keys())
                interactions = check_interactions(med_names)

                if not interactions:
                    st.success("✅ No known interactions detected between the entered medicines.")
                    st.caption("This does not guarantee safety. Always verify with your pharmacist.")
                else:
                    st.error(f"🚨 **{len(interactions)} interaction(s) detected!**")
                    for ix in interactions:
                        st.markdown(f"""
<div class="interaction-flag">
    <strong>⚠️ {ix['med_a']} + {ix['med_b']}</strong><br>
    {ix['warning']}
</div>""", unsafe_allow_html=True)

                # AI Safety Summary
                with st.spinner("🤖 Generating AI safety summary..."):
                    lines = [f"- {MED_DB[k]['name']}: {', '.join(MED_DB[k]['side_effects'][:3])}"
                             for k in matched.values()]
                    if interactions:
                        lines += [f"- Interaction: {ix['med_a']} + {ix['med_b']}" for ix in interactions]
                    ai_summary = llama_short_warning(lines)

                st.markdown(f"""
<div class="ai-box">
    <div class="ai-label">🤖 AI SAFETY SUMMARY</div>
    {ai_summary}
</div>""", unsafe_allow_html=True)

                # Log to session
                st.session_state.interaction_log.append({
                    "timestamp": datetime.now().isoformat(),
                    "medicines": med_names,
                    "interactions_found": len(interactions),
                })
                logger.info(f"INTERACTION_CHECK: {med_names} → {len(interactions)} interactions")

                # Expandable details
                with st.expander("📊 View full medicine details"):
                    for key in matched.values():
                        info = MED_DB[key]
                        st.markdown(f"""
**{info['name']}** ({info['salt']})
- **Category:** {info.get('category', 'N/A')}
- **Adult dose:** {info['standard_dose_mg']['adult']} mg
- **High risk:** {'Yes ⚠️' if info['high_risk'] else 'No'}
- **Side effects:** {', '.join(info['side_effects'][:4])}
---""")


# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — PRESCRIPTION OCR
# ════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("## 📋 Extract Medicines From Prescription Image")
    st.caption("Upload a prescription image. Tesseract OCR extracts the text; LLaMA 3 parses it into structured data.")

    uploaded_file = st.file_uploader(
        "Upload prescription image",
        type=["jpg", "jpeg", "png"],
        help="Clear, well-lit images give the best OCR results.",
        key="ocr_upload",
    )

    col_a, col_b = st.columns([1, 3])
    with col_a:
        demo_btn = st.button("🧪 Load Demo", help="Use a sample prescription for testing")
    with col_b:
        if not LLM_AVAILABLE:
            st.warning("⚠️ Ollama not running — OCR parsing will use regex fallback mode.")

    process_file = uploaded_file or (demo_btn or False)

    if uploaded_file or demo_btn:
        with st.spinner("🔍 Running OCR extraction..."):
            if uploaded_file:
                image = Image.open(uploaded_file)
                filename = uploaded_file.name
                st.image(image, caption="Uploaded Prescription", use_column_width=True)
                ocr_text = extract_text_from_image(image)
            else:
                from ocr_utils import _demo_ocr_text
                ocr_text = _demo_ocr_text()
                filename = "demo_prescription.jpg"

            st.session_state.ocr_raw_text = ocr_text
            st.session_state.last_ocr_filename = filename

        st.success(f"✅ OCR complete — {len(ocr_text)} characters extracted")

        with st.expander("📄 View raw OCR text"):
            st.code(ocr_text, language="text")

        # LLM Parsing
        with st.spinner("🤖 Parsing with AI..."):
            parsed = parse_medicines_with_llm(ocr_text, ollama)
            st.session_state.ocr_parsed_json = parsed
            st.session_state.ocr_medicines = [m["name"] for m in parsed.get("medicines", [])]

        st.markdown("### 🤖 AI-Parsed Medicines")

        medicines = parsed.get("medicines", [])
        if not medicines:
            st.warning("No medicines extracted. Try a clearer image.")
        else:
            for m in medicines:
                col1, col2, col3 = st.columns([2, 1, 2])
                with col1:
                    st.markdown(f"💊 **{m['name'].title()}**")
                    key = find_medicine_fuzzy(m["name"])
                    if key:
                        st.caption(f"Salt: {MED_DB[key]['salt']}")
                with col2:
                    st.metric("Dose", m.get("dose", "—"))
                with col3:
                    st.metric("Frequency", m.get("frequency", "—"))

        # Patient info
        if parsed.get("patient_age"):
            age = parsed["patient_age"]
            st.info(f"👤 Patient age detected: **{age} years**"
                    + (" — Elderly flag active" if age > 70 else ""))

        if parsed.get("allergies"):
            st.warning(f"🚨 Allergies on file: **{', '.join(parsed['allergies'])}**")

        # Persist for use in other tabs
        if st.session_state.ocr_medicines:
            st.success(f"✅ {len(st.session_state.ocr_medicines)} medicines saved to session. "
                       "You can use these in the Interaction Checker and Risk Predictor tabs.")

        with st.expander("🔍 View structured JSON output"):
            st.json(parsed)

        logger.info(f"OCR_PROCESSED: {filename} → {len(medicines)} medicines extracted")


# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — SYMPTOM & DOUBT SOLVER
# ════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("## 🔵 Symptom & Doubt Solver")
    st.caption("Get educational guidance on symptoms. Rule-based advice + AI-generated explanations.")

    all_symptoms = get_all_symptoms()

    col1, col2 = st.columns([2, 1])
    with col1:
        symptom_input = st.text_area(
            "Describe your symptom(s):",
            placeholder="e.g. I have a headache and mild fever since yesterday...",
            height=100,
            key="symptom_input",
        )
    with col2:
        st.markdown("**Quick select:**")
        quick_symptoms = ["headache", "fever", "nausea", "cough", "dizziness", "chest pain", "back pain", "rash"]
        for qs in quick_symptoms:
            if st.button(qs, key=f"qs_{qs}", use_container_width=True):
                symptom_input = qs

    analyze_btn = st.button("🔍 Analyze Symptom", type="primary", key="analyze_symptom")

    if analyze_btn and symptom_input.strip():
        with st.spinner("Analyzing..."):
            advice = symptom_advice(symptom_input)

            if advice:
                st.markdown("### 📋 Guidance")
                st.markdown(advice)
            else:
                st.info("No specific rule-based guidance found for this symptom. Showing AI response only.")

            # AI Enhancement
            if LLM_AVAILABLE and ollama:
                with st.spinner("🤖 Getting AI educational explanation..."):
                    try:
                        ai_resp = ollama.chat(
                            model="llama3",
                            messages=[{
                                "role": "user",
                                "content": (
                                    f"You are MedSafe AI. A user reports: '{symptom_input}'. "
                                    "Provide 3-4 educational sentences: possible common causes (non-diagnostic), "
                                    "one lifestyle tip, and when to seek medical care. "
                                    "End: 'This is educational only — consult a healthcare provider.'"
                                )
                            }]
                        )
                        ai_text = ai_resp["message"]["content"].strip()
                    except Exception as e:
                        ai_text = f"AI unavailable: {e}"
            else:
                ai_text = ("AI model (Ollama/LLaMA 3) is not running. "
                           "Install Ollama and run 'ollama pull llama3' for enhanced guidance.")

            st.markdown(f"""
<div class="ai-box">
    <div class="ai-label">🤖 AI EDUCATIONAL GUIDANCE</div>
    {ai_text}
</div>""", unsafe_allow_html=True)

            st.markdown("""
<div class="disclaimer">
    ⚕️ This is educational information only. Always consult a qualified healthcare provider for diagnosis and treatment.
</div>""", unsafe_allow_html=True)

    elif analyze_btn:
        st.warning("Please describe your symptom first.")


# ════════════════════════════════════════════════════════════════════════════
# TAB 4 — SIDE-EFFECT MONITOR
# ════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("## ⚠️ Experience & Side-Effect Monitor")
    st.caption("Analyze reported side effects in the context of age, gender, medicines, and dosage.")

    col1, col2 = st.columns(2)
    with col1:
        age_input = st.number_input("Enter your age:", min_value=1, max_value=120, value=25, step=1, key="se_age")
    with col2:
        gender_input = st.selectbox("Select your gender:", ["Male", "Female", "Other"], key="se_gender")

    medicines_se = st.text_input(
        "Enter medicine(s) taken (comma-separated):",
        placeholder="e.g. aspirin, metformin",
        key="se_medicines",
    )

    dose_input = st.text_input(
        "Enter dose(s) taken (mg, comma-separated if multiple):",
        placeholder="e.g. 75mg, 500mg",
        key="se_dose",
    )

    side_effect_input = st.text_area(
        "Describe the side effect experienced:",
        placeholder="e.g. Unusual bruising on arms after starting warfarin...",
        height=100,
        key="se_description",
    )

    analyze_se_btn = st.button("🔬 Analyze Side Effect", type="primary", key="analyze_se")

    if analyze_se_btn:
        if not side_effect_input.strip() or not medicines_se.strip():
            st.warning("⚠️ Please fill in both the medicines and side effect description.")
        else:
            med_list = [m.strip() for m in medicines_se.split(",") if m.strip()]

            # Match against known side-effect profiles
            known_matches = []
            for m in med_list:
                key = find_medicine_fuzzy(m)
                if key:
                    for effect in MED_DB[key].get("side_effects", []):
                        keyword = effect.split()[0].lower()
                        if keyword in side_effect_input.lower():
                            known_matches.append({
                                "medicine": MED_DB[key]["name"],
                                "effect": effect,
                            })

            st.markdown("### Analysis Results")

            if known_matches:
                for match in known_matches:
                    st.warning(f"⚠️ **{match['effect']}** is a documented side effect of **{match['medicine']}**")
            else:
                st.success("✅ No direct match found in known side-effect profiles for this combination.")
                st.caption("This does not rule out a drug-related cause.")

            # AI Assessment
            with st.spinner("🤖 AI assessing side effect..."):
                if LLM_AVAILABLE and ollama:
                    try:
                        prompt = (
                            f"Patient profile: Age {age_input}, {gender_input}. "
                            f"Taking: {medicines_se}. Dose(s): {dose_input or 'not specified'}. "
                            f"Reports: '{side_effect_input}'. "
                            + (f"Database match: {'; '.join([m['effect'] + ' from ' + m['medicine'] for m in known_matches])}. "
                               if known_matches else "No database match found. ") +
                            "Provide 3-4 sentences: could this be related, what to monitor, when to contact doctor. "
                            "End: 'Do not stop medication without consulting your prescriber.'"
                        )
                        ai_resp = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
                        ai_text = ai_resp["message"]["content"].strip()
                    except Exception as e:
                        ai_text = f"AI unavailable: {e}"
                else:
                    ai_text = "AI model not available. Please consult your doctor or pharmacist about this side effect."

            st.markdown(f"""
<div class="ai-box">
    <div class="ai-label">🤖 AI CLINICAL ASSESSMENT</div>
    {ai_text}
</div>""", unsafe_allow_html=True)

            # Log the side effect experience
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "age": age_input,
                "gender": gender_input,
                "medicines": med_list,
                "dose": dose_input,
                "side_effect": side_effect_input,
                "known_matches": known_matches,
            }
            log_side_effect(log_entry)
            st.caption(f"✅ This experience has been logged at {log_entry['timestamp'][:19]}")

    # Show session log
    if st.session_state.side_effect_log:
        with st.expander(f"📋 Session Side-Effect Log ({len(st.session_state.side_effect_log)} entries)"):
            for entry in reversed(st.session_state.side_effect_log):
                st.markdown(f"**{entry['timestamp'][:19]}** — "
                            f"Age {entry['age']}, {entry['gender']} — "
                            f"Meds: {', '.join(entry['medicines'])} — "
                            f"_{entry['side_effect'][:80]}..._")
                st.divider()


# ════════════════════════════════════════════════════════════════════════════
# TAB 5 — EMERGENCY RISK PREDICTOR
# ════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown("## 🚨 Emergency Risk Predictor")
    st.caption("Transparent rule-based risk scoring. Every flag is explained. Uses session data from OCR if available.")

    col1, col2 = st.columns(2)
    with col1:
        medicines_risk = st.text_input(
            "Medicines (comma-separated):",
            value=", ".join(st.session_state.ocr_medicines) if st.session_state.ocr_medicines else "",
            placeholder="aspirin, warfarin, lisinopril...",
            key="risk_medicines",
        )
        age_risk = st.number_input("Patient age:", min_value=1, max_value=120, value=50, step=1, key="risk_age")

    with col2:
        symptoms_risk = st.text_input(
            "Current symptoms (comma-separated):",
            placeholder="chest pain, shortness of breath...",
            key="risk_symptoms",
        )
        side_effects_risk = st.text_input(
            "Reported side effects:",
            placeholder="bleeding, severe bruising...",
            key="risk_side_effects",
        )

    compute_btn = st.button("⚡ Calculate Risk Score", type="primary", key="compute_risk")

    if compute_btn:
        if not medicines_risk.strip():
            st.warning("⚠️ Please enter at least one medicine.")
        else:
            med_list = [m.strip() for m in medicines_risk.split(",") if m.strip()]
            sym_list = [s.strip() for s in symptoms_risk.split(",") if s.strip()]

            with st.spinner("Computing risk score..."):
                result = compute_risk(
                    medicines=med_list,
                    age=age_risk,
                    symptoms=sym_list,
                    side_effects=side_effects_risk,
                )
                st.session_state.risk_results = result

            st.markdown("---")
            st.markdown("### Risk Score")

            # Gauge display
            score = result["score"]
            level = result["level"]
            color = result["color"]
            emoji = result["emoji"]

            col_gauge, col_details = st.columns([1, 2])

            with col_gauge:
                st.markdown(f"""
<div class="risk-gauge" style="border-color: {color}; background: {color}11;">
    <div class="risk-score-number" style="color: {color};">{score}</div>
    <div style="color: {color}; font-size: 1.1rem; font-weight: 700; letter-spacing: 2px; margin-top: 4px;">
        {emoji} {level}
    </div>
    <div style="color: #8b949e; font-size: 0.75rem; margin-top: 4px;">out of 100</div>
</div>""", unsafe_allow_html=True)

            with col_details:
                st.markdown("#### Risk Flags")
                if result["flags"]:
                    for flag in result["flags"]:
                        st.markdown(f"- {flag}")
                else:
                    st.markdown("✅ No risk flags triggered.")

                st.markdown("#### Recommendation")
                st.info(get_risk_recommendation(level))

            # Score breakdown
            with st.expander("📊 Score breakdown (transparency)"):
                if result["breakdown"]:
                    for item in result["breakdown"]:
                        col_r, col_p = st.columns([4, 1])
                        with col_r:
                            st.markdown(f"• {item['rule']}")
                        with col_p:
                            st.markdown(f"**+{item['points']}**")
                else:
                    st.info("No rules triggered.")

            # AI Narrative
            with st.spinner("🤖 Generating AI risk narrative..."):
                if LLM_AVAILABLE and ollama:
                    try:
                        prompt = (
                            f"MedSafe AI Risk Summary. Patient taking: {medicines_risk}. "
                            f"Age: {age_risk}. Symptoms: {symptoms_risk or 'none'}. "
                            f"Risk score: {score}/100 ({level}). "
                            f"Flags: {'; '.join(result['flags']) or 'none'}. "
                            "Provide 3 sentences: primary risk drivers, recommended action, what to discuss with doctor. "
                            "End: 'Seek immediate care if you feel unwell.'"
                        )
                        ai_resp = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
                        ai_narrative = ai_resp["message"]["content"].strip()
                    except Exception as e:
                        ai_narrative = f"AI unavailable: {e}"
                else:
                    ai_narrative = ("AI model not available. Based on the computed risk flags, "
                                    "please consult your healthcare provider promptly.")

            st.markdown(f"""
<div class="ai-box">
    <div class="ai-label">🤖 AI RISK NARRATIVE</div>
    {ai_narrative}
</div>""", unsafe_allow_html=True)

            logger.info(f"RISK_COMPUTED: meds={med_list}, age={age_risk}, score={score}, level={level}")


# ════════════════════════════════════════════════════════════════════════════
# FOOTER DISCLAIMER
# ════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="disclaimer">
    ⚕️ MedSafe AI is an educational prototype only. It is NOT a medical device and does NOT provide medical diagnoses.
    Always consult a qualified healthcare provider before making any medical decisions.
    · Built with Streamlit · LLaMA 3 via Ollama · Tesseract OCR ·
</div>
""", unsafe_allow_html=True)
