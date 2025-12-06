"""
MOMENTUM - AI-Powered Habit & Life Coach
Configuration Module

This module contains all knowledge bases, production rules, and configuration
for the AI algorithms including:
- Expert System Rules (IF-THEN knowledge base)
- Decision Tree Structure
- Heuristic Values for Goals
- Time Slot Constraints for CSP
- NLP Keyword Dictionaries
- Habit Categories and Achievement System
"""

# ============================================================================
# EXPERT SYSTEM KNOWLEDGE BASE - Production Rules (IF-THEN)
# ============================================================================

EXPERT_RULES = [
    {
        "id": "rule_001",
        "condition": lambda user_data: user_data.get("streak", 0) >= 7,
        "conclusion": "You're on fire! 🔥 A 7-day streak shows incredible consistency. Keep this momentum going!",
        "confidence": 0.95,
        "category": "motivation"
    },
    {
        "id": "rule_002",
        "condition": lambda user_data: user_data.get("completion_rate", 0) < 0.3,
        "conclusion": "Start small. Focus on just ONE habit this week. Build confidence through small wins.",
        "confidence": 0.9,
        "category": "advice"
    },
    {
        "id": "rule_003",
        "condition": lambda user_data: user_data.get("missed_days", 0) >= 3,
        "conclusion": "Don't break the chain! Missing days hurts momentum. Set a phone reminder for your habits.",
        "confidence": 0.85,
        "category": "warning"
    },
    {
        "id": "rule_004",
        "condition": lambda user_data: user_data.get("total_habits", 0) > 5 and user_data.get("completion_rate", 0) < 0.5,
        "conclusion": "You're overcommitted. Reduce to 2-3 core habits and master those first.",
        "confidence": 0.92,
        "category": "advice"
    },
    {
        "id": "rule_005",
        "condition": lambda user_data: user_data.get("morning_habits", 0) > 0 and user_data.get("morning_completion", 0) > 0.8,
        "conclusion": "Morning routines are your superpower! You excel at early habits. Build on this strength.",
        "confidence": 0.88,
        "category": "insight"
    },
    {
        "id": "rule_006",
        "condition": lambda user_data: user_data.get("weekend_completion", 0) < 0.4,
        "conclusion": "Weekends are your weak spot. Pre-plan Saturday activities to maintain consistency.",
        "confidence": 0.83,
        "category": "advice"
    },
    {
        "id": "rule_007",
        "condition": lambda user_data: user_data.get("streak", 0) >= 30,
        "conclusion": "LEGENDARY! 30+ days is habit mastery. You've rewired your brain. Time to level up!",
        "confidence": 0.98,
        "category": "celebration"
    },
    {
        "id": "rule_008",
        "condition": lambda user_data: user_data.get("difficulty", "") == "hard" and user_data.get("completion_rate", 0) > 0.7,
        "conclusion": "You're crushing difficult habits! Your discipline is exceptional. Consider mentoring others.",
        "confidence": 0.91,
        "category": "motivation"
    },
    {
        "id": "rule_009",
        "condition": lambda user_data: user_data.get("habit_variety", 0) >= 4,
        "conclusion": "Great balance across categories! You're building a holistic lifestyle.",
        "confidence": 0.87,
        "category": "insight"
    },
    {
        "id": "rule_010",
        "condition": lambda user_data: user_data.get("recent_decline", False),
        "conclusion": "Energy dip detected. Review your sleep and stress levels. It's okay to adjust goals temporarily.",
        "confidence": 0.79,
        "category": "warning"
    },
    {
        "id": "rule_011",
        "condition": lambda user_data: user_data.get("total_completions", 0) >= 100,
        "conclusion": "MILESTONE ACHIEVED! 100 completions is proof of commitment. You're in the top 1% of users.",
        "confidence": 0.96,
        "category": "celebration"
    },
    {
        "id": "rule_012",
        "condition": lambda user_data: user_data.get("consistency_score", 0) > 0.85,
        "conclusion": "Your consistency is world-class. Habits are now part of your identity, not just tasks.",
        "confidence": 0.93,
        "category": "insight"
    }
]

# ============================================================================
# DECISION TREE STRUCTURE for Habit Recommendations
# ============================================================================

