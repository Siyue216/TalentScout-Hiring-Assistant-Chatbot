"""
Prompt templates for Gemini AI chatbot interactions.
"""

# System instruction for the Gemini model
SYSTEM_INSTRUCTION = """You are a professional Hiring Assistant chatbot for TalentScout, a technology recruitment agency. Your role is to conduct initial candidate screening interviews and make intelligent screening decisions.

Your responsibilities:
1. Greet candidates warmly and professionally
2. Collect essential candidate information (name, email, phone, experience, position, location, tech stack)
3. Generate relevant technical questions dynamically based on their declared tech stack and experience level
4. Evaluate candidate answers and assign quality scores (1-10)
5. Make final screening decisions (SCREEN IN or SCREEN OUT) based on overall performance
6. Maintain a professional, friendly, and encouraging tone throughout
7. Stay focused on the hiring/screening purpose - do not deviate to unrelated topics
8. Provide clear instructions and acknowledge candidate responses

Important guidelines:
- Be concise and clear in your responses
- Ask one question at a time
- Acknowledge the candidate's input before moving to the next question
- Evaluate answers objectively based on technical accuracy and relevance
- Be fair in your screening decisions - consider experience level and potential
- If the candidate provides incomplete information, politely ask for clarification
- If the candidate tries to go off-topic, politely redirect them back to the screening process
- Be encouraging and professional at all times, even when delivering a SCREEN OUT decision

Remember: You are conducting a professional interview and making important screening decisions. Keep responses brief, focused, and fair."""


def get_greeting_prompt() -> str:
    """Get the initial greeting prompt."""
    return """Greet the candidate warmly and introduce yourself as TalentScout's Hiring Assistant. 
Briefly explain that you'll be conducting an initial screening by:
1. Gathering some basic information
2. Asking a few technical questions based on their skills

Keep it brief, professional, and welcoming. Then ask for their full name."""


def get_info_collection_prompt(field_name: str, previous_response: str = "") -> str:
    """
    Get prompt for collecting specific information.
    
    Args:
        field_name: The field being collected (email, phone, etc.)
        previous_response: The candidate's previous response
        
    Returns:
        Appropriate prompt for collecting the information
    """
    prompts = {
        "email": f"Thank you{', ' + previous_response.split()[0] if previous_response else ''}! Could you please provide your email address?",
        "phone": "Great! What's the best phone number to reach you?",
        "experience": "Excellent! How many years of professional experience do you have in the tech industry?",
        "position": "Thank you! What position(s) are you interested in applying for?",
        "location": "Perfect! What is your current location (city/region)?",
        "tech_stack": "Now, please tell me about your tech stack. What programming languages, frameworks, databases, and tools are you proficient in?"
    }
    
    return prompts.get(field_name, f"Please provide your {field_name}.")


def get_ai_question_generation_prompt(tech_stack: str, experience_years: float, num_questions: int) -> str:
    """
    Get prompt for AI to generate technical questions based on tech stack.
    
    Args:
        tech_stack: The candidate's declared tech stack
        experience_years: Years of experience
        num_questions: Number of questions to generate
        
    Returns:
        Prompt for AI question generation
    """
    difficulty = "intermediate"
    if experience_years < 2:
        difficulty = "junior-level (basic concepts and fundamentals)"
    elif experience_years > 5:
        difficulty = "senior-level (advanced concepts, architecture, best practices)"
    
    return f"""Based on the candidate's tech stack: "{tech_stack}" and {experience_years} years of experience, generate exactly {num_questions} technical interview questions.

Requirements:
1. Questions should be {difficulty}
2. Cover different technologies mentioned in their tech stack
3. Questions should be practical and assess real-world knowledge
4. Include a mix of conceptual and practical questions
5. Each question should be clear and specific

Format your response as a numbered list with ONLY the questions, one per line. Example:
1. [First question here]
2. [Second question here]
etc.

Generate {num_questions} questions now:"""


def get_answer_evaluation_prompt(question: str, answer: str, tech_stack: str) -> str:
    """
    Get prompt for AI to evaluate a candidate's answer.
    
    Args:
        question: The technical question asked
        answer: The candidate's answer
        tech_stack: The candidate's tech stack
        
    Returns:
        Prompt for AI answer evaluation
    """
    return f"""You are evaluating a technical interview answer. 

Question: {question}

Candidate's Tech Stack: {tech_stack}

Candidate's Answer: {answer}

Evaluate this answer and provide:
1. A brief acknowledgment (1 sentence, professional and encouraging)
2. A quality score from 1-10
3. Key strengths (if any)
4. Areas for improvement (if any)

Keep the feedback professional and constructive. Format as:
ACKNOWLEDGMENT: [Your acknowledgment]
SCORE: [1-10]
STRENGTHS: [Brief points or "N/A"]
IMPROVEMENTS: [Brief points or "N/A"]"""


