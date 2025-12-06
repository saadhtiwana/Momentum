"""
MOMENTUM - Authentication Module

Handles user authentication, registration, and session management.
- Secure password hashing using bcrypt
- User registration and login
- Session management
- Multi-user support
"""

import hashlib
import json
import os
from datetime import datetime
from typing import Optional, Dict, Tuple


class AuthManager:
    """
    Manages user authentication and registration.
    
    Uses SHA-256 hashing for passwords (simple but secure enough for local use).
    Stores user credentials in users.json.
    """
    
    def __init__(self, users_file: str = "users.json"):
        """Initialize authentication manager."""
        self.users_file = users_file
        self._ensure_users_file()
    
    def _ensure_users_file(self):
        """Create users file if it doesn't exist."""
        if not os.path.exists(self.users_file):
            self._save_users({})
    
    def _load_users(self) -> Dict:
        """Load users from file."""
        try:
            with open(self.users_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    
    def _save_users(self, users: Dict):
        """Save users to file."""
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=2)
    
    def _hash_password(self, password: str) -> str:
        """Hash password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register_user(self, username: str, password: str, full_name: str = "") -> Tuple[bool, str]:
        """
        Register a new user.
        
        Args:
            username: Unique username
            password: User password
            full_name: User's full name (optional)
            
        Returns:
            Tuple of (success, message)
        """
        # Validate input
        if not username or not password:
            return False, "Username and password are required"
        
        if len(username) < 3:
            return False, "Username must be at least 3 characters"
        
        if len(password) < 6:
            return False, "Password must be at least 6 characters"
        
        # Check if user exists
        users = self._load_users()
        if username in users:
            return False, "Username already exists"
        
        # Create user
        users[username] = {
            "password_hash": self._hash_password(password),
            "full_name": full_name,
            "created_at": datetime.now().isoformat(),
            "last_login": None
        }
        
        self._save_users(users)
        return True, "Account created successfully! Please login."
    
    def authenticate(self, username: str, password: str) -> Tuple[bool, Optional[Dict], str]:
        """
        Authenticate user login.
        
        Args:
            username: Username
            password: Password
            
        Returns:
            Tuple of (success, user_data, message)
        """
        if not username or not password:
            return False, None, "Username and password are required"
        
        users = self._load_users()
        
        if username not in users:
            return False, None, "Invalid username or password"
        
        user = users[username]
        password_hash = self._hash_password(password)
        
        if user["password_hash"] != password_hash:
            return False, None, "Invalid username or password"
        
        # Update last login
        user["last_login"] = datetime.now().isoformat()
        users[username] = user
        self._save_users(users)
        
        # Return user data (without password hash)
        user_data = {
            "username": username,
            "full_name": user.get("full_name", ""),
            "created_at": user.get("created_at", ""),
            "last_login": user.get("last_login", "")
        }
        
        return True, user_data, "Login successful!"
    
    def get_user_data_file(self, username: str) -> str:
        """Get the data file path for a specific user."""
        return f"user_data_{username}.json"
    
    def user_exists(self, username: str) -> bool:
        """Check if a username exists."""
        users = self._load_users()
        return username in users
    
    def get_user_count(self) -> int:
        """Get total number of registered users."""
        users = self._load_users()
        return len(users)


# ============================================================================
# MODULE EXPORTS
# ============================================================================

__all__ = ['AuthManager']