DECISION_TREE = {
    "node_id": "root",
    "question": "What is your primary goal?",
    "type": "categorical",
    "branches": {
        "health": {
            "node_id": "health_node",
            "question": "How much time can you commit daily?",
            "type": "threshold",
            "threshold": 30,  # minutes
            "branches": {
                "less": {
                    "node_id": "health_low_time",
                    "recommendation": "10-minute morning stretching",
                    "explanation": "Low time commitment, high impact for beginners. Builds consistency.",
                    "category": "health",
                    "difficulty": "easy"
                },
                "more": {
                    "node_id": "health_high_time",
                    "question": "What's your experience level?",
                    "type": "categorical",
                    "branches": {
                        "beginner": {
                            "recommendation": "30-minute daily walk",
                            "explanation": "Sustainable, low-impact cardio. Perfect for building endurance.",
                            "category": "health",
                            "difficulty": "easy"
                        },
                        "intermediate": {
                            "recommendation": "45-minute strength training",
                            "explanation": "Build muscle and metabolism. Proven long-term health benefits.",
                            "category": "health",
                            "difficulty": "medium"
                        },
                        "advanced": {
                            "recommendation": "HIIT workout + meal prep",
                            "explanation": "Maximum results for experienced athletes. Comprehensive health approach.",
                            "category": "health",
                            "difficulty": "hard"
                        }
                    }
                }
            }
        },
        "productivity": {
            "node_id": "productivity_node",
            "question": "Are you a morning or evening person?",
            "type": "categorical",
            "branches": {
                "morning": {
                    "recommendation": "5 AM deep work session",
                    "explanation": "Leverage peak morning energy for focused work. Elite performers swear by this.",
                    "category": "productivity",
                    "difficulty": "hard"
                },
                "evening": {
                    "recommendation": "Evening planning ritual",
                    "explanation": "Plan tomorrow before bed. Wake up with clarity and direction.",
                    "category": "productivity",
                    "difficulty": "easy"
                }
            }
        },
        "mindfulness": {
            "node_id": "mindfulness_node",
            "question": "Have you meditated before?",
            "type": "categorical",
            "branches": {
                "yes": {
                    "recommendation": "20-minute daily meditation",
                    "explanation": "Deepen your practice. Aim for consistency over duration.",
                    "category": "mindfulness",
                    "difficulty": "medium"
                },
                "no": {
                    "recommendation": "5-minute breathing exercise",
                    "explanation": "Start simple. Just breathe. Build from here.",
                    "category": "mindfulness",
                    "difficulty": "easy"
                }
            }
        },
        "learning": {
            "node_id": "learning_node",
            "question": "What do you want to learn?",
            "type": "categorical",
            "branches": {
                "skill": {
                    "recommendation": "Daily deliberate practice",
                    "explanation": "20 minutes of focused skill practice beats 2 hours of casual effort.",
                    "category": "learning",
                    "difficulty": "medium"
                },
                "knowledge": {
                    "recommendation": "Read 30 pages daily",
                    "explanation": "That's 10,000+ pages per year. Transform your knowledge in 12 months.",
                    "category": "learning",
                    "difficulty": "easy"
                }
            }
        }
    }
}

# ============================================================================
# HEURISTIC VALUES for A* Goal Planning
# ============================================================================

# Estimated effort (in days) for common goals and subgoals
GOAL_HEURISTICS = {
    "master_habit": 66,  # 66 days to form a habit (research-based)
    "lose_weight": 90,
    "learn_skill": 100,
    "build_muscle": 120,
    "read_book": 30,
    "meditate_daily": 21,
    "wake_early": 14,
    "exercise_routine": 30,
    "healthy_diet": 45,
    "productivity_system": 21,
    "stress_management": 30,
    "social_confidence": 60,
    
    # Subgoal estimates
    "research_topic": 3,
    "create_plan": 1,
    "buy_equipment": 1,
    "find_accountability": 2,
    "track_progress": 1,
    "build_streak": 7,
    "overcome_plateau": 14,
    "celebrate_milestone": 1,
    "adjust_difficulty": 2,
    "establish_trigger": 3,
    "remove_obstacles": 5,
    "visualize_success": 1
}

# Goal graph: maps goals to prerequisite subgoals with actual costs
GOAL_GRAPH = {
    "start": {
        "create_plan": 1,
        "research_topic": 2
    },
    "research_topic": {
        "create_plan": 1,
        "buy_equipment": 2
    },
    "create_plan": {
        "establish_trigger": 1,
        "find_accountability": 1
    },
    "buy_equipment": {
        "build_streak": 1
    },
    "establish_trigger": {
        "build_streak": 2
    },
    "find_accountability": {
        "track_progress": 1
    },
    "build_streak": {
        "track_progress": 1,
        "overcome_plateau": 7
    },
    "track_progress": {
        "adjust_difficulty": 2,
        "celebrate_milestone": 1
    },
    "overcome_plateau": {
        "celebrate_milestone": 3
    },
    "adjust_difficulty": {
        "master_habit": 10
    },
    "celebrate_milestone": {
        "master_habit": 5
    },
    "master_habit": {}  # Goal reached!
}

