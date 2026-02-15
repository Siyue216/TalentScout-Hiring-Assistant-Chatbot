"""
Configuration settings for the Hiring Assistant Chatbot.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-pro")

# Question Generation Settings
MAX_TECHNICAL_QUESTIONS = int(os.getenv("MAX_TECHNICAL_QUESTIONS", "7"))
MIN_TECHNICAL_QUESTIONS = int(os.getenv("MIN_TECHNICAL_QUESTIONS", "5"))

# Conversation Exit Keywords
EXIT_KEYWORDS = [
    "exit", "quit", "bye", "goodbye", "stop", "end", 
    "cancel", "leave", "close", "terminate"
]

# Data Storage
DATA_DIR = "data"
CANDIDATES_DIR = os.path.join(DATA_DIR, "candidates")

# Conversation States
class ConversationState:
    GREETING = "greeting"
    COLLECT_NAME = "collect_name"
    COLLECT_EMAIL = "collect_email"
    COLLECT_PHONE = "collect_phone"
    COLLECT_EXPERIENCE = "collect_experience"
    COLLECT_POSITION = "collect_position"
    COLLECT_LOCATION = "collect_location"
    COLLECT_TECH_STACK = "collect_tech_stack"
    ASK_TECHNICAL_QUESTIONS = "ask_technical_questions"
    CONCLUSION = "conclusion"
    ENDED = "ended"

# Required Information Fields
REQUIRED_FIELDS = [
    "name", "email", "phone", "experience", 
    "position", "location", "tech_stack"
]

# Ensure data directories exist
os.makedirs(CANDIDATES_DIR, exist_ok=True)
