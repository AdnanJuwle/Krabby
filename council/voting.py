from typing import List, Dict
from collections import Counter

class VotingSystem:
    """Handles voting mechanism for the council"""
    
    @staticmethod
    def count_votes(votes: List[Dict[str, str]]) -> Dict[str, int]:
        """Count votes and return vote counts"""
        vote_counts = Counter()
        
        for vote in votes:
            # Extract the chosen opinion ID
            chosen_id = vote.get("chosen_id")
            if chosen_id:
                vote_counts[chosen_id] += 1
        
        return dict(vote_counts)
    
    @staticmethod
    def get_winner(vote_counts: Dict[str, int]) -> str:
        """Get the opinion ID with the most votes"""
        if not vote_counts:
            return None
        
        return max(vote_counts.items(), key=lambda x: x[1])[0]
    
    @staticmethod
    def format_voting_results(vote_counts: Dict[str, int], 
                            opinions: List[Dict[str, str]]) -> Dict:
        """Format voting results with full details"""
        winner_id = VotingSystem.get_winner(vote_counts)
        
        # Find the winning opinion
        winning_opinion = None
        for opinion in opinions:
            if opinion["id"] == winner_id:
                winning_opinion = opinion
                break
        
        return {
            "winner_id": winner_id,
            "winner_content": winning_opinion["content"] if winning_opinion else None,
            "vote_counts": vote_counts,
            "total_votes": sum(vote_counts.values()),
            "winning_votes": vote_counts.get(winner_id, 0) if winner_id else 0
        }