# ============================================================================
# CSP - TIME SLOT CONSTRAINTS for Scheduling
# ============================================================================

TIME_SLOTS = {
    "5:00-7:00": {
        "name": "Early Morning",
        "energy_level": 8,
        "distraction_level": 1,
        "consistency_bonus": 10,
        "best_for": ["exercise", "meditation", "deep_work"]
    },
    "7:00-9:00": {
        "name": "Morning",
        "energy_level": 9,
        "distraction_level": 3,
        "consistency_bonus": 7,
        "best_for": ["exercise", "learning", "planning"]
    },
    "9:00-12:00": {
        "name": "Late Morning",
        "energy_level": 10,
        "distraction_level": 6,
        "consistency_bonus": 5,
        "best_for": ["deep_work", "learning", "creative"]
    },
    "12:00-14:00": {
        "name": "Lunch",
        "energy_level": 6,
        "distraction_level": 8,
        "consistency_bonus": 3,
        "best_for": ["social", "light_exercise", "rest"]
    },
    "14:00-17:00": {
        "name": "Afternoon",
        "energy_level": 7,
        "distraction_level": 7,
        "consistency_bonus": 4,
        "best_for": ["meetings", "collaboration", "routine_tasks"]
    },
    "17:00-19:00": {
        "name": "Evening",
        "energy_level": 6,
        "distraction_level": 5,
        "consistency_bonus": 6,
        "best_for": ["exercise", "hobbies", "social"]
    },
    "19:00-21:00": {
        "name": "Night",
        "energy_level": 5,
        "distraction_level": 4,
        "consistency_bonus": 5,
        "best_for": ["reading", "reflection", "family"]
    },
    "21:00-23:00": {
        "name": "Late Night",
        "energy_level": 4,
        "distraction_level": 2,
        "consistency_bonus": 3,
        "best_for": ["meditation", "journaling", "wind_down"]
    }
}

# Habit requirements for CSP matching
HABIT_REQUIREMENTS = {
    "exercise": {"min_energy": 7, "max_distraction": 5, "preferred_times": ["5:00-7:00", "7:00-9:00", "17:00-19:00"]},
    "meditation": {"min_energy": 3, "max_distraction": 3, "preferred_times": ["5:00-7:00", "21:00-23:00"]},
    "deep_work": {"min_energy": 8, "max_distraction": 4, "preferred_times": ["5:00-7:00", "9:00-12:00"]},
    "learning": {"min_energy": 7, "max_distraction": 5, "preferred_times": ["7:00-9:00", "9:00-12:00"]},
    "reading": {"min_energy": 5, "max_distraction": 4, "preferred_times": ["19:00-21:00", "21:00-23:00"]},
    "social": {"min_energy": 4, "max_distraction": 10, "preferred_times": ["12:00-14:00", "17:00-19:00"]},
    "creative": {"min_energy": 7, "max_distraction": 5, "preferred_times": ["9:00-12:00", "19:00-21:00"]},
}

# ============================================================================
# NLP - KEYWORD DICTIONARIES
# ============================================================================

# Sentiment Analysis Keywords
SENTIMENT_KEYWORDS = {
    "positive": [
        "great", "amazing", "awesome", "excellent", "wonderful", "fantastic",
        "happy", "excited", "motivated", "confident", "accomplished", "proud",
        "success", "win", "victory", "crushing", "killing", "nailing",
        "love", "enjoy", "fun", "easy", "smooth", "good"
    ],
    "negative": [
        "bad", "terrible", "awful", "horrible", "struggle", "struggling",
        "difficult", "hard", "tough", "failed", "failing", "missed",
        "sad", "depressed", "anxious", "stressed", "overwhelmed", "tired",
        "hate", "sucks", "impossible", "can't", "won't", "never"
    ],
    "neutral": [
        "okay", "fine", "alright", "normal", "average", "same",
        "continuing", "going", "doing", "working", "trying"
    ]
}

# Intent Classification Keywords
INTENT_KEYWORDS = {
    "motivation": [
        "motivate", "inspire", "encourage", "boost", "help", "support",
        "struggling", "need", "want", "how", "stuck", "lost"
    ],
    "advice": [
        "advice", "suggest", "recommend", "should", "what", "how",
        "tips", "ideas", "guidance", "help", "improve", "better"
    ],
    "progress": [
        "progress", "update", "completed", "done", "finished", "achieved",
        "success", "won", "streak", "milestone", "accomplished"
    ],
    "struggling": [
        "struggle", "struggling", "difficult", "hard", "failed", "missed",
        "can't", "unable", "stuck", "frustrated", "overwhelmed", "quit"
    ],
    "question": [
        "what", "why", "how", "when", "where", "who", "which",
        "?", "explain", "tell", "show"
    ],
    "general": [
        "hi", "hello", "hey", "thanks", "thank", "okay", "ok", "yes", "no"
    ]
}

