"""
MedSafe AI — Emergency Risk Scoring Engine (risk_engine.py)
Transparent, rule-based risk calculation.
Every point added is flagged and explained to the user.
Educational use only.
"""

from med_db import MED_DB, find_medicine

# ── Risk rule weights ────────────────────────────────────────────────────────
RULE_WEIGHTS = {
    "high_risk_medicine":       20,   # per high-risk medicine
    "drug_interaction":         20,   # per interaction pair
    "age_very_elderly":         20,   # age > 75
    "age_elderly":              12,   # age 65–75
    "age_pediatric":            20,   # age < 12
    "age_infant":               30,   # age < 2
    "critical_symptom":         25,   # per critical symptom
    "bleeding_reported":        25,   # bleeding in side effects
    "polypharmacy":             10,   # 5+ medicines
    "multiple_high_risk":       15,   # 2+ high-risk medicines
    "anticoagulant_nsaid":      25,   # anticoagulant + NSAID combo
}

CRITICAL_SYMPTOMS = [
    "chest pain", "shortness of breath", "difficulty breathing",
    "stroke", "seizure", "unconscious", "unresponsive",
    "severe allergic", "anaphylaxis", "coughing blood",
    "vomiting blood", "sudden weakness",
]

ANTICOAGULANTS = {"warfarin", "heparin", "clopidogrel", "rivaroxaban", "apixaban"}
NSAIDS = {"aspirin", "ibuprofen", "naproxen", "diclofenac", "celecoxib"}


