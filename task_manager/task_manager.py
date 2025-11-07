"""
TaskManager class for managing tasks with in-memory operations and database persistence.
"""

from typing import List, Optional, Dict, Any, Callable
from datetime import datetime
import uuid
from task_manager.task import Task
from task_manager.database_handler import DatabaseHandler
from task_manager.validators import Validators


class TaskManager:
    """
    Manages tasks with in-memory data structures and database persistence.
    
    This class uses a dictionary for O(1) lookups and implements
    custom sorting and filtering algorithms.
    """
    
    def __init__(self, db_handler: DatabaseHandler):
        """
        Initialize TaskManager.
        
        Args:
            db_handler: DatabaseHandler instance for persistence
        """
        self._db_handler = db_handler
        # Use dictionary for O(1) task lookups by ID
        self._tasks: Dict[str, Task] = {}
        # List for maintaining insertion order and efficient iteration
        self._task_list: List[Task] = []
    
    def load_tasks_from_db(self) -> bool:
        """
        Load all tasks from database into memory.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            tasks = self._db_handler.get_all_tasks()
            self._tasks.clear()
            self._task_list.clear()
            for task in tasks:
                self._tasks[task.task_id] = task
                self._task_list.append(task)
            return True
        except Exception as e:
            print(f"Error loading tasks from database: {e}")
            return False
    
    def add_task(
        self,
        title: str,
        description: str,
        due_date: datetime,
        priority: str,
        status: str = "Pending"
    ) -> Task:
        """
        Add a new task.
        
        Args:
            title: Task title
            description: Task description
            due_date: Due date
            priority: Priority level
            status: Task status (default: Pending)
            
        Returns:
            Created Task object
            
        Raises:
            ValueError: If validation fails
        """
        # Validate inputs
        title = Validators.validate_title(title)
        description = Validators.validate_description(description)
        priority = Validators.validate_priority(priority)
        status = Validators.validate_status(status)
        
        # Generate unique task ID
        task_id = str(uuid.uuid4())
        
        # Create task object
        task = Task(
            task_id=task_id,
            title=title,
            description=description,
            due_date=due_date,
            priority=priority,
            status=status
        )
        
        # Persist to database
        try:
            self._db_handler.insert_task(task)
            # Add to in-memory structures
            self._tasks[task_id] = task
            self._task_list.append(task)
            return task
        except ValueError as e:
            raise ValueError(f"Cannot add task: {e}")
        except Exception as e:
            raise Exception(f"Database error: {e}")
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """
        Get a task by ID.
        
        Supports both full UUID and partial ID (first 8 characters).
        
        Args:
            task_id: Unique task identifier (full UUID or first 8 characters)
            
        Returns:
            Task object if found, None otherwise
        """
        # Try exact match first
        if task_id in self._tasks:
            return self._tasks[task_id]
        
        # Try partial match (first 8 characters)
        task_id_lower = task_id.lower()
        for full_id, task in self._tasks.items():
            if full_id.lower().startswith(task_id_lower):
                return task
        
        return None
    
    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks.
        
        Returns:
            List of all tasks
        """
        return self._task_list.copy()
    
    def update_task(
        self,
        task_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        due_date: Optional[datetime] = None,
        priority: Optional[str] = None,
        status: Optional[str] = None
    ) -> bool:
        """
        Update task details.
        
        Supports both full UUID and partial ID (first 8 characters).
        
        Args:
            task_id: Unique task identifier (full UUID or first 8 characters)
            title: New title (optional)
            description: New description (optional)
            due_date: New due date (optional)
            priority: New priority (optional)
            status: New status (optional)
            
        Returns:
            True if update successful, False if task not found
            
        Raises:
            ValueError: If validation fails
        """
        # Find the task (supports partial ID)
        task = self.get_task(task_id)
        if not task:
            return False
        
        # Use the full task ID for database operations
        full_task_id = task.task_id
        
        # Build update dictionary
        update_data = {}
        
        if title is not None:
            task.title = Validators.validate_title(title)
            update_data["title"] = task.title
        
        if description is not None:
            task.description = Validators.validate_description(description)
            update_data["description"] = task.description
        
        if due_date is not None:
            task.due_date = due_date
            update_data["due_date"] = due_date
        
        if priority is not None:
            task.priority = Validators.validate_priority(priority)
            update_data["priority"] = task.priority
        
        if status is not None:
            task.status = Validators.validate_status(status)
            update_data["status"] = task.status
        
        # Update in database using full task ID
        try:
            if update_data:
                self._db_handler.update_task(full_task_id, update_data)
            return True
        except Exception as e:
            raise Exception(f"Database error: {e}")
    
    def mark_completed(self, task_id: str) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id: Unique task identifier
            
        Returns:
            True if successful, False if task not found
        """
        return self.update_task(task_id, status="Completed")
    
    def delete_task(self, task_id: str) -> bool:
        """
        Delete a task.
        
        Supports both full UUID and partial ID (first 8 characters).
        
        Args:
            task_id: Unique task identifier (full UUID or first 8 characters)
            
        Returns:
            True if deletion successful, False if task not found
        """
        # Find the task (supports partial ID)
        task = self.get_task(task_id)
        if not task:
            return False
        
        # Use the full task ID for deletion
        full_task_id = task.task_id
        
        try:
            # Delete from database using full ID
            self._db_handler.delete_task(full_task_id)
            # Remove from in-memory structures
            del self._tasks[full_task_id]
            self._task_list = [t for t in self._task_list if t.task_id != full_task_id]
            return True
        except Exception as e:
            raise Exception(f"Database error: {e}")
    
    def filter_tasks(
        self,
        priority: Optional[str] = None,
        status: Optional[str] = None,
        due_date: Optional[datetime] = None,
        due_date_before: Optional[datetime] = None,
        due_date_after: Optional[datetime] = None
    ) -> List[Task]:
        """
        Filter tasks based on criteria.
        
        Custom filtering algorithm that efficiently filters tasks
        using list comprehension and conditional checks.
        
        Args:
            priority: Filter by priority level
            status: Filter by status
            due_date: Filter by exact due date
            due_date_before: Filter tasks with due date before this date
            due_date_after: Filter tasks with due date after this date
            
        Returns:
            List of filtered tasks
        """
        filtered = self._task_list.copy()
        
        # Filter by priority
        if priority:
            priority = Validators.validate_priority(priority)
            filtered = [t for t in filtered if t.priority == priority]
        
        # Filter by status
        if status:
            status = Validators.validate_status(status)
            filtered = [t for t in filtered if t.status == status]
        
        # Filter by exact due date
        if due_date:
            filtered = [t for t in filtered if t.due_date.date() == due_date.date()]
        
        # Filter by due date before
        if due_date_before:
            filtered = [t for t in filtered if t.due_date < due_date_before]
        
        # Filter by due date after
        if due_date_after:
            filtered = [t for t in filtered if t.due_date > due_date_after]
        
        return filtered
    
    def sort_tasks(
        self,
        tasks: List[Task],
        sort_by: str = "created_at",
        reverse: bool = False
    ) -> List[Task]:
        """
        Sort tasks using custom sorting algorithm.
        
        Implements a stable sort based on the specified field.
        
        Args:
            tasks: List of tasks to sort
            sort_by: Field to sort by (created_at, due_date, priority, status, title)
            reverse: Sort in descending order if True
            
        Returns:
            Sorted list of tasks
        """
        valid_sort_fields = ["created_at", "due_date", "priority", "status", "title"]
        if sort_by not in valid_sort_fields:
            raise ValueError(f"Invalid sort field. Must be one of: {', '.join(valid_sort_fields)}")
        
        # Priority order mapping for custom sorting
        priority_order = {"High": 3, "Medium": 2, "Low": 1}
        status_order = {"Pending": 1, "In Progress": 2, "Completed": 3}
        
        def get_sort_key(task: Task) -> Any:
            """Get sort key based on sort_by field."""
            if sort_by == "priority":
                return priority_order.get(task.priority, 0)
            elif sort_by == "status":
                return status_order.get(task.status, 0)
            elif sort_by == "title":
                return task.title.lower()
            else:
                return getattr(task, sort_by)
        
        # Use Python's built-in sorted with custom key
        # This is efficient and stable
        sorted_tasks = sorted(tasks, key=get_sort_key, reverse=reverse)
        return sorted_tasks
    
    def get_task_count(self) -> int:
        """
        Get total number of tasks.
        
        Returns:
            Number of tasks
        """
        return len(self._task_list)

