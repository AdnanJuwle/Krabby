from typing import List, Dict, Any
from .models import BaseModel, create_model
from .anonymizer import Anonymizer
from .voting import VotingSystem
from .utils.logging import get_logger
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import time

logger = get_logger("council")

class Council:
    """Main council class that orchestrates the parliamentary process"""
    
    def __init__(self, model_configs: List[Dict[str, Any]], discussion_rounds: int = 2):
        self.models = []
        failed_models = []
        
        for config in model_configs:
            try:
                model = create_model(config)
                self.models.append(model)
                logger.info(f"✓ {config['name']} ({config['provider']}) initialized")
            except Exception as e:
                failed_models.append((config.get('name', 'unknown'), str(e)))
                logger.warning(f"✗ {config.get('name', 'unknown')} failed: {e}")
        
        if not self.models:
            error_msg = "No models were successfully initialized! Please check your API keys and Ollama connection."
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        if failed_models:
            logger.warning(f"{len(failed_models)} model(s) failed to initialize and were skipped")
        
        self.discussion_rounds = discussion_rounds
        self.anonymizer = Anonymizer()
        self.voting_system = VotingSystem()
        logger.info(f"Council initialized with {len(self.models)} active model(s)")
    
    def _get_initial_opinions(self, input_text: str) -> List[Dict[str, str]]:
        """Step 1: Get initial opinions from all models - PARALLEL"""
        system_prompt = """You are a member of a council. Provide your thoughtful opinion on the given input.
Be concise but comprehensive. Your response will be shared anonymously with other council members."""
        
        opinions = []
        opinions_lock = threading.Lock()
        
        def get_opinion(model):
            """Get opinion from a single model"""
            prompt = f"Please provide your opinion on the following:\n\n{input_text}"
            try:
                logger.debug(f"Getting opinion from {model.name}...")
                response = model.generate(prompt, system_prompt)
                if response and response.strip():
                    with opinions_lock:
                        opinions.append({
                            "model": model.name,
                            "content": response
                        })
                    logger.info(f"✓ {model.name} opinion completed")
                else:
                    logger.warning(f"⚠️  {model.name} returned empty response")
            except Exception as e:
                logger.warning(f"⚠️  Skipping {model.name}: {str(e)}")
        
        # Run all models in parallel
        logger.info(f"🚀 Starting {len(self.models)} models in parallel...")
        with ThreadPoolExecutor(max_workers=len(self.models)) as executor:
            futures = [executor.submit(get_opinion, model) for model in self.models]
            # Wait for all to complete
            for future in as_completed(futures):
                try:
                    future.result()  # This will raise exception if model failed
                except Exception as e:
                    pass  # Already handled in get_opinion
        
        if not opinions:
            error_msg = "No models were able to generate opinions. Please check your API keys and Ollama connection."
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        logger.info(f"✅ Collected {len(opinions)} opinions")
        return opinions
    
    def _discuss_opinions(self, input_text: str, 
                         anonymized_opinions: List[Dict[str, str]], 
                         round_num: int) -> List[Dict[str, str]]:
        """Step 2: Models discuss the anonymized opinions - PARALLEL"""
        system_prompt = """You are a member of a council. You are reviewing anonymous opinions from other council members.
Analyze each opinion critically. Provide your thoughts on which opinions are most valuable and why.
Remember: You don't know which opinion came from which model - they are all anonymous."""
        
        opinions_text = "\n\n".join([
            f"Opinion {i+1} (ID: {op['id']}):\n{op['content']}"
            for i, op in enumerate(anonymized_opinions)
        ])
        
        discussion_prompt = f"""Original Input:
{input_text}

Anonymous Opinions from Council Members:
{opinions_text}

Please provide your analysis of these opinions. Which ones do you find most compelling and why?"""
        
        discussions = []
        discussions_lock = threading.Lock()
        
        def get_discussion(model):
            """Get discussion from a single model"""
            try:
                logger.debug(f"Discussion from {model.name} (round {round_num})...")
                response = model.generate(discussion_prompt, system_prompt)
                if response and response.strip():
                    with discussions_lock:
                        discussions.append({
                            "model": model.name,
                            "content": response,
                            "round": round_num
                        })
                    logger.info(f"✓ {model.name} discussion completed")
                else:
                    logger.warning(f"⚠️  {model.name} returned empty discussion")
            except Exception as e:
                logger.warning(f"⚠️  Skipping discussion from {model.name}: {str(e)}")
        
        # Run all models in parallel
        logger.info(f"🚀 Starting {len(self.models)} models in parallel for discussion...")
        with ThreadPoolExecutor(max_workers=len(self.models)) as executor:
            futures = [executor.submit(get_discussion, model) for model in self.models]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    pass  # Already handled in get_discussion
        
        logger.info(f"✅ Collected {len(discussions)} discussions")
        return discussions
    
    def _vote_on_opinions(self, input_text: str, 
                         anonymized_opinions: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Step 3: Models vote on which opinion is best - PARALLEL"""
        system_prompt = """You are a member of a council. You must vote on which anonymous opinion best addresses the original input.
You can only vote for ONE opinion. Provide the ID of the opinion you choose."""
        
        opinions_text = "\n\n".join([
            f"Opinion ID: {op['id']}\nContent: {op['content']}"
            for op in anonymized_opinions
        ])
        
        voting_prompt = f"""Original Input:
{input_text}

Anonymous Opinions to Vote On:
{opinions_text}

Please vote by providing ONLY the Opinion ID (e.g., "Member-A7B2") that you think best addresses the original input.
Your response should be in the format: "I vote for [Opinion ID]" or just "[Opinion ID]"."""
        
        votes = []
        votes_lock = threading.Lock()
        
        def get_vote(model):
            """Get vote from a single model"""
            try:
                logger.debug(f"Getting vote from {model.name}...")
                response = model.generate(voting_prompt, system_prompt)
                if response and response.strip():
                    chosen_id = self._extract_opinion_id(response, anonymized_opinions)
                    if chosen_id:
                        with votes_lock:
                            votes.append({
                                "model": model.name,
                                "vote_response": response,
                                "chosen_id": chosen_id
                            })
                        logger.info(f"✓ {model.name} voted for {chosen_id}")
                    else:
                        logger.warning(f"⚠️  Could not extract vote from {model.name}")
                else:
                    logger.warning(f"⚠️  {model.name} returned empty vote")
            except Exception as e:
                logger.warning(f"⚠️  Skipping vote from {model.name}: {str(e)}")
        
        # Run all models in parallel
        logger.info(f"🚀 Starting {len(self.models)} models in parallel for voting...")
        with ThreadPoolExecutor(max_workers=len(self.models)) as executor:
            futures = [executor.submit(get_vote, model) for model in self.models]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    pass  # Already handled in get_vote
        
        if not votes:
            error_msg = "No models were able to vote. Please check your API keys and model connections."
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        logger.info(f"✅ Collected {len(votes)} votes")
        return votes
    
    def _extract_opinion_id(self, vote_response: str, 
                           opinions: List[Dict[str, str]]) -> str:
        """Extract the opinion ID from a vote response"""
        available_ids = [op["id"] for op in opinions]
        
        for op_id in available_ids:
            if op_id in vote_response:
                return op_id
        
        import re
        pattern = r'(Member|Councilor|Delegate)-[A-Z0-9]{4}'
        matches = re.findall(pattern, vote_response)
        if matches:
            for op_id in available_ids:
                if any(match in op_id for match in matches):
                    return op_id
        
        return available_ids[0] if available_ids else None
    
    def deliberate(self, input_text: str) -> Dict[str, Any]:
        """Main method: Run the full parliamentary process"""
        self.anonymizer.reset()
        
        logger.info("Step 1: Gathering initial opinions from all models...")
        initial_opinions = self._get_initial_opinions(input_text)
        anonymized_opinions = self.anonymizer.anonymize_opinions(initial_opinions)
        
        all_discussions = []
        for round_num in range(1, self.discussion_rounds + 1):
            logger.info(f"Step 2.{round_num}: Discussion round {round_num}...")
            discussions = self._discuss_opinions(input_text, anonymized_opinions, round_num)
            all_discussions.extend(discussions)
        
        logger.info("Step 3: Models are voting...")
        votes = self._vote_on_opinions(input_text, anonymized_opinions)
        
        logger.info("Step 4: Counting votes...")
        vote_counts = self.voting_system.count_votes(votes)
        results = self.voting_system.format_voting_results(vote_counts, anonymized_opinions)
        
        logger.info("Deliberation completed successfully")
        
        return {
            "input": input_text,
            "initial_opinions": initial_opinions,
            "anonymized_opinions": anonymized_opinions,
            "discussions": all_discussions,
            "votes": votes,
            "results": results,
            "final_output": results["winner_content"]
        }

