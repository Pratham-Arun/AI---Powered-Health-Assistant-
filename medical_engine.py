import random
import re
import datetime
import io

try:
    from fpdf import FPDF
    PDF_READY = True
except ImportError:
    PDF_READY = False

try:
    import easyocr
    OCR_READY = True
except ImportError:
    OCR_READY = False

import numpy as np
from PIL import Image

class MedicalEngine:
    def __init__(self):
        # Structured knowledge base with patient-friendly explanations and consultation triggers
        self.knowledge_base = {
            "headache": {
                "explanation": "A headache is pain or discomfort in the head or face area. They can range from minor annoyances to severe pain.",
                "common_causes": [
                    "Stress and tension",
                    "Dehydration (not drinking enough water)",
                    "Eye strain (especially from screens)",
                    "Lack of sleep",
                    "Caffeine withdrawal"
                ],
                "self_care": [
                    "Rest in a quiet, dark room.",
                    "Apply a cool cloth to your forehead.",
                    "Drink plenty of water.",
                    "Gentle stretching or massage of neck muscles."
                ],
                "consult_doctor_if": [
                    "The headache is sudden and the 'worst of your life'.",
                    "It follows a head injury.",
                    "It is accompanied by fever, stiff neck, or confusion.",
                    "You experience vision changes or numbness.",
                    "Headaches are becoming more frequent or severe."
                ],
                "common_otc_relief": [
                    "**Paracetamol (Acetaminophen)**: Commonly used for pain relief and fever.",
                    "**Ibuprofen**: Helps reduce inflammation and pain.",
                    "**Aspirin**: Sometimes used for adults (avoid in children due to Reye's syndrome risk)."
                ]
            },
            "fever": {
                "explanation": "A fever is a temporary increase in your body temperature, often due to an illness. It's a sign that your immune system is fighting something.",
                "common_causes": [
                    "Viral infections (like cold or flu)",
                    "Bacterial infections",
                    "Heat exhaustion",
                    "Certain inflammatory conditions"
                ],
                "self_care": [
                    "Drink plenty of fluids (water, broth, juice).",
                    "Get lots of rest.",
                    "Keep the room temperature cool.",
                    "Wear lightweight clothing."
                ],
                "consult_doctor_if": [
                    "Temperature is 103°F (39.4°C) or higher.",
                    "Fever lasts more than three days.",
                    "Accompanied by severe headache, rash, or stiff neck.",
                    "You have difficulty breathing or chest pain."
                ],
                "common_otc_relief": [
                    "**Paracetamol (Acetaminophen)**: Effective for lowering body temperature.",
                    "**Ibuprofen**: Can help reduce fever and associated body aches."
                ]
            },
            "abdominal pain": {
                "explanation": "Abdominal pain (stomach ache) is pain felt anywhere between your chest and groin.",
                "common_causes": [
                    "Indigestion or gas",
                    "Muscle strain",
                    "Stomach virus (gastritis)",
                    "Food intolerance"
                ],
                "self_care": [
                    "Sip water or clear fluids.",
                    "Avoid solid foods for a few hours.",
                    "Rest in a comfortable position.",
                    "Apply a heating pad (low setting) to the area."
                ],
                "consult_doctor_if": [
                    "Pain is severe, sudden, or sharp.",
                    "Your abdomen is tender to the touch.",
                    "Pain radiates to your chest, neck, or shoulder.",
                    "You have blood in your stool or are vomiting blood.",
                    "You have persistent nausea or fever."
                ]
            },
            "cough": {
                "explanation": "A cough is your body's way of clearing irritants and mucus from your airways.",
                "common_causes": [
                    "Common cold or flu",
                    "Allergies or asthma",
                    "Post-nasal drip",
                    "Environmental irritants (smoke, dust)"
                ],
                "self_care": [
                    "Stay hydrated to thin mucus.",
                    "Use a humidifier or take a steamy shower.",
                    "Try a spoonful of honey (for adults and children over 1).",
                    "Gargle with warm salt water."
                ],
                "consult_doctor_if": [
                    "Cough lasts longer than 3 weeks.",
                    "You are coughing up blood.",
                    "You have shortness of breath or wheezing.",
                    "Accompanied by high fever or chest pain."
                ],
                "common_otc_relief": [
                    "**Cough Suppressants (Antitussives)**: For dry, hacking coughs.",
                    "**Expectorants (Guaifenesin)**: To help thin and clear mucus from the chest.",
                    "**Decongestants**: If accompanied by a stuffy nose."
                ]
            },
            "diabetes": {
                "explanation": "Diabetes is a condition where your blood sugar (glucose) levels are too high. Glucose is your main source of energy, coming from the food you eat.",
                "tips": [
                    "Follow a balanced diet rich in vegetables, lean protein, and whole grains.",
                    "Monitor your blood sugar levels as recommended by your doctor.",
                    "Stay physically active with regular exercise.",
                    "Take all prescribed medications exactly as directed.",
                    "Check your feet daily for any cuts or sores."
                ],
                "consult_doctor_if": [
                    "You experience extreme thirst or frequent urination.",
                    "You have blurred vision that doesn't go away.",
                    "You feel unusually tired or weak.",
                    "Cuts or bruises are slow to heal."
                ]
            },
            "hypertension": {
                "explanation": "Hypertension (high blood pressure) means the force of blood against your artery walls is too high, which can damage your heart over time.",
                "tips": [
                    "Reduce salt (sodium) in your diet.",
                    "Maintain a healthy weight.",
                    "Exercise regularly.",
                    "Limit alcohol and quit smoking.",
                    "Manage stress through relaxation techniques."
                ],
                "consult_doctor_if": [
                    "You have severe headaches or nosebleeds.",
                    "You feel dizzy or have blurred vision.",
                    "You experience chest pain or shortness of breath.",
                    "Your home blood pressure readings are consistently high."
                ]
            },
            "fatigue": {
                "explanation": "Fatigue is a constant feeling of tiredness or lack of energy that doesn't go away with rest. It can be physical, mental, or both.",
                "common_causes": [
                    "Anemia (low blood count)",
                    "Sleep disorders (like apnea)",
                    "Stress, anxiety, or depression",
                    "Thyroid problems",
                    "Poor nutrition or dehydration"
                ],
                "self_care": [
                    "Maintain a regular sleep schedule.",
                    "Stay hydrated and eat balanced meals.",
                    "Engage in light physical activity.",
                    "Practice stress-reduction techniques."
                ],
                "consult_doctor_if": [
                    "Fatigue is severe and lasts more than two weeks.",
                    "Accompanied by unexplained weight loss.",
                    "Accompanied by low mood or loss of interest in activities.",
                    "You have difficulty performing daily tasks."
                ]
            },
            "anemia": {
                "explanation": "Anemia happens when your blood doesn't have enough healthy red blood cells or hemoglobin to carry oxygen to your tissues.",
                "tests_to_get": [
                    "**Complete Blood Count (CBC)**: This is the primary test to check your red blood cell, white blood cell, and platelet levels.",
                    "**Iron Tests**: To check if your iron levels are low.",
                    "**Vitamin B12 and Folate tests**: To check for nutritional deficiencies."
                ],
                "self_care": [
                    "Eat iron-rich foods (lean meat, leafy greens, beans).",
                    "Take vitamin supplements if recommended by a doctor.",
                    "Rest when you feel tired."
                ],
                "consult_doctor_if": [
                    "You feel unusually weak or dizzy.",
                    "Your skin looks pale or yellowish.",
                    "You have a fast or irregular heartbeat.",
                    "You experience chest pain or cold hands and feet."
                ]
            },
            "blood loss": {
                "explanation": "Blood loss (hemorrhage) can be internal or external and can lead to symptoms like dizziness, weakness, and fatigue.",
                "actions_to_take": [
                    "If bleeding is external, apply firm, direct pressure to the wound.",
                    "If you suspect internal bleeding due to an injury, seek medical attention immediately.",
                    "A **Complete Blood Count (CBC)** test is used to measure the impact of blood loss on your body."
                ],
                "consult_doctor_if": [
                    "Bleeding is heavy or won't stop with pressure.",
                    "You feel lightheaded or faint.",
                    "You have blood in your stool or vomit.",
                    "You have deep wounds or suspected internal injuries."
                ]
            },
            "blood tests": {
                "explanation": "Blood tests involve taking a sample of your blood to assess your overall health and detect specific conditions.",
                "common_profiles": [
                    "**Complete Blood Count (CBC)**: Measures red/white cells, hemoglobin, and platelets. Good for checking for fatigue, infection, and anemia.",
                    "**Lipid Profile**: Checks cholesterol levels (LDL, HDL, triglycerides).",
                    "**Kidney Function Test (KFT)**: Checks levels of urea and creatinine.",
                    "**Liver Function Test (LFT)**: Measures enzymes and proteins related to liver health.",
                    "**Blood Sugar Test**: Checks for glucose levels (Diabetes monitoring)."
                ],
                "tests_to_get": [
                    "Basic health screening (Annual physical)",
                    "Diagnostic tests based on specific symptoms (like fatigue or pain)",
                    "Monitoring chronic conditions"
                ],
                "consult_doctor_if": [
                    "You receive results outside the 'normal' range.",
                    "You have persistent symptoms despite normal results.",
                    "You need help interpreting complex lab reports."
                ]
            }
        }

        # Lab Markers Reference (Simplified)
        self.lab_markers = {
            "hemoglobin": {"min": 13.5, "max": 17.5, "unit": "g/dL", "low": "Potential Anemia", "high": "Polycythemia"},
            "glucose": {"min": 70, "max": 100, "unit": "mg/dL", "low": "Hypoglycemia", "high": "Potential Diabetes/Hyperglycemia"},
            "wbc": {"min": 4500, "max": 11000, "unit": "cells/mcL", "low": "Weakened Immune System", "high": "Infection or Inflammation"},
            "platelets": {"min": 150000, "max": 450000, "unit": "mcL", "low": "Thrombocytopenia (Bleeding risk)", "high": "Thrombocytosis (Clotting risk)"}
        }

        self.emergency_keywords = [
            "chest pain", "can't breathe", "shortness of breath", "stroke", 
            "unconscious", "heavy bleeding", "seizure", "poison", "worst headache"
        ]

        # Translation Mappings
        self.translations = {
            "en": {
                "understanding": "Understanding",
                "what_it_is": "What it is",
                "common_causes": "Common Causes",
                "self_care": "Self-Care & Relief",
                "tips": "Health Management Tips",
                "otc_relief": "Common Over-the-Counter (OTC) Relief",
                "diagnostic_profiles": "Common Diagnostic Profiles",
                "recommended_tests": "Recommended Tests",
                "tests_desc": "To better understand your condition, a doctor might recommend:",
                "actions": "Actions to Take",
                "consult_doctor": "When to Consult a Doctor",
                "consult_desc": "It is important to seek professional medical advice if:",
                "disclaimer": "*Disclaimer: This information is for educational purposes. Always consult a healthcare professional for diagnosis and treatment.*",
                "fallback_intro": "I've noted that you're asking about",
                "fallback_general": "While I don't have a detailed profile for this specific topic yet, here is some general guidance:",
                "emergency_title": "URGENT MEDICAL ADVICE: IMMEDIATE ACTION REQUIRED",
                "emergency_steps": "Please take the following steps immediately:",
                "emergency_disclaimer": "*This chatbot is for informational purposes and cannot provide emergency medical care.*",
                "lab_interpretation": "Lab Interpretation Report"
            },
            "hi": {
                "understanding": "समझना",
                "what_it_is": "यह क्या है",
                "common_causes": "सामान्य कारण",
                "self_care": "स्व-देखभाल और राहत",
                "tips": "स्वास्थ्य प्रबंधन टिप्स",
                "otc_relief": "सामान्य ओवर-द-काउंटर (OTC) राहत",
                "diagnostic_profiles": "सामान्य नैदानिक प्रोफाइल",
                "recommended_tests": "अनुशंसित परीक्षण",
                "tests_desc": "आपकी स्थिति को बेहतर ढंग से समझने के लिए, डॉक्टर इन परीक्षणों की सिफारिश कर सकते हैं:",
                "actions": "किए जाने वाले कार्य",
                "consult_doctor": "डॉक्टर से कब सलाह लें",
                "consult_desc": "यदि आपको निम्नलिखित समस्याएं हैं, तो पेशेवर चिकित्सा सलाह लेना महत्वपूर्ण है:",
                "disclaimer": "*अस्वीकरण: यह जानकारी केवल शैक्षिक उद्देश्यों के लिए है। निदान और उपचार के लिए हमेशा स्वास्थ्य देखभाल पेशेवर से परामर्श लें।*",
                "fallback_intro": "मैंने गौर किया है कि आप इसके बारे में पूछ रहे हैं",
                "fallback_general": "हालांकि मेरे पास अभी तक इस विशिष्ट विषय के लिए विस्तृत प्रोफाइल नहीं है, लेकिन यहां कुछ सामान्य मार्गदर्शन दिया गया है:",
                "emergency_title": "तत्काल चिकित्सा सलाह: तत्काल कार्रवाई की आवश्यकता है",
                "emergency_steps": "कृपया तुरंत निम्नलिखित कदम उठाएं:",
                "emergency_disclaimer": "*यह चैटबॉट केवल सूचनात्मक उद्देश्यों के लिए है और आपातकालीन चिकित्सा देखभाल प्रदान नहीं कर सकता है।*",
                "lab_interpretation": "लैब व्याख्या रिपोर्ट"
            },
            "hinglish": {
                "understanding": "Understanding",
                "what_it_is": "Ye kya hai",
                "common_causes": "Common Causes",
                "self_care": "Self-Care & Relief",
                "tips": "Health Management Tips",
                "otc_relief": "Common OTC Meds",
                "diagnostic_profiles": "Common Diagnostic Profiles",
                "recommended_tests": "Recommended Tests",
                "tests_desc": "Apni condition ko better samajhne ke liye, doctor ye tests suggest kar sakte hain:",
                "actions": "Actions to Take",
                "consult_doctor": "Doctor se kab consult karein",
                "consult_desc": "Professional medical advice lena zaroori hai agar:",
                "disclaimer": "*Disclaimer: Ye info sirf educational purposes ke liye hai. Diagnose aur treatment ke liye hamesha doctor se milein.*",
                "fallback_intro": "Maine dekha ki aap pooch rahe hain",
                "fallback_general": "Mere paas abhi is topic par detail info nahi hai, par ye general guidance hai:",
                "emergency_title": "URGENT MEDICAL ADVICE: IMMEDIATE ACTION REQUIRED",
                "emergency_steps": "Please jaldi ye steps follow karein:",
                "emergency_disclaimer": "*Ye chatbot sirf info ke liye hai aur emergency care provide nahi kar sakta.*",
                "lab_interpretation": "Lab Interpretation Report"
            }
        }

    def detect_language(self, text):
        """Automatically detect language: English, Hindi, or Hinglish."""
        # 1. Detect Hindi (Devanagari script)
        if any('\u0900' <= char <= '\u097F' for char in text):
            return "hi"
        
        # 2. Detect Hinglish (Heuristic keywords/patterns)
        # We look for common Hindi stop-words or sentence endings written in Roman script
        hinglish_keywords = {
            "hai", "kya", "ka", "ki", "ko", "mein", "bhi", "toh", "kar", "hoga", 
            "sakta", "nahi", "pe", "mil", "de", "do", "aap", "hu", "tha", "rahe",
            "raha", "chahiye", "karna", "ke", "ne", "liye", "kya", "bataye", "batana",
            "ho", "rha", "rhi", "hu", "tha", "thi", "rhe", "karne", "wali", "wala",
            "sir", "madam", "doktor", "doctor", "medicine", "dawaim", "dawae", "btaye"
        }
        words = set(text.lower().replace("?", "").replace(".", "").replace(",", "").split())
        
        if not words.isdisjoint(hinglish_keywords):
            return "hinglish"
            
        return "en"

    def process_query(self, query, lang=None):
        if lang is None:
            lang = self.detect_language(query)
            
        query_lower = query.lower()
        t = self.translations.get(lang, self.translations["en"])

        # 1. Check for Emergency
        for kw in self.emergency_keywords:
            if kw in query_lower:
                return self._format_emergency_response(kw, t)

        # 2. Identify All Matches
        matched_topics = []
        for topic in self.knowledge_base:
            if topic in query_lower:
                matched_topics.append(topic)
        
        # 3. Handle Matches
        if len(matched_topics) == 1:
            return self._format_detailed_response(matched_topics[0], t)
        elif len(matched_topics) > 1:
            return self._format_multi_condition_response(matched_topics, t)

        # 4. Handle Greeting/General
        if any(greet in query_lower for greet in ["hello", "hi", "hey"]):
            if lang == "hi":
                return "नमस्ते! मैं आपका हेल्थ असिस्टेंट हूं। मैं चिकित्सा स्थितियों के बारे में बता सकता हूं और आपको यह तय करने में मदद कर सकता हूं कि क्या आपको डॉक्टर को देखने की आवश्यकता है। आज आपके मन में क्या है?"
            elif lang == "hinglish":
                return "Hello! Main aapka Health Assistant hoon. Main medical conditions ke bare mein bata sakta hoon aur aapki help kar sakta hoon decide karne mein ki doctor se milna chahiye ya nahi. Aaj kya help chahiye?"
            return "Hello! I'm your Health Assistant. I can explain medical conditions in simple terms and help you decide if you need to see a doctor. What's on your mind today?"

        return self._format_fallback_response(query, t)

    def interpret_lab_results(self, text, lang="en"):
        t = self.translations.get(lang, self.translations["en"])
        found_markers = []
        text_lower = text.lower()

        for marker, bounds in self.lab_markers.items():
            # Simple regex to find "Marker: Value" or "Marker Value"
            pattern = rf"{marker}\s*(?::|)\s*(\d+(?:\.\d+|))"
            match = re.search(pattern, text_lower)
            if match:
                val = float(match.group(1))
                status = "Normal"
                if val < bounds["min"]: status = bounds["low"]
                elif val > bounds["max"]: status = bounds["high"]
                
                found_markers.append({
                    "name": marker.capitalize(),
                    "value": val,
                    "unit": bounds["unit"],
                    "range": f"{bounds['min']} - {bounds['max']}",
                    "status": status
                })

        if not found_markers:
            return "No common lab markers identified. Please ensure the report contains keywords like Hemoglobin, Glucose, or WBC."

        response = f"### 🔬 {t.get('lab_interpretation', 'Lab Interpretation')}\n\n"
        for m in found_markers:
            color = "green" if m["status"] == "Normal" else "red"
            response += f"- **{m['name']}**: {m['value']} {m['unit']} (Normal: {m['range']}) -> <span style='color:{color}'>{m['status']}</span>\n"
        
        response += "\n---\n*Disclaimer: Artificial intelligence analysis is not a medical diagnosis. Always review lab results with your doctor.*"
        return response

    def extract_text_from_image(self, image_bytes):
        """Extract text from an image using EasyOCR."""
        if not OCR_READY:
            return "OCR module (EasyOCR) is currently installing or not found. Please wait a moment or check your installation."
        try:
            reader = easyocr.Reader(['en']) # Support more if needed
            result = reader.readtext(image_bytes, detail=0)
            return " ".join(result)
        except Exception as e:
            return f"Error during OCR: {str(e)}"

    def generate_health_report(self, messages, bmi=None, water_intake=0, water_goal=2500, lang="en"):
        if not PDF_READY:
            raise ImportError("PDF module (fpdf2) is currently installing or not found. Please wait a moment.")
            
        t = self.translations.get(lang, self.translations["en"])
        pdf = FPDF()
        pdf.add_page()
        
        # Title
        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, txt="Health Assistant Report", ln=True, align='C')
        pdf.set_font("Arial", "", 10)
        pdf.cell(200, 10, txt=f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %I:%M %p')}", ln=True, align='C')
        pdf.ln(10)

        # Health Metrics
        pdf.set_font("Arial", "B", 14)
        pdf.cell(200, 10, txt="1. Health Metrics Summary", ln=True)
        pdf.set_font("Arial", "", 12)
        if bmi:
            pdf.cell(200, 10, txt=f"- BMI: {bmi:.1f}", ln=True)
        pdf.cell(200, 10, txt=f"- Water Intake: {water_intake}ml / {water_goal}ml", ln=True)
        pdf.ln(5)

        # Chat Summary
        pdf.set_font("Arial", "B", 14)
        pdf.cell(200, 10, txt="2. Consultation Summary", ln=True)
        pdf.set_font("Arial", "", 10)
        
        for msg in messages:
            role = "USER" if msg["role"] == "user" else "ASSISTANT"
            pdf.set_font("Arial", "B", 10)
            pdf.cell(200, 8, txt=f"{role}:", ln=True)
            pdf.set_font("Arial", "", 10)
            # Filter out icons and markdown bolding for the PDF
            content = msg["content"].replace("🩺", "").replace("🤖", "").replace("🧑‍💬", "").replace("**", "").replace("🚨", "")
            pdf.multi_cell(0, 5, txt=content)
            pdf.ln(2)

        pdf.ln(10)
        pdf.set_font("Arial", "I", 8)
        pdf.multi_cell(0, 5, txt="Disclaimer: This report is for informational purposes only and is not a clinical diagnosis. Always consult with a licensed healthcare professional.")
        
        return pdf.output(dest='S') # Return PDF as byte string

    def _format_multi_condition_response(self, topics, t):
        summary = f"## Potential Related Conditions\n\n"
        summary += f"Based on your symptoms, I found several related health topics: **{', '.join([t.capitalize() for t in topics])}**.\n\n"
        summary += "Here is a quick overview of how these may be related:\n\n"
        
        for topic in topics:
            data = self.knowledge_base[topic]
            summary += f"### {topic.capitalize()}\n"
            summary += f"{data['explanation']}\n\n"
        
        summary += "---\n### 🩺 Next Steps\n"
        summary += f"Since you are experiencing multiple symptoms, it is highly recommended to **consult a healthcare professional** for a proper diagnosis. They can determine if these are linked.\n\n"
        summary += f"{t['disclaimer']}"
        return summary

    def _format_emergency_response(self, keyword, t):
        return f"""
### 🚨 {t['emergency_title']}

You mentioned **{keyword}**, which can be a sign of a life-threatening emergency.

**{t['emergency_steps']}**
1. **Call emergency services (e.g., 911 or 108)** right now.
2. Do not attempt to drive yourself to the hospital.
3. Stay on the line with the emergency operator and follow their instructions.

{t['emergency_disclaimer']}
"""

    def _format_detailed_response(self, topic, t):
        data = self.knowledge_base[topic]
        response = f"## {t['understanding']} {topic.capitalize()}\n\n"
        response += f"**{t['what_it_is']}:** {data['explanation']}\n\n"

        if "common_causes" in data:
            response += f"### {t['common_causes']}\n"
            for cause in data['common_causes']:
                response += f"- {cause}\n"
            response += "\n"

        if "self_care" in data:
            response += f"### {t['self_care']}\n"
            for item in data['self_care']:
                response += f"- {item}\n"
            response += "\n"
        
        if "tips" in data:
            response += f"### {t['tips']}\n"
            for tip in data['tips']:
                response += f"- {tip}\n"
            response += "\n"

        if "common_otc_relief" in data:
            response += f"### 💊 {t['otc_relief']}\n"
            caution = "> [!CAUTION]\n> **Always consult a pharmacist or doctor before taking new medication.** Check for allergies, dosages, and interactions.\n\n"
            if t == self.translations["hi"]:
                caution = "> [!CAUTION]\n> **नई दवा लेने से पहले हमेशा फार्मासिस्ट या डॉक्टर से सलाह लें।** एलर्जी, खुराक और बातचीत की जांच करें।\n\n"
            elif t == self.translations["hinglish"]:
                caution = "> [!CAUTION]\n> **Nayi medicine lene se pehle hamesha pharmacist ya doctor se consult karein.** Allergies aur dosage zarur check karein.\n\n"
            
            response += caution
            for medicine in data['common_otc_relief']:
                response += f"- {medicine}\n"
            response += "\n"

        if "common_profiles" in data:
            response += f"### 📊 {t['diagnostic_profiles']}\n"
            for profile in data['common_profiles']:
                response += f"- {profile}\n"
            response += "\n"

        if "tests_to_get" in data:
            response += f"### 🧪 {t['recommended_tests']}\n"
            response += f"{t['tests_desc']}\n"
            for test in data['tests_to_get']:
                response += f"- {test}\n"
            response += "\n"

        if "actions_to_take" in data:
            response += f"### ✅ {t['actions']}\n"
            for action in data['actions_to_take']:
                response += f"- {action}\n"
            response += "\n"

        response += f"### 🩺 {t['consult_doctor']}\n"
        response += f"{t['consult_desc']}\n"
        for condition in data['consult_doctor_if']:
            response += f"- {condition}\n"
        
        response += f"\n---\n{t['disclaimer']}"
        return response

    def _format_fallback_response(self, query, t):
        # "Smart Brain" simulation: Identify intent and provide agentic feedback
        intent = "general"
        if any(w in query.lower() for w in ["how", "why", "what", "tell me"]): intent = "explanation"
        if any(w in query.lower() for w in ["help", "do", "action"]): intent = "advice"

        intro = f"{t['fallback_intro']} **\"{query}\"**."
        
        if intent == "explanation":
            middle = "I am analyzing your request to provide a clear explanation. While I search my medical database, keep in mind that I am a rule-based assistant optimized for specific health profiles."
        elif intent == "advice":
            middle = "I understand you are looking for advice. As your Health Assistant, I prioritize safety above all else. Here is how you can proceed:"
        else:
            middle = t['fallback_general']

        return f"""
{intro} {middle}

**My Thought Process:**
1. Search recognized medical conditions (Headache, Fever, Diabetes, etc.) -> **No exact match.**
2. Provide general wellness guidance and safety indicators.

**General Guidance:**
- **Observe**: Notice any new symptoms or changes in existing ones.
- **Hydrate**: Drink enough water for better recovery.
- **Rest**: Give your body time to heal.

**When to seek immediate help:**
If you have a high fever, sudden intense pain, or trouble breathing, please go to the nearest emergency center (A&E).

*Would you like to ask about a specific condition like 'Headache' or 'Diabetes' instead?*
"""

# Singleton instance
engine = MedicalEngine()