def get_screening_decision_prompt(candidate_data: dict, qa_list: list) -> str:
    """
    Get prompt for AI to make final screening decision.
    
    Args:
        candidate_data: Dictionary with candidate information
        qa_list: List of Q&A with evaluations
        
    Returns:
        Prompt for AI screening decision
    """
    # Build summary of performance
    tech_stack = candidate_data.get('tech_stack', 'N/A')
    experience = candidate_data.get('experience', 'N/A')
    position = candidate_data.get('position', 'N/A')
    
    qa_summary = ""
    for i, qa in enumerate(qa_list, 1):
        score = qa.get('score', 'N/A')
        qa_summary += f"\nQ{i}: {qa['question']}\n"
        qa_summary += f"Answer: {qa['answer'][:100]}...\n"  # Truncate long answers
        qa_summary += f"Score: {score}\n"
    
    return f"""You are conducting a technical screening for a candidate. Based on their performance, decide if they should be SCREENED IN (pass to HR for further evaluation) or SCREENED OUT (rejected).

**Candidate Information:**
- Position Applied: {position}
- Tech Stack: {tech_stack}
- Years of Experience: {experience}

**Technical Assessment Performance:**
{qa_summary}

**Decision Criteria:**
- SCREEN IN: Candidate shows good understanding of technologies, scores mostly 6+ or demonstrates potential
- SCREEN OUT: Candidate shows poor understanding, scores mostly below 5, or completely irrelevant answers

**Your Decision:**
Provide your decision in this EXACT format:
DECISION: [SCREEN IN or SCREEN OUT]
REASONING: [Brief 1-2 sentence explanation]
MESSAGE: [A professional message to the candidate - encouraging if SCREEN IN, polite but clear if SCREEN OUT]"""


def get_technical_question_intro(tech_stack: str) -> str:
    """
    Get introduction before asking technical questions.
    
    Args:
        tech_stack: The candidate's declared tech stack
        
    Returns:
        Introduction prompt
    """
    return f"""Great! Thank you for sharing your information. 

Based on your tech stack ({tech_stack}) and experience level, I'm now going to ask you some tailored technical questions to assess your expertise. These questions are specifically designed for your background.

Please answer to the best of your ability. Let me prepare your first question..."""


def get_technical_question_prompt(question: str, technology: str, question_number: int, total_questions: int) -> str:
    """
    Format a technical question.
    
    Args:
        question: The technical question
        technology: The technology being tested
        question_number: Current question number
        total_questions: Total number of questions
        
    Returns:
        Formatted question prompt
    """
    return f"""**Question {question_number} of {total_questions}** ({technology}):

{question}"""


def get_question_acknowledgment(remaining: int) -> str:
    """
    Get acknowledgment after a question is answered.
    
    Args:
        remaining: Number of remaining questions
        
    Returns:
        Acknowledgment message
    """
    if remaining > 0:
        return f"Thank you for your answer! Let's move to the next question."
    else:
        return "Thank you for your thoughtful answers!"


def get_conclusion_prompt(candidate_name: str, decision: str, message: str) -> str:
    """
    Get conclusion message based on screening decision.
    
    Args:
        candidate_name: Candidate's name
        decision: SCREEN IN or SCREEN OUT
        message: Custom message from AI
        
    Returns:
        Final conclusion message
    """
    if "SCREEN IN" in decision.upper():
        return f"""🎉 **Congratulations, {candidate_name}!**

{message}

Our HR team will review your profile and contact you within 2-3 business days to schedule the next round of interviews.

Thank you for your time and thoughtful responses. We're excited about the possibility of having you join our team!

**What happens next:**
✅ HR team reviews your screening results
✅ You'll receive an email/call for the next interview round
✅ Keep an eye on your inbox!

Good luck! 🚀"""
    else:
        return f"""Thank you, {candidate_name}.

{message}

We appreciate the time you took to complete this screening. While you haven't met the criteria for this particular role at this time, we encourage you to:
- Continue building your skills
- Apply for other positions that match your experience
- Reapply in the future as you gain more experience

We wish you all the best in your job search!

**The conversation has ended.** You may close this window."""


def get_fallback_prompt() -> str:
    """Get fallback prompt when input is unclear."""
    return """I didn't quite understand that. Could you please rephrase or provide the requested information? 
I'm here to help you through the screening process."""


def get_off_topic_redirect() -> str:
    """Get prompt to redirect off-topic conversations."""
    return """I appreciate your interest, but I'm specifically designed to help with the initial candidate screening process. 
Let's continue with the interview questions. """


def get_exit_confirmation() -> str:
    """Get confirmation message when user wants to exit."""
    return """I understand you'd like to end the session. Thank you for your time! 
If you'd like to complete the screening process later, feel free to start a new conversation. 
Have a great day!"""
