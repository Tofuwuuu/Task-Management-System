"""
Task class representing a single task entity.
"""

from datetime import datetime
from typing import Optional


class Task:
    """
    Represents a task with all its attributes.
    
    Attributes:
        task_id (str): Unique identifier for the task
        title (str): Title of the task
        description (str): Detailed description of the task
        due_date (datetime): Due date for the task
        priority (str): Priority level (Low, Medium, High)
        status (str): Current status (Pending, In Progress, Completed)
        created_at (datetime): Timestamp when task was created
    """
    
    VALID_PRIORITIES = ["Low", "Medium", "High"]
    VALID_STATUSES = ["Pending", "In Progress", "Completed"]
    
    def __init__(
        self,
        task_id: str,
        title: str,
        description: str,
        due_date: datetime,
        priority: str,
        status: str = "Pending",
        created_at: Optional[datetime] = None
    ):
        """
        Initialize a Task object.
        
        Args:
            task_id: Unique identifier for the task
            title: Title of the task
            description: Detailed description
            due_date: Due date for the task
            priority: Priority level (Low, Medium, High)
            status: Current status (default: Pending)
            created_at: Creation timestamp (default: current time)
        """
        self._task_id = task_id
        self._title = title
        self._description = description
        self._due_date = due_date
        self._priority = priority
        self._status = status
        self._created_at = created_at if created_at else datetime.now()
    
    @property
    def task_id(self) -> str:
        """Get task ID."""
        return self._task_id
    
    @property
    def title(self) -> str:
        """Get task title."""
        return self._title
    
    @title.setter
    def title(self, value: str):
        """Set task title with validation."""
        if not value or not value.strip():
            raise ValueError("Title cannot be empty")
        self._title = value.strip()
    
    @property
    def description(self) -> str:
        """Get task description."""
        return self._description
    
    @description.setter
    def description(self, value: str):
        """Set task description."""
        self._description = value if value else ""
    
    @property
    def due_date(self) -> datetime:
        """Get due date."""
        return self._due_date
    
    @due_date.setter
    def due_date(self, value: datetime):
        """Set due date with validation."""
        if not isinstance(value, datetime):
            raise TypeError("Due date must be a datetime object")
        self._due_date = value
    
    @property
    def priority(self) -> str:
        """Get priority level."""
        return self._priority
    
    @priority.setter
    def priority(self, value: str):
        """Set priority with validation."""
        if value not in self.VALID_PRIORITIES:
            raise ValueError(f"Priority must be one of: {', '.join(self.VALID_PRIORITIES)}")
        self._priority = value
    
    @property
    def status(self) -> str:
        """Get task status."""
        return self._status
    
    @status.setter
    def status(self, value: str):
        """Set status with validation."""
        if value not in self.VALID_STATUSES:
            raise ValueError(f"Status must be one of: {', '.join(self.VALID_STATUSES)}")
        self._status = value
    
    @property
    def created_at(self) -> datetime:
        """Get creation timestamp."""
        return self._created_at
    
    def to_dict(self) -> dict:
        """
        Convert task to dictionary for database storage.
        
        Returns:
            Dictionary representation of the task
        """
        return {
            "task_id": self._task_id,
            "title": self._title,
            "description": self._description,
            "due_date": self._due_date,
            "priority": self._priority,
            "status": self._status,
            "created_at": self._created_at
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        """
        Create a Task object from a dictionary.
        
        Args:
            data: Dictionary containing task data
            
        Returns:
            Task object
        """
        return cls(
            task_id=data["task_id"],
            title=data["title"],
            description=data["description"],
            due_date=data["due_date"],
            priority=data["priority"],
            status=data.get("status", "Pending"),
            created_at=data.get("created_at")
        )
    
    def __str__(self) -> str:
        """String representation of the task."""
        return f"Task(ID: {self._task_id}, Title: {self._title}, Status: {self._status})"
    
    def __repr__(self) -> str:
        """Developer representation of the task."""
        return (f"Task(task_id='{self._task_id}', title='{self._title}', "
                f"status='{self._status}', priority='{self._priority}')")

