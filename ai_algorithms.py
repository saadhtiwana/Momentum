"""
MOMENTUM - AI-Powered Habit & Life Coach
AI Algorithms Module

This module implements core classical AI algorithms:
1. A* Search - for optimal goal path planning
2. Expert System - rule-based inference with forward chaining
3. NLP Engine - tokenization, sentiment analysis, intent classification, TF-IDF
4. Decision Tree - for personalized habit recommendations
5. CSP Solver - constraint satisfaction for optimal scheduling
6. Best-First Search - for habit optimization

All algorithms are implemented from scratch to demonstrate AI techniques.
"""

import heapq
import re
import math
from collections import Counter, defaultdict
from datetime import datetime
from typing import List, Dict, Tuple, Optional, Any
from config import (
    EXPERT_RULES, DECISION_TREE, GOAL_GRAPH, GOAL_HEURISTICS,
    TIME_SLOTS, HABIT_REQUIREMENTS, SENTIMENT_KEYWORDS, INTENT_KEYWORDS
)


# ============================================================================
# A* SEARCH ALGORITHM - Goal Path Planning
# ============================================================================

class AStarGoalPlanner:
    """
    Implements A* search algorithm for finding optimal path to goal achievement.
    
    A* uses f(n) = g(n) + h(n) where:
    - g(n) = actual cost from start to node n
    - h(n) = heuristic estimate from n to goal
    - f(n) = total estimated cost
    
    Priority queue ensures we expand lowest f(n) first.
    """
    
    def __init__(self, goal_graph: Dict = None, heuristics: Dict = None):
        """Initialize A* planner with goal graph and heuristic values."""
        self.graph = goal_graph or GOAL_GRAPH
        self.heuristics = heuristics or GOAL_HEURISTICS
    
    def heuristic(self, node: str, goal: str) -> float:
        """
        Heuristic function: estimated cost from node to goal.
        Uses predefined effort estimates in days.
        """
        if node == goal:
            return 0
        return self.heuristics.get(node, 10)  # Default 10 days if unknown
    
    def get_neighbors(self, node: str) -> List[Tuple[str, float]]:
        """Get neighboring nodes with edge costs."""
        neighbors = self.graph.get(node, {})
        return [(neighbor, cost) for neighbor, cost in neighbors.items()]
    
    def reconstruct_path(self, came_from: Dict, current: str) -> List[str]:
        """Reconstruct path from start to goal."""
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path
    
    def search(self, start: str = "start", goal: str = "master_habit") -> Dict[str, Any]:
        """
        Execute A* search to find optimal path from start to goal.
        
        Returns:
            Dictionary with path, total_cost, nodes_explored, and success status
        """
        # Priority queue: (f_score, counter, node)
        # Counter prevents comparison issues with nodes
        counter = 0
        frontier = [(0, counter, start)]
        counter += 1
        
        came_from = {}  # Reconstruction path
        g_score = {start: 0}  # Cost from start to node
        f_score = {start: self.heuristic(start, goal)}  # Total estimated cost
        
        explored = set()
        
        while frontier:
            current_f, _, current = heapq.heappop(frontier)
            
            # Goal reached!
            if current == goal:
                path = self.reconstruct_path(came_from, current)
                return {
                    "success": True,
                    "path": path,
                    "total_cost": g_score[current],
                    "nodes_explored": len(explored),
                    "message": f"Optimal path found! Estimated {g_score[current]} days to mastery."
                }
            
            explored.add(current)
            
            # Explore neighbors
            for neighbor, cost in self.get_neighbors(current):
                tentative_g = g_score[current] + cost
                
                # Found better path to neighbor
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + self.heuristic(neighbor, goal)
                    
                    if neighbor not in explored:
                        heapq.heappush(frontier, (f_score[neighbor], counter, neighbor))
                        counter += 1
        
        # No path found
        return {
            "success": False,
            "path": [],
            "total_cost": float('inf'),
            "nodes_explored": len(explored),
            "message": "No path found to goal."
        }


# ============================================================================
# EXPERT SYSTEM - Rule-Based Inference Engine
# ============================================================================

