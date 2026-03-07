# 🏥 MedSafe AI — Intelligent Medicine Safety Assistant (Python/Streamlit)

> **Educational use only. Not a substitute for professional medical advice.**

---

## 🚀 Quick Start

### 1. Clone & Set Up Environment

```bash
git clone https://github.com/YOUR_USERNAME/medsafe-ai.git
cd medsafe-ai

# Create virtual environment
python -m venv medsafe_env

# Activate it
# Windows:
medsafe_env\Scripts\activate
# Mac/Linux:
source medsafe_env/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Tesseract OCR

- **Windows:** Download from https://github.com/tesseract-ocr/tesseract
- **Mac:** `brew install tesseract`
- **Linux:** `sudo apt install tesseract-ocr`

### 4. Install & Run Ollama (LLaMA 3)

```bash
# Install Ollama from https://ollama.com
ollama pull llama3
ollama serve   # Keep this running in a terminal
```

### 5. Run MedSafe AI

```bash
streamlit run main.py
```

Opens at: **http://localhost:8501**

---

## 📁 Project Structure

```
medsafe-ai/
├── main.py              # Streamlit app — all 5 tabs + UI logic
├── med_db.py            # Medicine database (15+ drugs, interactions, side effects)
├── symptom.py           # Rule-based symptom advice (30+ symptoms)
├── ocr_utils.py         # Tesseract OCR + LLM prescription parsing
├── risk_engine.py       # Transparent rule-based risk scoring engine
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variable template
├── .streamlit/
│   └── config.toml      # Streamlit dark theme config
├── medsafe_log.txt      # Auto-generated runtime logs
└── README.md
```

---

## 🧪 Features

| Tab | Feature |
|-----|---------|
| 🔴 Drug Checker | Fuzzy matching + interaction database + AI summary |
| 📋 Prescription OCR | Tesseract OCR + LLaMA 3 JSON parsing |
| 🔵 Symptom Solver | Rule-based advice + AI educational guidance |
| ⚠️ Side-Effect Monitor | Profile matching + AI assessment + session logging |
| 🚨 Risk Predictor | 8-rule transparent scoring + animated gauge + AI narrative |

---

## ⚙️ Dependencies

| Library | Purpose |
|---------|---------|
| `streamlit` | Web UI framework |
| `pytesseract` | OCR text extraction |
| `Pillow` | Image loading & preprocessing |
| `rapidfuzz` | Fast fuzzy string matching |
| `ollama` | Local LLaMA 3 LLM client |
| `python-dotenv` | Environment variable management |

---

## 🔧 Configuration

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Set `TESSERACT_PATH` if Tesseract is not on your system PATH.

---

## ☁️ Streamlit Cloud Deployment

1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo, set main file as `main.py`
4. Add secrets in Streamlit Cloud dashboard (replace `.env` values)

> **Note:** Ollama (local LLM) does not run on Streamlit Cloud. For cloud deployment, replace the Ollama client in `main.py` with an OpenAI API call and set `OPENAI_API_KEY` in secrets.

---

## ⚠️ Disclaimer

MedSafe AI is strictly an **educational prototype**. It is NOT a medical device, does NOT diagnose conditions, and does NOT replace professional medical advice. Always consult a qualified healthcare provider.
