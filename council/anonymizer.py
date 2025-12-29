import random
import string
from typing import List, Dict

class Anonymizer:
    """Handles anonymization of opinions to prevent bias"""
    
    def __init__(self):
        self.used_ids = set()
    
    def generate_anonymous_id(self) -> str:
        """Generate a unique anonymous identifier"""
        while True:
            # Generate a random ID like "Member-A7B2"
            prefix = random.choice(["Member", "Councilor", "Delegate"])
            suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
            anonymous_id = f"{prefix}-{suffix}"
            
            if anonymous_id not in self.used_ids:
                self.used_ids.add(anonymous_id)
                return anonymous_id
    
    def anonymize_opinions(self, opinions: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Anonymize opinions by replacing model names with random IDs
        Returns shuffled list of opinions with anonymous IDs
        """
        anonymized = []
        
        for opinion in opinions:
            anonymous_id = self.generate_anonymous_id()
            anonymized.append({
                "id": anonymous_id,
                "content": opinion["content"],
                "original_model": opinion["model"]  # Keep for internal tracking only
            })
        
        # Shuffle to further anonymize
        random.shuffle(anonymized)
        return anonymized
    
    def reset(self):
        """Reset used IDs for a new session"""
        self.used_ids.clear()

