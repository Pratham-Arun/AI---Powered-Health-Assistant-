import streamlit as st
import random
import time

# Set page config
st.set_page_config(
    page_title="Health Assistant",
    page_icon="🩺",
    layout="wide"
)

# Health knowledge base
health_responses = {
    "headache": [
        "Headaches can be caused by stress, dehydration, eye strain, or lack of sleep. Try resting in a quiet, dark room, staying hydrated, and taking a break from screens.",
        "Consider over-the-counter pain relievers like acetaminophen or ibuprofen. If headaches are severe or frequent, consult a doctor.",
        "Practice relaxation techniques like deep breathing. Ensure you're getting enough sleep and staying hydrated."
    ],
    "fever": [
        "Fever is often a sign of infection. Monitor your temperature and rest. Seek medical attention if fever is high (>103°F/39.4°C) or persistent.",
        "Stay hydrated and rest. Use acetaminophen or ibuprofen to reduce fever. If fever persists for more than 3 days, see a doctor.",
        "Fever helps your body fight infection. Rest, drink plenty of fluids, and monitor your symptoms."
    ],
    "chest pain": [
        "⚠️ CHEST PAIN CAN BE SERIOUS! If you're experiencing chest pain, especially with shortness of breath, seek immediate medical attention. Call emergency services if needed.",
        "Chest pain requires immediate medical evaluation. Don't ignore it - it could be a sign of a heart condition.",
        "If chest pain is severe, crushing, or accompanied by other symptoms, call emergency services immediately."
    ],
    "cough": [
        "Rest, stay hydrated, and consider honey for soothing. Over-the-counter cough medicines may help. If severe or persistent, see a doctor.",
        "A cough can be caused by cold, flu, or allergies. Rest and stay hydrated. If it persists for weeks, consult a healthcare provider.",
        "Try honey, warm tea, or over-the-counter remedies. If cough is severe or produces colored mucus, see a doctor."
    ],
    "cold": [
        "Rest, stay hydrated, and get plenty of sleep. Over-the-counter medications can help with symptoms. Most colds resolve in 7-10 days.",
        "There's no cure for the common cold, but rest and fluids help. Consider zinc supplements and vitamin C.",
        "Use saline nasal sprays, stay hydrated, and rest. Avoid antibiotics unless prescribed by a doctor."
    ],
    "exercise": [
        "Aim for 150 minutes of moderate exercise per week. Start gradually and build up. Walking, swimming, and cycling are great options.",
        "Regular exercise benefits both physical and mental health. Start with 10-15 minutes daily and gradually increase.",
        "Include both cardio and strength training. Always warm up and cool down. Consult your doctor before starting a new exercise program."
    ],
    "diet": [
        "A balanced diet includes fruits, vegetables, lean proteins, whole grains, and healthy fats. Stay hydrated with water.",
        "Eat a variety of colorful fruits and vegetables. Limit processed foods, added sugars, and excessive salt.",
        "Consider the Mediterranean diet or DASH diet for heart health. Portion control and regular meal times are important."
    ],
    "sleep": [
        "Adults need 7-9 hours of sleep per night. Maintain a regular sleep schedule and create a relaxing bedtime routine.",
        "Avoid screens before bed, keep your room cool and dark, and avoid caffeine late in the day.",
        "Good sleep hygiene includes a consistent schedule, comfortable environment, and avoiding large meals before bed."
    ],
    "stress": [
        "Practice stress management techniques like deep breathing, meditation, or yoga. Regular exercise and adequate sleep help.",
        "Consider talking to a counselor or therapist. Mindfulness and relaxation techniques can be very effective.",
        "Identify stress triggers and develop healthy coping mechanisms. Don't hesitate to seek professional help if needed."
    ],
    "medication": [
        "Always take medications exactly as prescribed by your doctor. Don't stop or change doses without consulting your healthcare provider.",
        "Store medications properly and check expiration dates. Never share prescription medications with others.",
        "Keep a list of all medications you're taking. Report any side effects to your doctor immediately."
    ]
}

def get_health_response(user_input):
    """Get a health response based on user input"""
    user_input_lower = user_input.lower()
    
    # Check for emergency keywords first
    emergency_keywords = ["chest pain", "heart attack", "stroke", "unconscious", "severe bleeding"]
    for keyword in emergency_keywords:
        if keyword in user_input_lower:
            return "🚨 EMERGENCY: If you're experiencing a medical emergency, call emergency services (911) immediately! This is not a substitute for emergency medical care."
    
    # Check for health topics
    for topic, responses in health_responses.items():
        if topic in user_input_lower:
            return random.choice(responses)
    
    # General responses for other queries
    general_responses = [
        "I can provide general health information, but for specific medical advice, please consult a healthcare professional.",
        "This is general information only. For personalized medical advice, please see your doctor.",
        "I'm here to provide health information, but I can't diagnose or treat medical conditions. Please consult a healthcare provider for specific concerns.",
        "For medical diagnosis or treatment, please consult a qualified healthcare professional.",
        "This information is for educational purposes only. Always consult your doctor for medical advice."
    ]
    
    return random.choice(general_responses)

def main():
    # Header
    st.markdown("""
    <div style='text-align: center; padding: 20px; background-color: #f0f8ff; border-radius: 10px; margin-bottom: 20px;'>
        <h1>🩺 Health Assistant</h1>
        <p style='font-size: 18px; color: #666;'>Your AI-powered health information companion</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Disclaimer
    st.warning("""
    ⚠️ **Medical Disclaimer**: This app provides general health information only. 
    It is not a substitute for professional medical advice, diagnosis, or treatment. 
    Always consult with qualified healthcare professionals for medical concerns.
    """)
    
    # Sidebar
    with st.sidebar:
        st.header("💡 Health Topics")
        st.markdown("""
        Try asking about:
        - Headaches
        - Fever
        - Cough & Cold
        - Exercise
        - Diet & Nutrition
        - Sleep
        - Stress
        - Medications
        """)
        
        st.header("🚨 Emergency")
        st.markdown("""
        **For medical emergencies:**
        - Call 108 immediately
        - Don't rely on this app for emergency care
        """)
    
    # Main chat area
    st.header("💬 Ask me about health")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("What health question do you have?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("🤖 Thinking..."):
                time.sleep(0.5)  # Small delay for better UX
                response = get_health_response(prompt)
                st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Clear chat button
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    
if __name__ == "__main__":
    main()
