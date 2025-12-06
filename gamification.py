"""
MOMENTUM - Gamification Engine
Maximum Dopamine Optimization System

Implements psychological engagement mechanics:
- Streak tracking with FOMO triggers
- Variable reward schedule (random bonuses)
- Achievement system with unlocks
- Daily login bonuses
- Point accumulation
- Progress celebrations
"""

import random
from datetime import datetime, date, timedelta
from typing import Dict, List, Any, Tuple, Optional
import json


# ============================================================================
# ACHIEVEMENTS DATABASE
# ============================================================================

ACHIEVEMENTS = {
    # Beginner Tier
    "first_habit": {
        "name": "First Step",
        "description": "Create your first habit",
        "tier": "bronze",
        "points": 50,
        "criteria": lambda stats: stats.get("total_habits", 0) >= 1
    },
    "first_week": {
        "name": "Week Warrior",
        "description": "Maintain a 7-day streak",
        "tier": "bronze",
        "points": 100,
        "criteria": lambda stats: stats.get("max_streak", 0) >= 7
    },
    "perfect_day": {
        "name": "Perfect Day",
        "description": "Complete all habits in one day",
        "tier": "bronze",
        "points": 75,
        "criteria": lambda stats: stats.get("perfect_days", 0) >= 1
    },
    
    # Silver Tier
    "consistency_king": {
        "name": "Consistency King",
        "description": "30-day streak achieved",
        "tier": "silver",
        "points": 300,
        "criteria": lambda stats: stats.get("max_streak", 0) >= 30
    },
    "hundred_club": {
        "name": "Hundred Club",
        "description": "Complete 100 total habits",
        "tier": "silver",
        "points": 250,
        "criteria": lambda stats: stats.get("total_completions", 0) >= 100
    },
    "early_bird": {
        "name": "Early Bird",
        "description": "Complete a habit before 7 AM",
        "tier": "silver",
        "points": 150,
        "criteria": lambda stats: stats.get("early_completions", 0) >= 1
    },
    
    # Gold Tier
    "legend": {
        "name": "Legend",
        "description": "100-day streak milestone",
        "tier": "gold",
        "points": 1000,
        "criteria": lambda stats: stats.get("max_streak", 0) >= 100
    },
    "master": {
        "name": "Habit Master",
        "description": "500 total completions",
        "tier": "gold",
        "points": 800,
        "criteria": lambda stats: stats.get("total_completions", 0) >= 500
    },
    "perfectionist": {
        "name": "Perfectionist",
        "description": "7 perfect days in a row",
        "tier": "gold",
        "points": 600,
        "criteria": lambda stats: stats.get("perfect_day_streak", 0) >= 7
    },
    
    # Diamond Tier
    "year_strong": {
        "name": "Year Strong",
        "description": "365-day streak completed",
        "tier": "diamond",
        "points": 5000,
        "criteria": lambda stats: stats.get("max_streak", 0) >= 365
    },
    "elite": {
        "name": "Elite Status",
        "description": "1000 total completions",
        "tier": "diamond",
        "points": 3000,
        "criteria": lambda stats: stats.get("total_completions", 0) >= 1000
    }
}


# ============================================================================
# GAMIFICATION ENGINE
# ============================================================================

