# 💼 TalentScout Hiring Assistant Chatbot

An intelligent AI-powered chatbot for conducting initial candidate screening interviews for technology positions. Built with Streamlit and Google's Gemini AI.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-red.svg)
![Gemini](https://img.shields.io/badge/Gemini-AI-orange.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Technical Details](#technical-details)
- [Prompt Engineering](#prompt-engineering)
- [Data Privacy](#data-privacy)
- [Challenges & Solutions](#challenges--solutions)
- [Future Enhancements](#future-enhancements)

## 🎯 Overview

TalentScout Hiring Assistant is an intelligent chatbot designed to streamline and automate the initial candidate screening process for technology recruitment. The chatbot:

- **Collects** essential candidate information (name, email, phone, experience, position, location, tech stack)
- **Generates** relevant technical questions dynamically using AI based on the candidate's tech stack and experience
- **Evaluates** answers intelligently with scoring (1-10) and constructive feedback
- **Decides** whether to SCREEN IN (pass to HR) or SCREEN OUT (reject) based on overall performance
- **Maintains** context-aware conversations with professional and encouraging tone
- **Stores** complete screening data including decisions and reasoning in JSON format

## ✨ Features

### Core Functionality
- ✅ **Interactive Chat Interface** - Clean Streamlit-based UI with improved visibility
- ✅ **Smart Information Collection** - Validates email, phone, experience, and other fields
- ✅ **AI-Powered Question Generation** - Gemini dynamically creates 5-7 questions based on tech stack and experience
- ✅ **Intelligent Answer Evaluation** - AI scores answers (1-10) and provides constructive feedback
- ✅ **Automated Screening Decision** - AI makes SCREEN IN/OUT decisions based on performance
- ✅ **Experience-Based Calibration** - Adjusts question difficulty (junior/mid/senior level)
- ✅ **Context Maintenance** - Keeps conversation coherent throughout the screening process
- ✅ **Exit Keyword Detection** - Recognizes when candidate wants to end the conversation
- ✅ **Comprehensive Data Storage** - Saves QA, scores, evaluations, and screening decisions

### User Experience
- 🎨 **Custom Styled UI** - Professional design with high-contrast chat bubbles
- 📱 **Responsive Design** - Works on desktop and mobile devices
- 💾 **Auto-Save** - Automatically saves candidate data with screening results
- 🔄 **Conversation Reset** - Easy restart for new screening sessions
- ℹ️ **Helpful Sidebar** - Process overview and tips for candidates
- 🎯 **Smart Validation** - AI validates tech stack responses for relevance

## 📁 Project Structure

```
assignment-PGAGI/
├── app.py                    # Main Streamlit application
├── chatbot.py                # Core chatbot logic with AI integration
├── prompts.py                # AI prompts for all interactions
├── data_handler.py           # Candidate data storage and retrieval
├── validators.py             # Input validation utilities
├── config.py                 # Configuration and constants
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (API keys)
├── .gitignore               # Git ignore rules
├── README.md                # This file
└── data/                    # Candidate data storage
    └── candidates/          # Individual candidate JSON files
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))
- pip (Python package manager)

### Step-by-Step Setup

1. **Clone or Download the Repository**
   ```bash
   cd d:\assignment-PGAGI
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**
   
   Create a `.env` file in the project root:
   ```bash
   copy .env.example .env
   ```
   
   Edit `.env` and add your Gemini API key:
   ```env
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   GEMINI_MODEL=gemini-pro
   MAX_TECHNICAL_QUESTIONS=5
   MIN_TECHNICAL_QUESTIONS=3
   ```

4. **Verify Installation**
   ```bash
   python -c "import streamlit; import google.generativeai; print('Setup successful!')"
   ```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Your Google Gemini API key | *Required* |
| `GEMINI_MODEL` | Gemini model to use | `gemini-pro` |
| `MAX_TECHNICAL_QUESTIONS` | Maximum technical questions | `5` |
| `MIN_TECHNICAL_QUESTIONS` | Minimum technical questions | `3` |

### Exit Keywords

The chatbot recognizes the following keywords to end conversations:
`exit`, `quit`, `bye`, `goodbye`, `stop`, `end`, `cancel`, `leave`, `close`, `terminate`

## 💻 Usage

### Running Locally

1. **Start the Application**
   ```bash
   streamlit run app.py
   ```

2. **Access the Interface**
   - The application will automatically open in your default browser
   - Default URL: `http://localhost:8501`

3. **Complete a Screening**
   - Chatbot will greet you and explain the process
   - Answer questions about your information
   - Declare your tech stack (e.g., "Python, Django, PostgreSQL, AWS")
   - Answer 3-5 technical questions
   - Receive confirmation and next steps

### Example Interaction

```
🤖 Assistant: Hello! I'm the TalentScout Hiring Assistant. I'll be conducting 
an initial screening by gathering some basic information and asking a few 
technical questions based on your skills. Let's get started! May I have your 
full name?

👤 You: John Doe

🤖 Assistant: Thank you, John! Could you please provide your email address?

👤 You: john.doe@example.com

🤖 Assistant: Great! What's the best phone number to reach you?

👤 You: 555-123-4567

... [continues through all information collection] ...

🤖 Assistant: Now, based on your tech stack (Python, Django, React), I'd like 
to ask you a few technical questions. Let's begin:

**Question 1 of 3** (Python):
Explain the difference between list and tuple in Python.

... [continues through technical questions] ...
```

## 🔧 Technical Details

### Architecture

The application follows a modular architecture with clear separation of concerns:

1. **Presentation Layer** (`app.py`)
   - Streamlit UI components
   - Session state management
   - User interaction handling

2. **Business Logic Layer** (`chatbot.py`)
   - Conversation state machine
   - Gemini AI integration
   - Flow control

3. **Data Layer** (`data_handler.py`, `validators.py`)
   - Data validation
   - JSON storage
   - Data retrieval

4. **Question Generation** (`question_generator.py`)
   - Tech stack parsing
   - Question template matching
   - Difficulty calibration

### Technologies Used

- **Frontend**: Streamlit 1.31.0
- **AI Model**: Google Gemini Pro (via `google-generativeai`)
- **Validation**: Pydantic 2.5.3
- **Environment**: python-dotenv 1.0.0
- **Data Storage**: JSON files
- **Language**: Python 3.8+

### Conversation State Machine

```
GREETING → COLLECT_NAME → COLLECT_EMAIL → COLLECT_PHONE → 
COLLECT_EXPERIENCE → COLLECT_POSITION → COLLECT_LOCATION → 
COLLECT_TECH_STACK → ASK_TECHNICAL_QUESTIONS → CONCLUSION → ENDED
```

Each state:
- Validates input before proceeding
- Provides appropriate error messages
- Maintains conversation context
- Handles edge cases

### Supported Technologies (Question Templates)

**Programming Languages**: Python, JavaScript, Java, C++

**Web Frameworks**: Django, Flask, React, Angular, Vue

**Databases**: SQL, MongoDB, PostgreSQL

**Cloud & DevOps**: AWS, Docker, Kubernetes

**ML/AI**: TensorFlow, PyTorch, Machine Learning

## 🎨 Prompt Engineering

### System Instruction

The chatbot uses a comprehensive system instruction that:
- Defines its role as a professional Hiring Assistant
- Sets clear behavioral guidelines (professional, friendly, encouraging)
- Establishes boundaries (stay on-topic, one question at a time)
- Ensures consistent tone throughout the conversation

### Prompt Design Strategies

1. **Role Definition**
   - Clear identity as TalentScout's Hiring Assistant
   - Professional yet approachable tone

2. **Contextual Prompts**
   - Different prompts for each conversation stage
   - Include candidate responses for personalization

3. **Structured Questions**
   - Technical questions formatted with technology and numbering
   - Clear expectations for answers

4. **Fallback Handling**
   - Graceful error messages
   - Redirection for off-topic responses

5. **Exit Management**
   - Keyword detection for early termination
   - Polite conclusion messages

### Example Prompts

**Greeting Prompt:**
```python
"Greet the candidate warmly and introduce yourself as TalentScout's 
Hiring Assistant. Briefly explain that you'll be conducting an initial 
screening by gathering basic information and asking technical questions."
```

**Question Format:**
```python
f"**Question {num} of {total}** ({technology}):
{question_text}"
```

## 🔒 Data Privacy

### GDPR Compliance Measures

- ✅ **Local Storage**: All data stored locally, not sent to external servers (except Gemini API)
- ✅ **No Database**: Uses file-based storage for easy data management and deletion
- ✅ **Timestamp Tracking**: All submissions timestamped for audit trails
- ✅ **Anonymization Ready**: Data structure supports easy anonymization
- ✅ **Data Export**: Built-in CSV export functionality for data portability

### Data Security Best Practices

1. **Environment Variables**: Sensitive API keys stored in `.env` (gitignored)
2. **Input Validation**: All user inputs validated before storage
3. **Structured Storage**: Consistent data format for integrity
4. **Access Control**: Data stored in protected directory

### What Data is Collected

- Name (required)
- Email address (validated)
- Phone number (validated)
- Years of experience (validated)
- Desired position(s)
- Current location
- Tech stack declaration
- Technical Q&A pairs (questions and answers)
- Submission timestamp

## 🚧 Challenges & Solutions

### Challenge 1: Dynamic Question Generation

**Problem**: Need to generate relevant questions for diverse tech stacks

**Solution**: 
- Created comprehensive question template library (20+ technologies)
- Implemented fuzzy matching for tech stack parsing
- Added experience-based difficulty calibration
- Fallback to generic questions when tech not recognized

### Challenge 2: Conversation State Management

**Problem**: Maintaining coherent multi-turn conversations with validation

**Solution**:
- Implemented state machine with clear states
- Validation at each step before state transition
- Error handling without losing conversation context
- Stored all data in session state for persistence

### Challenge 3: Input Validation

**Problem**: Ensuring data quality and proper formatting

**Solution**:
- Created dedicated validators module
- Regex-based validation for email and phone
- Helpful error messages guiding users
- Re-prompting on invalid input without losing context

### Challenge 4: API Key Security

**Problem**: Keeping API keys secure while making setup easy

**Solution**:
- Environment variable configuration
- `.env.example` template for easy setup
- Clear error messages when API key missing
- Gitignore to prevent accidental commits

## 🎯 Future Enhancements

### Planned Features

- [ ] **Sentiment Analysis** - Detect candidate emotions and adapt responses
- [ ] **Multilingual Support** - Support for Spanish, French, German, etc.
- [ ] **Advanced Analytics** - Dashboard for reviewing candidate responses
- [ ] **Email Integration** - Automated email sending to candidates
- [ ] **Calendar Integration** - Schedule follow-up interviews automatically
- [ ] **Resume Parsing** - Auto-fill information from uploaded resumes
- [ ] **Video Recording** - Optional video response capability
- [ ] **Custom Branding** - Configurable company branding and colors

### Cloud Deployment Options

**Streamlit Community Cloud** (Recommended)
```bash
# 1. Push to GitHub
# 2. Visit share.streamlit.io
# 3. Connect repository
# 4. Add GEMINI_API_KEY to secrets
# 5. Deploy!
```

**Google Cloud Platform**
```bash
gcloud app deploy
```

**AWS EC2**
```bash
# Deploy using Docker
docker build -t hiring-assistant .
docker run -p 8501:8501 hiring-assistant
```

## 📄 License

This project is created as part of an AI/ML internship assignment.

## 👨‍💻 Author

Created for TalentScout AI/ML Intern Assignment

---

## 🆘 Troubleshooting

### Common Issues

**Issue**: "GEMINI_API_KEY not found"
- **Solution**: Ensure `.env` file exists with correct API key

**Issue**: Dependencies not installing
- **Solution**: Update pip: `python -m pip install --upgrade pip`

**Issue**: Port 8501 already in use
- **Solution**: Use custom port: `streamlit run app.py --server.port 8502`

**Issue**: Streamlit not opening browser
- **Solution**: Manually navigate to `http://localhost:8501`

---

**For questions or issues, please refer to the documentation or contact the development team.**
