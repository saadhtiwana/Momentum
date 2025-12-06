"""
MOMENTUM - Advanced AI Algorithms Module (Part 2)

Additional Classical AI Algorithms:
- Q-Learning: Reinforcement learning for habit time optimization
- Bayesian Inference: Probabilistic success prediction  
- Monte Carlo Simulation: Goal achievement forecasting
- Genetic Algorithm: Habit schedule evolution
- Simulated Annealing: Optimal habit ordering
- Minimax: Game-theoretic habit selection
"""

import random
import math
from typing import Dict, List, Any, Tuple
from collections import defaultdict


# ============================================================================
# Q-LEARNING - Reinforcement Learning for Time Optimization
# ============================================================================

class QLearningOptimizer:
    """
    Q-Learning agent that learns optimal times for habit completion.
    
    Learns from success/failure history to recommend best time slots.
    """
    
    def __init__(self, learning_rate: float = 0.1, discount_factor: float = 0.9):
        """
        Initialize Q-Learning optimizer.
        
        Args:
            learning_rate: Alpha parameter (0-1)
            discount_factor: Gamma parameter (0-1)
        """
        self.alpha = learning_rate
        self.gamma = discount_factor
        self.q_table = {}  # (habit_type, hour) -> Q-value
        
    def update(self, habit_type: str, hour: int, completed: bool):
        """
        Update Q-value based on outcome.
        
        Args:
            habit_type: Type of habit
            hour: Hour of day (0-23)
            completed: Whether habit was completed
        """
        state = (habit_type, hour)
        
        # Initialize if needed
        if state not in self.q_table:
            self.q_table[state] = 0.0
        
        # Reward: +10 for completion, -5 for miss
        reward = 10.0 if completed else -5.0
        
        # Q-learning update
        old_q = self.q_table[state]
        self.q_table[state] = old_q + self.alpha * (reward - old_q)
    
    def recommend_time(self, habit_type: str) -> Dict[str, Any]:
        """
        Recommend best time for habit.
        
        Args:
            habit_type: Type of habit
            
        Returns:
            Dictionary with recommended hour and confidence
        """
        # Get Q-values for all hours
        q_values = {}
        for hour in range(24):
            state = (habit_type, hour)
            q_values[hour] = self.q_table.get(state, 0.0)
        
        # Find best hour
        best_hour = max(q_values, key=q_values.get)
        best_q = q_values[best_hour]
        
        # Convert hour to time slot name
        time_slots = {
            range(5, 9): "Early Morning",
            range(9, 12): "Morning",
            range(12, 14): "Midday",
            range(14, 17): "Afternoon",
            range(17, 20): "Evening",
            range(20, 23): "Night"
        }
        
        slot_name = "Morning"
        for hours, name in time_slots.items():
            if best_hour in hours:
                slot_name = name
                break
        
        return {
            "recommended_hour": best_hour,
            "time_slot": slot_name,
            "confidence": min(abs(best_q) / 10, 1.0),
            "q_value": best_q
        }


# ============================================================================
# BAYESIAN INFERENCE - Probabilistic Prediction
# ============================================================================