class GamificationEngine:
    """
    Core gamification system for maximum engagement.
    
    Features:
    - Streak tracking with loss aversion
    - Variable reward schedule
    - Achievement unlocking
    - Daily login bonuses
    - Point accumulation
    """
    
    def __init__(self):
        """Initialize gamification engine."""
        self.achievements_unlocked = set()
        self.total_points = 0
        self.streak_freezes_available = 3
        self.daily_bonus_streak = 0
        self.last_login_date = None
        self.last_completion_date = None
        self.current_streak = 0
        self.max_streak = 0
        self.perfect_day_streak = 0
        
    def log_completion(self, completion_date: date = None) -> Dict[str, Any]:
        """
        Log habit completion and trigger rewards.
        
        Returns reward information for display.
        """
        if completion_date is None:
            completion_date = date.today()
        
        # Update streak
        streak_info = self._update_streak(completion_date)
        
        # Calculate base points
        base_points = 10
        
        # Variable reward (30% chance of bonus)
        bonus_points = 0
        bonus_triggered = False
        
        if random.random() < 0.30:  # 30% chance
            bonus_points = random.randint(10, 50)
            bonus_triggered = True
        
        # Rare jackpot (2% chance)
        jackpot = False
        if random.random() < 0.02:
            bonus_points += 200
            jackpot = True
        
        total_points = base_points + bonus_points
        self.total_points += total_points
        
        # Generate celebratory message
        message = self._generate_celebration_message(streak_info['current_streak'])
        
        return {
            "points_earned": total_points,
            "base_points": base_points,
            "bonus_points": bonus_points,
            "bonus_triggered": bonus_triggered,
            "jackpot": jackpot,
            "total_points": self.total_points,
            "streak": streak_info['current_streak'],
            "streak_milestone": streak_info['milestone_reached'],
            "message": message
        }
    
    def _update_streak(self, completion_date: date) -> Dict[str, Any]:
        """Update streak counter."""
        if self.last_completion_date is None:
            # First completion
            self.current_streak = 1
            self.max_streak = 1
            self.last_completion_date = completion_date
            return {"current_streak": 1, "milestone_reached": None}
        
        days_since = (completion_date - self.last_completion_date).days
        
        if days_since == 1:
            # Consecutive day
            self.current_streak += 1
            if self.current_streak > self.max_streak:
                self.max_streak = self.current_streak
        elif days_since == 0:
            # Same day, no change
            pass
        else:
            # Streak broken
            self.current_streak = 1
        
        self.last_completion_date = completion_date
        
        # Check for milestone
        milestone = None
        if self.current_streak in [7, 14, 30, 50, 100, 365]:
            milestone = self.current_streak
        
        return {
            "current_streak": self.current_streak,
            "max_streak": self.max_streak,
            "milestone_reached": milestone
        }
    
    def get_streak_status(self) -> Dict[str, Any]:
        """Get current streak status with urgency messaging."""
        if self.last_completion_date is None:
            return {
                "current_streak": 0,
                "status": "neutral",
                "message": "Start your streak today!",
                "hours_remaining": None
            }
        
        days_since = (date.today() - self.last_completion_date).days
        
        if days_since == 0:
            return {
                "current_streak": self.current_streak,
                "status": "safe",
                "message": f"You're on a {self.current_streak}-day streak! Keep it going tomorrow.",
                "hours_remaining": None
            }
        elif days_since == 1:
            # Today, haven't completed yet
            hours_left = 24 - datetime.now().hour
            status = "urgent" if hours_left < 6 else "warning"
            
            if status == "urgent":
                message = f"URGENT: Only {hours_left} hours left to save your {self.current_streak}-day streak!"
            else:
                message = f"Complete a habit today to maintain your {self.current_streak}-day streak"
            
            return {
                "current_streak": self.current_streak,
                "status": status,
                "message": message,
                "hours_remaining": hours_left
            }
        else:
            return {
                "current_streak": 0,
                "status": "broken",
                "message": "Streak broken. Start fresh today!",
                "hours_remaining": None
            }
    
    def check_daily_bonus(self) -> Dict[str, Any]:
        """
        Check and award daily login bonus.
        
        Uses commitment escalation psychology.
        """
        today = date.today()
        
        if self.last_login_date is None:
            self.last_login_date = today
            self.daily_bonus_streak = 1
            bonus = 10
        else:
            days_since = (today - self.last_login_date).days
            
            if days_since == 0:
                # Already logged in today
                return {"eligible": False, "message": "Already claimed today"}
            elif days_since == 1:
                # Consecutive day
                self.daily_bonus_streak += 1
                bonus = 10 * self.daily_bonus_streak  # Escalating reward
            else:
                # Streak broken
                self.daily_bonus_streak = 1
                bonus = 10
            
            self.last_login_date = today
        
        self.total_points += bonus
        
        # Special rewards at milestones
        special_reward = None
        if self.daily_bonus_streak == 7:
            special_reward = "Streak Freeze"
            self.streak_freezes_available += 1
        elif self.daily_bonus_streak == 30:
            special_reward = "Legendary Badge"
        
        return {
            "eligible": True,
            "bonus": bonus,
            "streak": self.daily_bonus_streak,
            "total_points": self.total_points,
            "special_reward": special_reward,
            "message": f"Day {self.daily_bonus_streak} bonus: +{bonus} points!"
        }
    
    def check_achievements(self, user_stats: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Check for newly unlocked achievements.
        
        Returns list of newly unlocked achievements.
        """
        newly_unlocked = []
        
        for achievement_id, achievement in ACHIEVEMENTS.items():
            if achievement_id not in self.achievements_unlocked:
                if achievement['criteria'](user_stats):
                    self.achievements_unlocked.add(achievement_id)
                    self.total_points += achievement['points']
                    newly_unlocked.append({
                        "id": achievement_id,
                        "name": achievement['name'],
                        "description": achievement['description'],
                        "tier": achievement['tier'],
                        "points": achievement['points']
                    })
        
        return newly_unlocked
    
    def get_progress_to_next_achievement(self, user_stats: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get progress towards locked achievements."""
        progress_list = []
        
        for achievement_id, achievement in ACHIEVEMENTS.items():
            if achievement_id not in self.achievements_unlocked:
                # Attempt to calculate progress (simplified)
                progress_list.append({
                    "id": achievement_id,
                    "name": achievement['name'],
                    "description": achievement['description'],
                    "tier": achievement['tier'],
                    "points": achievement['points'],
                    "locked": True
                })
        
        return progress_list[:3]  # Return next 3 achievable
    
    def _generate_celebration_message(self, streak: int) -> str:
        """Generate dynamic celebration messages."""
        if streak >= 100:
            messages = [
                "Legendary discipline!",
                "You're unstoppable!",
                "Hall of fame material!",
                "This is mastery!"
            ]
        elif streak >= 30:
            messages = [
                "Absolutely crushing it!",
                "You're on fire!",
                "One month strong!",
                "Incredible consistency!"
            ]
        elif streak >= 7:
            messages = [
                "One week down!",
                "You're building momentum!",
                "Keep this energy!",
                "Strong start!"
            ]
        elif streak >= 3:
            messages = [
                "Great work!",
                "You're on a roll!",
                "Keep it up!",
                "Momentum building!"
            ]
        else:
            messages = [
                "Nice!",
                "Well done!",
                "Progress!",
                "Every step counts!"
            ]
        
        return random.choice(messages)
    
    def get_leaderboard_position(self, user_score: int) -> Dict[str, Any]:
        """
        Generate simulated leaderboard position.
        
        Always makes user feel good about their position.
        """
        # Generate realistic spread around user's score
        total_users = random.randint(1000, 2000)
        
        # Calculate percentile (always top 50%)
        percentile = random.uniform(0.1, 0.5)  # Top 10-50%
        rank = int(total_users * percentile)
        
        # Generate nearby competitors
        competitors = []
        for i in range(3):
            offset = random.randint(10, 50)
            competitor_score = user_score + offset
            competitors.append({
                "rank": rank - (i + 1),
                "name": self._generate_name(),
                "points": competitor_score
            })
        
        return {
            "rank": rank,
            "total_users": total_users,
            "percentile": int((1 - percentile) * 100),
            "above": competitors,
            "user_points": user_score
        }
    
    def _generate_name(self) -> str:
        """Generate realistic competitor names."""
        first_names = ["Alex", "Jordan", "Taylor", "Morgan", "Casey", "Riley", "Avery", "Quinn"]
        last_initial = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        return f"{random.choice(first_names)} {last_initial}."
    
    def save_state(self) -> Dict[str, Any]:
        """Save gamification state."""
        return {
            "achievements_unlocked": list(self.achievements_unlocked),
            "total_points": self.total_points,
            "streak_freezes_available": self.streak_freezes_available,
            "daily_bonus_streak": self.daily_bonus_streak,
            "last_login_date": self.last_login_date.isoformat() if self.last_login_date else None,
            "last_completion_date": self.last_completion_date.isoformat() if self.last_completion_date else None,
            "current_streak": self.current_streak,
            "max_streak": self.max_streak,
            "perfect_day_streak": self.perfect_day_streak
        }
    
    def load_state(self, state: Dict[str, Any]) -> None:
        """Load gamification state."""
        self.achievements_unlocked = set(state.get("achievements_unlocked", []))
        self.total_points = state.get("total_points", 0)
        self.streak_freezes_available = state.get("streak_freezes_available", 3)
        self.daily_bonus_streak = state.get("daily_bonus_streak", 0)
        
        if state.get("last_login_date"):
            self.last_login_date = date.fromisoformat(state["last_login_date"])
        if state.get("last_completion_date"):
            self.last_completion_date = date.fromisoformat(state["last_completion_date"])
        
        self.current_streak = state.get("current_streak", 0)
        self.max_streak = state.get("max_streak", 0)
        self.perfect_day_streak = state.get("perfect_day_streak", 0)


# ============================================================================
# MODULE EXPORTS
# ============================================================================

__all__ = ['GamificationEngine', 'ACHIEVEMENTS']
