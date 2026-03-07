"""
MedSafe AI — Medicine Database (med_db.py)
Curated drug interaction metadata, dosage info, and safety classifications.
Educational use only.
"""

MED_DB = {
    # ── Analgesics / Anti-inflammatory ──────────────────────────────────────
    "aspirin": {
        "name": "Aspirin",
        "salt": "Acetylsalicylic Acid",
        "standard_dose_mg": {"adult": 75, "child": None},
        "interactions": {
            "warfarin":     "High ⚠️ — Increased bleeding risk. Avoid combination.",
            "ibuprofen":    "Moderate ⚠️ — Reduced cardioprotective effect of aspirin.",
            "naproxen":     "Moderate ⚠️ — Additive GI bleeding risk.",
            "clopidogrel":  "High ⚠️ — Dual antiplatelet therapy; increases bleeding risk significantly.",
            "heparin":      "High ⚠️ — Additive anticoagulant effect; serious bleeding risk.",
            "methotrexate": "High ⚠️ — Aspirin reduces methotrexate clearance; toxicity risk.",
        },
        "side_effects": ["Stomach bleeding", "Nausea", "Tinnitus", "Dizziness", "GI upset"],
        "high_risk": False,
        "category": "Antiplatelet / NSAID",
    },

    "ibuprofen": {
        "name": "Ibuprofen",
        "salt": "Ibuprofen",
        "standard_dose_mg": {"adult": 400, "child": 10},
        "interactions": {
            "aspirin":      "Moderate ⚠️ — Reduces aspirin's cardioprotective effect.",
            "warfarin":     "High ⚠️ — Significantly increases bleeding risk.",
            "lithium":      "High ⚠️ — NSAIDs increase lithium levels; toxicity risk.",
            "methotrexate": "High ⚠️ — Reduces methotrexate excretion; serious toxicity.",
            "lisinopril":   "Moderate ⚠️ — Reduces antihypertensive effect; kidney risk.",
        },
        "side_effects": ["Stomach ulcer", "Kidney damage", "High blood pressure", "Nausea", "Headache"],
        "high_risk": False,
        "category": "NSAID",
    },

    "paracetamol": {
        "name": "Paracetamol",
        "salt": "Acetaminophen",
        "standard_dose_mg": {"adult": 500, "child": 15},
        "interactions": {
            "alcohol":   "High ⚠️ — Severe hepatotoxicity risk with chronic alcohol use.",
            "warfarin":  "Moderate ⚠️ — Enhances anticoagulant effect at high doses.",
            "isoniazid": "High ⚠️ — Increases risk of hepatotoxicity.",
        },
        "side_effects": ["Liver damage (overdose)", "Nausea", "Rash", "Anemia (rare)"],
        "high_risk": False,
        "category": "Analgesic / Antipyretic",
    },

    # ── Anticoagulants / Antiplatelets ───────────────────────────────────────
    "warfarin": {
        "name": "Warfarin",
        "salt": "Warfarin Sodium",
        "standard_dose_mg": {"adult": 5, "child": None},
        "interactions": {
            "aspirin":       "High ⚠️ — Major bleeding risk. Requires close INR monitoring.",
            "ibuprofen":     "High ⚠️ — Increases anticoagulant effect significantly.",
            "naproxen":      "High ⚠️ — Additive anticoagulation; avoid if possible.",
            "amoxicillin":   "Moderate ⚠️ — Alters gut flora; may affect INR.",
            "paracetamol":   "Moderate ⚠️ — Enhances anticoagulation at regular doses.",
            "metronidazole": "High ⚠️ — Strongly potentiates warfarin effect.",
        },
        "side_effects": ["Bleeding", "Bruising", "Hair loss", "Skin necrosis", "Purple toe syndrome"],
        "high_risk": True,
        "category": "Anticoagulant",
    },

    "clopidogrel": {
        "name": "Clopidogrel",
        "salt": "Clopidogrel Bisulfate",
        "standard_dose_mg": {"adult": 75, "child": None},
        "interactions": {
            "aspirin":    "High ⚠️ — Dual antiplatelet therapy; significant bleeding risk.",
            "omeprazole": "Moderate ⚠️ — Omeprazole reduces clopidogrel activation.",
            "warfarin":   "High ⚠️ — Triple antithrombotic therapy; major bleeding risk.",
        },
        "side_effects": ["Bleeding", "Bruising", "Stomach pain", "Diarrhea", "Rash"],
        "high_risk": True,
        "category": "Antiplatelet",
    },

    # ── Antihypertensives ────────────────────────────────────────────────────
    "lisinopril": {
        "name": "Lisinopril",
        "salt": "Lisinopril",
        "standard_dose_mg": {"adult": 10, "child": None},
        "interactions": {
            "ibuprofen":      "Moderate ⚠️ — NSAIDs reduce antihypertensive effect; kidney risk.",
            "potassium":      "High ⚠️ — ACE inhibitors cause potassium retention; hyperkalemia risk.",
            "spironolactone": "High ⚠️ — Combined use significantly increases hyperkalemia risk.",
            "aliskiren":      "High ⚠️ — Dual RAAS blockade; contraindicated in diabetic patients.",
        },
        "side_effects": ["Dry cough", "Dizziness", "Hyperkalemia", "Angioedema (rare but serious)", "Low blood pressure"],
        "high_risk": False,
        "category": "ACE Inhibitor",
    },

    "amlodipine": {
        "name": "Amlodipine",
        "salt": "Amlodipine Besylate",
        "standard_dose_mg": {"adult": 5, "child": None},
        "interactions": {
            "simvastatin":     "Moderate ⚠️ — Increases simvastatin exposure; myopathy risk.",
            "cyclosporine":    "High ⚠️ — Amlodipine increases cyclosporine levels.",
            "clarithromycin":  "Moderate ⚠️ — CYP3A4 inhibitor increases amlodipine effect.",
        },
        "side_effects": ["Ankle swelling", "Flushing", "Headache", "Fatigue", "Palpitations"],
        "high_risk": False,
        "category": "Calcium Channel Blocker",
    },

    # ── Antidiabetics ────────────────────────────────────────────────────────
    "metformin": {
        "name": "Metformin",
        "salt": "Metformin Hydrochloride",
        "standard_dose_mg": {"adult": 500, "child": None},
        "interactions": {
            "alcohol":       "High ⚠️ — Increased lactic acidosis risk.",
            "contrast dye":  "High ⚠️ — Must hold metformin before contrast procedures.",
            "topiramate":    "Moderate ⚠️ — Lactic acidosis risk increased.",
        },
        "side_effects": ["Lactic acidosis (rare)", "Nausea", "Diarrhea", "Vitamin B12 deficiency", "GI upset"],
        "high_risk": False,
        "category": "Biguanide / Antidiabetic",
    },

    # ── Statins ──────────────────────────────────────────────────────────────
    "atorvastatin": {
        "name": "Atorvastatin",
        "salt": "Atorvastatin Calcium",
        "standard_dose_mg": {"adult": 10, "child": None},
        "interactions": {
            "clarithromycin": "High ⚠️ — CYP3A4 inhibitors increase statin levels; myopathy risk.",
            "niacin":         "Moderate ⚠️ — Increased risk of myopathy and rhabdomyolysis.",
            "gemfibrozil":    "High ⚠️ — Significantly increases statin exposure; rhabdomyolysis risk.",
            "cyclosporine":   "High ⚠️ — Major increase in statin levels; avoid combination.",
        },
        "side_effects": ["Muscle pain (myalgia)", "Liver damage", "Memory issues", "Increased diabetes risk"],
        "high_risk": False,
        "category": "Statin",
    },

    "rosuvastatin": {
        "name": "Rosuvastatin",
        "salt": "Rosuvastatin Calcium",
        "standard_dose_mg": {"adult": 10, "child": None},
        "interactions": {
            "cyclosporine": "High ⚠️ — Increases rosuvastatin levels significantly.",
            "gemfibrozil":  "Moderate ⚠️ — Increased myopathy risk.",
        },
        "side_effects": ["Muscle pain", "Headache", "Nausea", "Abdominal pain"],
        "high_risk": False,
        "category": "Statin",
    },

    # ── Antibiotics ──────────────────────────────────────────────────────────
    "amoxicillin": {
        "name": "Amoxicillin",
        "salt": "Amoxicillin Trihydrate",
        "standard_dose_mg": {"adult": 500, "child": 25},
        "interactions": {
            "warfarin":     "Moderate ⚠️ — May alter gut flora affecting INR.",
            "methotrexate": "High ⚠️ — Reduces methotrexate excretion; toxicity risk.",
            "allopurinol":  "Moderate ⚠️ — Increased risk of rash.",
        },
        "side_effects": ["Diarrhea", "Rash", "Nausea", "Allergic reaction", "Yeast infection"],
        "high_risk": False,
        "category": "Penicillin Antibiotic",
    },

    "amoxicillin_clavulanate": {
        "name": "Amoxicillin-Clavulanate",
        "salt": "Amoxicillin + Clavulanic Acid",
        "standard_dose_mg": {"adult": 625, "child": 30},
        "interactions": {
            "warfarin":  "Moderate ⚠️ — May potentiate anticoagulant effect.",
            "allopurinol": "Moderate ⚠️ — Increased rash risk.",
        },
        "side_effects": ["Diarrhea", "Nausea", "Vomiting", "Rash", "Liver enzyme elevation"],
        "high_risk": False,
        "category": "Beta-lactam Antibiotic",
    },

    "cefuroxime": {
        "name": "Cefuroxime",
        "salt": "Cefuroxime Axetil",
        "standard_dose_mg": {"adult": 500, "child": 15},
        "interactions": {
            "warfarin":  "Moderate ⚠️ — May enhance anticoagulant effect.",
            "probenecid": "Moderate ⚠️ — Increases cefuroxime blood levels.",
        },
        "side_effects": ["Diarrhea", "Nausea", "Headache", "Rash", "Vaginal candidiasis"],
        "high_risk": False,
        "category": "Cephalosporin Antibiotic",
    },

    "metronidazole": {
        "name": "Metronidazole",
        "salt": "Metronidazole",
        "standard_dose_mg": {"adult": 400, "child": 7},
        "interactions": {
            "alcohol":   "High ⚠️ — Disulfiram-like reaction: severe nausea, vomiting, flushing.",
            "warfarin":  "High ⚠️ — Strongly enhances anticoagulant effect.",
            "lithium":   "Moderate ⚠️ — May increase lithium toxicity.",
        },
        "side_effects": ["Nausea", "Metallic taste", "Headache", "Dizziness", "Peripheral neuropathy (prolonged use)"],
        "high_risk": False,
        "category": "Antibiotic / Antiprotozoal",
    },

    # ── GI / Proton Pump Inhibitors ──────────────────────────────────────────
    "omeprazole": {
        "name": "Omeprazole",
        "salt": "Omeprazole Magnesium",
        "standard_dose_mg": {"adult": 20, "child": None},
        "interactions": {
            "clopidogrel":        "Moderate ⚠️ — Reduces clopidogrel antiplatelet activation.",
            "methotrexate":       "Moderate ⚠️ — May increase methotrexate toxicity.",
            "iron supplements":   "Moderate ⚠️ — Reduces iron absorption.",
        },
        "side_effects": ["Headache", "Diarrhea", "Magnesium deficiency", "C. diff risk (long-term)", "Bone fracture (long-term)"],
        "high_risk": False,
        "category": "Proton Pump Inhibitor",
    },

    # ── Psychiatric / Mood ───────────────────────────────────────────────────
    "lithium": {
        "name": "Lithium",
        "salt": "Lithium Carbonate",
        "standard_dose_mg": {"adult": 300, "child": None},
        "interactions": {
            "ibuprofen":     "High ⚠️ — NSAIDs increase lithium levels; toxicity risk.",
            "naproxen":      "High ⚠️ — Same as ibuprofen; serious toxicity.",
            "lisinopril":    "High ⚠️ — ACE inhibitors increase lithium levels.",
            "metronidazole": "Moderate ⚠️ — May increase lithium toxicity.",
        },
        "side_effects": ["Tremor", "Polyuria", "Hypothyroidism", "Renal toxicity", "Weight gain"],
        "high_risk": True,
        "category": "Mood Stabilizer",
    },

    # ── Immunosuppressants ───────────────────────────────────────────────────
    "methotrexate": {
        "name": "Methotrexate",
        "salt": "Methotrexate Sodium",
        "standard_dose_mg": {"adult": 7.5, "child": None},
        "interactions": {
            "aspirin":       "High ⚠️ — NSAIDs reduce MTX excretion; serious toxicity risk.",
            "ibuprofen":     "High ⚠️ — Reduces methotrexate clearance significantly.",
            "amoxicillin":   "High ⚠️ — Reduces methotrexate excretion.",
            "omeprazole":    "Moderate ⚠️ — May increase methotrexate toxicity.",
            "trimethoprim":  "High ⚠️ — Additive folate antagonism; serious toxicity.",
        },
        "side_effects": ["Liver toxicity", "Bone marrow suppression", "Nausea", "Mucositis", "Lung toxicity"],
        "high_risk": True,
        "category": "Immunosuppressant / DMARD",
    },
}


def find_medicine(name: str) -> str | None:
    """
    Find a medicine key in MED_DB by exact or normalized name match.
    Returns the key string or None if not found.
    """
    normalized = name.lower().strip().replace(" ", "_").replace("-", "_")
    if normalized in MED_DB:
        return normalized
    # Also try without underscores
    for key in MED_DB:
        if key.replace("_", "") == normalized.replace("_", ""):
            return key
    return None


def get_medicine_info(name: str) -> dict | None:
    """Return full medicine info dict or None."""
    key = find_medicine(name)
    return MED_DB.get(key) if key else None


def get_all_medicine_names() -> list[str]:
    """Return list of all medicine display names."""
    return [v["name"] for v in MED_DB.values()]


def get_all_medicine_keys() -> list[str]:
    """Return list of all medicine keys."""
    return list(MED_DB.keys())
