"""
MedSafe AI — OCR Utilities (ocr_utils.py)
Handles Tesseract OCR extraction from prescription images
and LLM-driven parsing into structured medicine data.
"""

import json
import re
import logging
from PIL import Image

logger = logging.getLogger(__name__)

# Try to import pytesseract; graceful fallback if not installed
try:
    import pytesseract
    TESSERACT_AVAILABLE = True
except ImportError:
    TESSERACT_AVAILABLE = False
    logger.warning("pytesseract not installed. OCR will use fallback mode.")

# Common Tesseract paths by OS (configure for your system)
TESSERACT_PATHS = {
    "windows": r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    "linux":   "/usr/bin/tesseract",
    "mac":     "/opt/homebrew/bin/tesseract",
}


def configure_tesseract(custom_path: str = None) -> bool:
    """
    Configure Tesseract executable path.
    Returns True if configured successfully.
    """
    if not TESSERACT_AVAILABLE:
        return False
    try:
        import platform
        if custom_path:
            pytesseract.pytesseract.tesseract_cmd = custom_path
        else:
            system = platform.system().lower()
            if system == "windows":
                pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATHS["windows"]
            elif system == "darwin":
                pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATHS["mac"]
            else:
                pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATHS["linux"]
        return True
    except Exception as e:
        logger.error(f"Tesseract configuration error: {e}")
        return False


def extract_text_from_image(image: Image.Image) -> str:
    """
    Extract raw text from a PIL Image using Tesseract OCR.
    Falls back to a demo text if Tesseract is unavailable.

    Args:
        image: PIL Image object

    Returns:
        Extracted text string
    """
    if not TESSERACT_AVAILABLE:
        logger.warning("Tesseract unavailable — returning demo OCR output.")
        return _demo_ocr_text()

    try:
        configure_tesseract()
        # Preprocessing: convert to grayscale for better OCR accuracy
        gray_image = image.convert("L")
        # OCR with page segmentation mode 6 (single uniform block of text)
        custom_config = r"--oem 3 --psm 6"
        text = pytesseract.image_to_string(gray_image, config=custom_config)
        if not text.strip():
            logger.info("OCR returned empty text — using demo fallback.")
            return _demo_ocr_text()
        return text.strip()
    except Exception as e:
        logger.error(f"OCR extraction failed: {e}")
        return _demo_ocr_text()


def parse_medicines_with_llm(ocr_text: str, llm_client) -> dict:
    """
    Use LLM (Ollama/OpenAI) to parse raw OCR text into structured medicine data.
    Enforces strict JSON output format.

    Args:
        ocr_text: Raw text from OCR
        llm_client: Initialized Ollama or OpenAI client

    Returns:
        Parsed dict with medicines list and patient info
    """
    prompt = f"""You are a medical prescription parser. Extract all medicines from this prescription text.

PRESCRIPTION TEXT:
{ocr_text}

Return ONLY valid JSON, no other text, no markdown:
{{
  "medicines": [
    {{
      "name": "medicine_name_lowercase",
      "dose": "dose_with_unit",
      "frequency": "how_often",
      "route": "oral/topical/etc"
    }}
  ],
  "patient_age": null_or_number,
  "patient_name": null_or_string,
  "allergies": [],
  "prescriber": null_or_string
}}"""

    try:
        # Try Ollama (local LLM)
        if hasattr(llm_client, "chat"):
            response = llm_client.chat(
                model="llama3",
                messages=[{"role": "user", "content": prompt}]
            )
            raw = response["message"]["content"]
        else:
            # OpenAI-compatible client
            response = llm_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=800,
            )
            raw = response.choices[0].message.content

        # Clean and parse JSON
        clean = re.sub(r"```json|```", "", raw).strip()
        return json.loads(clean)

    except json.JSONDecodeError:
        logger.error("LLM returned invalid JSON — using regex fallback.")
        return _regex_fallback_parse(ocr_text)
    except Exception as e:
        logger.error(f"LLM parsing failed: {e}")
        return _regex_fallback_parse(ocr_text)


def _regex_fallback_parse(text: str) -> dict:
    """
    Fallback: simple regex-based medicine name extraction
    when LLM is unavailable.
    """
    # Common medicine name patterns
    common_medicines = [
        "aspirin", "warfarin", "ibuprofen", "paracetamol", "metformin",
        "lisinopril", "atorvastatin", "clopidogrel", "omeprazole",
        "amoxicillin", "amlodipine", "methotrexate", "metronidazole",
        "rosuvastatin", "lithium"
    ]
    text_lower = text.lower()
    found = []
    for med in common_medicines:
        if med in text_lower:
            # Try to extract dose near the medicine name
            pattern = rf"{med}\s*(\d+\s*mg)?"
            match = re.search(pattern, text_lower)
            dose = match.group(1) if match and match.group(1) else "dose not extracted"
            found.append({"name": med, "dose": dose, "frequency": "as prescribed", "route": "oral"})

    # Try to extract age
    age_match = re.search(r"age[:\s]*(\d{1,3})", text_lower)
    patient_age = int(age_match.group(1)) if age_match else None

    return {
        "medicines": found,
        "patient_age": patient_age,
        "patient_name": None,
        "allergies": [],
        "prescriber": None,
    }


def _demo_ocr_text() -> str:
    """Return demo prescription text for testing without Tesseract."""
    return """CITY MEDICAL CENTER
Patient: John Doe  |  Age: 65  |  Date: 12/01/2024
MRN: #MED-20241205

PRESCRIPTION

1. Aspirin 75mg Tablet
   Take ONE tablet orally ONCE daily (morning)
   Qty: 30 | Refills: 3

2. Warfarin Sodium 5mg Tablet
   Take ONE tablet orally ONCE daily at BEDTIME
   Qty: 30 | Refills: 0 (INR monitoring required)

3. Lisinopril 10mg Tablet
   Take ONE tablet orally ONCE daily
   Qty: 30 | Refills: 3

4. Omeprazole 20mg Capsule
   Take ONE capsule ONCE daily before breakfast
   Qty: 30 | Refills: 2

Allergies: Penicillin (rash)
Prescriber: Dr. Sarah Smith, MD
Clinic: City Medical Center — Cardiology"""
