"""
MOMENTUM - AI-Powered Habit & Life Coach
AI Coach Module

This module orchestrates all AI components to provide personalized coaching:
- Integrates Expert System, A*, NLP, Decision Tree, CSP, and Best-First Search
- Generates daily greetings and motivational messages
- Provides personalized advice based on user data
- Plans goal achievement paths
- Optimizes habit selection
- Recommends optimal scheduling
- Analyzes user messages for sentiment and intent
- Optional Gemini API integration for natural conversation
"""

import random
from datetime import datetime
from typing import Dict, List, Any, Optional

from ai_algorithms import (
    AStarGoalPlanner,
    ExpertSystem,
    NLPEngine,
    DecisionTreeAdvisor,
    SchedulingCSP,
    HabitOptimizer
)
from advanced_ai import (
    QLearningOptimizer,
    BayesianPredictor,
    MonteCarloSimulator,
    GeneticScheduler,
    SimulatedAnnealing,
    MinimaxSelector
)
from config import MOTIVATIONAL_QUOTES



class AICoach:
    """
    Central AI coaching system that orchestrates all AI components.
    
    Provides high-level AI coaching features by combining:
    - Expert System for rule-based advice
    - A* Search for goal planning
    - NLP for message understanding
    - Decision Tree for personalized recommendations
    - CSP for optimal scheduling
    - Best-First Search for habit optimization
    """
    
    def __init__(self, use_gemini: bool = False, gemini_api_key: Optional[str] = None):
        """
        Initialize AI Coach with all AI components.
        
        Args:
            use_gemini: Whether to use Gemini API for enhanced chat
            gemini_api_key: Gemini API key (if using Gemini)
        """
        # Initialize all AI algorithms
        self.expert_system = ExpertSystem()
        self.goal_planner = AStarGoalPlanner()
        self.nlp_engine = NLPEngine()
        self.decision_tree = DecisionTreeAdvisor()
        self.scheduler = SchedulingCSP()
        self.optimizer = HabitOptimizer()
        
        # Initialize advanced AI algorithms
        self.q_learner = QLearningOptimizer()
        self.bayesian = BayesianPredictor()
        self.monte_carlo = MonteCarloSimulator()
        self.genetic = GeneticScheduler()
        self.annealing = SimulatedAnnealing()
        self.minimax = MinimaxSelector()
        
        # Gemini integration (optional)
        self.use_gemini = use_gemini
        self.gemini_api_key = gemini_api_key
        self.gemini_model = None
        
        if self.use_gemini and self.gemini_api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.gemini_api_key)
                
                # Try different model names and verify they work
                model_names = ['gemini-2.0-flash-exp', 'models/gemini-2.0-flash', 'gemini-pro']
                for model_name in model_names:
                    try:
                        test_model = genai.GenerativeModel(model_name)
                        # Test if model actually works
                        test_response = test_model.generate_content("Hi")
                        if test_response and test_response.text:
                            self.gemini_model = test_model
                            print(f"✅ Gemini AI enabled with model: {model_name}")
                            break
                    except Exception as e:
                        print(f"❌ Model {model_name} failed: {str(e)[:50]}")
                        continue
                else:
                    print("⚠️ Gemini unavailable - using rule-based AI")
                    self.use_gemini = False
                    
            except ImportError:
                print("Gemini API not available. Install: pip install google-generativeai")
                self.use_gemini = False
            except Exception as e:
                print(f"Error initializing Gemini: {e}")
                self.use_gemini = False
    
    def generate_daily_greeting(self, user_data: Dict[str, Any]) -> str:
        """
        Generate personalized daily greeting using expert system.
        
        Args:
            user_data: User statistics and current state
            
        Returns:
            Personalized greeting message
        """
        # Get time of day
        hour = datetime.now().hour
        
        if hour < 12:
            time_greeting = "Good morning"
        elif hour < 18:
            time_greeting = "Good afternoon"
        else:
            time_greeting = "Good evening"
        
        # Get expert system insights
        fired_rules = self.expert_system.forward_chain(user_data, limit=1)
        
        # Build greeting
        greeting_parts = [f"{time_greeting}! 🌟"]
        
        if fired_rules:
            top_rule = fired_rules[0]
            greeting_parts.append(top_rule["conclusion"])
        else:
            # Fallback motivational message
            quote = random.choice(MOTIVATIONAL_QUOTES)
            greeting_parts.append(f"💭 {quote}")
        
        return " ".join(greeting_parts)
    
    def get_personalized_advice(self, user_data: Dict[str, Any], 
                               context: str = "general") -> Dict[str, Any]:
        """
        Get personalized advice combining expert system and decision tree.
        
        Args:
            user_data: User statistics and preferences
            context: Context for advice (general, struggling, planning, etc.)
            
        Returns:
            Dictionary with advice, reasoning, and confidence
        """
        # Get expert system recommendations
        expert_advice = self.expert_system.forward_chain(user_data, limit=3)
        
        # Get decision tree recommendation if goal is specified
        tree_recommendation = None
        if "goal" in user_data:
            user_profile = {
                "root": user_data.get("goal", "health"),
                user_data.get("goal", "health") + "_node": user_data.get("time_available", 30),
                "health_high_time": user_data.get("experience", "beginner")
            }
            tree_recommendation = self.decision_tree.get_recommendation(user_profile)
        
        # Combine insights
        advice = {
            "expert_rules": expert_advice,
            "decision_tree": tree_recommendation,
            "primary_advice": expert_advice[0]["conclusion"] if expert_advice else "Stay consistent!",
            "confidence": expert_advice[0]["confidence"] if expert_advice else 0.5,
            "context": context
        }
        
        return advice
    
    def plan_goal(self, start: str = "start", goal: str = "master_habit") -> Dict[str, Any]:
        """
        Plan optimal path to goal achievement using A* search.
        
        Args:
            start: Starting node
            goal: Goal node
            
        Returns:
            A* search result with optimal path
        """
        result = self.goal_planner.search(start=start, goal=goal)
        
        # Add interpretable explanation
        if result["success"]:
            path_names = [step.replace("_", " ").title() for step in result["path"]]
            result["path_readable"] = path_names
            result["explanation"] = (
                f"Optimal path found in {result['nodes_explored']} explorations. "
                f"Follow {len(result['path'])} steps over approximately {result['total_cost']} days."
            )
        
        return result
    
    def optimize_habit_selection(self, candidate_habits: List[Dict], 
                                 user_stats: Dict, max_habits: int = 3) -> List[Dict]:
        """
        Optimize habit selection using best-first search.
        
        Args:
            candidate_habits: List of potential habits
            user_stats: User statistics and history
            max_habits: Maximum habits to recommend
            
        Returns:
            Ordered list of recommended habits with success probabilities
        """
        selected_habits = self.optimizer.optimize_habit_selection(
            candidate_habits, user_stats, max_habits
        )
        
        # Add explanations
        for habit in selected_habits:
            probability = habit.get("success_probability", 0.5)
            
            if probability >= 0.75:
                habit["recommendation_reason"] = "High success probability based on your history!"
            elif probability >= 0.5:
                habit["recommendation_reason"] = "Good match for your current level."
            else:
                habit["recommendation_reason"] = "Challenging but achievable with commitment."
        
        return selected_habits
    
    def recommend_best_time(self, habit_type: str) -> Dict[str, Any]:
        """
        Recommend optimal time slot for habit using CSP.
        
        Args:
            habit_type: Type of habit (exercise, meditation, etc.)
            
        Returns:
            Best time slot with reasoning
        """
        result = self.scheduler.find_best_slot(habit_type)
        
        # Add actionable recommendation
        if "time_slot" in result:
            result["action_item"] = (
                f"🕐 Schedule your {habit_type} habit during {result['slot_name']} "
                f"({result['time_slot']}) for best results."
            )
        
        return result
    
    def schedule_multiple_habits(self, habits: List[str]) -> Dict[str, Any]:
        """
        Create optimal schedule for multiple habits.
        
        Args:
            habits: List of habit types
            
        Returns:
            Schedule with recommendations
        """
        schedule = self.scheduler.schedule_multiple_habits(habits)
        
        # Create visual schedule
        schedule_display = []
        for habit, time_slot in schedule.items():
            slot_data = self.scheduler.time_slots.get(time_slot, {})
            schedule_display.append({
                "habit": habit,
                "time_slot": time_slot,
                "slot_name": slot_data.get("name", ""),
                "energy_level": slot_data.get("energy_level", 5)
            })
        
        return {
            "schedule": schedule,
            "schedule_display": schedule_display,
            "total_habits_scheduled": len(schedule)
        }
    
    def analyze_user_message(self, message: str) -> Dict[str, Any]:
        """
        Analyze user message using NLP engine.
        
        Args:
            message: User's message
            
        Returns:
            NLP analysis with sentiment and intent
        """
        analysis = self.nlp_engine.analyze_message(message)
        
        # Add response suggestion based on intent
        intent = analysis["intent"]["intent"]
        sentiment = analysis["sentiment"]["sentiment"]
        
        response_suggestions = {
            "motivation": "Provide encouragement and motivational quotes",
            "advice": "Share expert system insights and recommendations",
            "progress": "Celebrate achievements and show statistics",
            "struggling": "Offer support, simplify goals, expert advice",
            "question": "Answer with relevant information",
            "general": "Engage in friendly conversation"
        }
        
        analysis["suggested_response_type"] = response_suggestions.get(intent, "general")
        
        # Add sentiment-based tone
        if sentiment == "negative":
            analysis["response_tone"] = "empathetic and supportive"
        elif sentiment == "positive":
            analysis["response_tone"] = "enthusiastic and celebratory"
        else:
            analysis["response_tone"] = "friendly and informative"
        
        return analysis
    
    def generate_ai_response(self, message: str, user_data: Dict[str, Any]) -> str:
        """
        Generate AI response to user message.
        
        Combines NLP analysis with expert system and Gemini AI (if available).
        
        Args:
            message: User message
            user_data: User statistics and context
            
        Returns:
            AI-generated response
        """
        # Analyze message with NLP
        analysis = self.analyze_user_message(message)
        intent = analysis["intent"]["intent"]
        sentiment = analysis["sentiment"]["sentiment"]
        
        # Build comprehensive context for Gemini
        if self.use_gemini and self.gemini_model:
            try:
                # Get expert system insights
                expert_advice = self.expert_system.forward_chain(user_data, limit=3)
                expert_insights = "\n".join([f"- {rule['conclusion']}" for rule in expert_advice]) if expert_advice else "No specific insights yet"
                
                # Build rich user profile
                user_profile = f"""
User Habit Profile:
- Total Active Habits: {user_data.get('total_habits', 0)}
- Total Completions: {user_data.get('total_completions', 0)}
- Overall Completion Rate: {user_data.get('completion_rate', 0):.0%}
- Current Average Streak: {user_data.get('streak', 0)} days
- Active Categories: {user_data.get('habit_variety', 0)}
- Best Category: {user_data.get('best_category', 'None')}

Expert System Insights:
{expert_insights}

Current Habits:
{user_data.get('habits_list', 'No habits yet')}


Recent Progress:
{user_data.get('recent_activity', 'No recent activity')}
"""
                
                # Create comprehensive system prompt WITH USER NAME
                user_name = user_data.get('user_name', 'Friend')
                system_prompt = f"""You are MOMENTUM's AI Life Coach - a supportive, motivational, and insightful habit tracking assistant.

**THE USER'S NAME IS: {user_name}** - ALWAYS address them by name!

Your personality:
- Warm and encouraging, like a friend who believes in the user
- CALL THEM BY THEIR NAME ({user_name}) in your responses
- Use specific data to give personalized advice
- Celebrate wins, no matter how small
- When user struggles, offer concrete solutions
- Keep responses conversational and natural (2-4 sentences)
- Use their actual stats to make your advice relevant

{user_profile}

User's Message Sentiment: {sentiment}
User's Intent: {intent}

Guidelines:
1. START by addressing {user_name} by name
2. Always reference their actual data and habits when relevant
3. Celebrate streaks and completion rates specifically
4. If they're struggling, acknowledge it and offer one actionable tip
5. If they achieved something, make them feel amazing about it
6. Keep it real - don't be overly formal or robotic
7. End with encouragement or a thought-provoking question when appropriate
"""
                
                # Generate response with Gemini
                response = self.gemini_model.generate_content(
                    f"{system_prompt}\n\nUser says: {message}\n\nYour response:"
                )
                
                return response.text.strip()
                
            except Exception as e:
                print(f"Gemini error: {e}")
                # Fall through to rule-based response
        
        # Fallback: Rule-based responses if Gemini not available
        if intent == "motivation":
            # Use expert system for motivation
            advice = self.expert_system.get_advice(user_data)
            quote = random.choice(MOTIVATIONAL_QUOTES)
            response = f"{advice}\n\n💭 {quote}"
        
        elif intent == "advice":
            # Use expert system and decision tree
            personalized = self.get_personalized_advice(user_data)
            response = personalized["primary_advice"]
        
        elif intent == "progress":
            # Celebrate progress
            completion_rate = user_data.get("completion_rate", 0)
            streak = user_data.get("streak", 0)
            
            if completion_rate >= 0.8:
                response = f"Outstanding! {completion_rate:.0%} completion rate! You're crushing it!"
            elif streak >= 7:
                response = f"{streak}-day streak! That's the power of consistency!"
            else:
                response = "Great progress! Every step forward counts. Keep it up!"
        
        elif intent == "struggling":
            # Provide support
            response = (
                "I hear you. Struggles are part of the journey. "
                "Let's simplify: focus on ONE small habit today. "
                "Just one win to rebuild momentum. You've got this!"
            )
        
        else:
            # General response
            if sentiment == "positive":
                response = "That's great to hear! Your positive energy will fuel your success."
            elif sentiment == "negative":
                response = "I understand. Remember, every master was once a beginner. Small steps matter."
            else:
                response = "Thanks for sharing! How can I help you achieve your goals today?"
        
        return response
    
    def get_daily_insights(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive daily insights combining all AI algorithms.
        
        Args:
            user_data: Complete user statistics and history
            
        Returns:
            Dictionary with insights from all AI systems
        """
        insights = {
            "timestamp": datetime.now().isoformat(),
            "greeting": self.generate_daily_greeting(user_data),
            "expert_advice": self.expert_system.forward_chain(user_data, limit=3),
            "motivational_quote": random.choice(MOTIVATIONAL_QUOTES)
        }
        
        # Add goal plan if goal specified
        if user_data.get("current_goal"):
            insights["goal_plan"] = self.plan_goal(goal=user_data["current_goal"])
        
        # Add habit recommendations
        if user_data.get("candidate_habits"):
            insights["recommended_habits"] = self.optimize_habit_selection(
                user_data["candidate_habits"],
                user_data,
                max_habits=3
            )
        
        return insights
    
    def get_algorithm_explanations(self) -> Dict[str, str]:
        """
        Get explanations of all 12 AI algorithms being used.
        
        Returns:
            Dictionary mapping algorithm names to explanations
        """
        return {
            "A* Search": (
                "Finds optimal path to goal using f(n) = g(n) + h(n), where g(n) is actual cost "
                "and h(n) is heuristic estimate. Guarantees shortest path to habit mastery."
            ),
            "Expert System": (
                "Rule-based inference engine with forward chaining. Evaluates IF-THEN production rules "
                "against your data to provide expert advice with confidence scores."
            ),
            "NLP Engine": (
                "Analyzes your messages using tokenization, sentiment analysis (positive/negative/neutral), "
                "and intent classification to understand what you need."
            ),
            "Decision Tree": (
                "Traverses decision nodes based on your characteristics (goal, time, experience) "
                "to recommend personalized habits with explanations."
            ),
            "CSP Solver": (
                "Constraint Satisfaction Problem solver that finds optimal time slots matching "
                "habit requirements (energy, focus) with available times."
            ),
            "Best-First Search": (
                "Uses priority queue to select habits with highest success probability based on "
                "your completion history and habit characteristics."
            ),
            "Q-Learning": (
                "Reinforcement learning that learns optimal habit times from your success/failure history. "
                "Updates Q-values: Q(habit,time) += α(reward - Q(habit,time))"
            ),
            "Bayesian Inference": (
                "Probabilistic reasoning using Beta distribution to predict success with confidence intervals. "
                "Updates beliefs based on your actual performance data."
            ),
            "Monte Carlo Simulation": (
                "Runs thousands of random simulations to forecast goal achievement probability "
                "and predict expected outcomes with statistical confidence."
            ),
            "Genetic Algorithm": (
                "Evolves optimal habit schedules through selection, crossover, and mutation. "
                "Mimics natural evolution to find best time arrangements."
            ),
            "Simulated Annealing": (
                "Temperature-based optimization that finds optimal habit completion order. "
                "Uses probabilistic acceptance to escape local optima."
            ),
            "Minimax": (
                "Game-theoretic strategy for habit selection. Models choice as a game "
                "between you (maximizing success) and resistance (minimizing completion)."
            )
        }


# ============================================================================
# MODULE EXPORTS
# ============================================================================

__all__ = ['AICoach']
