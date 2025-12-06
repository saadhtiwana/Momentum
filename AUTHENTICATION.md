# MOMENTUM - User Authentication Guide

## ✨ New Authentication Features

### What's New
- **User Accounts**: Create personal accounts with username and password
- **Secure Storage**: Passwords hashed with SHA-256
- **Per-User Data**: Each user has their own habits and progress
- **Login/Logout**: Full session management
- **Multi-User Support**: Multiple users can use the same app

### How to Use

#### 1. Create an Account
- Run the app: `streamlit run app.py`
- Click "Create Account"
- Fill in:
  - Full Name
  - Username (minimum 3 characters)
  - Password (minimum 6 characters)
  - Confirm Password
- Click "Sign Up"

#### 2. Login
- Enter your username
- Enter your password
- Click "Login"
- You're in!

#### 3. Use the App
- All your habits are saved under your account
- Your data is separate from other users
- Track your personal progress

#### 4. Logout
- Click "Logout" button in the sidebar
- You'll be returned to the login screen

### Data Storage

**User Credentials**: `users.json`
```json
{
  "username": {
    "password_hash": "...",
    "full_name": "John Doe",
    "created_at": "2025-12-06T...",
    "last_login": "2025-12-06T..."
  }
}
```

**User Habit Data**: `user_data_username.json`
- Each user gets their own data file
- Format: `user_data_john.json`, `user_data_sarah.json`, etc.

### Security Features

✅ Password hashing (SHA-256)  
✅ No plain text passwords  
✅ Session management  
✅ Per-user data isolation  
✅ Secure logout (clears session)  

### Files Created

1. **`auth.py`** - Authentication module
   - User registration
   - Login authentication  
   - Password hashing
   - User management

2. **Updated `app.py`**
   - Login page
   - Signup page
   - Authentication guards
   - Logout button
   - User welcome message

### User Flow

```
Start App
    ↓
Not Logged In?
    ↓
Login/Signup Page
    ↓
Enter Credentials
    ↓
✅ Valid? → Load User Data → Dashboard
❌ Invalid? → Error Message → Try Again
    ↓
Use App (All Pages Available)
    ↓
Logout → Return to Login
```

### Apple-Style UI

- Clean login/signup forms
- Centered layout
- Minimal design
- Professional appearance
- Smooth transitions

## Try It Now!

```bash
streamlit run app.py
```

Create your first account and start tracking habits! 🚀
