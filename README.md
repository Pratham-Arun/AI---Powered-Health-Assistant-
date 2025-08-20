# AI-Powered Health Assistant

A comprehensive health assistant chatbot built with Streamlit and AI models, providing general health information and guidance while maintaining safety-first principles.

## Problem Statement
- Many people seek quick, reliable health information and basic triage guidance, but medical advice online is inconsistent and unsafe. There is a need for an easy, accessible assistant that offers general health information, symptom guidance, and next-step suggestions while avoiding medical claims.
- Users often struggle to find trustworthy health information quickly
- Need for immediate health guidance without replacing professional medical care
- Lack of accessible, user-friendly health information platforms

## How the Prototype Solves It
- Provides a simple chat interface where users ask health-related questions and receive informative, safety-first responses.
- Combines basic healthcare keyword guidance with a lightweight language model to keep answers general and non-diagnostic.
- Clear medical disclaimer and prompts to consult professionals for urgent or serious issues.
- Instant access to health information without registration or complex setup
- User-friendly interface that works on any device with a web browser

## Features

### Core Features
- 🤖 **AI-Powered Chat**: Intelligent responses using Hugging Face's DistilGPT2 model
- 💬 **Natural Conversation**: Human-like interaction with health-related queries
- 📚 **Health Knowledge Base**: Comprehensive coverage of common health topics
- ⚡ **Instant Responses**: Real-time health information and guidance
- 🛡️ **Safety First**: Built-in medical disclaimers and emergency guidance

### Health Topics Covered
- 🩺 **Symptoms & Conditions**: Headaches, fever, pain, COVID-19, etc.
- 💊 **Medications & Treatments**: General medication guidance and safety
- 🏃‍♂️ **Exercise & Fitness**: Physical activity recommendations
- 🥗 **Diet & Nutrition**: Healthy eating and lifestyle advice
- 😴 **Sleep & Rest**: Sleep hygiene and rest recommendations
- 😰 **Stress & Mental Health**: Mental wellness and stress management
- 🏥 **Preventive Care**: Regular check-ups and health maintenance
- 🚨 **Emergency Situations**: When to seek immediate medical care

## Current Progress Status

### ✅ Completed
- Working demo (`app.py`) — Basic Streamlit chatbot with rule-based hints + text generation
- Core AI integration with Hugging Face Transformers
- Medical disclaimer and safety warnings
- Responsive web interface
- Health keyword detection and responses

### 🔄 In Progress
- Advanced UI enhancements (`streamlit_app.py`)
- User authentication system
- Chat history persistence
- Theme customization options

### 📋 Pending Work
- Backend API for advanced features (auth, chat history endpoints)
- Enhanced safety guardrails (stricter disclaimers, emergency detection)
- Expanded medical domains and multilingual support
- Mobile app version
- Integration with medical databases
- Voice interaction capabilities

## Technologies / Tools Used

### Frontend
- **Streamlit**: Web application framework for rapid prototyping
- **HTML/CSS**: Custom styling and responsive design
- **JavaScript**: Interactive elements and animations

### Backend & AI
- **Python 3.8+**: Core programming language
- **Hugging Face Transformers**: DistilGPT2 model for text generation
- **NLTK**: Natural language processing and tokenization
- **PyTorch**: Deep learning framework (via transformers)

### Development Tools
- **Git**: Version control
- **Pip**: Package management
- **Virtual Environment**: Isolated Python environment

### Optional Dependencies (for advanced features)
- **FastAPI**: Backend API framework
- **Uvicorn**: ASGI server
- **Requests**: HTTP library for API calls
- **Python-dotenv**: Environment variable management

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git (for cloning the repository)

### Step-by-Step Installation

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd AI---Powered-Health-Assistant-
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   # Basic version (recommended)
   python -m streamlit run app.py
   
   # Advanced version (requires backend)
   python -m streamlit run streamlit_app.py
   ```

5. **Access the Application**
   - Open your browser and go to: `http://localhost:8501`
   - The application will be ready to use immediately

## Usage Examples

### Basic Health Queries
```
User: "I have a headache"
Assistant: "Headaches can have various causes. Consider factors like stress, 
dehydration, or eye strain. If severe or persistent, please see a doctor."

User: "What should I do about fever?"
Assistant: "Fever is often a sign of infection. Monitor your temperature and 
rest. Seek medical attention if fever is high (>103°F/39.4°C) or persistent."
```