class ExpertSystem:
    """
    Rule-based expert system using forward chaining inference.
    
    Evaluates production rules (IF-THEN) against user data to provide
    expert advice with confidence scores.
    """
    
    def __init__(self, rules: List[Dict] = None):
        """Initialize expert system with knowledge base rules."""
        self.rules = rules or EXPERT_RULES
    
    def evaluate_rule(self, rule: Dict, user_data: Dict) -> Optional[Dict]:
        """
        Evaluate a single rule against user data.
        
        Args:
            rule: Production rule with condition and conclusion
            user_data: Current user statistics and state
            
        Returns:
            Fired rule with conclusion and confidence, or None
        """
        try:
            # Check if rule condition is satisfied
            if rule["condition"](user_data):
                return {
                    "rule_id": rule["id"],
                    "conclusion": rule["conclusion"],
                    "confidence": rule["confidence"],
                    "category": rule["category"]
                }
        except Exception as e:
            # Rule evaluation error (missing data, etc.)
            pass
        
        return None
    
    def forward_chain(self, user_data: Dict, limit: int = 5) -> List[Dict]:
        """
        Forward chaining inference: evaluate all rules and return fired ones.
        
        Args:
            user_data: User statistics and current state
            limit: Maximum number of rules to return
            
        Returns:
            List of fired rules sorted by confidence
        """
        fired_rules = []
        
        for rule in self.rules:
            result = self.evaluate_rule(rule, user_data)
            if result:
                fired_rules.append(result)
        
        # Sort by confidence (highest first) and limit results
        fired_rules.sort(key=lambda x: x["confidence"], reverse=True)
        return fired_rules[:limit]
    
    def get_advice(self, user_data: Dict) -> str:
        """
        Get top advice from expert system.
        
        Args:
            user_data: User statistics
            
        Returns:
            Expert advice string
        """
        fired_rules = self.forward_chain(user_data, limit=1)
        
        if fired_rules:
            top_rule = fired_rules[0]
            return f"{top_rule['conclusion']} (Confidence: {top_rule['confidence']:.0%})"
        
        return "Keep going! Consistency is the key to success. 🚀"


# ============================================================================
# NLP ENGINE - Natural Language Processing
# ============================================================================

