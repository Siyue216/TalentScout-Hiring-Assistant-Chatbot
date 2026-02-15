"""
TalentScout Hiring Assistant - Streamlit Application
Main entry point for the chatbot interface.
"""
import streamlit as st
from chatbot import HiringAssistantChatbot
from data_handler import CandidateDataHandler, create_candidate_record
from config import ConversationState
import os


# Page configuration
st.set_page_config(
    page_title="TalentScout Hiring Assistant",
    page_icon="💼",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better UI with high contrast
st.markdown("""
    <style>
    /* Main background */
    .main {
        background-color: #ffffff;
    }
    
    /* Chat messages - better contrast */
    [data-testid="stChatMessage"] {
        background-color: #f8f9fa !important;
        border: 1px solid #e9ecef !important;
        border-radius: 12px !important;
        padding: 16px !important;
        margin: 12px 0 !important;
    }
    
    /* User messages - blue background */
    [data-testid="stChatMessage"][data-testid*="user"] {
        background-color: #e3f2fd !important;
        border-left: 4px solid #2196F3 !important;
    }
    
    /* Assistant messages - green background */
    [data-testid="stChatMessage"]:not([data-testid*="user"]) {
        background-color: #f1f8f4 !important;
        border-left: 4px solid #4CAF50 !important;
    }
    
    /* Message text - ensure visibility */
    [data-testid="stChatMessage"] p {
        color: #212529 !important;
        font-size: 15px !important;
        line-height: 1.6 !important;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 12px 28px;
        border: none;
        font-weight: 600;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #45a049;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Headers */
    h1 {
        color: #1a1a1a;
        text-align: center;
        font-weight: 700;
    }
    
    .subtitle {
        text-align: center;
        color: #666;
        margin-bottom: 30px;
        font-size: 18px;
    }
    
    /* Chat input */
    [data-testid="stChatInput"] {
        border: 2px solid #4CAF50;
        border-radius: 8px;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
    }
    </style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'chatbot' not in st.session_state:
        try:
            st.session_state.chatbot = HiringAssistantChatbot()
        except ValueError as e:
            st.error(f"❌ Configuration Error: {str(e)}")
            st.info("Please create a `.env` file in the project root with your `GEMINI_API_KEY`.")
            st.stop()
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'conversation_started' not in st.session_state:
        st.session_state.conversation_started = False
    
    if 'data_saved' not in st.session_state:
        st.session_state.data_saved = False


def display_header():
    """Display the application header."""
    st.title("💼 TalentScout Hiring Assistant")
    st.markdown("<p class='subtitle'>AI-Powered Initial Candidate Screening</p>", unsafe_allow_html=True)
    st.markdown("---")


def start_conversation():
    """Start the conversation with greeting."""
    if not st.session_state.conversation_started:
        greeting = st.session_state.chatbot.get_greeting()
        st.session_state.messages.append({
            "role": "assistant",
            "content": greeting
        })
        st.session_state.conversation_started = True


def save_candidate_data():
    """Save candidate data to storage."""
    if not st.session_state.data_saved and st.session_state.chatbot.is_conversation_complete():
        data_handler = CandidateDataHandler()
        candidate_data = st.session_state.chatbot.get_candidate_data()
        
        if candidate_data and 'name' in candidate_data:
            # Create structured record
            record = create_candidate_record(
                name=candidate_data.get('name', ''),
                email=candidate_data.get('email', ''),
                phone=candidate_data.get('phone', ''),
                experience=candidate_data.get('experience', ''),
                position=candidate_data.get('position', ''),
                location=candidate_data.get('location', ''),
                tech_stack=candidate_data.get('tech_stack', ''),
                technical_qa=candidate_data.get('technical_qa', [])
            )
            
            # Save to file
            filepath = data_handler.save_candidate(record)
            st.session_state.data_saved = True
            
            return filepath
    
    return None


def reset_conversation():
    """Reset the conversation to start fresh."""
    st.session_state.chatbot.reset()
    st.session_state.messages = []
    st.session_state.conversation_started = False
    st.session_state.data_saved = False


def main():
    """Main application function."""
    # Initialize session state
    initialize_session_state()
    
    # Display header
    display_header()
    
    # Sidebar with information
    with st.sidebar:
        st.header("ℹ️ About")
        st.write("""
        This AI chatbot conducts initial candidate screening for technology positions.
        
        **Process:**
        1. Basic information collection
        2. Tech stack declaration
        3. Technical questions
        4. Completion & next steps
        
        **Tips:**
        - Provide complete information
        - Be specific about your tech stack
        - Answer technical questions thoughtfully
        - Type 'exit' anytime to end
        """)
        
        st.markdown("---")
        
        if st.button("🔄 Start New Screening"):
            reset_conversation()
            st.rerun()
        
        st.markdown("---")
        st.caption("Powered by Google Gemini AI")
    
    # Start conversation if not started
    if not st.session_state.conversation_started:
        start_conversation()
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Check if conversation is complete
    if st.session_state.chatbot.is_conversation_complete():
        # Save data if not already saved
        saved_path = save_candidate_data()
        
        if saved_path and st.session_state.data_saved:
            st.success("✅ Your information has been successfully recorded!")
            st.info("Thank you for completing the screening. Our team will be in touch soon!")
        
        # Offer to start new conversation
        if st.button("Start Another Screening"):
            reset_conversation()
            st.rerun()
        
        return
    
    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to chat
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get bot response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = st.session_state.chatbot.process_message(prompt)
                st.markdown(response)
        
        # Add assistant response to chat
        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })
        
        # Rerun to update the interface
        st.rerun()


if __name__ == "__main__":
    main()
