"""
Input validation utilities for candidate information.
"""
import re
from typing import Tuple


def validate_email(email: str) -> Tuple[bool, str]:
    """
    Validate email address format.
    
    Args:
        email: Email address to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not email:
        return False, "Email address is required."
    
    # Basic email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if re.match(pattern, email.strip()):
        return True, ""
    else:
        return False, "Please provide a valid email address (e.g., name@example.com)."


def validate_phone(phone: str) -> Tuple[bool, str]:
    """
    Validate phone number format.
    
    Args:
        phone: Phone number to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not phone:
        return False, "Phone number is required."
    
    # Remove common separators
    cleaned = re.sub(r'[\s\-\(\)\+]', '', phone)
    
    # Check if it contains only digits and is of reasonable length
    if cleaned.isdigit() and 10 <= len(cleaned) <= 15:
        return True, ""
    else:
        return False, "Please provide a valid phone number (10-15 digits)."


def validate_experience(experience: str) -> Tuple[bool, str]:
    """
    Validate years of experience.
    
    Args:
        experience: Years of experience string
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not experience:
        return False, "Years of experience is required."
    
    try:
        years = float(experience)
        if 0 <= years <= 50:
            return True, ""
        else:
            return False, "Please provide a valid number of years (0-50)."
    except ValueError:
        return False, "Please provide a valid number for years of experience."


def validate_name(name: str) -> Tuple[bool, str]:
    """
    Validate candidate name.
    
    Args:
        name: Candidate name to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not name or len(name.strip()) < 2:
        return False, "Please provide your full name (at least 2 characters)."
    
    return True, ""


def validate_non_empty(value: str, field_name: str) -> Tuple[bool, str]:
    """
    Validate that a field is not empty.
    
    Args:
        value: Value to validate
        field_name: Name of the field for error message
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not value or len(value.strip()) == 0:
        return False, f"{field_name} is required."
    
    return True, ""
