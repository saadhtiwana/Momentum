# 🚀 MOMENTUM - Quick Start Guide

## Installation & Run Commands

### Step 1: Open Terminal/Command Prompt
Navigate to the project directory:
```bash
cd C:\Users\DELL\Desktop\AI\Momentum
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
streamlit run app.py
```

### Step 4: Open in Browser
The app will automatically open at: `http://localhost:8501`

If it doesn't open automatically, copy-paste that URL into your browser.

---

## That's It! 🎉

Your AI-powered habit coach is now running!

### Quick Tips:
- Start by creating a habit in "➕ Add Habit"
- Log your progress daily in "✅ Log Progress"
- Chat with the AI coach in "🤖 AI Coach"
- See your analytics in "📈 Analytics"
- Explore AI algorithms in "🧠 AI Insights"

---

## Troubleshooting

If you get errors:

**Error: "streamlit: command not found"**
```bash
python -m pip install --upgrade streamlit
```

**Error: Module not found**
```bash
pip install --upgrade -r requirements.txt
```

**Port already in use:**
```bash
streamlit run app.py --server.port 8502
```

---

Enjoy building better habits with AI! 💪
