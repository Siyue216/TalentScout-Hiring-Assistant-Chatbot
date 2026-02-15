"""
Data handling for candidate information storage and retrieval.
"""
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
from config import CANDIDATES_DIR


class CandidateDataHandler:
    """Handle storage and retrieval of candidate information."""
    
    def __init__(self):
        """Initialize the data handler."""
        self.candidates_dir = CANDIDATES_DIR
        
    def save_candidate(self, candidate_data: Dict[str, Any]) -> str:
        """
        Save candidate information to a JSON file.
        
        Args:
            candidate_data: Dictionary containing candidate information
            
        Returns:
            Path to the saved file
        """
        # Add timestamp
        candidate_data['submission_time'] = datetime.now().isoformat()
        
        # Generate filename from name and timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name_slug = candidate_data.get('name', 'unknown').lower().replace(' ', '_')
        filename = f"{name_slug}_{timestamp}.json"
        filepath = os.path.join(self.candidates_dir, filename)
        
        # Save to JSON file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(candidate_data, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    def load_candidate(self, filepath: str) -> Optional[Dict[str, Any]]:
        """
        Load candidate information from a JSON file.
        
        Args:
            filepath: Path to the JSON file
            
        Returns:
            Dictionary containing candidate data or None if file doesn't exist
        """
        if not os.path.exists(filepath):
            return None
        
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def get_all_candidates(self) -> list[Dict[str, Any]]:
        """
        Retrieve all candidate records.
        
        Returns:
            List of candidate data dictionaries
        """
        candidates = []
        
        for filename in os.listdir(self.candidates_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.candidates_dir, filename)
                candidate = self.load_candidate(filepath)
                if candidate:
                    candidates.append(candidate)
        
        return candidates
    
    def export_to_csv(self, output_path: str) -> None:
        """
        Export all candidate data to CSV format.
        
        Args:
            output_path: Path for the output CSV file
        """
        import csv
        
        candidates = self.get_all_candidates()
        
        if not candidates:
            return
        
        # Get all unique keys from all candidates
        all_keys = set()
        for candidate in candidates:
            all_keys.update(candidate.keys())
        
        fieldnames = sorted(all_keys)
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(candidates)


def create_candidate_record(
    name: str,
    email: str,
    phone: str,
    experience: str,
    position: str,
    location: str,
    tech_stack: str,
    technical_qa: list[Dict[str, str]] = None
) -> Dict[str, Any]:
    """
    Create a structured candidate record.
    
    Args:
        name: Candidate full name
        email: Email address
        phone: Phone number
        experience: Years of experience
        position: Desired position(s)
        location: Current location
        tech_stack: Declared tech stack
        technical_qa: List of technical questions and answers
        
    Returns:
        Structured candidate data dictionary
    """
    return {
        "name": name,
        "email": email,
        "phone": phone,
        "experience": experience,
        "position": position,
        "location": location,
        "tech_stack": tech_stack,
        "technical_qa": technical_qa or [],
        "status": "screened"
    }