def compute_risk(
    medicines: list[str],
    age: int = 50,
    symptoms: list[str] = None,
    side_effects: str = "",
    dosages: list[str] = None,
) -> dict:
    """
    Compute an emergency risk score from patient profile.

    Args:
        medicines: List of medicine name strings
        age: Patient age (integer)
        symptoms: List of current symptom strings
        side_effects: Free-text description of reported side effects
        dosages: Optional list of dosage strings (for future expansion)

    Returns:
        dict with keys: score, level, color, flags, breakdown
    """
    if symptoms is None:
        symptoms = []
    if dosages is None:
        dosages = []

    score = 0
    flags = []
    breakdown = []

    # Normalize medicine keys
    med_keys = []
    for m in medicines:
        key = find_medicine(m)
        if key:
            med_keys.append(key)

    # ── Rule 1: High-risk medicines ──────────────────────────────────────────
    for key in med_keys:
        if MED_DB[key].get("high_risk"):
            pts = RULE_WEIGHTS["high_risk_medicine"]
            score += pts
            flags.append(f"⚠️ **{MED_DB[key]['name']}** is a high-risk medicine requiring close monitoring")
            breakdown.append({"rule": f"High-risk medicine: {MED_DB[key]['name']}", "points": pts})

    # ── Rule 2: Drug-drug interactions ──────────────────────────────────────
    checked = set()
    for i, key_a in enumerate(med_keys):
        for key_b in med_keys[i + 1:]:
            pair = tuple(sorted([key_a, key_b]))
            if pair in checked:
                continue
            checked.add(pair)

            interactions_a = MED_DB[key_a].get("interactions", {})
            interactions_b = MED_DB[key_b].get("interactions", {})

            if key_b in interactions_a or key_a in interactions_b:
                pts = RULE_WEIGHTS["drug_interaction"]
                score += pts
                name_a = MED_DB[key_a]["name"]
                name_b = MED_DB[key_b]["name"]
                detail = interactions_a.get(key_b) or interactions_b.get(key_a, "Interaction detected")
                flags.append(f"🔴 **{name_a}** + **{name_b}** — {detail}")
                breakdown.append({"rule": f"Drug interaction: {name_a} + {name_b}", "points": pts})

    # ── Rule 3: Anticoagulant + NSAID combination ────────────────────────────
    has_anticoag = any(k in ANTICOAGULANTS for k in med_keys)
    has_nsaid = any(k in NSAIDS for k in med_keys)
    if has_anticoag and has_nsaid:
        pts = RULE_WEIGHTS["anticoagulant_nsaid"]
        score += pts
        flags.append("🩸 Anticoagulant + NSAID combination — significantly elevated bleeding risk")
        breakdown.append({"rule": "Anticoagulant + NSAID combination", "points": pts})

    # ── Rule 4: Age modifiers ────────────────────────────────────────────────
    if age > 0:
        if age < 2:
            pts = RULE_WEIGHTS["age_infant"]
            score += pts
            flags.append(f"👶 Age {age}: Infant — extreme caution required with all medications")
            breakdown.append({"rule": f"Infant age ({age})", "points": pts})
        elif age < 12:
            pts = RULE_WEIGHTS["age_pediatric"]
            score += pts
            flags.append(f"👶 Age {age}: Pediatric — dosing requires careful weight-based calculation")
            breakdown.append({"rule": f"Pediatric age ({age})", "points": pts})
        elif age > 75:
            pts = RULE_WEIGHTS["age_very_elderly"]
            score += pts
            flags.append(f"👴 Age {age}: Very elderly — significantly increased medication sensitivity")
            breakdown.append({"rule": f"Very elderly ({age})", "points": pts})
        elif age > 65:
            pts = RULE_WEIGHTS["age_elderly"]
            score += pts
            flags.append(f"👴 Age {age}: Elderly — increased sensitivity to medications")
            breakdown.append({"rule": f"Elderly age ({age})", "points": pts})

    # ── Rule 5: Critical symptoms ────────────────────────────────────────────
    for symptom in symptoms:
        s_lower = symptom.lower().strip()
        for critical in CRITICAL_SYMPTOMS:
            if critical in s_lower:
                pts = RULE_WEIGHTS["critical_symptom"]
                score += pts
                flags.append(f"🚨 Critical symptom: **{symptom}** — requires urgent medical attention")
                breakdown.append({"rule": f"Critical symptom: {symptom}", "points": pts})
                break

    # ── Rule 6: Bleeding indicators ──────────────────────────────────────────
    se_lower = side_effects.lower()
    bleed_keywords = ["bleed", "bleeding", "blood", "haemorrhage", "hemorrhage", "bruising severely"]
    if any(kw in se_lower for kw in bleed_keywords):
        pts = RULE_WEIGHTS["bleeding_reported"]
        score += pts
        flags.append("🩸 Bleeding or haemorrhage reported — urgent medical review required")
        breakdown.append({"rule": "Bleeding reported in side effects", "points": pts})

    # ── Rule 7: Polypharmacy (5+ medicines) ──────────────────────────────────
    if len(med_keys) >= 5:
        pts = RULE_WEIGHTS["polypharmacy"]
        score += pts
        flags.append(f"💊 Polypharmacy: {len(med_keys)} medications — increased interaction complexity")
        breakdown.append({"rule": f"Polypharmacy ({len(med_keys)} meds)", "points": pts})

    # ── Rule 8: Multiple high-risk medicines ─────────────────────────────────
    high_risk_count = sum(1 for k in med_keys if MED_DB[k].get("high_risk"))
    if high_risk_count >= 2:
        pts = RULE_WEIGHTS["multiple_high_risk"]
        score += pts
        flags.append(f"⚠️ {high_risk_count} high-risk medications taken concurrently")
        breakdown.append({"rule": f"Multiple high-risk meds ({high_risk_count})", "points": pts})

    # ── Final score ──────────────────────────────────────────────────────────
    final_score = min(score, 100)

    level, color, emoji = classify_risk(final_score)

    return {
        "score":     final_score,
        "level":     level,
        "color":     color,
        "emoji":     emoji,
        "flags":     flags,
        "breakdown": breakdown,
        "total_rules_triggered": len(breakdown),
    }


def classify_risk(score: int) -> tuple[str, str, str]:
    """Map score to level, CSS color, and emoji."""
    if score >= 75:
        return "CRITICAL", "#ff2d55", "🚨"
    elif score >= 50:
        return "HIGH",     "#ff9f0a", "⚠️"
    elif score >= 25:
        return "MODERATE", "#ffd60a", "🔶"
    else:
        return "LOW",      "#30d158", "✅"


def get_risk_recommendation(level: str) -> str:
    """Return recommended action for a given risk level."""
    recommendations = {
        "CRITICAL": (
            "**CRITICAL RISK — Seek immediate medical attention.** "
            "Do not delay. Contact emergency services or go to the nearest emergency department now."
        ),
        "HIGH": (
            "**HIGH RISK — Contact your doctor or pharmacist today.** "
            "Do not wait for your next scheduled appointment. Review your medication list urgently."
        ),
        "MODERATE": (
            "**MODERATE RISK — Discuss with your prescriber at your next appointment.** "
            "Monitor for any unusual symptoms and keep a log of side effects."
        ),
        "LOW": (
            "**LOW RISK — No major risk factors detected at this time.** "
            "Continue as directed by your doctor. Maintain regular follow-up appointments."
        ),
    }
    return recommendations.get(level, "Consult your healthcare provider.")