class NLPEngine:
    """
    Natural Language Processing engine for user message analysis.
    
    Implements:
    - Tokenization (split, lowercase, remove punctuation)
    - Sentiment analysis (positive/negative/neutral)
    - Intent classification (motivation, advice, progress, etc.)
    - TF-IDF calculation for document importance
    """
    
    def __init__(self):
        """Initialize NLP engine with keyword dictionaries."""
        self.sentiment_keywords = SENTIMENT_KEYWORDS
        self.intent_keywords = INTENT_KEYWORDS
    
    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize text: lowercase, split, remove punctuation.
        
        Args:
            text: Raw input text
            
        Returns:
            List of cleaned tokens
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove punctuation (except apostrophes in contractions)
        text = re.sub(r'[^\w\s\']', ' ', text)
        
        # Split into tokens
        tokens = text.split()
        
        # Remove extra whitespace
        tokens = [t.strip() for t in tokens if t.strip()]
        
        return tokens
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment of text using keyword matching.
        
        Args:
            text: Input text
            
        Returns:
            Dictionary with sentiment label and scores
        """
        tokens = self.tokenize(text)
        
        # Count sentiment keywords
        positive_count = sum(1 for token in tokens if token in self.sentiment_keywords["positive"])
        negative_count = sum(1 for token in tokens if token in self.sentiment_keywords["negative"])
        neutral_count = sum(1 for token in tokens if token in self.sentiment_keywords["neutral"])
        
        total = positive_count + negative_count + neutral_count
        
        if total == 0:
            return {
                "sentiment": "neutral",
                "confidence": 0.5,
                "scores": {"positive": 0.33, "negative": 0.33, "neutral": 0.34}
            }
        
        # Calculate sentiment scores
        scores = {
            "positive": positive_count / total if total > 0 else 0,
            "negative": negative_count / total if total > 0 else 0,
            "neutral": neutral_count / total if total > 0 else 0
        }
        
        # Determine dominant sentiment
        if positive_count > negative_count and positive_count > neutral_count:
            sentiment = "positive"
            confidence = scores["positive"]
        elif negative_count > positive_count and negative_count > neutral_count:
            sentiment = "negative"
            confidence = scores["negative"]
        else:
            sentiment = "neutral"
            confidence = scores["neutral"]
        
        return {
            "sentiment": sentiment,
            "confidence": confidence,
            "scores": scores
        }
    
    def classify_intent(self, text: str) -> Dict[str, Any]:
        """
        Classify user intent from text.
        
        Intents: motivation, advice, progress, struggling, question, general
        
        Args:
            text: Input text
            
        Returns:
            Dictionary with intent label and confidence
        """
        tokens = self.tokenize(text)
        
        # Count intent keywords
        intent_scores = {}
        for intent, keywords in self.intent_keywords.items():
            count = sum(1 for token in tokens if token in keywords)
            intent_scores[intent] = count
        
        # Determine dominant intent
        if sum(intent_scores.values()) == 0:
            return {
                "intent": "general",
                "confidence": 0.5,
                "scores": intent_scores
            }
        
        max_intent = max(intent_scores, key=intent_scores.get)
        max_score = intent_scores[max_intent]
        total_score = sum(intent_scores.values())
        
        return {
            "intent": max_intent,
            "confidence": max_score / total_score if total_score > 0 else 0,
            "scores": intent_scores
        }
    
    def calculate_tfidf(self, documents: List[str]) -> Dict[str, Dict[str, float]]:
        """
        Calculate TF-IDF (Term Frequency-Inverse Document Frequency) scores.
        
        TF-IDF measures importance of words in documents.
        - TF: frequency of term in document
        - IDF: log(total docs / docs containing term)
        - TF-IDF: TF * IDF
        
        Args:
            documents: List of text documents
            
        Returns:
            Dictionary mapping doc_id to term TF-IDF scores
        """
        if not documents:
            return {}
        
        # Tokenize all documents
        tokenized_docs = [self.tokenize(doc) for doc in documents]
        
        # Calculate term frequency (TF) for each document
        tf_scores = []
        for tokens in tokenized_docs:
            term_count = Counter(tokens)
            total_terms = len(tokens)
            tf = {term: count / total_terms for term, count in term_count.items()}
            tf_scores.append(tf)
        
        # Calculate document frequency (DF) and inverse document frequency (IDF)
        df = defaultdict(int)
        for tokens in tokenized_docs:
            unique_terms = set(tokens)
            for term in unique_terms:
                df[term] += 1
        
        num_docs = len(documents)
        idf = {term: math.log(num_docs / doc_freq) for term, doc_freq in df.items()}
        
        # Calculate TF-IDF
        tfidf_scores = {}
        for i, tf in enumerate(tf_scores):
            tfidf_scores[f"doc_{i}"] = {
                term: tf_value * idf.get(term, 0)
                for term, tf_value in tf.items()
            }
        
        return tfidf_scores
    
    def analyze_message(self, text: str) -> Dict[str, Any]:
        """
        Complete NLP analysis of user message.
        
        Args:
            text: User message
            
        Returns:
            Analysis with tokens, sentiment, and intent
        """
        tokens = self.tokenize(text)
        sentiment = self.analyze_sentiment(text)
        intent = self.classify_intent(text)
        
        return {
            "original_text": text,
            "tokens": tokens,
            "sentiment": sentiment,
            "intent": intent,
            "analysis_timestamp": datetime.now().isoformat()
        }


# ============================================================================
# DECISION TREE - Habit Recommendation System
# ============================================================================

class DecisionTreeAdvisor:
    """
    Decision tree for personalized habit recommendations.
    
    Traverses tree based on user characteristics to provide
    tailored habit suggestions with explanations.
    """
    
    def __init__(self, tree: Dict = None):
        """Initialize decision tree with structure."""
        self.tree = tree or DECISION_TREE
    
    def traverse(self, node: Dict, user_input: Dict) -> Dict[str, Any]:
        """
        Recursively traverse decision tree based on user input.
        
        Args:
            node: Current tree node
            user_input: User's answers to questions
            
        Returns:
            Recommendation with explanation
        """
        # Leaf node - return recommendation
        if "recommendation" in node:
            return {
                "recommendation": node["recommendation"],
                "explanation": node["explanation"],
                "category": node.get("category", "general"),
                "difficulty": node.get("difficulty", "medium")
            }
        
        # Decision node - evaluate condition
        question_key = node["node_id"]
        user_answer = user_input.get(question_key)
        
        if user_answer is None:
            # No answer provided, return question
            return {
                "question": node["question"],
                "node_id": node["node_id"],
                "type": node["type"],
                "needs_input": True
            }
        
        # Threshold-based decision
        if node["type"] == "threshold":
            threshold = node["threshold"]
            branch_key = "less" if user_answer < threshold else "more"
            next_node = node["branches"][branch_key]
            return self.traverse(next_node, user_input)
        
        # Categorical decision
        elif node["type"] == "categorical":
            if user_answer in node["branches"]:
                next_node = node["branches"][user_answer]
                return self.traverse(next_node, user_input)
            else:
                return {
                    "error": f"Invalid answer '{user_answer}' for question",
                    "valid_options": list(node["branches"].keys())
                }
        
        return {"error": "Unknown node type"}
    
    def get_recommendation(self, user_profile: Dict) -> Dict[str, Any]:
        """
        Get habit recommendation based on user profile.
        
        Args:
            user_profile: User characteristics (goal, time, experience, etc.)
            
        Returns:
            Personalized recommendation
        """
        return self.traverse(self.tree, user_profile)


# ============================================================================
# CSP SOLVER - Constraint Satisfaction for Scheduling
# ============================================================================

class SchedulingCSP:
    """
    Constraint Satisfaction Problem solver for optimal habit scheduling.
    
    Finds best time slots for habits based on:
    - Energy level requirements
    - Distraction tolerance
    - Consistency factors
    """
    
    def __init__(self, time_slots: Dict = None, requirements: Dict = None):
        """Initialize CSP with time slots and habit requirements."""
        self.time_slots = time_slots or TIME_SLOTS
        self.requirements = requirements or HABIT_REQUIREMENTS
    
    def calculate_slot_score(self, slot_data: Dict, habit_type: str) -> float:
        """
        Calculate how well a time slot matches habit requirements.
        
        Score based on:
        - Energy level match
        - Distraction level match
        - Consistency bonus
        - Preferred time match
        
        Args:
            slot_data: Time slot characteristics
            habit_type: Type of habit (exercise, meditation, etc.)
            
        Returns:
            Score (0-100, higher is better)
        """
        reqs = self.requirements.get(habit_type, {})
        
        if not reqs:
            return 50  # Default medium score
        
        score = 0
        
        # Energy level match (+30 points max)
        min_energy = reqs.get("min_energy", 5)
        if slot_data["energy_level"] >= min_energy:
            score += 30 * (slot_data["energy_level"] / 10)
        
        # Distraction level match (+30 points max)
        max_distraction = reqs.get("max_distraction", 10)
        if slot_data["distraction_level"] <= max_distraction:
            score += 30 * (1 - slot_data["distraction_level"] / 10)
        
        # Consistency bonus (+20 points max)
        score += slot_data["consistency_bonus"] * 2
        
        # Preferred time bonus (+20 points)
        # Note: slot names need to match between TIME_SLOTS keys and preferred_times
        # This is a simplified check
        score += 20  # Simplified - could match against preferred_times
        
        return min(score, 100)
    
    def find_best_slot(self, habit_type: str) -> Dict[str, Any]:
        """
        Find optimal time slot for a habit type.
        
        Args:
            habit_type: Type of habit
            
        Returns:
            Best time slot with score and reasoning
        """
        best_slot = None
        best_score = -1
        all_scores = {}
        
        for slot_name, slot_data in self.time_slots.items():
            score = self.calculate_slot_score(slot_data, habit_type)
            all_scores[slot_name] = score
            
            if score > best_score:
                best_score = score
                best_slot = slot_name
        
        if best_slot:
            slot_data = self.time_slots[best_slot]
            return {
                "time_slot": best_slot,
                "slot_name": slot_data["name"],
                "score": best_score,
                "energy_level": slot_data["energy_level"],
                "distraction_level": slot_data["distraction_level"],
                "all_scores": all_scores,
                "reasoning": self._generate_reasoning(habit_type, best_slot, slot_data)
            }
        
        return {"error": "No suitable time slot found"}
    
    def _generate_reasoning(self, habit_type: str, slot: str, slot_data: Dict) -> str:
        """Generate human-readable reasoning for time slot recommendation."""
        reasons = []
        
        if slot_data["energy_level"] >= 8:
            reasons.append("high energy levels")
        
        if slot_data["distraction_level"] <= 3:
            reasons.append("minimal distractions")
        
        if slot_data["consistency_bonus"] >= 7:
            reasons.append("excellent for building consistency")
        
        if reasons:
            return f"Best for {habit_type}: {', '.join(reasons)}."
        
        return f"Good time for {habit_type}."
    
    def schedule_multiple_habits(self, habits: List[str]) -> Dict[str, str]:
        """
        Schedule multiple habits to optimal time slots.
        
        Args:
            habits: List of habit types
            
        Returns:
            Dictionary mapping habits to time slots
        """
        schedule = {}
        used_slots = set()
        
        # Sort habits by priority (could be enhanced)
        for habit in habits:
            result = self.find_best_slot(habit)
            if "time_slot" in result:
                time_slot = result["time_slot"]
                
                # Avoid double-booking (simplified - could allow multiple)
                if time_slot not in used_slots:
                    schedule[habit] = time_slot
                    used_slots.add(time_slot)
                else:
                    # Find next best slot
                    all_scores = result.get("all_scores", {})
                    sorted_slots = sorted(all_scores.items(), key=lambda x: x[1], reverse=True)
                    for slot, score in sorted_slots:
                        if slot not in used_slots:
                            schedule[habit] = slot
                            used_slots.add(slot)
                            break
        
        return schedule


# ============================================================================
# BEST-FIRST SEARCH - Habit Optimization
# ============================================================================

class HabitOptimizer:
    """
    Best-First Search for optimal habit selection and prioritization.
    
    Uses priority queue to select habits with highest success probability
    based on user history and characteristics.
    """
    
    def __init__(self):
        """Initialize habit optimizer."""
        pass
    
    def calculate_success_probability(self, habit: Dict, user_stats: Dict) -> float:
        """
        Calculate probability of habit success.
        
        Factors:
        - User's historical completion rate
        - Habit difficulty
        - Category match with user strengths
        - Time commitment feasibility
        
        Args:
            habit: Habit details
            user_stats: User statistics and history
            
        Returns:
            Success probability (0-1)
        """
        base_probability = 0.5
        
        # Historical success boosts confidence
        overall_rate = user_stats.get("overall_completion_rate", 0.5)
        base_probability += (overall_rate - 0.5) * 0.3
        
        # Difficulty adjustment
        difficulty = habit.get("difficulty", "medium")
        if difficulty == "easy":
            base_probability += 0.2
        elif difficulty == "hard":
            base_probability -= 0.15
        
        # Category strength
        category = habit.get("category", "")
        strong_categories = user_stats.get("strong_categories", [])
        if category in strong_categories:
            base_probability += 0.15
        
        # Time commitment
        required_time = habit.get("time_minutes", 30)
        available_time = user_stats.get("available_time", 60)
        if required_time <= available_time:
            base_probability += 0.1
        else:
            base_probability -= 0.2
        
        # Clamp to [0, 1]
        return max(0, min(1, base_probability))
    
    def optimize_habit_selection(self, candidate_habits: List[Dict], 
                                 user_stats: Dict, max_habits: int = 3) -> List[Dict]:
        """
        Select optimal habits using best-first search.
        
        Args:
            candidate_habits: List of potential habits
            user_stats: User statistics
            max_habits: Maximum habits to select
            
        Returns:
            Ordered list of recommended habits
        """
        # Priority queue: (negative probability for max-heap, habit)
        heap = []
        
        for habit in candidate_habits:
            probability = self.calculate_success_probability(habit, user_stats)
            # Negative for max-heap behavior
            heapq.heappush(heap, (-probability, habit))
        
        # Extract top habits
        selected = []
        for _ in range(min(max_habits, len(heap))):
            if heap:
                neg_prob, habit = heapq.heappop(heap)
                habit["success_probability"] = -neg_prob
                selected.append(habit)
        
        return selected


# ============================================================================
# MODULE EXPORTS
# ============================================================================

__all__ = [
    'AStarGoalPlanner',
    'ExpertSystem',
    'NLPEngine',
    'DecisionTreeAdvisor',
    'SchedulingCSP',
    'HabitOptimizer'
]
