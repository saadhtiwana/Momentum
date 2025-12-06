"""
MOMENTUM - AI-Powered Habit & Life Coach
Habit Engine Module

This module handles all habit tracking functionality:
- Habit creation and management
- Completion logging with timestamps
- Streak calculation (current and maximum)
- Completion rate analysis
- Weekly pattern detection
- Success probability prediction
- Overall statistics and insights
"""

from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Any
from collections import defaultdict
import uuid


class HabitEngine:
    """
    Core habit tracking and analysis engine.
    
    Manages habit lifecycle and provides analytics for AI decision making.
    """
    
    def __init__(self):
        """Initialize habit engine with empty habits dictionary."""
        self.habits = {}  # habit_id -> habit_data
    
    def create_habit(self, name: str, category: str, difficulty: str = "medium",
                    time_minutes: int = 30, goal: str = "", notes: str = "") -> str:
        """
        Create a new habit.
        
        Args:
            name: Habit name
            category: Category (health, productivity, mindfulness, etc.)
            difficulty: Difficulty level (easy, medium, hard)
            time_minutes: Required time in minutes
            goal: Habit goal description
            notes: Additional notes
            
        Returns:
            Unique habit ID
        """
        habit_id = str(uuid.uuid4())
        
        self.habits[habit_id] = {
            "id": habit_id,
            "name": name,
            "category": category,
            "difficulty": difficulty,
            "time_minutes": time_minutes,
            "goal": goal,
            "notes": notes,
            "created_at": datetime.now().isoformat(),
            "completions": [],  # List of completion dates
            "completion_notes": {},  # date -> note
            "active": True,
            "archived_at": None
        }
        
        return habit_id
    
    def log_completion(self, habit_id: str, completion_date: Optional[date] = None,
                      note: str = "") -> bool:
        """
        Log a habit completion.
        
        Args:
            habit_id: Habit ID
            completion_date: Date of completion (default: today)
            note: Optional note about completion
            
        Returns:
            True if logged successfully
        """
        if habit_id not in self.habits:
            return False
        
        habit = self.habits[habit_id]
        
        if completion_date is None:
            completion_date = date.today()
        
        # Convert date to string for JSON serialization
        date_str = completion_date.isoformat()
        
        # Avoid duplicate entries for same day
        if date_str not in habit["completions"]:
            habit["completions"].append(date_str)
            habit["completions"].sort()  # Keep chronological
        
        # Store note if provided
        if note:
            habit["completion_notes"][date_str] = note
        
        return True
    
    def calculate_streak(self, habit_id: str) -> Dict[str, int]:
        """
        Calculate current and maximum streak for a habit.
        
        A streak is consecutive days of completion.
        
        Args:
            habit_id: Habit ID
            
        Returns:
            Dictionary with current_streak and max_streak
        """
        if habit_id not in self.habits:
            return {"current_streak": 0, "max_streak": 0}
        
        habit = self.habits[habit_id]
        completions = [date.fromisoformat(d) for d in habit["completions"]]
        
        if not completions:
            return {"current_streak": 0, "max_streak": 0}
        
        completions.sort()
        
        # Calculate current streak (working backwards from today)
        current_streak = 0
        check_date = date.today()
        
        # Check if completed today or yesterday (allow 1 day gap)
        if completions[-1] >= check_date - timedelta(days=1):
            current_streak = 1
            check_date = completions[-1] - timedelta(days=1)
            
            # Count backwards
            for i in range(len(completions) - 2, -1, -1):
                if completions[i] == check_date:
                    current_streak += 1
                    check_date -= timedelta(days=1)
                elif completions[i] < check_date - timedelta(days=1):
                    # Gap found, streak broken
                    break
        
        # Calculate maximum streak
        max_streak = 0
        temp_streak = 1
        
        for i in range(1, len(completions)):
            days_diff = (completions[i] - completions[i-1]).days
            
            if days_diff == 1:
                temp_streak += 1
                max_streak = max(max_streak, temp_streak)
            else:
                temp_streak = 1
        
        max_streak = max(max_streak, temp_streak)
        
        return {
            "current_streak": current_streak,
            "max_streak": max_streak
        }
    
    def get_completion_rate(self, habit_id: str, days: int = 30) -> float:
        """
        Calculate completion rate over last N days.
        
        Args:
            habit_id: Habit ID
            days: Number of days to analyze
            
        Returns:
            Completion rate (0.0 to 1.0)
        """
        if habit_id not in self.habits:
            return 0.0
        
        habit = self.habits[habit_id]
        created_at = date.fromisoformat(habit["created_at"][:10])
        
        # Calculate actual days to check (don't go before creation)
        end_date = date.today()
        start_date = max(end_date - timedelta(days=days), created_at)
        actual_days = (end_date - start_date).days + 1
        
        if actual_days <= 0:
            return 0.0
        
        # Count completions in range
        completions = [date.fromisoformat(d) for d in habit["completions"]]
        completions_in_range = sum(1 for d in completions if start_date <= d <= end_date)
        
        return completions_in_range / actual_days
    
    def analyze_weekly_pattern(self, habit_id: str) -> Dict[str, float]:
        """
        Analyze completion patterns by day of week.
        
        Args:
            habit_id: Habit ID
            
        Returns:
            Dictionary mapping day name to completion rate
        """
        if habit_id not in self.habits:
            return {}
        
        habit = self.habits[habit_id]
        completions = [date.fromisoformat(d) for d in habit["completions"]]
        
        # Count completions by weekday
        weekday_completions = defaultdict(int)
        weekday_totals = defaultdict(int)
        
        # Analyze from creation to today
        created_at = date.fromisoformat(habit["created_at"][:10])
        current_date = created_at
        
        while current_date <= date.today():
            weekday_name = current_date.strftime("%A")
            weekday_totals[weekday_name] += 1
            
            if current_date in completions:
                weekday_completions[weekday_name] += 1
            
            current_date += timedelta(days=1)
        
        # Calculate rates
        pattern = {}
        for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]:
            if weekday_totals[day] > 0:
                pattern[day] = weekday_completions[day] / weekday_totals[day]
            else:
                pattern[day] = 0.0
        
        return pattern
    
    def predict_success_probability(self, habit_id: str) -> float:
        """
        Predict probability of maintaining this habit based on history.
        
        Uses completion rate, streak, and consistency as factors.
        
        Args:
            habit_id: Habit ID
            
        Returns:
            Success probability (0.0 to 1.0)
        """
        if habit_id not in self.habits:
            return 0.5
        
        # Get metrics
        completion_rate = self.get_completion_rate(habit_id, days=30)
        streak_data = self.calculate_streak(habit_id)
        current_streak = streak_data["current_streak"]
        
        # Base probability from completion rate
        probability = completion_rate * 0.6
        
        # Streak bonus (up to 0.3)
        if current_streak >= 30:
            probability += 0.3
        elif current_streak >= 7:
            probability += 0.2
        elif current_streak >= 3:
            probability += 0.1
        
        # Recent momentum (last 7 days)
        recent_rate = self.get_completion_rate(habit_id, days=7)
        probability += recent_rate * 0.1
        
        # Clamp to [0, 1]
        return max(0.0, min(1.0, probability))
    
    def get_habit_stats(self, habit_id: str) -> Dict[str, Any]:
        """
        Get comprehensive statistics for a habit.
        
        Args:
            habit_id: Habit ID
            
        Returns:
            Dictionary with all habit statistics
        """
        if habit_id not in self.habits:
            return {}
        
        habit = self.habits[habit_id]
        streak_data = self.calculate_streak(habit_id)
        
        return {
            "name": habit["name"],
            "category": habit["category"],
            "difficulty": habit["difficulty"],
            "total_completions": len(habit["completions"]),
            "current_streak": streak_data["current_streak"],
            "max_streak": streak_data["max_streak"],
            "completion_rate_7d": self.get_completion_rate(habit_id, days=7),
            "completion_rate_30d": self.get_completion_rate(habit_id, days=30),
            "success_probability": self.predict_success_probability(habit_id),
            "weekly_pattern": self.analyze_weekly_pattern(habit_id),
            "created_at": habit["created_at"],
            "active": habit["active"]
        }
    
    def get_all_habits(self, active_only: bool = True) -> List[Dict]:
        """
        Get all habits with basic info.
        
        Args:
            active_only: Only return active habits
            
        Returns:
            List of habit dictionaries
        """
        habits_list = []
        
        for habit_id, habit in self.habits.items():
            if active_only and not habit["active"]:
                continue
            
            habits_list.append({
                "id": habit_id,
                "name": habit["name"],
                "category": habit["category"],
                "difficulty": habit["difficulty"],
                "active": habit["active"]
            })
        
        return habits_list
    
    def get_overall_statistics(self) -> Dict[str, Any]:
        """
        Get overall statistics across all habits.
        
        Returns:
            Dictionary with aggregate statistics
        """
        active_habits = [h for h in self.habits.values() if h["active"]]
        
        if not active_habits:
            return {
                "total_habits": 0,
                "total_completions": 0,
                "overall_completion_rate": 0.0,
                "active_categories": 0,
                "average_streak": 0,
                "best_category": None
            }
        
        total_completions = sum(len(h["completions"]) for h in active_habits)
        
        # Calculate overall completion rate
        completion_rates = [self.get_completion_rate(h["id"], days=30) for h in active_habits]
        overall_rate = sum(completion_rates) / len(completion_rates) if completion_rates else 0
        
        # Count active categories
        categories = set(h["category"] for h in active_habits)
        
        # Calculate average streak
        streaks = [self.calculate_streak(h["id"])["current_streak"] for h in active_habits]
        avg_streak = sum(streaks) / len(streaks) if streaks else 0
        
        # Find best category
        category_completions = defaultdict(int)
        for habit in active_habits:
            category_completions[habit["category"]] += len(habit["completions"])
        
        best_category = max(category_completions.items(), key=lambda x: x[1])[0] if category_completions else None
        
        return {
            "total_habits": len(active_habits),
            "total_completions": total_completions,
            "overall_completion_rate": overall_rate,
            "active_categories": len(categories),
            "average_streak": avg_streak,
            "best_category": best_category,
            "categories": list(categories)
        }
    
    def get_todays_habits(self) -> List[Dict[str, Any]]:
        """
        Get today's habit checklist with completion status.
        
        Returns:
            List of habits with today's completion status
        """
        today = date.today().isoformat()
        habits_today = []
        
        for habit_id, habit in self.habits.items():
            if not habit["active"]:
                continue
            
            completed_today = today in habit["completions"]
            streak_data = self.calculate_streak(habit_id)
            
            habits_today.append({
                "id": habit_id,
                "name": habit["name"],
                "category": habit["category"],
                "difficulty": habit["difficulty"],
                "time_minutes": habit["time_minutes"],
                "completed_today": completed_today,
                "current_streak": streak_data["current_streak"],
                "note": habit["completion_notes"].get(today, "")
            })
        
        return habits_today
    
    def archive_habit(self, habit_id: str) -> bool:
        """
        Archive a habit (make inactive).
        
        Args:
            habit_id: Habit ID
            
        Returns:
            True if archived successfully
        """
        if habit_id not in self.habits:
            return False
        
        self.habits[habit_id]["active"] = False
        self.habits[habit_id]["archived_at"] = datetime.now().isoformat()
        return True
    
    def delete_habit(self, habit_id: str) -> bool:
        """
        Permanently delete a habit.
        
        Args:
            habit_id: Habit ID
            
        Returns:
            True if deleted successfully
        """
        if habit_id in self.habits:
            del self.habits[habit_id]
            return True
        return False
    
    def load_habits(self, habits_data: Dict) -> None:
        """
        Load habits from saved data.
        
        Args:
            habits_data: Dictionary of habit data
        """
        self.habits = habits_data
    
    def get_habits_data(self) -> Dict:
        """
        Get all habits data for serialization.
        
        Returns:
            Dictionary of all habit data
        """
        return self.habits


# ============================================================================
# MODULE EXPORTS
# ============================================================================

__all__ = ['HabitEngine']
