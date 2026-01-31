import streamlit as st
import traceback

try:
    from medical_engine import engine
except Exception as e:
    st.error(f"Error loading Medical Engine: {e}")
    st.code(traceback.format_exc())
    st.stop()

# Set page config
st.set_page_config(page_title="Health Assistant", page_icon="🩺", layout="wide")

# Apply Theme / CSS
def apply_custom_css(theme):
    if theme == "🌙 Dark Mode":
        st.markdown("""
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
                html, body, [data-testid="stAppViewContainer"] {
                    font-family: 'Inter', sans-serif;
                    background-color: #0f172a !important;
                    color: #f8fafc !important;
                }
                .stChatMessage {
                    background-color: #1e293b !important;
                    border: 1px solid #334155 !important;
                    border-radius: 12px !important;
                    padding: 15px !important;
                    margin-bottom: 10px !important;
                }
                .stTextInput>div>div>input {
                    background-color: #1e293b !important;
                    color: white !important;
                    border: 1px solid #475569 !important;
                    border-radius: 10px;
                }
                .stButton>button {
                    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
                    color: white !important;
                    border: none !important;
                    border-radius: 8px !important;
                    font-weight: 600 !important;
                }
                [data-testid="stSidebar"] {
                    background-color: #0f172a !important;
                    border-right: 1px solid #1e293b !important;
                }
            </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
                html, body, [data-testid="stAppViewContainer"] {
                    font-family: 'Inter', sans-serif;
                    background-color: #f1f5f9 !important;
                    color: #1e293b !important;
                }
                .stChatMessage {
                    background-color: #ffffff !important;
                    border: 1px solid #e2e8f0 !important;
                    border-radius: 12px !important;
                    padding: 15px !important;
                    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
                    color: #1e293b !important;
                }
                /* Target all text inside chat messages */
                .stChatMessage p, .stChatMessage div, .stChatMessage span {
                    color: #1e293b !important;
                }
                .stTextInput>div>div>input {
                    background-color: #ffffff !important;
                    color: #1e293b !important;
                    border: 1px solid #cbd5e1 !important;
                    border-radius: 10px;
                }
                .stButton>button {
                    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
                    color: white !important;
                    border: none !important;
                    border-radius: 8px !important;
                    font-weight: 600 !important;
                }
                [data-testid="stSidebar"] {
                    background-color: #ffffff !important;
                    border-right: 1px solid #e2e8f0 !important;
                }
                [data-testid="stSidebar"] * {
                    color: #1e293b !important;
                }
            </style>
        """, unsafe_allow_html=True)

# Initialize session states
if "messages" not in st.session_state:
    st.session_state.messages = []
if "theme" not in st.session_state:
    st.session_state.theme = "🌙 Dark Mode"
if "language" not in st.session_state:
    st.session_state.language = "en" # Internal tracking for last detected lang
if "med_checklist" not in st.session_state:
    st.session_state.med_checklist = []

# Sidebar
with st.sidebar:
    st.title("🩺 Health Assistant")
    
    # Theme Selection
    st.session_state.theme = st.radio("Appearance", ["🌞 Light Mode", "🌙 Dark Mode"], index=1 if st.session_state.theme == "🌙 Dark Mode" else 0)
    apply_custom_css(st.session_state.theme)
    
    st.divider()
    
    st.subheader("🚀 Quick Examples")
    examples = ["Fatigue & Blood Loss", "सिरदर्द से राहत", "Need Blood Test info"]
    
    for ex in examples:
        if st.button(ex):
            st.session_state.quick_query = ex

    st.divider()
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Main Application Interface
st.markdown("<h1 style='text-align: center;'>🩺 Your Personal Health Assistant</h1>", unsafe_allow_html=True)

# Tabs for different features
tab_chat, tab_tools = st.tabs(["💬 Chat", "📊 Health Tools"])

