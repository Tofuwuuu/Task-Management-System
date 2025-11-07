"""
Input validation utilities.
"""

from datetime import datetime
from typing import Optional


class Validators:
    """Static utility class for input validation."""
    
    @staticmethod
    def validate_title(title: str) -> str:
        """
        Validate and sanitize task title.
        
        Args:
            title: Title string to validate
            
        Returns:
            Sanitized title
            
        Raises:
            ValueError: If title is invalid
        """
        if not title or not title.strip():
            raise ValueError("Title cannot be empty")
        return title.strip()
    
    @staticmethod
    def validate_priority(priority: str) -> str:
        """
        Validate priority level.
        
        Handles case-insensitive input and converts to proper format.
        Examples: "high" -> "High", "MEDIUM" -> "Medium"
        
        Args:
            priority: Priority string to validate
            
        Returns:
            Validated priority (properly formatted)
            
        Raises:
            ValueError: If priority is invalid
        """
        valid_priorities = ["Low", "Medium", "High"]
        priority_lower = priority.strip().lower()
        
        # Map lowercase variations to proper format
        priority_map = {
            "low": "Low",
            "medium": "Medium",
            "high": "High"
        }
        
        if priority_lower in priority_map:
            return priority_map[priority_lower]
        
        # If direct match fails, try case-insensitive comparison
        for valid_priority in valid_priorities:
            if valid_priority.lower() == priority_lower:
                return valid_priority
        
        raise ValueError(f"Priority must be one of: {', '.join(valid_priorities)}")
    
    @staticmethod
    def validate_status(status: str) -> str:
        """
        Validate task status.
        
        Handles case-insensitive input and converts to proper format.
        Examples: "in progress" -> "In Progress", "PENDING" -> "Pending"
        
        Args:
            status: Status string to validate
            
        Returns:
            Validated status (properly formatted)
            
        Raises:
            ValueError: If status is invalid
        """
        valid_statuses = ["Pending", "In Progress", "Completed"]
        status_lower = status.strip().lower()
        
        # Map lowercase variations to proper format
        status_map = {
            "pending": "Pending",
            "in progress": "In Progress",
            "completed": "Completed"
        }
        
        if status_lower in status_map:
            return status_map[status_lower]
        
        # If direct match fails, try case-insensitive comparison
        for valid_status in valid_statuses:
            if valid_status.lower() == status_lower:
                return valid_status
        
        raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
    
    @staticmethod
    def validate_date(date_string: str, date_format: str = "%Y-%m-%d") -> datetime:
        """
        Validate and parse date string.
        
        Args:
            date_string: Date string to parse
            date_format: Expected date format (default: YYYY-MM-DD)
            
        Returns:
            Parsed datetime object
            
        Raises:
            ValueError: If date format is invalid
        """
        try:
            return datetime.strptime(date_string.strip(), date_format)
        except ValueError:
            raise ValueError(f"Invalid date format. Expected format: {date_format}")
    
    @staticmethod
    def validate_task_id(task_id: str) -> str:
        """
        Validate task ID format.
        
        Args:
            task_id: Task ID string to validate
            
        Returns:
            Sanitized task ID
            
        Raises:
            ValueError: If task ID is invalid
        """
        if not task_id or not task_id.strip():
            raise ValueError("Task ID cannot be empty")
        return task_id.strip()
    
    @staticmethod
    def validate_description(description: Optional[str]) -> str:
        """
        Validate and sanitize description.
        
        Args:
            description: Description string to validate
            
        Returns:
            Sanitized description (empty string if None)
        """
        return description.strip() if description and description.strip() else ""
    
    @staticmethod
    def validate_menu_choice(choice: str, min_val: int = 1, max_val: int = 9) -> str:
        """
        Validate menu choice input.
        
        Args:
            choice: Menu choice string to validate
            min_val: Minimum valid choice (default: 1)
            max_val: Maximum valid choice (default: 9)
            
        Returns:
            Validated choice string
            
        Raises:
            ValueError: If choice is invalid
        """
        choice = choice.strip()
        if not choice:
            raise ValueError("Choice cannot be empty")
        
        try:
            choice_num = int(choice)
            if choice_num < min_val or choice_num > max_val:
                raise ValueError(f"Choice must be between {min_val} and {max_val}")
            return choice
        except ValueError as e:
            if "Choice must be" in str(e):
                raise
            raise ValueError(f"Invalid choice format. Must be a number between {min_val} and {max_val}")
    
    @staticmethod
    def validate_sort_choice(choice: str) -> str:
        """
        Validate sort option choice.
        
        Args:
            choice: Sort choice string (1-5)
            
        Returns:
            Validated choice string
            
        Raises:
            ValueError: If choice is invalid
        """
        choice = choice.strip()
        if not choice:
            return "1"  # Default to option 1
        
        valid_choices = ["1", "2", "3", "4", "5"]
        if choice not in valid_choices:
            raise ValueError("Sort choice must be between 1 and 5")
        return choice
    
    @staticmethod
    def validate_confirmation(confirm: str) -> bool:
        """
        Validate confirmation input (yes/no).
        
        Args:
            confirm: Confirmation string
            
        Returns:
            True if confirmed, False otherwise
            
        Raises:
            ValueError: If input is invalid
        """
        confirm = confirm.strip().lower()
        valid_confirmations = ["yes", "y", "no", "n", ""]
        
        if confirm not in valid_confirmations:
            raise ValueError("Confirmation must be 'yes' or 'no'")
        
        return confirm in ["yes", "y"]