### Lifestyle Questions
```
User: "How much exercise should I get?"
Assistant: "Regular exercise (150 minutes/week of moderate activity) benefits 
physical and mental health. Start gradually and consult your doctor if you 
have health concerns."

User: "What's a healthy diet?"
Assistant: "A balanced diet with fruits, vegetables, lean proteins, and whole 
grains supports good health. Consider consulting a nutritionist for 
personalized advice."
```

### Emergency Guidance
```
User: "I'm having chest pain"
Assistant: "Chest pain can be serious. If you're experiencing chest pain, 
especially with other symptoms like shortness of breath, seek immediate 
medical attention. Call emergency services if needed."
```

## Project Structure

```
AI---Powered-Health-Assistant-/
├── app.py                    # Main Streamlit application (basic version)
├── streamlit_app.py          # Advanced Streamlit application
├── requirements.txt          # Python dependencies
├── gitignore.txt            # Git ignore rules
├── README.md                # Project documentation
└── screenshots/             # Application screenshots
    ├── home.png             # Home screen
    ├── chat.png             # Chat interface
    └── disclaimer.png       # Medical disclaimer
```

## Configuration

### Environment Variables
Create a `.env` file (optional) for advanced features:
```env
API_BASE_URL=http://localhost:8000
HUGGINGFACE_API_TOKEN=your_token_here
```

### Customization Options
- Modify health responses in the `health_keywords` dictionary
- Adjust AI model parameters in the `load_ai_model()` function
- Customize UI styling in the CSS sections
- Add new health topics and keywords

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Kill existing processes on port 8501
   netstat -ano | findstr :8501
   taskkill /PID <PID> /F
   ```

2. **Model Download Fails**
   - Check internet connection
   - The app will continue with rule-based responses
   - Try running with `--no-cache` flag

3. **Import Errors**
   ```bash
   # Reinstall dependencies
   pip install -r requirements.txt --force-reinstall
   ```

4. **Memory Issues**
   - Close other applications
   - Use the basic version (`app.py`) for lower memory usage
   - Consider using a smaller AI model

### Performance Optimization
- Use SSD storage for faster model loading
- Ensure adequate RAM (4GB+ recommended)
- Close unnecessary browser tabs
- Use a modern web browser

## Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Code Style
- Follow PEP 8 guidelines
- Add docstrings to functions
- Include type hints where appropriate
- Write clear commit messages

## Screenshots

### Home Screen
![Home](screenshots/home.png)
*Main interface with chat input and health assistant*

### Chat Interface
![Chat](screenshots/chat.png)
*Interactive conversation with health queries and responses*

### Medical Disclaimer
![Disclaimer](screenshots/disclaimer.png)
*Safety-first approach with clear medical disclaimers*

## Future Enhancements

### Planned Features
- 🔐 **User Authentication**: Secure login and user profiles
- 📊 **Health Analytics**: Track health queries and trends
- 🌐 **Multi-language Support**: International health guidance
- 📱 **Mobile App**: Native iOS and Android applications
- 🎤 **Voice Interface**: Speech-to-text and text-to-speech
- 🔗 **Medical Database Integration**: Connect with reliable health sources

### Advanced AI Features
- 🤖 **Enhanced NLP**: Better understanding of complex health queries
- 📈 **Personalization**: Tailored health recommendations
- 🔍 **Symptom Analysis**: More detailed symptom assessment
- 📋 **Health Tracking**: Monitor health metrics over time

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

### Getting Help
- Check the troubleshooting section above
- Review the project documentation
- Create an issue on the repository
- Contact the development team

### Reporting Issues
When reporting issues, please include:
- Operating system and version
- Python version
- Error messages and stack traces
- Steps to reproduce the problem

## Notes

⚠️ **Important Medical Disclaimer**: This AI assistant provides general health information only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare professionals for medical concerns.

- This assistant is for informational purposes only and does not provide medical advice
- Always consult qualified healthcare professionals for diagnosis or treatment
- In case of emergency, call emergency services immediately
- The information provided may not be complete or up-to-date
- Individual health needs vary and require personalized medical attention

---

**Made with ❤️ for better healthcare accessibility** 