class BayesianPredictor:
    """
    Bayesian inference for success probability estimation.
    
    Uses Beta distribution to model success probability with confidence.
    """
    
    def predict_success(self, successes: int, failures: int) -> Dict[str, Any]:
        """
        Predict success probability using Bayesian inference.
        
        Args:
            successes: Number of successful completions
            failures: Number of failures
            
        Returns:
            Dictionary with probability, confidence interval
        """
        # Beta distribution parameters (with prior)
        alpha = successes + 1  # Prior: alpha=1
        beta = failures + 1     # Prior: beta=1
        
        # Mean (expected value)
        mean_prob = alpha / (alpha + beta)
        
        # 95% credible interval (simplified)
        variance = (alpha * beta) / ((alpha + beta) ** 2 * (alpha + beta + 1))
        std_dev = math.sqrt(variance)
        
        lower_bound = max(0, mean_prob - 1.96 * std_dev)
        upper_bound = min(1, mean_prob + 1.96 * std_dev)
        
        # Confidence (narrower interval = higher confidence)
        confidence = 1.0 - (upper_bound - lower_bound)
        
        return {
            "probability": mean_prob,
            "confidence": confidence,
            "credible_interval": (lower_bound, upper_bound),
            "sample_size": successes + failures
        }
    
    def compare_habits(self, habit_a_data: Tuple[int, int], 
                      habit_b_data: Tuple[int, int]) -> Dict[str, Any]:
        """
        Compare two habits probabilistically.
        
        Args:
            habit_a_data: (successes, failures) for habit A
            habit_b_data: (successes, failures) for habit B
            
        Returns:
            Comparison with probability that A > B
        """
        a_pred = self.predict_success(*habit_a_data)
        b_pred = self.predict_success(*habit_b_data)
        
        # Simple comparison
        prob_a_better = 1.0 if a_pred["probability"] > b_pred["probability"] else 0.0
        
        return {
            "habit_a_prob": a_pred["probability"],
            "habit_b_prob": b_pred["probability"],
            "probability_a_better": prob_a_better,
            "difference": abs(a_pred["probability"] - b_pred["probability"])
        }


# ============================================================================
# MONTE CARLO SIMULATION - Goal Forecasting
# ============================================================================

class MonteCarloSimulator:
    """
    Monte Carlo simulation for goal achievement forecasting.
    
    Runs thousands of simulations to predict outcome probability.
    """
    
    def simulate_goal(self, daily_success_prob: float, goal_days: int, 
                     required_completions: int, simulations: int = 1000) -> Dict[str, Any]:
        """
        Simulate goal achievement probability.
        
        Args:
            daily_success_prob: Probability of daily completion (0-1)
            goal_days: Number of days to simulate
            required_completions: Completions needed for goal
            simulations: Number of simulations to run
            
        Returns:
            Dictionary with success probability and statistics
        """
        success_count = 0
        completion_counts = []
        
        for _ in range(simulations):
            completions = 0
            
            # Simulate each day
            for day in range(goal_days):
                if random.random() < daily_success_prob:
                    completions += 1
            
            completion_counts.append(completions)
            
            if completions >= required_completions:
                success_count += 1
        
        # Calculate statistics
        avg_completions = sum(completion_counts) / len(completion_counts)
        min_completions = min(completion_counts)
        max_completions = max(completion_counts)
        
        return {
            "success_probability": success_count / simulations,
            "expected_completions": avg_completions,
            "min_completions": min_completions,
            "max_completions": max_completions,
            "simulations_run": simulations
        }
    
    def predict_streak_length(self, daily_success_prob: float, 
                             simulations: int = 1000) -> Dict[str, Any]:
        """
        Predict expected streak length.
        
        Args:
            daily_success_prob: Daily completion probability
            simulations: Number of simulations
            
        Returns:
            Streak predictions
        """
        streak_lengths = []
        
        for _ in range(simulations):
            streak = 0
            while random.random() < daily_success_prob:
                streak += 1
                if streak > 365:  # Cap at 1 year
                    break
            streak_lengths.append(streak)
        
        avg_streak = sum(streak_lengths) / len(streak_lengths)
        max_streak = max(streak_lengths)
        
        return {
            "expected_streak": avg_streak,
            "likely_max_streak": max_streak,
            "probability_7day": sum(1 for s in streak_lengths if s >= 7) / simulations,
            "probability_30day": sum(1 for s in streak_lengths if s >= 30) / simulations
        }


# ============================================================================
# GENETIC ALGORITHM - Schedule Evolution
# ============================================================================

