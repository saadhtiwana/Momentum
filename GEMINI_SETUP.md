# MOMENTUM - Gemini API Setup

## How to Enable Gemini AI

1. **Get your Gemini API Key:**
   - Go to https://aistudio.google.com/app/apikey
   - Click "Create API Key"
   - Copy your key

2. **Create secrets file:**
   - Create folder: `.streamlit` in your project directory
   - Create file: `.streamlit/secrets.toml`

3. **Add your key:**
   ```toml
   GEMINI_API_KEY = "your-api-key-here"
   ```

4. **Restart the app:**
   ```bash
   streamlit run app.py
   ```

## What Gemini Gets

The AI will have access to:
- All your habits with streaks and completion rates
- Your overall statistics
- Recent activity and progress
- Expert system insights
- Your message sentiment and intent

## Privacy Note

Your data stays local. Gemini only receives:
- Your message
- Anonymous habit statistics
- No personal identifying information

Enjoy personalized AI conversations! 🤖