with tab_chat:
    st.markdown("<p style='text-align: center; opacity: 0.8;'>Detailed health insights and guidance at your fingertips.</p>", unsafe_allow_html=True)

    # Disclaimer
    with st.expander("⚠️ Medical Disclaimer", expanded=False):
        st.warning("This tool provides educational information only and is NOT a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or qualified health provider.")

    # Display Chat History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Input
    query = st.chat_input("💬 Ask me something about your health...")

    # Handle Quick Example button clicks
    if hasattr(st.session_state, 'quick_query'):
        query = st.session_state.quick_query
        del st.session_state.quick_query

    if query:
        st.session_state.messages.append({"role": "user", "content": query})
        with st.chat_message("user"):
            st.markdown(query)

        with st.spinner("🤖 Consulting medical knowledge base..."):
            try:
                # Automatically detect and use language
                bot_response = engine.process_query(query)
                st.session_state.messages.append({"role": "assistant", "content": bot_response})
                with st.chat_message("assistant"):
                    st.markdown(bot_response)
            except Exception as e:
                st.error(f"⚠️ I encountered an error: {e}")

        st.rerun()

    # --- PDF Export Section ---
    st.divider()
    if st.session_state.messages:
        if st.button("📄 Download My Health Report"):
            with st.spinner("Generating PDF Report..."):
                try:
                    pdf_bytes = engine.generate_health_report(
                        st.session_state.messages,
                        bmi=st.session_state.get("last_bmi"),
                        water_intake=st.session_state.get("water_intake", 0),
                        water_goal=st.session_state.get("water_goal", 2500)
                    )
                    st.download_button(
                        label="Click Here to Download PDF",
                        data=pdf_bytes,
                        file_name=f"Health_Report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        mime="application/pdf"
                    )
                except Exception as e:
                    st.error(f"Error generating PDF: {e}")

        st.rerun()

if "water_goal" not in st.session_state:
    st.session_state.water_goal = 2500  # ml
if "water_intake" not in st.session_state:
    st.session_state.water_intake = 0
if "water_intake" not in st.session_state:
    st.session_state.water_intake = 0

with tab_tools:
    st.header("📊 Health Tracking Tools")
    tool_choice = st.selectbox("Select Tool", ["BMI Calculator", "Water Tracker", "Medicine Checklist"])
    
    if tool_choice == "BMI Calculator":
        col1, col2 = st.columns(2)
        with col1:
            weight = st.number_input("Weight (kg)", min_value=1.0, max_value=300.0, value=70.0)
            height = st.number_input("Height (cm)", min_value=50.0, max_value=250.0, value=170.0)
            if st.button("Calculate BMI"):
                bmi = weight / ((height/100)**2)
                st.session_state.last_bmi = bmi
        
        if "last_bmi" in st.session_state:
            bmi = st.session_state.last_bmi
            st.metric("Your BMI", f"{bmi:.1f}")
            if bmi < 18.5: st.warning("Status: Underweight. You may need a more nutrient-dense diet.")
            elif 18.5 <= bmi < 25: st.success("Status: Healthy Weight. Keep it up!")
            elif 25 <= bmi < 30: st.warning("Status: Overweight. Consider checking your daily activity levels.")
            else: st.error("Status: Obese. It's recommended to consult a healthcare provider for a plan.")

    elif tool_choice == "Water Tracker":
        st.subheader("💧 Daily Water Tracker")
        goal = st.number_input("Goal (ml)", min_value=1000, max_value=10000, value=st.session_state.get("water_goal", 2500))
        st.session_state.water_goal = goal
        
        progress = st.session_state.water_intake / st.session_state.water_goal
        st.progress(min(progress, 1.0))
        st.write(f"Intake: **{st.session_state.water_intake} ml** / {st.session_state.water_goal} ml")
        
        cols = st.columns(3)
        if cols[0].button("➕ 250ml (Cup)"):
            st.session_state.water_intake += 250
            st.rerun()
        if cols[1].button("➕ 500ml (Bottle)"):
            st.session_state.water_intake += 500
            st.rerun()
        if cols[2].button("🔄 Reset"):
            st.session_state.water_intake = 0
            st.rerun()

    elif tool_choice == "Medicine Checklist":
        st.subheader("💊 Daily Medicine Checklist")
        st.write("Track the medicines you've taken today.")
        
        with st.form("med_checklist_form", clear_on_submit=True):
            col1, col2 = st.columns([3, 1])
            new_med = col1.text_input("Add Medicine (e.g., Paracetamol 500mg)")
            if col2.form_submit_button("➕ Add"):
                if new_med:
                    st.session_state.med_checklist.append({"name": new_med, "taken": False})
                    st.rerun()
        
        if st.session_state.med_checklist:
            st.divider()
            for i, med in enumerate(st.session_state.med_checklist):
                cols = st.columns([4, 1, 1])
                # Checkbox for taken status
                is_taken = cols[1].checkbox("Taken", value=med["taken"], key=f"taken_{i}")
                if is_taken != med["taken"]:
                    st.session_state.med_checklist[i]["taken"] = is_taken
                    st.rerun()
                
                # Strike-through if taken
                med_text = f"~~{med['name']}~~" if med["taken"] else med["name"]
                cols[0].markdown(f"**{med_text}**")
                
                # Delete button
                if cols[2].button("🗑️", key=f"del_{i}"):
                    st.session_state.med_checklist.pop(i)
                    st.rerun()
            
            if st.button("🔄 Reset All for New Day"):
                for med in st.session_state.med_checklist:
                    med["taken"] = False
                st.rerun()
        else:
            st.info("No medicines added yet. Use the form above to start your list.")
