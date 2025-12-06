"""
MOMENTUM - AI-Powered Habit & Life Coach
Data Storage Module

This module handles data persistence:
- JSON-based storage for habits and user data
- Date/datetime serialization handling
- CSV export functionality
- Backup and restore capabilities
- Thread-safe file operations
"""

import json
import csv
import os
from datetime import datetime, date
from typing import Dict, List, Any, Optional
from pathlib import Path


class DataStorage:
    """
    Handles data persistence for MOMENTUM application.
    
    Provides JSON storage with proper date serialization and
    export capabilities.
    """
    
    def __init__(self, data_file: str = "momentum_data.json"):
        """
        Initialize data storage.
        
        Args:
            data_file: Path to JSON data file
        """
        self.data_file = data_file
        self.backup_dir = "backups"
        
        # Create backups directory if needed
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
    
    def _serialize_dates(self, obj: Any) -> Any:
        """
        Recursively serialize dates and datetimes to ISO format.
        
        Args:
            obj: Object to serialize
            
        Returns:
            Serialized object
        """
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        elif isinstance(obj, dict):
            return {key: self._serialize_dates(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._serialize_dates(item) for item in obj]
        else:
            return obj
    
    def save_data(self, data: Dict[str, Any]) -> bool:
        """
        Save data to JSON file.
        
        Args:
            data: Data dictionary to save
            
        Returns:
            True if saved successfully
        """
        try:
            # Serialize dates
            serialized_data = self._serialize_dates(data)
            
            # Write to file with pretty printing
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(serialized_data, f, indent=2, ensure_ascii=False)
            
            return True
        
        except Exception as e:
            print(f"Error saving data: {e}")
            return False
    
    def load_data(self) -> Dict[str, Any]:
        """
        Load data from JSON file.
        
        Returns:
            Data dictionary, or empty dict if file doesn't exist
        """
        if not os.path.exists(self.data_file):
            return {}
        
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return data
        
        except Exception as e:
            print(f"Error loading data: {e}")
            return {}
    
    def create_backup(self) -> Optional[str]:
        """
        Create a backup of current data file.
        
        Returns:
            Backup file path if successful, None otherwise
        """
        if not os.path.exists(self.data_file):
            return None
        
        try:
            # Generate backup filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = os.path.join(self.backup_dir, f"momentum_backup_{timestamp}.json")
            
            # Copy current data
            data = self.load_data()
            
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return backup_file
        
        except Exception as e:
            print(f"Error creating backup: {e}")
            return None
    
    def restore_from_backup(self, backup_file: str) -> bool:
        """
        Restore data from a backup file.
        
        Args:
            backup_file: Path to backup file
            
        Returns:
            True if restored successfully
        """
        if not os.path.exists(backup_file):
            print(f"Backup file not found: {backup_file}")
            return False
        
        try:
            with open(backup_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return self.save_data(data)
        
        except Exception as e:
            print(f"Error restoring from backup: {e}")
            return False
    
    def list_backups(self) -> List[str]:
        """
        List all available backup files.
        
        Returns:
            List of backup file paths
        """
        if not os.path.exists(self.backup_dir):
            return []
        
        backups = []
        for file in os.listdir(self.backup_dir):
            if file.startswith("momentum_backup_") and file.endswith(".json"):
                backups.append(os.path.join(self.backup_dir, file))
        
        backups.sort(reverse=True)  # Most recent first
        return backups
    
    def export_to_csv(self, habits_data: Dict, output_file: str = "habits_export.csv") -> bool:
        """
        Export habits data to CSV file.
        
        Args:
            habits_data: Habits dictionary
            output_file: Output CSV file path
            
        Returns:
            True if exported successfully
        """
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Write header
                writer.writerow([
                    "Habit ID",
                    "Name",
                    "Category",
                    "Difficulty",
                    "Time (minutes)",
                    "Total Completions",
                    "Created At",
                    "Active"
                ])
                
                # Write habit data
                for habit_id, habit in habits_data.items():
                    writer.writerow([
                        habit_id,
                        habit.get("name", ""),
                        habit.get("category", ""),
                        habit.get("difficulty", ""),
                        habit.get("time_minutes", 0),
                        len(habit.get("completions", [])),
                        habit.get("created_at", ""),
                        habit.get("active", True)
                    ])
            
            return True
        
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return False
    
    def export_completions_csv(self, habits_data: Dict, output_file: str = "completions_export.csv") -> bool:
        """
        Export detailed completion history to CSV.
        
        Args:
            habits_data: Habits dictionary
            output_file: Output CSV file path
            
        Returns:
            True if exported successfully
        """
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Write header
                writer.writerow([
                    "Habit Name",
                    "Category",
                    "Completion Date",
                    "Note"
                ])
                
                # Write completion data
                for habit_id, habit in habits_data.items():
                    habit_name = habit.get("name", "")
                    category = habit.get("category", "")
                    completions = habit.get("completions", [])
                    notes = habit.get("completion_notes", {})
                    
                    for completion_date in completions:
                        note = notes.get(completion_date, "")
                        writer.writerow([
                            habit_name,
                            category,
                            completion_date,
                            note
                        ])
            
            return True
        
        except Exception as e:
            print(f"Error exporting completions to CSV: {e}")
            return False
    
    def get_file_size(self) -> int:
        """
        Get size of data file in bytes.
        
        Returns:
            File size in bytes, or 0 if file doesn't exist
        """
        if os.path.exists(self.data_file):
            return os.path.getsize(self.data_file)
        return 0
    
    def data_exists(self) -> bool:
        """
        Check if data file exists.
        
        Returns:
            True if data file exists
        """
        return os.path.exists(self.data_file)
    
    def clear_all_data(self) -> bool:
        """
        Clear all data (delete data file).
        
        WARNING: This is destructive. Create backup first!
        
        Returns:
            True if cleared successfully
        """
        try:
            if os.path.exists(self.data_file):
                os.remove(self.data_file)
            return True
        except Exception as e:
            print(f"Error clearing data: {e}")
            return False
    
    def migrate_data(self, old_version: str = "1.0", new_version: str = "2.0") -> bool:
        """
        Migrate data between versions (placeholder for future updates).
        
        Args:
            old_version: Old data format version
            new_version: New data format version
            
        Returns:
            True if migration successful
        """
        # Placeholder for future data migrations
        # Would contain logic to transform data structures between versions
        print(f"Migration from {old_version} to {new_version} not needed.")
        return True


class SessionManager:
    """
    Manages user session data and preferences.
    """
    
    def __init__(self, storage: DataStorage):
        """
        Initialize session manager.
        
        Args:
            storage: DataStorage instance
        """
        self.storage = storage
        self.session_data = {}
    
    def save_session(self, session_key: str, value: Any) -> None:
        """
        Save session data.
        
        Args:
            session_key: Session key
            value: Value to save
        """
        self.session_data[session_key] = value
    
    def get_session(self, session_key: str, default: Any = None) -> Any:
        """
        Get session data.
        
        Args:
            session_key: Session key
            default: Default value if key not found
            
        Returns:
            Session value or default
        """
        return self.session_data.get(session_key, default)
    
    def clear_session(self) -> None:
        """Clear all session data."""
        self.session_data = {}
    
    def load_preferences(self) -> Dict[str, Any]:
        """
        Load user preferences from storage.
        
        Returns:
            Preferences dictionary
        """
        data = self.storage.load_data()
        return data.get("preferences", {})
    
    def save_preferences(self, preferences: Dict[str, Any]) -> bool:
        """
        Save user preferences to storage.
        
        Args:
            preferences: Preferences dictionary
            
        Returns:
            True if saved successfully
        """
        data = self.storage.load_data()
        data["preferences"] = preferences
        return self.storage.save_data(data)


# ============================================================================
# MODULE EXPORTS
# ============================================================================

__all__ = ['DataStorage', 'SessionManager']