class GeneticScheduler:
    """
    Genetic algorithm for evolving optimal habit schedules.
    
    Uses selection, crossover, and mutation to find best schedule.
    """
    
    def __init__(self, population_size: int = 20, generations: int = 50):
        """
        Initialize genetic algorithm.
        
        Args:
            population_size: Number of schedules in population
            generations: Number of evolution iterations
        """
        self.population_size = population_size
        self.generations = generations
    
    def evolve_schedule(self, habits: List[str], constraints: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evolve optimal schedule for habits.
        
        Args:
            habits: List of habit IDs
            constraints: Time/energy constraints
            
        Returns:
            Best schedule found
        """
        # Initialize population (random schedules)
        population = self._create_population(habits)
        
        for gen in range(self.generations):
            # Evaluate fitness
            fitness_scores = [self._fitness(schedule, constraints) for schedule in population]
            
            # Selection (top 50%)
            sorted_pop = sorted(zip(population, fitness_scores), key=lambda x: x[1], reverse=True)
            survivors = [schedule for schedule, _ in sorted_pop[:self.population_size // 2]]
            
            # Crossover + Mutation
            offspring = []
            while len(offspring) < self.population_size // 2:
                parent1 = random.choice(survivors)
                parent2 = random.choice(survivors)
                child = self._crossover(parent1, parent2)
                child = self._mutate(child)
                offspring.append(child)
            
            population = survivors + offspring
        
        # Return best schedule
        final_fitness = [self._fitness(s, constraints) for s in population]
        best_idx = final_fitness.index(max(final_fitness))
        
        return {
            "schedule": population[best_idx],
            "fitness": final_fitness[best_idx],
            "generations": self.generations
        }
    
    def _create_population(self, habits: List[str]) -> List[Dict]:
        """Create random initial population."""
        population = []
        for _ in range(self.population_size):
            schedule = {}
            for habit in habits:
                schedule[habit] = random.randint(0, 23)  # Random hour
            population.append(schedule)
        return population
    
    def _fitness(self, schedule: Dict, constraints: Dict) -> float:
        """Calculate schedule fitness."""
        score = 0
        
        # Prefer morning for exercise
        for habit, hour in schedule.items():
            if "exercise" in habit.lower() and 6 <= hour <= 9:
                score += 10
            if "meditation" in habit.lower() and (6 <= hour <= 8 or 19 <= hour <= 21):
                score += 10
            # Penalize late night (22-24)
            if hour >= 22:
                score -= 5
        
        # Bonus for spread out schedule
        hours_used = set(schedule.values())
        score += len(hours_used) * 2
        
        return score
    
    def _crossover(self, parent1: Dict, parent2: Dict) -> Dict:
        """Crossover two schedules."""
        child = {}
        for habit in parent1.keys():
            child[habit] = parent1[habit] if random.random() < 0.5 else parent2[habit]
        return child
    
    def _mutate(self, schedule: Dict, mutation_rate: float = 0.1) -> Dict:
        """Mutate schedule."""
        mutated = schedule.copy()
        for habit in mutated:
            if random.random() < mutation_rate:
                mutated[habit] = random.randint(0, 23)
        return mutated


# ============================================================================
# SIMULATED ANNEALING - Habit Order Optimization
# ============================================================================

class SimulatedAnnealing:
    """
    Simulated annealing for finding optimal habit completion order.
    
    Uses temperature-based acceptance to escape local optima.
    """
    
    def optimize_order(self, habits: List[Dict], initial_temp: float = 100,
                      cooling_rate: float = 0.95, iterations: int = 100) -> Dict[str, Any]:
        """
        Find optimal habit completion order.
        
        Args:
            habits: List of habits with difficulty/time
            initial_temp: Starting temperature
            cooling_rate: Temperature decay rate
            iterations: Number of iterations
            
        Returns:
            Optimal order and score
        """
        current_order = habits.copy()
        random.shuffle(current_order)
        current_score = self._score_order(current_order)
        
        best_order = current_order.copy()
        best_score = current_score
        
        temp = initial_temp
        
        for iteration in range(iterations):
            # Generate neighbor (swap two habits)
            new_order = current_order.copy()
            
            # Safety check: need at least 2 items to swap
            if len(new_order) < 2:
                break
                
            i, j = random.sample(range(len(new_order)), 2)
            new_order[i], new_order[j] = new_order[j], new_order[i]
            
            new_score = self._score_order(new_order)
            
            # Accept if better, or probabilistically if worse
            delta = new_score - current_score
            if delta > 0 or random.random() < math.exp(delta / temp):
                current_order = new_order
                current_score = new_score
                
                if new_score > best_score:
                    best_order = new_order
                    best_score = new_score
            
            # Cool down
            temp *= cooling_rate
        
        return {
            "optimal_order": [h["name"] for h in best_order],
            "score": best_score,
            "reasoning": self._explain_order(best_order)
        }
    
    def _score_order(self, order: List[Dict]) -> float:
        """Score a habit order (higher is better)."""
        score = 0
        remaining_energy = 100
        
        for habit in order:
            difficulty_map = {"easy": 20, "medium": 40, "hard": 60}
            energy_cost = difficulty_map.get(habit.get("difficulty", "medium"), 40)
            
            # Prefer doing hard tasks when energy is high
            if remaining_energy >= energy_cost:
                score += 10
            else:
                score -= 5  # Penalize doing hard task when tired
            
            remaining_energy -= energy_cost
            remaining_energy = max(0, remaining_energy)
        
        return score
    
    def _explain_order(self, order: List[Dict]) -> str:
        """Explain the recommended order."""
        if not order:
            return "No habits to order"
        
        first = order[0]["name"]
        last = order[-1]["name"]
        return f"Start with {first} (high energy), end with {last} (lower energy required)"


# ============================================================================
# MINIMAX - Game-Theoretic Habit Selection
# ============================================================================

class MinimaxSelector:
    """
    Minimax algorithm for strategic habit selection.
    
    Models habit selection as a game against laziness/resistance.
    """
    
    def select_habit(self, available_habits: List[Dict], 
                    user_state: Dict, depth: int = 3) -> Dict[str, Any]:
        """
        Select best habit using minimax strategy.
        
        Args:
            available_habits: Habits to choose from
            user_state: Current user state (energy, time, mood)
            depth: Search depth
            
        Returns:
            Best habit and expected value
        """
        best_habit = None
        best_value = float('-inf')
        
        for habit in available_habits:
            value = self._minimax(habit, user_state, depth, False)
            if value > best_value:
                best_value = value
                best_habit = habit
        
        return {
            "selected_habit": best_habit["name"] if best_habit else None,
            "expected_value": best_value,
            "reasoning": self._explain_selection(best_habit, user_state)
        }
    
    def _minimax(self, habit: Dict, state: Dict, depth: int, maximizing: bool) -> float:
        """Minimax recursion."""
        if depth == 0:
            return self._evaluate(habit, state)
        
        if maximizing:
            # User's turn (wants to succeed)
            value = self._evaluate(habit, state)
            # Consider resistance
            resistance = self._calculate_resistance(habit, state)
            return value - resistance * 0.3
        else:
            # Resistance's turn (wants to prevent)
            resistance = self._calculate_resistance(habit, state)
            return -resistance
    
    def _evaluate(self, habit: Dict, state: Dict) -> float:
        """Evaluate habit value."""
        value = 0
        
        # High value for important habits
        if habit.get("category") == "health":
            value += 20
        
        # Match difficulty to energy
        energy = state.get("energy", 50)
        diff_map = {"easy": 20, "medium": 50, "hard": 80}
        required_energy = diff_map.get(habit.get("difficulty"), 50)
        
        if energy >= required_energy:
            value += 15
        else:
            value -= 10
        
        return value
    
    def _calculate_resistance(self, habit: Dict, state: Dict) -> float:
        """Calculate psychological resistance."""
        resistance = 0
        
        # Higher difficulty = more resistance
        diff_map = {"easy": 10, "medium": 25, "hard": 40}
        resistance += diff_map.get(habit.get("difficulty"), 25)
        
        # Low energy = more resistance
        energy = state.get("energy", 50)
        if energy < 30:
            resistance += 20
        
        return resistance
    
    def _explain_selection(self, habit: Dict, state: Dict) -> str:
        """Explain why this habit was selected."""
        if not habit:
            return "No suitable habit found"
        
        energy = state.get("energy", 50)
        return f"Selected {habit['name']} - matches your current energy level ({energy})"


# ============================================================================
# MODULE EXPORTS
# ============================================================================

__all__ = [
    'QLearningOptimizer',
    'BayesianPredictor',
    'MonteCarloSimulator',
    'GeneticScheduler',
    'SimulatedAnnealing',
    'MinimaxSelector'
]
