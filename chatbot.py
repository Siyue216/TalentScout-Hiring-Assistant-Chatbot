"""
Core chatbot logic with conversation state management and Gemini AI integration.
"""
import google.generativeai as genai
from typing import Dict, Any, Optional, List
from config import (
    GEMINI_API_KEY, GEMINI_MODEL, ConversationState, 
    EXIT_KEYWORDS, MAX_TECHNICAL_QUESTIONS, MIN_TECHNICAL_QUESTIONS
)
from validators import (
    validate_email, validate_phone, validate_experience, 
    validate_name, validate_non_empty
)
import prompts


class HiringAssistantChatbot:
    """Main chatbot class handling conversation flow and AI interactions."""
    
    def __init__(self):
        """Initialize the chatbot with Gemini AI and state management."""
        # Configure Gemini
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found. Please set it in your .env file.")
        
        genai.configure(api_key=GEMINI_API_KEY)
        
        # Initialize the model with system instruction
        self.model = genai.GenerativeModel(
            model_name=GEMINI_MODEL,
            system_instruction=prompts.SYSTEM_INSTRUCTION
        )
        
        # Start chat session
        self.chat = self.model.start_chat(history=[])
        
        # Initialize state
        self.state = ConversationState.GREETING
        self.candidate_data = {}
        self.technical_questions = []
        self.current_question_index = 0
        
    def reset(self):
        """Reset the chatbot to initial state."""
        self.chat = self.model.start_chat(history=[])
        self.state = ConversationState.GREETING
        self.candidate_data = {}
        self.technical_questions = []
        self.current_question_index = 0
    
    def check_exit_intent(self, message: str) -> bool:
        """
        Check if the user wants to exit the conversation.
        
        Args:
            message: User's message
            
        Returns:
            True if exit intent detected
        """
        message_lower = message.lower().strip()
        return any(keyword in message_lower for keyword in EXIT_KEYWORDS)
    
    def get_greeting(self) -> str:
        """
        Get the initial greeting message.
        
        Returns:
            Greeting message from AI
        """
        response = self.chat.send_message(prompts.get_greeting_prompt())
        self.state = ConversationState.COLLECT_NAME
        return response.text
    
    def process_message(self, user_message: str) -> str:
        """
        Process user message and return chatbot response.
        
        Args:
            user_message: Message from the user
            
        Returns:
            Chatbot response
        """
        # Check for exit intent
        if self.check_exit_intent(user_message):
            self.state = ConversationState.ENDED
            return prompts.get_exit_confirmation()
        
        # Handle based on current state
        if self.state == ConversationState.GREETING:
            return self.get_greeting()
        
        elif self.state == ConversationState.COLLECT_NAME:
            return self._collect_name(user_message)
        
        elif self.state == ConversationState.COLLECT_EMAIL:
            return self._collect_email(user_message)
        
        elif self.state == ConversationState.COLLECT_PHONE:
            return self._collect_phone(user_message)
        
        elif self.state == ConversationState.COLLECT_EXPERIENCE:
            return self._collect_experience(user_message)
        
        elif self.state == ConversationState.COLLECT_POSITION:
            return self._collect_position(user_message)
        
        elif self.state == ConversationState.COLLECT_LOCATION:
            return self._collect_location(user_message)
        
        elif self.state == ConversationState.COLLECT_TECH_STACK:
            return self._collect_tech_stack(user_message)
        
        elif self.state == ConversationState.ASK_TECHNICAL_QUESTIONS:
            # First check if we need to show the first question
            if self.current_question_index == 0 and user_message.strip().lower() in ['ok', 'yes', 'ready', 'sure', 'continue', 'let\'s go', 'proceed']:
                # Show first question
                return self._show_current_question()
            else:
                return self._handle_technical_question(user_message)
        
        elif self.state == ConversationState.CONCLUSION:
            return self._conclude_conversation()
        
        elif self.state == ConversationState.ENDED:
            return "The conversation has ended. Please refresh to start a new screening session."
        
        return prompts.get_fallback_prompt()
    
    def _collect_name(self, name: str) -> str:
        """Collect and validate candidate name."""
        is_valid, error_msg = validate_name(name)
        
        if not is_valid:
            return error_msg
        
        self.candidate_data['name'] = name.strip()
        self.state = ConversationState.COLLECT_EMAIL
        return prompts.get_info_collection_prompt('email', name)
    
    def _collect_email(self, email: str) -> str:
        """Collect and validate email address."""
        is_valid, error_msg = validate_email(email)
        
        if not is_valid:
            return error_msg
        
        self.candidate_data['email'] = email.strip()
        self.state = ConversationState.COLLECT_PHONE
        return prompts.get_info_collection_prompt('phone')
    
    def _collect_phone(self, phone: str) -> str:
        """Collect and validate phone number."""
        is_valid, error_msg = validate_phone(phone)
        
        if not is_valid:
            return error_msg
        
        self.candidate_data['phone'] = phone.strip()
        self.state = ConversationState.COLLECT_EXPERIENCE
        return prompts.get_info_collection_prompt('experience')
    
    def _collect_experience(self, experience: str) -> str:
        """Collect and validate years of experience."""
        is_valid, error_msg = validate_experience(experience)
        
        if not is_valid:
            return error_msg
        
        self.candidate_data['experience'] = experience.strip()
        self.state = ConversationState.COLLECT_POSITION
        return prompts.get_info_collection_prompt('position')
    
    def _collect_position(self, position: str) -> str:
        """Collect desired position."""
        is_valid, error_msg = validate_non_empty(position, "Position")
        
        if not is_valid:
            return error_msg
        
        # Ensure meaningful input (at least 3 characters)
        if len(position.strip()) < 3:
            return "Please provide a valid position title (e.g., Software Engineer, Data Scientist, etc.)."
        
        self.candidate_data['position'] = position.strip()
        self.state = ConversationState.COLLECT_LOCATION
        return prompts.get_info_collection_prompt('location')
    
    def _collect_location(self, location: str) -> str:
        """Collect current location."""
        is_valid, error_msg = validate_non_empty(location, "Location")
        
        if not is_valid:
            return error_msg
        
        # Ensure meaningful input (at least 2 characters for city abbreviations)
        if len(location.strip()) < 2:
            return "Please provide a valid location (city, state, or country)."
        
        self.candidate_data['location'] = location.strip()
        self.state = ConversationState.COLLECT_TECH_STACK
        return prompts.get_info_collection_prompt('tech_stack')
    
    def _collect_tech_stack(self, tech_stack: str) -> str:
        """Collect tech stack and generate technical questions using AI."""
        # Basic validation
        is_valid, error_msg = validate_non_empty(tech_stack, "Tech stack")
        
        if not is_valid:
            return error_msg
        
        # Enhanced validation - ensure it's meaningful
        tech_stack_clean = tech_stack.strip()
        
        # Check minimum length (at least 3 characters)
        if len(tech_stack_clean) < 3:
            return "Please provide a valid tech stack with at least one technology (e.g., Python, JavaScript, React, etc.)."
        
        # Check if it looks like a tech stack (contains letters and possibly commas/spaces)
        if tech_stack_clean.isdigit() or len(tech_stack_clean.split()) == 0:
            return "Please provide a valid tech stack listing the technologies you work with (e.g., Python, Django, PostgreSQL)."
        
        # Check if response seems too short or invalid
        words = tech_stack_clean.replace(',', ' ').split()
        if len(words) == 1 and len(words[0]) <= 2:
            return "Please provide your complete tech stack. List the programming languages, frameworks, and tools you're proficient in."
        
        # Basic sanity check - ensure it contains some letters (not just numbers/symbols)
        if not any(c.isalpha() for c in tech_stack_clean):
            return "Please provide a valid tech stack (e.g., Python, JavaScript, React, AWS, etc.)."
        
        # Accept the tech stack - AI validation was too strict
        self.candidate_data['tech_stack'] = tech_stack_clean
        
        # Get experience years
        try:
            experience_years = float(self.candidate_data['experience'])
        except:
            experience_years = 0
        
        # Generate questions using AI (not templates!)
        num_questions = MAX_TECHNICAL_QUESTIONS  # Will generate 5-7 questions
        
        question_prompt = prompts.get_ai_question_generation_prompt(
            tech_stack, 
            experience_years, 
            num_questions
        )
        
        # Get AI-generated questions
        try:
            ai_response = self.chat.send_message(question_prompt)
            generated_text = ai_response.text
            
            # Parse the numbered questions
            questions_list = []
            for line in generated_text.split('\n'):
                line = line.strip()
                # Match numbered questions like "1." or "1)"
                if line and (line[0].isdigit() or line.startswith('-') or line.startswith('*')):
                    # Remove numbering and clean
                    question_text = line
                    # Remove leading numbers, dots, parentheses, bullets
                    import re
                    question_text = re.sub(r'^[\d\.\)\-\*\s]+', '', question_text).strip()
                    if question_text and len(question_text) > 10:  # Valid question
                        questions_list.append(question_text)
            
            # Ensure we have at least MIN_TECHNICAL_QUESTIONS
            if len(questions_list) < MIN_TECHNICAL_QUESTIONS:
                # Ask AI to generate more
                return "I'm having trouble generating enough questions. Could you please re-enter your tech stack with more details?"
            
            # Store as structured questions (take first num_questions)
            self.technical_questions = [
                {"technology": "AI-Generated", "question": q} 
                for q in questions_list[:num_questions]
            ]
            
        except Exception as e:
            # Fallback: use generic questions
            self.technical_questions = [
                {"technology": "General", "question": "Describe your most challenging technical project and how you solved it."},
                {"technology": "General", "question": "How do you approach learning new technologies?"},
                {"technology": "General", "question": "Explain your experience with the technologies in your tech stack."},
                {"technology": "General", "question": "How do you ensure code quality in your projects?"},
                {"technology": "General", "question": "Describe a time when you had to debug a complex issue."}
            ]
        
        # Initialize Q&A storage with evaluation scores
        self.candidate_data['technical_qa'] = []
        self.candidate_data['evaluation_scores'] = []
        
        self.state = ConversationState.ASK_TECHNICAL_QUESTIONS
        self.current_question_index = 0
        
        # Return introduction and ask user to proceed
        intro = prompts.get_technical_question_intro(tech_stack)
        
        return intro + "\n\n**Type 'ready' when you're ready for the first question.**"
    
    def _show_current_question(self) -> str:
        """Show the current technical question."""
        if self.current_question_index < len(self.technical_questions):
            current_q = self.technical_questions[self.current_question_index]
            return prompts.get_technical_question_prompt(
                current_q['question'],
                current_q['technology'],
                self.current_question_index + 1,
                len(self.technical_questions)
            )
        return "No more questions."
    
    def _handle_technical_question(self, answer: str) -> str:
        """Handle technical question answers with AI evaluation."""
        current_q = self.technical_questions[self.current_question_index]
        
        # Use AI to evaluate the answer
        evaluation_prompt = prompts.get_answer_evaluation_prompt(
            current_q['question'],
            answer,
            self.candidate_data['tech_stack']
        )
        
        try:
            eval_response = self.chat.send_message(evaluation_prompt)
            evaluation_text = eval_response.text
            
            # Parse evaluation (extract score if possible)
            score = "N/A"
            acknowledgment = "Thank you for your answer."
            
            for line in evaluation_text.split('\n'):
                if 'SCORE:' in line.upper():
                    score = line.split(':', 1)[1].strip()
                elif 'ACKNOWLEDGMENT:' in line.upper():
                    acknowledgment = line.split(':', 1)[1].strip()
            
            # Store the answer with evaluation
            self.candidate_data['technical_qa'].append({
                "technology": current_q['technology'],
                "question": current_q['question'],
                "answer": answer.strip(),
                "evaluation": evaluation_text,
                "score": score
            })
            
            # Move to next question
            self.current_question_index += 1
            
            # Check if more questions remain
            if self.current_question_index < len(self.technical_questions):
                next_question = self.technical_questions[self.current_question_index]
                
                question_prompt = prompts.get_technical_question_prompt(
                    next_question['question'],
                    next_question['technology'],
                    self.current_question_index + 1,
                    len(self.technical_questions)
                )
                
                # Return acknowledgment + next question
                return f"{acknowledgment}\n\n{question_prompt}"
            else:
                # All questions answered, show summary and conclude
                total_score = 0
                scored_count = 0
                
                for qa in self.candidate_data['technical_qa']:
                    try:
                        score_val = float(qa['score'].split('/')[0])
                        total_score += score_val
                        scored_count += 1
                    except:
                        pass
                
                avg_score = total_score / scored_count if scored_count > 0 else 0
                
                self.state = ConversationState.CONCLUSION
                
                summary = f"\n\n📊 **Interview Summary:**\n"
                summary += f"- Questions answered: {len(self.candidate_data['technical_qa'])}\n"
                if scored_count > 0:
                    summary += f"- Average score: {avg_score:.1f}/10\n"
                summary += "\n"
                
                return acknowledgment + summary + self._conclude_conversation()
                
        except Exception as e:
            # Fallback if AI evaluation fails
            self.candidate_data['technical_qa'].append({
                "technology": current_q['technology'],
                "question": current_q['question'],
                "answer": answer.strip()
            })
            
            self.current_question_index += 1
            
            if self.current_question_index < len(self.technical_questions):
                remaining = len(self.technical_questions) - self.current_question_index
                ack = prompts.get_question_acknowledgment(remaining)
                
                next_question = self.technical_questions[self.current_question_index]
                question_prompt = prompts.get_technical_question_prompt(
                    next_question['question'],
                    next_question['technology'],
                    self.current_question_index + 1,
                    len(self.technical_questions)
                )
                
                return f"{ack}\n\n{question_prompt}"
            else:
                self.state = ConversationState.CONCLUSION
                return self._conclude_conversation()
    
    def _conclude_conversation(self) -> str:
        """Conclude the conversation with AI screening decision."""
        candidate_name = self.candidate_data.get('name', 'there')
        
        # Get AI to make screening decision based on all answers
        try:
            decision_prompt = prompts.get_screening_decision_prompt(
                self.candidate_data,
                self.candidate_data.get('technical_qa', [])
            )
            
            decision_response = self.chat.send_message(decision_prompt)
            decision_text = decision_response.text
            
            # Parse the decision
            decision = "SCREEN OUT"  # Default
            reasoning = ""
            message = "Thank you for your time."
            
            for line in decision_text.split('\n'):
                line = line.strip()
                if 'DECISION:' in line.upper():
                    decision = line.split(':', 1)[1].strip()
                elif 'REASONING:' in line.upper():
                    reasoning = line.split(':', 1)[1].strip()
                elif 'MESSAGE:' in line.upper():
                    message = line.split(':', 1)[1].strip()
            
            # Store decision in candidate data
            self.candidate_data['screening_decision'] = decision
            self.candidate_data['screening_reasoning'] = reasoning
            
            # Get appropriate conclusion message
            conclusion = prompts.get_conclusion_prompt(candidate_name, decision, message)
            
            self.state = ConversationState.ENDED
            return conclusion
            
        except Exception as e:
            # Fallback if AI decision fails
            self.state = ConversationState.ENDED
            return f"""Thank you, {candidate_name}, for completing the screening!

Our HR team will review your responses and contact you if you're selected for the next round.

We appreciate your time and interest in our company. Good luck! 🤞"""
    
    def get_candidate_data(self) -> Dict[str, Any]:
        """
        Get collected candidate data.
        
        Returns:
            Dictionary with all candidate information
        """
        return self.candidate_data.copy()
    
    def is_conversation_complete(self) -> bool:
        """
        Check if the conversation is complete.
        
        Returns:
            True if conversation ended
        """
        return self.state == ConversationState.ENDED