# ============================================================================
# HABIT CATEGORIES
# ============================================================================

HABIT_CATEGORIES = {
    "health": {
        "emoji": "💪",
        "color": "#FF6B6B",
        "examples": ["Exercise", "Healthy Eating", "Sleep 8 hours", "Drink Water"]
    },
    "productivity": {
        "emoji": "🎯",
        "color": "#4ECDC4",
        "examples": ["Deep Work", "Time Blocking", "No Social Media", "Plan Tomorrow"]
    },
    "mindfulness": {
        "emoji": "🧘",
        "color": "#95E1D3",
        "examples": ["Meditation", "Journaling", "Gratitude Practice", "Breathing Exercise"]
    },
    "learning": {
        "emoji": "📚",
        "color": "#F38181",
        "examples": ["Read 30 Pages", "Online Course", "Practice Skill", "Learn Language"]
    },
    "social": {
        "emoji": "👥",
        "color": "#AA96DA",
        "examples": ["Call Family", "Meet Friends", "Network", "Help Someone"]
    },
    "creative": {
        "emoji": "🎨",
        "color": "#FCBAD3",
        "examples": ["Write", "Draw", "Music", "Photography"]
    }
}

# ============================================================================
# ACHIEVEMENT SYSTEM
# ============================================================================

ACHIEVEMENTS = {
    "first_habit": {
        "name": "Getting Started",
        "description": "Created your first habit",
        "emoji": "🎯",
        "criteria": lambda stats: stats.get("total_habits", 0) >= 1
    },
    "week_warrior": {
        "name": "Week Warrior",
        "description": "Maintained a 7-day streak",
        "emoji": "🔥",
        "criteria": lambda stats: stats.get("max_streak", 0) >= 7
    },
    "month_master": {
        "name": "Month Master",
        "description": "Maintained a 30-day streak",
        "emoji": "👑",
        "criteria": lambda stats: stats.get("max_streak", 0) >= 30
    },
    "centurion": {
        "name": "Centurion",
        "description": "Completed 100 habit instances",
        "emoji": "💯",
        "criteria": lambda stats: stats.get("total_completions", 0) >= 100
    },
    "balanced_life": {
        "name": "Balanced Life",
        "description": "Active habits in 4+ categories",
        "emoji": "⚖️",
        "criteria": lambda stats: stats.get("active_categories", 0) >= 4
    },
    "perfectionist": {
        "name": "Perfectionist",
        "description": "100% completion rate for a week",
        "emoji": "✨",
        "criteria": lambda stats: stats.get("perfect_week", False)
    },
    "comeback_kid": {
        "name": "Comeback Kid",
        "description": "Rebuilt a streak after breaking it",
        "emoji": "🦅",
        "criteria": lambda stats: stats.get("rebuild_count", 0) >= 1
    }
}

# ============================================================================
# MOTIVATIONAL MESSAGES
# ============================================================================

MOTIVATIONAL_QUOTES = [
    "We are what we repeatedly do. Excellence, then, is not an act, but a habit. - Aristotle",
    "The secret of getting ahead is getting started. - Mark Twain",
    "Success is the sum of small efforts repeated day in and day out. - Robert Collier",
    "You don't have to be great to start, but you have to start to be great. - Zig Ziglar",
    "The only way to do great work is to love what you do. - Steve Jobs",
    "Don't watch the clock; do what it does. Keep going. - Sam Levenson",
    "The future depends on what you do today. - Mahatma Gandhi",
    "Discipline is choosing between what you want now and what you want most.",
    "Motivation is what gets you started. Habit is what keeps you going. - Jim Ryun",
    "Your life does not get better by chance, it gets better by change. - Jim Rohn"
]

# ============================================================================
# APP CONFIGURATION
# ============================================================================

APP_CONFIG = {
    "app_name": "MOMENTUM",
    "tagline": "AI-Powered Habit & Life Coach",
    "version": "1.0.0",
    "theme": {
        "primary_gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "secondary_gradient": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
        "success_color": "#10b981",
        "warning_color": "#f59e0b",
        "danger_color": "#ef4444"
    },
    "data_file": "momentum_data.json",
    "max_habits": 10,
    "streak_threshold": 7,  # Days to celebrate
    "reminder_enabled": True
}
