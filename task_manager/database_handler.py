"""
Database handler for MongoDB operations.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
import pymongo
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from task_manager.task import Task


class DatabaseHandler:
    """
    Handles all database operations for tasks.
    
    This class encapsulates database connection and CRUD operations
    without using ORM, directly using pymongo.
    """
    
    def __init__(self, connection_string: str = "mongodb://localhost:27017/", 
                 database_name: str = "task_management"):
        """
        Initialize database handler.
        
        Args:
            connection_string: MongoDB connection string
            database_name: Name of the database to use
        """
        self._connection_string = connection_string
        self._database_name = database_name
        self._client: Optional[MongoClient] = None
        self._database = None
        self._collection = None
    
    def connect(self) -> bool:
        """
        Establish connection to MongoDB.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            self._client = MongoClient(self._connection_string, serverSelectionTimeoutMS=5000)
            # Test connection
            self._client.server_info()
            self._database = self._client[self._database_name]
            self._collection = self._database["tasks"]
            # Create index on task_id for faster lookups
            self._collection.create_index("task_id", unique=True)
            return True
        except ConnectionFailure:
            return False
        except Exception as e:
            print(f"Database connection error: {e}")
            return False
    
    def disconnect(self):
        """Close database connection."""
        if self._client:
            self._client.close()
            self._client = None
            self._database = None
            self._collection = None
    
    def is_connected(self) -> bool:
        """Check if database is connected."""
        try:
            if self._client:
                self._client.server_info()
                return True
        except:
            pass
        return False
    
    def insert_task(self, task: Task) -> bool:
        """
        Insert a new task into the database.
        
        Args:
            task: Task object to insert
            
        Returns:
            True if successful, False otherwise
        """
        if not self.is_connected():
            raise ConnectionError("Database not connected")
        
        try:
            task_dict = task.to_dict()
            # Convert datetime objects to ensure proper serialization
            task_dict["due_date"] = task_dict["due_date"]
            task_dict["created_at"] = task_dict["created_at"]
            self._collection.insert_one(task_dict)
            return True
        except pymongo.errors.DuplicateKeyError:
            raise ValueError(f"Task with ID {task.task_id} already exists")
        except Exception as e:
            raise Exception(f"Failed to insert task: {e}")
    
    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """
        Retrieve a task by its ID.
        
        Args:
            task_id: Unique task identifier
            
        Returns:
            Task object if found, None otherwise
        """
        if not self.is_connected():
            raise ConnectionError("Database not connected")
        
        try:
            result = self._collection.find_one({"task_id": task_id})
            if result:
                # Remove MongoDB _id field
                result.pop("_id", None)
                return Task.from_dict(result)
            return None
        except Exception as e:
            raise Exception(f"Failed to retrieve task: {e}")
    
    def get_all_tasks(self) -> List[Task]:
        """
        Retrieve all tasks from the database.
        
        Returns:
            List of Task objects
        """
        if not self.is_connected():
            raise ConnectionError("Database not connected")
        
        try:
            results = self._collection.find({})
            tasks = []
            for result in results:
                result.pop("_id", None)
                tasks.append(Task.from_dict(result))
            return tasks
        except Exception as e:
            raise Exception(f"Failed to retrieve tasks: {e}")
    
    def update_task(self, task_id: str, update_data: Dict[str, Any]) -> bool:
        """
        Update a task in the database.
        
        Args:
            task_id: Unique task identifier
            update_data: Dictionary with fields to update
            
        Returns:
            True if update successful, False if task not found
        """
        if not self.is_connected():
            raise ConnectionError("Database not connected")
        
        try:
            result = self._collection.update_one(
                {"task_id": task_id},
                {"$set": update_data}
            )
            return result.modified_count > 0
        except Exception as e:
            raise Exception(f"Failed to update task: {e}")
    
    def delete_task(self, task_id: str) -> bool:
        """
        Delete a task from the database.
        
        Args:
            task_id: Unique task identifier
            
        Returns:
            True if deletion successful, False if task not found
        """
        if not self.is_connected():
            raise ConnectionError("Database not connected")
        
        try:
            result = self._collection.delete_one({"task_id": task_id})
            return result.deleted_count > 0
        except Exception as e:
            raise Exception(f"Failed to delete task: {e}")
    
    def task_exists(self, task_id: str) -> bool:
        """
        Check if a task with given ID exists.
        
        Args:
            task_id: Unique task identifier
            
        Returns:
            True if task exists, False otherwise
        """
        if not self.is_connected():
            raise ConnectionError("Database not connected")
        
        try:
            return self._collection.count_documents({"task_id": task_id}) > 0
        except Exception as e:
            raise Exception(f"Failed to check task existence: {e}")

