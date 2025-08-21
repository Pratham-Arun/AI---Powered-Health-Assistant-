import streamlit as st
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download necessary NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
except:
    pass

# Initialize chatbot variable
chatbot = None

# Try to load the transformers pipeline with error handling
try:
    from transformers import pipeline
    chatbot = pipeline("text-generation", model="distilgpt2", device=-1)  # Use CPU
except Exception as e:
    st.warning(f"⚠️ AI model could not be loaded: {str(e)}. Using rule-based responses only.")

# Define healthcare-specific response logic
def healthcare_chatbot(user_input):
    user_input_lower = user_input.lower()
    
    # Simple rule-based keywords to respond
    if any(word in user_input_lower for word in ["headache", "head pain", "migraine"]):
        return "Headaches can have various causes like stress, dehydration, or eye strain. Consider resting in a quiet, dark room and staying hydrated. If severe or persistent, please consult a doctor."
    
    elif any(word in user_input_lower for word in ["fever", "temperature", "hot"]):
        return "Fever is often a sign of infection. Monitor your temperature and rest. Seek medical attention if fever is high (>103°F/39.4°C) or persistent for more than 3 days."
    
    elif any(word in user_input_lower for word in ["chest pain", "chest discomfort"]):
        return "⚠️ Chest pain can be serious. If you're experiencing chest pain, especially with shortness of breath, seek immediate medical attention. Call emergency services if needed."
    
    elif any(word in user_input_lower for word in ["cough", "cold", "flu"]):
        return "Rest, stay hydrated, and consider over-the-counter remedies for symptom relief. If symptoms are severe or persist, consult a healthcare provider."
    
    elif any(word in user_input_lower for word in ["exercise", "workout", "fitness"]):
        return "Regular exercise (150 minutes/week of moderate activity) benefits physical and mental health. Start gradually and consult your doctor if you have health concerns."
    
    elif any(word in user_input_lower for word in ["diet", "nutrition", "food", "eating"]):
        return "A balanced diet with fruits, vegetables, lean proteins, and whole grains supports good health. Consider consulting a nutritionist for personalized advice."
    
    elif any(word in user_input_lower for word in ["sleep", "insomnia", "tired"]):
        return "Good sleep hygiene includes a regular schedule, dark/quiet environment, and avoiding screens before bed. Adults need 7-9 hours of sleep per night."
    
    elif any(word in user_input_lower for word in ["stress", "anxiety", "mental health"]):
        return "Mental health is important. Consider stress management techniques like deep breathing, meditation, or talking to a counselor. Seek professional help if needed."
    
    elif any(word in user_input_lower for word in ["medication", "medicine", "pill"]):
        return "Always take medications as prescribed by your doctor. Don't stop or change doses without consulting your healthcare provider."
    
    elif any(word in user_input_lower for word in ["appointment", "doctor", "clinic"]):
        return "I can't schedule appointments, but I can provide general health information. Contact your healthcare provider directly for appointments."
    
    elif any(word in user_input_lower for word in ["symptom", "pain", "hurt", "ache"]):
        return "I can provide general information about symptoms, but for specific medical advice, please consult a healthcare professional."
    
    else:
        # Try to use AI model if available, otherwise provide a general response
        if chatbot:
            try:
                response = chatbot(user_input, max_length=200, num_return_sequences=1, do_sample=True, temperature=0.7)
                return response[0]['generated_text']
            except Exception as e:
                return f"I understand you're asking about '{user_input}'. This is a general health question. For specific medical advice, please consult a healthcare professional."
        else:
            return f"I understand you're asking about '{user_input}'. This is a general health question. For specific medical advice, please consult a healthcare professional."

# Streamlit web app interface
def main():
    # Set up the web app title and input area
    st.title("🩺 Healthcare Assistant Chatbot")
    st.markdown("**Disclaimer:** This is for informational purposes only and is not a substitute for professional medical advice.")
    
    # Display a simple text input for user queries
    user_input = st.text_input("How can I assist you today?", placeholder="e.g., I have a headache")
    
    # Display chatbot response
    if st.button("Submit", type="primary"):
        if user_input:
            with st.spinner("🤖 Thinking..."):
                response = healthcare_chatbot(user_input)
            
            st.write("**User:**", user_input)
            st.write("**Healthcare Assistant:**", response)
        else:
            st.warning("Please enter a query.")

if __name__ == "__main__":
    main()
