"""
MedSafe AI — Symptom Advice Module (symptom.py)
Rule-based guidance for common symptoms.
Educational use only — not a diagnostic tool.
"""

SYMPTOM_ADVICE = {
    # ── Respiratory ──────────────────────────────────────────────────────────
    "cough": (
        "🤧 **Cough**\n"
        "- Stay hydrated; warm fluids like ginger-honey tea help soothe throat.\n"
        "- Honey + warm water helps soothe throat.\n"
        "- Avoid cold drinks.\n"
        "- Yoga: 'Anulom-Vilom', 'Kapalbhati' (if no breathlessness).\n"
        "- If blood in cough or > 2 weeks → doctor visit essential."
    ),
    "cold": (
        "🤧 **Cold / Sneezing / Runny Nose**\n"
        "- Drink warm liquids like soup or kadha.\n"
        "- Try saline nasal drops.\n"
        "- Steam inhalation recommended.\n"
        "- Yoga: 'Anulom-Vilom'.\n"
        "- Usually resolves in 5–7 days."
    ),
    "runny nose": (
        "🤧 **Cold / Sneezing / Runny Nose**\n"
        "- Drink warm liquids like soup or kadha.\n"
        "- Try saline nasal drops.\n"
        "- Steam inhalation recommended.\n"
        "- Yoga: 'Anulom-Vilom'.\n"
        "- Usually resolves in 5–7 days."
    ),
    "sneezing": (
        "🤧 **Cold / Sneezing / Runny Nose**\n"
        "- Drink warm liquids like soup or kadha.\n"
        "- Try saline nasal drops.\n"
        "- Steam inhalation recommended.\n"
        "- Usually resolves in 5–7 days."
    ),
    "shortness of breath": (
        "🚨 **Shortness of Breath — Seek Medical Attention**\n"
        "- Sit upright; loosen tight clothing.\n"
        "- Practice pursed-lip breathing (inhale 2 sec, exhale 4 sec).\n"
        "- Avoid exertion immediately.\n"
        "- ⚠️ If sudden onset or with chest pain → CALL EMERGENCY SERVICES."
    ),
    "breathlessness": (
        "🚨 **Breathlessness — Seek Medical Attention**\n"
        "- Sit upright; loosen tight clothing.\n"
        "- Practice pursed-lip breathing.\n"
        "- Avoid exertion immediately.\n"
        "- ⚠️ If sudden onset or with chest pain → CALL EMERGENCY SERVICES."
    ),

    # ── GI ───────────────────────────────────────────────────────────────────
    "diarrhea": (
        "💧 **Diarrhea / Loose Motion**\n"
        "- ORS is mandatory — frequent sips.\n"
        "- Avoid milk, spicy food, and raw salads.\n"
        "- BRAT diet: Banana, Rice, Applesauce, Toast.\n"
        "- Probiotics (curd/yogurt) can help restore gut flora.\n"
        "- If bloody diarrhea or > 3 days → doctor visit."
    ),
    "loose motion": (
        "💧 **Diarrhea / Loose Motion**\n"
        "- ORS is mandatory — frequent sips.\n"
        "- Avoid milk, spicy food, and raw salads.\n"
        "- BRAT diet: Banana, Rice, Applesauce, Toast.\n"
        "- If bloody diarrhea or > 3 days → doctor visit."
    ),
    "nausea": (
        "🤢 **Nausea / Vomiting**\n"
        "- Sip ginger tea or cold water slowly.\n"
        "- Eat small bland meals: crackers, toast, rice.\n"
        "- Avoid strong smells and fatty foods.\n"
        "- Rest in a comfortable position.\n"
        "- If vomiting blood → emergency care immediately."
    ),
    "vomiting": (
        "🤢 **Nausea / Vomiting**\n"
        "- Sip ginger tea or cold water slowly.\n"
        "- Stay hydrated — small frequent sips.\n"
        "- Avoid solid food for 1–2 hours after vomiting.\n"
        "- If vomiting blood or lasting > 24 hours → doctor visit."
    ),
    "stomach pain": (
        "🫀 **Stomach Pain / Abdominal Pain**\n"
        "- Rest and apply a warm compress to abdomen.\n"
        "- Avoid heavy, spicy, or fatty meals.\n"
        "- Peppermint tea may help with gas-related pain.\n"
        "- ⚠️ Severe, worsening, or sudden pain → seek emergency care."
    ),
    "acidity": (
        "🔥 **Acidity / Heartburn**\n"
        "- Avoid spicy, oily, acidic foods and caffeine.\n"
        "- Don't lie down for 2 hours after eating.\n"
        "- Cold milk or buttermilk may provide relief.\n"
        "- Elevate head of bed slightly.\n"
        "- Persistent symptoms → consult a doctor."
    ),
    "constipation": (
        "🌿 **Constipation**\n"
        "- Increase water intake (8–10 glasses/day).\n"
        "- Add high-fibre foods: fruits, vegetables, whole grains.\n"
        "- Light physical activity like walking helps.\n"
        "- Warm water with lemon in the morning can stimulate bowels.\n"
        "- If no relief in > 1 week → consult a doctor."
    ),

    # ── Pain ─────────────────────────────────────────────────────────────────
    "headache": (
        "🤕 **Headache**\n"
        "- Rest in a dark, quiet room.\n"
        "- Apply cold or warm compress to forehead/neck.\n"
        "- Stay well hydrated.\n"
        "- Peppermint oil on temples may help tension headache.\n"
        "- ⚠️ Sudden severe 'thunderclap' headache or with fever/stiff neck → emergency."
    ),
    "migraine": (
        "🤕 **Migraine**\n"
        "- Rest in a dark, quiet room.\n"
        "- Apply cold compress to head.\n"
        "- Avoid trigger foods: chocolate, caffeine, aged cheese.\n"
        "- Stay hydrated.\n"
        "- Consult a doctor for preventive medication if frequent."
    ),
    "back pain": (
        "🦴 **Back Pain**\n"
        "- Apply ice for first 48 hours, then switch to heat.\n"
        "- Gentle stretching and light walking — avoid prolonged bed rest.\n"
        "- Check posture, especially when sitting.\n"
        "- ⚠️ With numbness/tingling in legs or loss of bladder control → emergency."
    ),
    "joint pain": (
        "🦴 **Joint Pain**\n"
        "- Rest the affected joint; apply ice or heat.\n"
        "- Gentle range-of-motion exercises.\n"
        "- Turmeric with warm milk has anti-inflammatory properties.\n"
        "- ⚠️ Swollen, hot, red joint with fever → seek medical attention."
    ),

    # ── Cardiovascular ───────────────────────────────────────────────────────
    "chest pain": (
        "🚨 **Chest Pain — EMERGENCY**\n"
        "- ⚠️ CALL EMERGENCY SERVICES (112/911) IMMEDIATELY.\n"
        "- Sit or lie down in comfortable position.\n"
        "- Chew aspirin 325mg if not allergic and no contraindications.\n"
        "- Do NOT drive yourself to hospital.\n"
        "- Do NOT ignore or dismiss chest pain."
    ),
    "palpitations": (
        "💓 **Palpitations / Fast Heartbeat**\n"
        "- Sit down and rest immediately.\n"
        "- Try vagal maneuvers: slow deep breathing or splashing cold water on face.\n"
        "- Reduce caffeine and alcohol intake.\n"
        "- ⚠️ With chest pain, dizziness, or fainting → emergency care."
    ),

    # ── General ──────────────────────────────────────────────────────────────
    "fever": (
        "🌡️ **Fever**\n"
        "- Stay well hydrated; rest is essential.\n"
        "- Lukewarm sponge bath can help reduce temperature.\n"
        "- Light breathable clothing.\n"
        "- Paracetamol (as directed) for comfort.\n"
        "- ⚠️ Fever above 103°F (39.4°C) or lasting > 3 days → doctor visit.\n"
        "- Infants under 3 months with any fever → immediate medical attention."
    ),
    "dizziness": (
        "😵 **Dizziness**\n"
        "- Sit or lie down immediately to prevent falls.\n"
        "- Avoid sudden position changes — rise slowly.\n"
        "- Stay hydrated.\n"
        "- ⚠️ With chest pain, sudden severe dizziness, or neurological symptoms → emergency."
    ),
    "fatigue": (
        "😴 **Fatigue / Tiredness**\n"
        "- Ensure 7–9 hours of quality sleep.\n"
        "- Stay hydrated and eat balanced meals.\n"
        "- Light exercise like walking improves energy levels.\n"
        "- Check iron, vitamin B12, and thyroid levels if persistent.\n"
        "- Persistent fatigue > 2 weeks → consult a doctor."
    ),
    "rash": (
        "🔴 **Skin Rash**\n"
        "- Avoid scratching to prevent infection.\n"
        "- Apply calamine lotion or aloe vera for comfort.\n"
        "- Oatmeal bath may soothe itching.\n"
        "- Note any new medications started recently.\n"
        "- ⚠️ Widespread rash with fever or difficulty breathing → emergency."
    ),
    "itching": (
        "🔴 **Itching / Pruritus**\n"
        "- Avoid scratching.\n"
        "- Apply cold compress or calamine lotion.\n"
        "- Use mild, fragrance-free soap.\n"
        "- Antihistamines may provide relief.\n"
        "- ⚠️ With swelling of face/throat → emergency (possible anaphylaxis)."
    ),
    "swelling": (
        "💧 **Swelling / Edema**\n"
        "- Elevate the affected limb above heart level.\n"
        "- Reduce salt intake.\n"
        "- Avoid prolonged sitting or standing.\n"
        "- ⚠️ Sudden swelling of face, lips, or throat → emergency.\n"
        "- Unexplained leg swelling with pain → rule out DVT urgently."
    ),
    "insomnia": (
        "🌙 **Insomnia / Sleep Issues**\n"
        "- Maintain consistent sleep and wake times.\n"
        "- Avoid screens 1 hour before bed.\n"
        "- Keep bedroom cool and dark.\n"
        "- Chamomile tea or warm milk before bed.\n"
        "- Avoid caffeine after 2 PM."
    ),
    "anxiety": (
        "🧘 **Anxiety / Stress**\n"
        "- Practice deep breathing: 4-7-8 technique.\n"
        "- Regular exercise reduces anxiety symptoms.\n"
        "- Limit caffeine and alcohol.\n"
        "- Talk to a trusted person or mental health professional.\n"
        "- Meditation and mindfulness can help significantly."
    ),
}


def symptom_advice(symptom: str) -> str | None:
    """
    Return rule-based advice for a given symptom string.
    Checks for exact match first, then keyword match.
    Returns None if no match found.
    """
    symptom_lower = symptom.lower().strip()

    # Exact match
    if symptom_lower in SYMPTOM_ADVICE:
        return SYMPTOM_ADVICE[symptom_lower]

    # Keyword-based partial match
    for key in SYMPTOM_ADVICE:
        if key in symptom_lower or symptom_lower in key:
            return SYMPTOM_ADVICE[key]

    return None


def get_all_symptoms() -> list[str]:
    """Return list of all known symptoms."""
    return sorted(set(SYMPTOM_ADVICE.keys()))
