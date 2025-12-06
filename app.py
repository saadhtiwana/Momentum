"""
MOMENTUM - AI-Powered Habit & Life Coach
Streamlit Web Application

Beautiful gradient-themed habit tracking application with AI coaching features:
- Dashboard with AI greetings and overview
- Add Habit page
- Log Progress page
- AI Coach Chat with NLP
- Goal Planner with A* visualization
- Analytics with charts
- AI Insights with all algorithms explained
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, date, timedelta
import pandas as pd
from typing import Dict, List

from ai_coach import AICoach
from habit_engine import HabitEngine
from storage import DataStorage
from auth import AuthManager
from config import HABIT_CATEGORIES, ACHIEVEMENTS, APP_CONFIG


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="MOMENTUM",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================================
# CUSTOM CSS - BEAUTIFUL GRADIENT THEME
# ============================================================================

def load_css():
    """Load ultra-minimal Apple-inspired design with subtle animations."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Smooth global transitions */
    * {
        font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Inter', sans-serif;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* Pure white canvas */
    .stApp {
        background: #ffffff;
        animation: fadeIn 0.3s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Minimal sidebar */
    [data-testid="stSidebar"] {
        background: #fafafa;
        border-right: 1px solid #f0f0f0;
    }
    
    /* Typography - ultra refined */
    h1 {
        color: #1d1d1f;
        font-weight: 600;
        font-size: 3rem;
        letter-spacing: -0.04em;
        margin: 0 0 0.5rem 0;
        line-height: 1.1;
    }
    
    h2 {
        color: #1d1d1f;
        font-weight: 500;
        font-size: 1.5rem;
        letter-spacing: -0.02em;
        margin: 3rem 0 1.5rem 0;
    }
    
    h3 {
        color: #1d1d1f;
        font-weight: 500;
        font-size: 1.125rem;
        letter-spacing: -0.01em;
        margin: 2rem 0 1rem 0;
    }
    
    p, div, span, label {
        color: #1d1d1f;
        line-height: 1.5;
    }
    
    /* Metrics - clean numbers */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem;
        font-weight: 300;
        color: #1d1d1f;
        letter-spacing: -0.04em;
    }
    
    [data-testid="stMetricLabel"] {
        color: #8e8e93;
        font-size: 0.75rem;
        font-weight: 400;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    
    /* Buttons - refined */
    button, .stButton>button {
        background: #007aff !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        font-size: 0.9375rem !important;
        font-weight: 400 !important;
        letter-spacing: -0.01em !important;
        box-shadow: none !important;
        cursor: pointer !important;
    }
    
    button:hover, .stButton>button:hover {
        background: #0051d5 !important;
        transform: scale(0.98);
    }
    
    button:active {
        transform: scale(0.96);
    }
    
    button *, .stButton>button * {
        color: #ffffff !important;
    }
    
    /* Inputs - minimal */
    input, textarea, select {
        background: #fafafa !important;
        border: 1px solid #e8e8ed !important;
        border-radius: 8px !important;
        padding: 10px 14px !important;
        color: #1d1d1f !important;
        font-size: 0.9375rem !important;
    }
    
    input:focus, textarea:focus, select:focus {
        border-color: #007aff !important;
        box-shadow: 0 0 0 3px rgba(0, 122, 255, 0.08) !important;
        outline: none !important;
        background: #ffffff !important;
    }
    
    /* Alerts - subtle */
    .stSuccess {
        background: #f0fdf4;
        border: none;
        border-left: 2px solid #34c759;
        border-radius: 0;
        padding: 12px 16px;
        color: #1d1d1f;
    }
    
    .stInfo {
        background: #f0f9ff;
        border: none;
        border-left: 2px solid #007aff;
        border-radius: 0;
        padding: 12px 16px;
        color: #1d1d1f;
    }
    
    .stWarning {
        background: #fffbeb;
        border: none;
        border-left: 2px solid #ff9500;
        border-radius: 0;
        padding: 12px 16px;
        color: #1d1d1f;
    }
    
    .stError {
        background: #fef2f2;
        border: none;
        border-left: 2px solid #ff3b30;
        border-radius: 0;
        padding: 12px 16px;
        color: #1d1d1f;
    }
    
    /* Progress bar */
    .stProgress > div > div {
        background: #007aff;
        border-radius: 10px;
    }
    
    /* Radio buttons - clean */
    [data-testid="stSidebar"] label {
        padding: 10px 12px;
        border-radius: 6px;
        margin: 2px 0;
        color: #1d1d1f;
    }
    
    [data-testid="stSidebar"] label:hover {
        background: #f0f0f0;
    }
    
    /* Divider - hair line */
    hr {
        border: none;
        height: 1px;
        background: #f0f0f0;
        margin: 2.5rem 0;
    }
    
    /* Remove all shadows */
    .element-container {
        box-shadow: none !important;
        border: none !important;
    }
    
    /* Expander - minimal */
    .streamlit-expanderHeader {
        background: transparent;
        border: 1px solid #f0f0f0;
        border-radius: 8px;
        padding: 12px 16px;
        color: #1d1d1f;
    }
    
    .streamlit-expanderHeader:hover {
        background: #fafafa;
    }
    
    /* Clean spacing */
    .block-container {
        padding: 2rem 1.5rem;
        max-width: 1100px;
    }
    
    /* Slider */
    .stSlider > div > div > div {
        background: #007aff !important;
    }
    
    /* Selectbox */
    [data-baseweb="select"] {
        border-radius: 8px;
    }
    
    /* Number input */
    input[type="number"] {
        -moz-appearance: textfield;
    }
    
    /* Remove spinners */
    input::-webkit-outer-spin-button,
    input::-webkit-inner-spin-button {
        -webkit-appearance: none;
        margin: 0;
    }
    
    /* Fade in animation for content */
    [data-testid="stVerticalBlock"] > div {
        animation: slideUp 0.3s ease-out;
    }
    
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    </style>
    """, unsafe_allow_html=True)


# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

def init_session_state():
    """Initialize session state variables."""
    # Authentication - Initialize FIRST before any checks
    if 'auth_manager' not in st.session_state:
        st.session_state.auth_manager = AuthManager()
    
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if 'current_user' not in st.session_state:
        st.session_state.current_user = None
    
    if 'show_signup' not in st.session_state:
        st.session_state.show_signup = False
    
    # Only initialize app state if user is logged in
    if st.session_state.logged_in and st.session_state.current_user:
        username = st.session_state.current_user['username']
        user_data_file = st.session_state.auth_manager.get_user_data_file(username)
        
        if 'storage' not in st.session_state:
            st.session_state.storage = DataStorage(user_data_file)
        
        if 'habit_engine' not in st.session_state:
            st.session_state.habit_engine = HabitEngine()
            # Load existing data
            data = st.session_state.storage.load_data()
            if 'habits' in data:
                st.session_state.habit_engine.load_habits(data['habits'])
        
        # Initialize gamification engine
        if 'gamification' not in st.session_state:
            from gamification import GamificationEngine
            st.session_state.gamification = GamificationEngine()
            # Load saved gamification data
            data = st.session_state.storage.load_data()
            if 'gamification' in data:
                st.session_state.gamification.load_state(data['gamification'])
        
        if 'ai_coach' not in st.session_state:
            # Check if Gemini API key is available (optional)
            gemini_key = None
            use_gemini = False
            try:
                gemini_key = st.secrets.get("GEMINI_API_KEY", None)
                if gemini_key:
                    use_gemini = True
            except:
                pass  # Secrets file doesn't exist, Gemini will be disabled
            
            st.session_state.ai_coach = AICoach(use_gemini=use_gemini, gemini_api_key=gemini_key)
        
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []


# ============================================================================
# DATA PERSISTENCE
# ============================================================================

def save_data():
    """Save all data to storage."""
    data = {
        'habits': st.session_state.habit_engine.get_habits_data(),
        "chat_history": st.session_state.chat_history,
        "gamification": st.session_state.gamification.save_state(),  # Save gamification state
        'last_updated': datetime.now().isoformat()
    }
    st.session_state.storage.save_data(data)


# ============================================================================
# AUTHENTICATION PAGES
# ============================================================================

def render_login():
    """Render login page."""
    st.markdown("<div style='text-align: center; padding: 40px 0;'>", unsafe_allow_html=True)
    st.markdown("# MOMENTUM")
    st.markdown("<p style='color: #86868b; margin-top: -10px;'>AI-Powered Life Coach</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### Welcome Back")
        st.markdown("<p style='color: #86868b;'>Login to continue your habit journey</p>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", placeholder="Enter your password", type="password")
            
            col_a, col_b = st.columns(2)
            with col_a:
                login_btn = st.form_submit_button("Login", width='stretch')
            with col_b:
                signup_link = st.form_submit_button("Create Account", width='stretch')
            
            if login_btn:
                if username and password:
                    success, user_data, message = st.session_state.auth_manager.authenticate(username, password)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.current_user = user_data
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.error("Please enter username and password")
            
            if signup_link:
                st.session_state.show_signup = True
                st.rerun()


def render_signup():
    """Render signup page."""
    st.markdown("<div style='text-align: center; padding: 40px 0;'>", unsafe_allow_html=True)
    st.markdown("# MOMENTUM")
    st.markdown("<p style='color: #86868b; margin-top: -10px;'>AI-Powered Life Coach</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### Create Account")
        st.markdown("<p style='color: #86868b;'>Start your habit-building journey today</p>", unsafe_allow_html=True)
        
        with st.form("signup_form"):
            full_name = st.text_input("Full Name", placeholder="Enter your full name")
            username = st.text_input("Username", placeholder="Choose a username (min 3 characters)")
            password = st.text_input("Password", placeholder="Choose a password (min 6 characters)", type="password")
            confirm_password = st.text_input("Confirm Password", placeholder="Re-enter your password", type="password")
            
            col_a, col_b = st.columns(2)
            with col_a:
                signup_btn = st.form_submit_button("Sign Up", width='stretch')
            with col_b:
                back_btn = st.form_submit_button("Back to Login", width='stretch')
            
            if signup_btn:
                if not all([username, password, full_name]):
                    st.error("All fields are required")
                elif password != confirm_password:
                    st.error("Passwords don't match")
                else:
                    success, message = st.session_state.auth_manager.register_user(username, password, full_name)
                    if success:
                        st.success(message)
                        st.session_state.show_signup = False
                        st.balloons()
                        st.info("Redirecting to login...")
                        st.rerun()
                    else:
                        st.error(message)
            
            if back_btn:
                st.session_state.show_signup = False
                st.rerun()


# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================

def render_sidebar():
    """Render sidebar with navigation and stats."""
    with st.sidebar:
        st.markdown("# MOMENTUM")
        st.markdown("AI-Powered Life Coach")
        
        # User info and logout
        if st.session_state.logged_in and st.session_state.current_user:
            st.markdown("---")
            user_name = st.session_state.current_user.get('full_name', st.session_state.current_user['username'])
            st.markdown(f"**Welcome, {user_name}!**")
            if st.button("Logout", width='stretch'):
                # Clear session state
                st.session_state.logged_in = False
                st.session_state.current_user = None
                st.session_state.clear()
                st.rerun()
        
        st.markdown("---")
        
        # Navigation
        page = st.radio(
            "Navigate",
            ["Dashboard", "Add Habit", "Log Progress", 
             "AI Coach", "Goal Planner", "Analytics", "AI Insights"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Quick stats
        stats = st.session_state.habit_engine.get_overall_statistics()
        
        st.markdown("### Statistics")
        st.metric("Active Habits", stats['total_habits'])
        st.metric("Total Completions", stats['total_completions'])
        st.metric("Completion Rate", f"{stats['overall_completion_rate']:.0%}")
        
        st.markdown("---")
        st.markdown("<small style='color: #86868b;'>Version 1.0</small>", unsafe_allow_html=True)
        
        return page


# ============================================================================
# PAGE 1: DASHBOARD
# ============================================================================

def render_dashboard():
    """Render main dashboard with AI greeting and overview."""
    st.title("Dashboard")
    st.markdown("<p style='color: #86868b; margin-top: -10px;'>Your daily habit overview</p>", unsafe_allow_html=True)
    
    # Get user data for AI
    stats = st.session_state.habit_engine.get_overall_statistics()
    user_data = {
        "streak": stats.get('average_streak', 0),
        "completion_rate": stats.get('overall_completion_rate', 0),
        "total_habits": stats.get('total_habits', 0),
        "total_completions": stats.get('total_completions', 0),
        "habit_variety": stats.get('active_categories', 0)
    }
    
    # AI Daily Greeting
    greeting = st.session_state.ai_coach.generate_daily_greeting(user_data)
    st.markdown(f"## {greeting}")
    st.markdown("---")
    
    # Today's habits
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Today's Habits")
        today_habits = st.session_state.habit_engine.get_todays_habits()
        
        if not today_habits:
            st.info("No habits yet. Start by adding your first habit.")
        else:
            for habit in today_habits:
                col_a, col_b, col_c = st.columns([3, 1, 1])
                
                with col_a:
                    status = "●" if habit['completed_today'] else "○"
                    status_color = "#34c759" if habit['completed_today'] else "#d2d2d7"
                    st.markdown(f"<span style='color: {status_color}; font-size: 1.2em;'>{status}</span> **{habit['name']}** <small style='color: #86868b;'>({habit['time_minutes']} min)</small>", unsafe_allow_html=True)
                
                with col_b:
                    st.markdown(f"<small style='color: #86868b;'>{habit['current_streak']} day streak</small>", unsafe_allow_html=True)
                
                with col_c:
                    st.markdown(f"<small style='color: #86868b;'>{habit['difficulty'].title()}</small>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("### Key Metrics")
        
        if today_habits:
            completed_today = sum(1 for h in today_habits if h['completed_today'])
            completion_pct = (completed_today / len(today_habits)) * 100
            
            st.metric("Today's Progress", f"{completed_today}/{len(today_habits)}")
            st.progress(completion_pct / 100)
            
            # Best streak
            best_streak = max((h['current_streak'] for h in today_habits), default=0)
            st.metric("Best Streak", f"{best_streak} days")
        
        # Check achievements
        st.markdown("### Achievements")
        unlocked = []
        for achieve_id, achieve_data in ACHIEVEMENTS.items():
            if achieve_data['criteria'](stats):
                unlocked.append(f"{achieve_data['emoji']} {achieve_data['name']}")
        
        if unlocked:
            for achievement in unlocked[:3]:
                st.success(achievement)
        else:
            st.info("Complete your first habit to unlock achievements")
    
    # Motivational quote
    st.markdown("---")
    st.markdown("### Daily Inspiration")
    from config import MOTIVATIONAL_QUOTES
    import random
    quote = random.choice(MOTIVATIONAL_QUOTES)
    st.markdown(f"> *{quote}*")


# ============================================================================
# PAGE 2: ADD HABIT
# ============================================================================

def render_add_habit():
    """Render add habit page with form."""
    st.title("Add New Habit")
    st.markdown("Create a new habit to track. Be specific and realistic!")
    
    with st.form("add_habit_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            habit_name = st.text_input("Habit Name *", placeholder="e.g., Morning Meditation")
            
            category = st.selectbox(
                "Category *",
                options=list(HABIT_CATEGORIES.keys()),
                format_func=lambda x: f"{HABIT_CATEGORIES[x]['emoji']} {x.title()}"
            )
            
            time_minutes = st.number_input("Time Required (minutes) *", min_value=5, max_value=180, value=30)
        
        with col2:
            difficulty = st.select_slider(
                "Difficulty",
                options=["easy", "medium", "hard"],
                value="medium"
            )
            
            goal = st.text_input("Goal (optional)", placeholder="e.g., Mediate 100 days")
            
            notes = st.text_area("Notes (optional)", placeholder="Why this habit matters to you...")
        
        submitted = st.form_submit_button("Create Habit", width='stretch')
        
        if submitted:
            if habit_name:
                habit_id = st.session_state.habit_engine.create_habit(
                    name=habit_name,
                    category=category,
                    difficulty=difficulty,
                    time_minutes=time_minutes,
                    goal=goal,
                    notes=notes
                )
                save_data()
                st.success(f"Habit '{habit_name}' created successfully")
            else:
                st.error("Please provide a habit name!")
    
    # Show existing habits
    st.markdown("---")
    st.markdown("### Your Habits")
    
    habits = st.session_state.habit_engine.get_all_habits()
    if habits:
        for habit in habits:
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            
            with col1:
                st.markdown(f"**{habit['name']}**")
            with col2:
                st.markdown(f"*{habit['category']}*")
            with col3:
                st.markdown(f"*{habit['difficulty']}*")
            with col4:
                if st.button("Delete", key=f"delete_{habit['id']}"):
                    st.session_state.habit_engine.archive_habit(habit['id'])
                    save_data()
                    st.rerun()
    else:
        st.info("No habits yet. Create your first one above!")


# ============================================================================
# PAGE 3: LOG PROGRESS
# ============================================================================

def render_log_progress():
    """Render progress logging page."""
    st.title("Log Progress")
    st.markdown("<p style='color: #86868b; margin-top: -10px;'>Track your daily habit completions</p>", unsafe_allow_html=True)
    
    today_habits = st.session_state.habit_engine.get_todays_habits()
    
    if not today_habits:
        st.info("No habits to log. Add habits first.")
        return
    
    st.markdown("### " + date.today().strftime("%A, %B %d, %Y"))
    
    for habit in today_habits:
        category_data = HABIT_CATEGORIES.get(habit['category'], {})
        emoji = category_data.get('emoji', '📌')
        
        with st.expander(f"{habit['name']}", expanded=not habit['completed_today']):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**Category:** {habit['category'].title()}")
                st.markdown(f"**Time:** {habit['time_minutes']} minutes")
                st.markdown(f"**Current Streak:** {habit['current_streak']} days")
                st.markdown(f"**Difficulty:** {habit['difficulty'].title()}")
            
            with col2:
                if habit['completed_today']:
                    st.success("Completed Today")
                else:
                    st.warning("Not completed")
            
            # Completion form
            if not habit['completed_today']:
                with st.form(f"complete_{habit['id']}", clear_on_submit=True):
                    note = st.text_input("Add a note (optional)", key=f"note_{habit['id']}")
                    submit = st.form_submit_button("Mark Complete", width='stretch')
                    
                    if submit:
                        st.session_state.habit_engine.log_completion(habit['id'], note=note)
                        save_data()
                        st.success("Habit logged successfully")
                        st.rerun()
            else:
                if habit['note']:
                    st.info(f"Note: {habit['note']}")
    
    # Progress summary
    st.markdown("---")
    completed = sum(1 for h in today_habits if h['completed_today'])
    total = len(today_habits)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Completed Today", completed)
    with col2:
        st.metric("Remaining", total - completed)
    with col3:
        st.metric("Completion Rate", f"{(completed/total)*100:.0f}%")
    
    if completed == total:
        st.success("Perfect day! All habits completed")
        st.balloons()


# ============================================================================
# PAGE 4: AI COACH CHAT
# ============================================================================

def render_ai_coach():
    """Render AI coach chat interface with NLP analysis."""
    st.title("AI Coach")
    st.markdown("<p style='color: #86868b; margin-top: -10px;'>Natural language conversation with AI</p>", unsafe_allow_html=True)
    
    # Chat history
    st.markdown("### Conversation")
    
    for msg in st.session_state.chat_history:
        if msg['role'] == 'user':
            st.markdown(f"**You:** {msg['content']}")
            if 'analysis' in msg:
                with st.expander("NLP Analysis"):
                    analysis = msg['analysis']
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**Sentiment:** {analysis['sentiment']['sentiment'].upper()} "
                                  f"({analysis['sentiment']['confidence']:.0%})")
                    with col2:
                        st.markdown(f"**Intent:** {analysis['intent']['intent'].upper()} "
                                  f"({analysis['intent']['confidence']:.0%})")
        else:
            st.markdown(f"**AI Coach:** {msg['content']}")
        st.markdown("---")
    
    # Input form
    with st.form("chat_form", clear_on_submit=True):
        user_message = st.text_area("Your message:", placeholder="How can I stay motivated?")
        send = st.form_submit_button("Send Message", width='stretch')
        
        if send and user_message:
            # Analyze with NLP
            analysis = st.session_state.ai_coach.analyze_user_message(user_message)
            
            # Get COMPREHENSIVE stats for ultra-personalized Gemini responses
            stats = st.session_state.habit_engine.get_overall_statistics()
            
            # Build DETAILED habits list with full analytics
            all_habits = st.session_state.habit_engine.get_all_habits()
            habits_details = []
            weekly_patterns = {}
            category_performance = {}
            
            for habit in all_habits:
                habit_stats = st.session_state.habit_engine.get_habit_stats(habit['id'])
                
                # Individual habit details
                habits_details.append(
                    f"• {habit['name']} ({habit['category']}, {habit['difficulty']}) - "
                    f"{habit_stats.get('current_streak', 0)} day streak (max: {habit_stats.get('max_streak', 0)}), "
                    f"30-day rate: {habit_stats.get('completion_rate_30d', 0):.0%}, "
                    f"7-day rate: {habit_stats.get('completion_rate_7d', 0):.0%}"
                )
                
                # Weekly patterns
                pattern = st.session_state.habit_engine.analyze_weekly_pattern(habit['id'])
                if pattern:
                    best_day = max(pattern, key=pattern.get)
                    worst_day = min(pattern, key=pattern.get)
                    weekly_patterns[habit['name']] = f"Best: {best_day} ({pattern[best_day]:.0%}), Worst: {worst_day} ({pattern[worst_day]:.0%})"
                
                # Category performance
                cat = habit['category']
                if cat not in category_performance:
                    category_performance[cat] = []
                category_performance[cat].append(habit_stats.get('completion_rate_30d', 0))
            
            habits_list = "\n".join(habits_details) if habits_details else "No habits yet"
            
            # Calculate category averages
            category_summary = []
            for cat, rates in category_performance.items():
                avg_rate = sum(rates) / len(rates) if rates else 0
                category_summary.append(f"{cat}: {avg_rate:.0%} avg completion")
            
            # Get recent activity with trends
            today_habits = st.session_state.habit_engine.get_todays_habits()
            completed_today = sum(1 for h in today_habits if h['completed_today'])
            recent_activity = f"Today: {completed_today}/{len(today_habits)} habits completed" if today_habits else "No activity today"
            
            # Best and worst performing habits
            if all_habits:
                sorted_habits = sorted(all_habits, key=lambda h: st.session_state.habit_engine.get_habit_stats(h['id']).get('completion_rate_30d', 0), reverse=True)
                best_habit = sorted_habits[0] if sorted_habits else None
                worst_habit = sorted_habits[-1] if len(sorted_habits) > 1 else None
                
                performance_analysis = ""
                if best_habit:
                    best_stats = st.session_state.habit_engine.get_habit_stats(best_habit['id'])
                    performance_analysis += f"\nBest Performer: {best_habit['name']} ({best_stats.get('completion_rate_30d', 0):.0%})"
                if worst_habit and worst_habit != best_habit:
                    worst_stats = st.session_state.habit_engine.get_habit_stats(worst_habit['id'])
                    performance_analysis += f"\nNeeds Work: {worst_habit['name']} ({worst_stats.get('completion_rate_30d', 0):.0%})"
            else:
                performance_analysis = "No habits to analyze yet"
            
            # Check achievements
            achievements_unlocked = []
            for achieve_id, achieve_data in ACHIEVEMENTS.items():
                if achieve_data['criteria'](stats):
                    achievements_unlocked.append(achieve_data['name'])
            
            # Weekly pattern summary
            weekly_summary = "\n".join([f"{habit}: {pattern}" for habit, pattern in weekly_patterns.items()]) if weekly_patterns else "No pattern data yet"
            
            # Build ULTRA-COMPREHENSIVE user data for Gemini
            user_data = {
                # Core stats
                "completion_rate": stats.get('overall_completion_rate', 0),
                "streak": stats.get('average_streak', 0),
                "total_habits": stats.get('total_habits', 0),
                "total_completions": stats.get('total_completions', 0),
                "best_category": stats.get('best_category', 'None'),
                "habit_variety": stats.get('active_categories', 0),
                
                # Detailed breakdowns
                "habits_list": habits_list,
                "recent_activity": recent_activity,
                "category_performance": "\n".join(category_summary),
                "performance_analysis": performance_analysis,
                "weekly_patterns": weekly_summary,
                "achievements": ", ".join(achievements_unlocked) if achievements_unlocked else "None yet",
                
                # Context
                "context": "habit tracking and personal growth",
                "user_name": st.session_state.current_user.get('full_name', st.session_state.current_user['username'])
            }
            
            # Generate response with FULL context
            response = st.session_state.ai_coach.generate_ai_response(user_message, user_data)
            
            # Add to history
            st.session_state.chat_history.append({
                'role': 'user',
                'content': user_message,
                'analysis': analysis
            })
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': response
            })
            
            st.rerun()
    
    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()


# ============================================================================
# PAGE 5: GOAL PLANNER (A* Visualization)
# ============================================================================

def render_goal_planner():
    """Render goal planner with A* search visualization."""
    st.title("Goal Planner")
    st.markdown("<p style='color: #86868b; margin-top: -10px;'>Optimal path planning using A* search</p>", unsafe_allow_html=True)
    
    st.markdown("### How A* Search Works")
    st.info("""
    **A* Search Algorithm** finds the optimal path using:
    - **g(n)**: Actual cost from start to current node
    - **h(n)**: Heuristic estimate from current to goal
    - **f(n) = g(n) + h(n)**: Total estimated cost
    
    The algorithm explores nodes with lowest f(n) first, guaranteeing the shortest path!
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        start_node = st.selectbox("Start Node", ["start", "research_topic", "create_plan"])
    
    with col2:
        goal_node = st.selectbox("Goal Node", ["master_habit", "celebrate_milestone", "build_streak"])
    
    if st.button("Find Optimal Path", width='stretch'):
        # Run A* search
        result = st.session_state.ai_coach.plan_goal(start=start_node, goal=goal_node)
        
        if result['success']:
            st.success(f"{result['message']}")
            
            # Display path
            st.markdown("### Optimal Path")
            path = result['path_readable']
            
            for i, step in enumerate(path, 1):
                st.markdown(f"{i}. **{step}**")
            
            # Metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Steps", len(result['path']))
            with col2:
                st.metric("Estimated Days", result['total_cost'])
            with col3:
                st.metric("Nodes Explored", result['nodes_explored'])
            
            # Visualization
            st.markdown("### Path Visualization")
            
            # Create path flow chart
            fig = go.Figure()
            
            for i in range(len(path)):
                fig.add_trace(go.Scatter(
                    x=[i],
                    y=[0],
                    mode='markers+text',
                    marker=dict(size=30, color='#667eea'),
                    text=[path[i]],
                    textposition="bottom center",
                    name=path[i]
                ))
                
                if i < len(path) - 1:
                    fig.add_trace(go.Scatter(
                        x=[i, i+1],
                        y=[0, 0],
                        mode='lines',
                        line=dict(color='#0071e3', width=3),
                        showlegend=False
                    ))
            
            fig.update_layout(
                title="Goal Achievement Path",
                showlegend=False,
                height=300,
                xaxis=dict(showticklabels=False, showgrid=False),
                yaxis=dict(showticklabels=False, showgrid=False, range=[-0.5, 0.5])
            )
            
            st.plotly_chart(fig, width='stretch')
        
        else:
            st.error("No path found. Try different nodes")
    
    # Algorithm explanation
    st.markdown("---")
    st.markdown("### Algorithm Details")
    
    explanations = st.session_state.ai_coach.get_algorithm_explanations()
    st.markdown(f"**{explanations['A* Search']}**")


# ============================================================================
# PAGE 6: ANALYTICS
# ============================================================================

def render_analytics():
    """Render analytics page with charts."""
    st.title("Analytics")
    st.markdown("<p style='color: #86868b; margin-top: -10px;'>Visualize your habit tracking data</p>", unsafe_allow_html=True)
    
    habits = st.session_state.habit_engine.get_all_habits()
    
    if not habits:
        st.info("No data yet. Start tracking habits to see analytics!")
        return
    
    # Overall stats
    stats = st.session_state.habit_engine.get_overall_statistics()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Habits", stats['total_habits'])
    with col2:
        st.metric("Total Completions", stats['total_completions'])
    with col3:
        st.metric("Completion Rate", f"{stats['overall_completion_rate']:.0%}")
    with col4:
        st.metric("Active Categories", stats['active_categories'])
    
    st.markdown("---")
    
    # Category breakdown
    st.markdown("### Category Breakdown")
    
    category_data = {}
    for habit in habits:
        habit_stats = st.session_state.habit_engine.get_habit_stats(habit['id'])
        cat = habit['category']
        if cat not in category_data:
            category_data[cat] = 0
        category_data[cat] += habit_stats.get('total_completions', 0)
    
    if category_data:
        fig = px.pie(
            values=list(category_data.values()),
            names=list(category_data.keys()),
            title="Completions by Category",
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        st.plotly_chart(fig, width='stretch')
    
    # Completion rates
    st.markdown("### Completion Rates (30 Days)")
    
    habit_names = []
    completion_rates = []
    
    for habit in habits:
        habit_stats = st.session_state.habit_engine.get_habit_stats(habit['id'])
        habit_names.append(habit['name'])
        completion_rates.append(habit_stats.get('completion_rate_30d', 0) * 100)
    
    if habit_names:
        fig = go.Figure(data=[
            go.Bar(
                x=habit_names,
                y=completion_rates,
                marker_color='#0071e3',
                text=[f"{rate:.0f}%" for rate in completion_rates],
                textposition='auto'
            )
        ])
        
        fig.update_layout(
            title="30-Day Completion Rate by Habit",
            xaxis_title="Habit",
            yaxis_title="Completion %",
            yaxis=dict(range=[0, 100])
        )
        
        st.plotly_chart(fig, width='stretch')
    
    # Weekly patterns
    st.markdown("### Weekly Patterns")
    
    selected_habit = st.selectbox(
        "Select habit to analyze:",
        options=[h['id'] for h in habits],
        format_func=lambda x: next(h['name'] for h in habits if h['id'] == x)
    )
    
    if selected_habit:
        pattern = st.session_state.habit_engine.analyze_weekly_pattern(selected_habit)
        
        days = list(pattern.keys())
        rates = [pattern[day] * 100 for day in days]
        
        fig = go.Figure(data=[
            go.Bar(
                x=days,
                y=rates,
                marker_color=['#0071e3'] * 7,
                text=[f"{rate:.0f}%" for rate in rates],
                textposition='auto'
            )
        ])
        
        fig.update_layout(
            title="Completion Rate by Day of Week",
            xaxis_title="Day",
            yaxis_title="Completion %",
            yaxis=dict(range=[0, 100])
        )
        
        st.plotly_chart(fig, width='stretch')


# ============================================================================
# PAGE 7: AI INSIGHTS
# ============================================================================

def render_ai_insights():
    """Render AI insights page showing all algorithms at work."""
    st.title("AI Insights")
    st.markdown("<p style='color: #86868b; margin-top: -10px;'>Explore the AI algorithms powering your coach</p>", unsafe_allow_html=True)
    
    # Get user data
    stats = st.session_state.habit_engine.get_overall_statistics()
    user_data = {
        "streak": stats.get('average_streak', 0),
        "completion_rate": stats.get('overall_completion_rate', 0),
        "total_habits": stats.get('total_habits', 0),
        "total_completions": stats.get('total_completions', 0),
        "habit_variety": stats.get('active_categories', 0),
        "missed_days": 0,  # Could calculate from data
        "morning_completion": 0.7,  # Placeholder
        "weekend_completion": 0.6  # Placeholder
    }
    
    # Expert System
    st.markdown("### Expert System (Rule-Based Inference)")
    st.info(st.session_state.ai_coach.get_algorithm_explanations()['Expert System'])
    
    expert_advice = st.session_state.ai_coach.expert_system.forward_chain(user_data, limit=5)
    
    if expert_advice:
        for i, rule in enumerate(expert_advice, 1):
            st.markdown(f"**Rule {rule['rule_id']}** ({rule['confidence']:.0%} confidence)")
            st.success(f"{rule['category'].upper()}: {rule['conclusion']}")
    else:
        st.warning("No expert rules fired. Keep tracking to unlock insights!")
    
    st.markdown("---")
    
    # Decision Tree
    st.markdown("### Decision Tree Recommendations")
    st.info(st.session_state.ai_coach.get_algorithm_explanations()['Decision Tree'])
    
    col1, col2 = st.columns(2)
    with col1:
        goal = st.selectbox("Your Goal", ["health", "productivity", "mindfulness", "learning"])
    with col2:
        time_available = st.number_input("Daily Time (minutes)", 10, 120, 30)
    
    if st.button("Get Recommendation"):
        # Build complete user profile for decision tree
        user_profile = {
            "root": goal,
            f"{goal}_node": time_available,
            "health_high_time": "beginner",  # Default experience level
            "productivity_high_time": "beginner",
            "mindfulness_high_time": "beginner",
            "learning_high_time": "beginner"
        }
        
        recommendation = st.session_state.ai_coach.decision_tree.get_recommendation(user_profile)
        
        if recommendation and "recommendation" in recommendation:
            st.success(f"**Recommended Habit:** {recommendation['recommendation']}")
            st.markdown(f"**Explanation:** {recommendation['explanation']}")
            st.markdown(f"**Category:** {recommendation['category']} | **Difficulty:** {recommendation['difficulty']}")
        else:
            st.error("Could not generate recommendation. Try different parameters!")
    
    
    st.markdown("---")
    
    # CSP Scheduling
    st.markdown("### CSP-Based Optimal Scheduling")
    st.info(st.session_state.ai_coach.get_algorithm_explanations()['CSP Solver'])
    
    habit_type = st.selectbox(
        "Habit Type to Schedule",
        ["exercise", "meditation", "deep_work", "learning", "reading", "creative"]
    )
    
    if st.button("Find Best Time"):
        result = st.session_state.ai_coach.recommend_best_time(habit_type)
        
        if "time_slot" in result:
            st.success(result['action_item'])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Score", f"{result['score']:.0f}/100")
            with col2:
                st.metric("Energy Level", f"{result['energy_level']}/10")
            with col3:
                st.metric("Distractions", f"{result['distraction_level']}/10")
            st.markdown(f"**Reasoning:** {result['reasoning']}")
    
    st.markdown("---")
    
    # === Q-LEARNING ===
    st.markdown("### 🎓 Q-Learning Time Optimizer")
    st.info(st.session_state.ai_coach.get_algorithm_explanations()['Q-Learning'])
    if st.button("Learn Optimal Time", key="q_btn"):
        # Simulate learning
        for h in range(6, 9):
            st.session_state.ai_coach.q_learner.update("exercise", h, True)
        result = st.session_state.ai_coach.q_learner.recommend_time("exercise")
        st.success(f"⏰ **Best Time:** {result['time_slot']} (Q-value: {result['q_value']:.1f})")
    
    st.markdown("---")
    
    # === BAYESIAN ===
    st.markdown("### 📊 Bayesian Success Predictor")
    st.info(st.session_state.ai_coach.get_algorithm_explanations()['Bayesian Inference'])
    if stats['total_completions'] > 0:
        pred = st.session_state.ai_coach.bayesian.predict_success(stats['total_completions'], 20)
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Success Probability", f"{pred['probability']:.0%}")
        with col2:
            st.metric("Confidence", f"{pred['confidence']:.0%}")
    
    st.markdown("---")
    
    # === MONTE CARLO ===
    st.markdown("### 🎲 Monte Carlo Simulator")
    st.info(st.session_state.ai_coach.get_algorithm_explanations()['Monte Carlo Simulation'])
    if st.button("Simulate 30-Day Goal", key="mc_btn"):
        result = st.session_state.ai_coach.monte_carlo.simulate_goal(0.7, 30, 21)
        st.success(f"🎯 **Success Chance:** {result['success_probability']:.0%}")
        st.metric("Expected Completions", f"{result['expected_completions']:.0f}")
    
    st.markdown("---")
    
    # === GENETIC ===
    st.markdown("### 🧬 Genetic Scheduler")
    st.info(st.session_state.ai_coach.get_algorithm_explanations()['Genetic Algorithm'])
    if st.button("Evolve Schedule", key="gen_btn"):
        habits = [h['name'] for h in st.session_state.habit_engine.get_all_habits()[:3]]
        if habits:
            result = st.session_state.ai_coach.genetic.evolve_schedule(habits, {})
            st.success(f"✨ Fitness: {result['fitness']:.0f}")
            for h, hour in result['schedule'].items():
                st.write(f"- {h}: {hour}:00")
    
    st.markdown("---")
    
    # === SIMULATED ANNEALING ===
    st.markdown("### 🔥 Simulated Annealing")
    st.info(st.session_state.ai_coach.get_algorithm_explanations()['Simulated Annealing'])
    if st.button("Optimize Order", key="sa_btn"):
        habits = [{'name': h['name'], 'difficulty': h['difficulty']} 
                 for h in st.session_state.habit_engine.get_all_habits()[:3]]
        if habits:
            result = st.session_state.ai_coach.annealing.optimize_order(habits)
            st.success(f"📋 **Order:** {' → '.join(result['optimal_order'])}")
    
    st.markdown("---")
    
    # === MINIMAX ===
    st.markdown("### ⚔️ Minimax Strategy")
    st.info(st.session_state.ai_coach.get_algorithm_explanations()['Minimax'])
    energy = st.slider("Energy", 0, 100, 70, key="mm_energy")
    if st.button("Strategic Pick", key="mm_btn"):
        habits = [{'name': h['name'], 'category': h['category'], 'difficulty': h['difficulty']}
                 for h in st.session_state.habit_engine.get_all_habits()[:3]]
        if habits:
            result = st.session_state.ai_coach.minimax.select_habit(habits, {'energy': energy})
            st.success(f"🎯 **Choice:** {result['selected_habit']}")
    
    st.markdown("---")
    
    # Algorithm Explanations
    st.markdown("### All AI Algorithms")
    
    explanations = st.session_state.ai_coach.get_algorithm_explanations()
    
    for algo_name, explanation in explanations.items():
        with st.expander(f"{algo_name}"):
            st.markdown(explanation)


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application entry point."""
    # Initialize authentication state FIRST - before anything else
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'current_user' not in st.session_state:
        st.session_state.current_user = None
    if 'show_signup' not in st.session_state:
        st.session_state.show_signup = False
    if 'auth_manager' not in st.session_state:
        st.session_state.auth_manager = AuthManager()
    
    # Now load CSS and initialize rest
    load_css()
    init_session_state()
    
    # Check authentication status
    if not st.session_state.logged_in:
        # Show login or signup page
        if st.session_state.show_signup:
            render_signup()
        else:
            render_login()
    else:
        # User is logged in - show main app
        # Render sidebar and get selected page
        page = render_sidebar()
        
        # Render selected page
        if page == "Dashboard":
            render_dashboard()
        elif page == "Add Habit":
            render_add_habit()
        elif page == "Log Progress":
            render_log_progress()
        elif page == "AI Coach":
            render_ai_coach()
        elif page == "Goal Planner":
            render_goal_planner()
        elif page == "Analytics":
            render_analytics()
        elif page == "AI Insights":
            render_ai_insights()


if __name__ == "__main__":
    main()
