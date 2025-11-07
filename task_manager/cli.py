"""
Command-line interface for the Task Management application.
"""

from typing import Optional, List, Callable
from datetime import datetime
import threading
from task_manager.task_manager import TaskManager
from task_manager.task import Task
from task_manager.validators import Validators


class CLI:
    """
    Command-line interface for task management.
    
    Provides an intuitive CLI with clear instructions and feedback.
    """
    
    def __init__(self, task_manager: TaskManager):
        """
        Initialize CLI.
        
        Args:
            task_manager: TaskManager instance
        """
        self._task_manager = task_manager
        self._running = True
        self._background_thread: Optional[threading.Thread] = None
        self._background_stats: Optional[dict] = None
    
    def display_menu(self):
        """Display the main menu."""
        print("\n" + "=" * 60)
        print("           TASK MANAGEMENT APPLICATION")
        print("=" * 60)
        print("\nOptions:")
        print("  1. Add a new task")
        print("  2. List all tasks")
        print("  3. Filter tasks")
        print("  4. Update a task")
        print("  5. Mark task as completed")
        print("  6. Delete a task")
        print("  7. View task details")
        print("  8. View background statistics")
        print("  9. Exit")
        print("=" * 60)
    
    def display_task(self, task: Task, detailed: bool = False):
        """
        Display a single task.
        
        Args:
            task: Task object to display
            detailed: If True, show detailed information
        """
        if detailed:
            print("\n" + "-" * 60)
            print(f"Task ID: {task.task_id}")
            print(f"Title: {task.title}")
            print(f"Description: {task.description}")
            print(f"Due Date: {task.due_date.strftime('%Y-%m-%d')}")
            print(f"Priority: {task.priority}")
            print(f"Status: {task.status}")
            print(f"Created At: {task.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print("-" * 60)
        else:
            print(f"  [{task.task_id[:8]}...] {task.title:<30} | "
                  f"Priority: {task.priority:<8} | Status: {task.status:<12} | "
                  f"Due: {task.due_date.strftime('%Y-%m-%d')}")
    
    def display_tasks(self, tasks: List[Task], title: str = "Tasks"):
        """
        Display a list of tasks.
        
        Args:
            tasks: List of tasks to display
            title: Title for the task list
        """
        if not tasks:
            print(f"\nNo {title.lower()} found.")
            return
        
        print(f"\n{title} ({len(tasks)}):")
        print("-" * 100)
        print(f"{'ID (first 8)':<12} {'Title':<30} {'Priority':<10} {'Status':<15} {'Due Date':<12}")
        print("-" * 100)
        for task in tasks:
            print(f"{task.task_id[:8]:<12} {task.title[:28]:<30} {task.priority:<10} "
                  f"{task.status:<15} {task.due_date.strftime('%Y-%m-%d'):<12}")
        print("-" * 100)
        print("\n[NOTE] You can use the first 8 characters of the ID to reference tasks.")
    
    def get_input(self, prompt: str, validator: Optional[Callable] = None, 
                  default: Optional[str] = None) -> str:
        """
        Get user input with optional validation.
        
        Args:
            prompt: Input prompt
            validator: Optional validation function
            default: Default value if input is empty
            
        Returns:
            Validated input string
        """
        while True:
            try:
                if default:
                    user_input = input(f"{prompt} (default: {default}): ").strip()
                    if not user_input:
                        return default
                else:
                    user_input = input(f"{prompt}: ").strip()
                    if not user_input:
                        print("This field is required. Please try again.")
                        continue
                
                if validator:
                    return validator(user_input)
                return user_input
            except ValueError as e:
                print(f"Invalid input: {e}. Please try again.")
            except KeyboardInterrupt:
                print("\n\nOperation cancelled.")
                return None
            except Exception as e:
                print(f"Error: {e}. Please try again.")
    
    def add_task(self):
        """Handle adding a new task."""
        print("\n--- Add New Task ---")
        
        try:
            title = self.get_input("Enter task title", Validators.validate_title)
            if not title:
                return
            
            description = self.get_input("Enter task description (optional)", 
                                        default="")
            
            due_date_input = input("Enter due date (YYYY-MM-DD): ").strip()
            if not due_date_input:
                print("Due date is required.")
                return
            due_date = Validators.validate_date(due_date_input)
            
            priority = self.get_input("Enter priority (Low/Medium/High)", 
                                     Validators.validate_priority)
            if not priority:
                return
            
            status = self.get_input("Enter status (Pending/In Progress/Completed)", 
                                   Validators.validate_status, default="Pending")
            if not status:
                return
            
            task = self._task_manager.add_task(
                title=title,
                description=description,
                due_date=due_date,
                priority=priority,
                status=status
            )
            
            print(f"\n[OK] Task added successfully!")
            print(f"  Task ID: {task.task_id}")
            
        except ValueError as e:
            print(f"\n[ERROR] Error: {e}")
        except Exception as e:
            print(f"\n[ERROR] Error adding task: {e}")
    
    def list_tasks(self):
        """Handle listing all tasks."""
        print("\n--- All Tasks ---")
        
        try:
            tasks = self._task_manager.get_all_tasks()
            
            if not tasks:
                print("\nNo tasks found.")
                return
            
            # Ask for sorting preference
            print("\nSort options:")
            print("  1. By creation date (default)")
            print("  2. By due date")
            print("  3. By priority")
            print("  4. By status")
            print("  5. By title")
            
            sort_choice_input = input("\nChoose sort option (1-5, default: 1): ").strip()
            try:
                sort_choice = Validators.validate_sort_choice(sort_choice_input)
            except ValueError as e:
                print(f"[ERROR] {e}. Using default option 1.")
                sort_choice = "1"
            
            sort_map = {
                "1": "created_at",
                "2": "due_date",
                "3": "priority",
                "4": "status",
                "5": "title"
            }
            sort_by = sort_map.get(sort_choice, "created_at")
            
            reverse = input("Sort in descending order? (y/N): ").strip().lower() == 'y'
            
            sorted_tasks = self._task_manager.sort_tasks(tasks, sort_by=sort_by, reverse=reverse)
            self.display_tasks(sorted_tasks)
            
        except Exception as e:
            print(f"\n[ERROR] Error listing tasks: {e}")
    
    def filter_tasks(self):
        """Handle filtering tasks."""
        print("\n--- Filter Tasks ---")
        
        try:
            print("\nFilter options (press Enter to skip):")
            
            priority = None
            priority_input = input("Filter by priority (Low/Medium/High): ").strip()
            if priority_input:
                priority = Validators.validate_priority(priority_input)
            
            status = None
            status_input = input("Filter by status (Pending/In Progress/Completed): ").strip()
            if status_input:
                status = Validators.validate_status(status_input)
            
            due_date = None
            due_date_input = input("Filter by exact due date (YYYY-MM-DD): ").strip()
            if due_date_input:
                due_date = Validators.validate_date(due_date_input)
            
            due_before = None
            due_before_input = input("Filter tasks due before (YYYY-MM-DD): ").strip()
            if due_before_input:
                due_before = Validators.validate_date(due_before_input)
            
            due_after = None
            due_after_input = input("Filter tasks due after (YYYY-MM-DD): ").strip()
            if due_after_input:
                due_after = Validators.validate_date(due_after_input)
            
            if not any([priority, status, due_date, due_before, due_after]):
                print("\nNo filter criteria provided. Showing all tasks.")
                tasks = self._task_manager.get_all_tasks()
            else:
                tasks = self._task_manager.filter_tasks(
                    priority=priority,
                    status=status,
                    due_date=due_date,
                    due_date_before=due_before,
                    due_date_after=due_after
                )
            
            self.display_tasks(tasks, "Filtered Tasks")
            
        except ValueError as e:
            print(f"\n[ERROR] Error: {e}")
        except Exception as e:
            print(f"\n[ERROR] Error filtering tasks: {e}")
    
    def update_task(self):
        """Handle updating a task."""
        print("\n--- Update Task ---")
        
        try:
            # Show list of tasks first so user can see available IDs
            tasks = self._task_manager.get_all_tasks()
            if tasks:
                print("\nAvailable tasks:")
                self.display_tasks(tasks, "Tasks")
            
            task_id = self.get_input("Enter task ID to update (Ctrl+C to cancel)", Validators.validate_task_id)
            if not task_id:
                return
            
            task = self._task_manager.get_task(task_id)
            if not task:
                print(f"\n[ERROR] Task with ID '{task_id}' not found.")
                print("[INFO] You can use the first 8 characters of the task ID shown in the list.")
                return
            
            print("\nCurrent task details:")
            self.display_task(task, detailed=True)
            
            print("\nEnter new values (press Enter to keep current value):")
            
            title = input(f"Title [{task.title}]: ").strip()
            if title:
                try:
                    title = Validators.validate_title(title)
                except ValueError as e:
                    print(f"[ERROR] {e}")
                    title = None
            else:
                title = None
            
            description = input(f"Description [{task.description}]: ").strip()
            description = description if description else None
            
            due_date_str = input(f"Due date (YYYY-MM-DD) [{task.due_date.strftime('%Y-%m-%d')}]: ").strip()
            due_date = Validators.validate_date(due_date_str) if due_date_str else None
            
            priority = input(f"Priority (Low/Medium/High) [{task.priority}]: ").strip()
            priority = Validators.validate_priority(priority) if priority else None
            
            status = input(f"Status (Pending/In Progress/Completed) [{task.status}]: ").strip()
            status = Validators.validate_status(status) if status else None
            
            if self._task_manager.update_task(
                task_id=task_id,
                title=title,
                description=description,
                due_date=due_date,
                priority=priority,
                status=status
            ):
                print("\n[OK] Task updated successfully!")
            else:
                print("\n[ERROR] Failed to update task.")
                
        except ValueError as e:
            print(f"\n[ERROR] Error: {e}")
        except Exception as e:
            print(f"\n[ERROR] Error updating task: {e}")
    
    def mark_completed(self):
        """Handle marking a task as completed."""
        print("\n--- Mark Task as Completed ---")
        
        try:
            # Show list of tasks first so user can see available IDs
            tasks = self._task_manager.get_all_tasks()
            if tasks:
                print("\nAvailable tasks:")
                self.display_tasks(tasks, "Tasks")
            
            task_id = self.get_input("Enter task ID to mark as completed (Ctrl+C to cancel)", 
                                    Validators.validate_task_id)
            if not task_id:
                return
            
            task = self._task_manager.get_task(task_id)
            if not task:
                print(f"\n[ERROR] Task with ID '{task_id}' not found.")
                print("[INFO] You can use the first 8 characters of the task ID shown in the list.")
            elif self._task_manager.mark_completed(task_id):
                print("\n[OK] Task marked as completed!")
            else:
                print(f"\n[ERROR] Failed to mark task as completed.")
                
        except ValueError as e:
            print(f"\n[ERROR] Error: {e}")
        except Exception as e:
            print(f"\n[ERROR] Error marking task: {e}")
    
    def delete_task(self):
        """Handle deleting a task."""
        print("\n--- Delete Task ---")
        
        try:
            # Show list of tasks first so user can see available IDs
            tasks = self._task_manager.get_all_tasks()
            if tasks:
                print("\nAvailable tasks:")
                self.display_tasks(tasks, "Tasks")
            
            task_id = self.get_input("Enter task ID to delete (Ctrl+C to cancel)", Validators.validate_task_id)
            if not task_id:
                return
            
            task = self._task_manager.get_task(task_id)
            if not task:
                print(f"\n[ERROR] Task with ID '{task_id}' not found.")
                print("[INFO] You can use the first 8 characters of the task ID shown in the list.")
                return
            
            print("\nTask to delete:")
            self.display_task(task, detailed=True)
            print(f"\n[INFO] Full Task ID: {task.task_id}")
            
            confirm_input = input("\nAre you sure you want to delete this task? (yes/no): ").strip()
            try:
                confirm = Validators.validate_confirmation(confirm_input)
            except ValueError as e:
                print(f"[ERROR] {e}")
                confirm = False
            
            if confirm:
                if self._task_manager.delete_task(task_id):
                    print("\n[OK] Task deleted successfully!")
                else:
                    print("\n[ERROR] Failed to delete task.")
            else:
                print("\nDeletion cancelled.")
                
        except ValueError as e:
            print(f"\n[ERROR] Error: {e}")
        except Exception as e:
            print(f"\n[ERROR] Error deleting task: {e}")
    
    def view_task_details(self):
        """Handle viewing detailed task information."""
        print("\n--- View Task Details ---")
        
        try:
            # Show list of tasks first so user can see available IDs
            tasks = self._task_manager.get_all_tasks()
            if tasks:
                print("\nAvailable tasks:")
                self.display_tasks(tasks, "Tasks")
            
            task_id = self.get_input("Enter task ID (Ctrl+C to cancel)", Validators.validate_task_id)
            if not task_id:
                return
            
            task = self._task_manager.get_task(task_id)
            if task:
                self.display_task(task, detailed=True)
            else:
                print(f"\n[ERROR] Task with ID '{task_id}' not found.")
                print("[INFO] You can use the first 8 characters of the task ID shown in the list.")
                
        except ValueError as e:
            print(f"\n[ERROR] Error: {e}")
        except Exception as e:
            print(f"\n[ERROR] Error viewing task: {e}")
    
    def view_background_stats(self):
        """
        Display background statistics calculated by the background thread.
        
        This demonstrates that background operations are running concurrently
        while the user performs other operations like adding tasks.
        """
        print("\n--- Background Statistics ---")
        print("\n[INFO] These statistics are calculated by a background thread")
        print("       that runs concurrently while you use the application.\n")
        
        if self._background_stats:
            stats = self._background_stats
            print(f"Last Updated: {stats['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
            print("-" * 60)
            print(f"Total Tasks: {stats['total']}")
            print(f"  - Completed: {stats['completed']}")
            print(f"  - In Progress: {stats['in_progress']}")
            print(f"  - Pending: {stats['pending']}")
            print(f"\nOverdue Tasks: {stats['overdue']}")
            print(f"High Priority Pending: {stats['high_priority_pending']}")
            
            if stats['total'] > 0:
                completion_rate = (stats['completed'] / stats['total']) * 100
                print(f"\nCompletion Rate: {completion_rate:.1f}%")
        else:
            print("[INFO] Background statistics are being calculated...")
            print("       (Statistics update every 10 seconds)")
            print("       Try adding some tasks and check back!")
        
        print("\n[NOTE] The background thread continues running even while")
        print("       you add, update, or delete tasks - demonstrating")
        print("       concurrent operations with multithreading!")
    
    def background_task_cleanup(self):
        """
        Background thread function for periodic operations.
        
        This demonstrates multithreading capability by performing
        background operations while the user interacts with the application.
        """
        import time
        from datetime import datetime
        
        while self._running:
            try:
                # Wait 10 seconds between background operations
                threading.Event().wait(10)
                
                if not self._running:
                    break
                
                # Perform background operations while user can still interact
                tasks = self._task_manager.get_all_tasks()
                
                if tasks:
                    # Calculate statistics in the background
                    total_tasks = len(tasks)
                    completed = sum(1 for t in tasks if t.status == "Completed")
                    in_progress = sum(1 for t in tasks if t.status == "In Progress")
                    pending = sum(1 for t in tasks if t.status == "Pending")
                    
                    # Check for overdue tasks
                    now = datetime.now()
                    overdue = sum(1 for t in tasks if t.due_date < now and t.status != "Completed")
                    
                    # Count by priority
                    high_priority = sum(1 for t in tasks if t.priority == "High" and t.status != "Completed")
                    
                    # Store statistics (could be used for reporting)
                    # This demonstrates background processing while user adds tasks
                    self._background_stats = {
                        "timestamp": datetime.now(),
                        "total": total_tasks,
                        "completed": completed,
                        "in_progress": in_progress,
                        "pending": pending,
                        "overdue": overdue,
                        "high_priority_pending": high_priority
                    }
                    
                    # Optional: Could perform background database operations here
                    # For example: periodic sync, cleanup, or optimization
                    
            except Exception:
                # Silently handle errors in background thread
                pass
    
    def start_background_thread(self):
        """Start background thread for concurrent operations."""
        if not self._background_thread or not self._background_thread.is_alive():
            self._background_thread = threading.Thread(
                target=self.background_task_cleanup,
                daemon=True
            )
            self._background_thread.start()
    
    def run(self):
        """Run the CLI main loop."""
        print("\nWelcome to Task Management Application!")
        print("Loading tasks from database...")
        
        # Load tasks from database
        if not self._task_manager.load_tasks_from_db():
            print("Warning: Could not load tasks from database. Starting with empty task list.")
        
        # Start background thread for concurrent operations
        self.start_background_thread()
        print("[INFO] Background thread started - performing concurrent operations...")
        
        task_count = self._task_manager.get_task_count()
        print(f"Loaded {task_count} task(s) from database.")
        print("\n[NOTE] You can add tasks while background operations run concurrently!")
        
        while self._running:
            try:
                self.display_menu()
                choice_input = input("\nEnter your choice (1-9): ").strip()
                
                try:
                    choice = Validators.validate_menu_choice(choice_input, min_val=1, max_val=9)
                except ValueError as e:
                    print(f"\n[ERROR] {e}")
                    choice = None
                
                if choice == "1":
                    self.add_task()
                elif choice == "2":
                    self.list_tasks()
                elif choice == "3":
                    self.filter_tasks()
                elif choice == "4":
                    self.update_task()
                elif choice == "5":
                    self.mark_completed()
                elif choice == "6":
                    self.delete_task()
                elif choice == "7":
                    self.view_task_details()
                elif choice == "8":
                    self.view_background_stats()
                elif choice == "9":
                    print("\nThank you for using Task Management Application!")
                    self._running = False
                elif choice is None:
                    # Error already displayed in validation
                    pass
                else:
                    print("\n[ERROR] Invalid choice. Please enter a number between 1 and 9.")
                
                if self._running:
                    input("\nPress Enter to continue...")
                    
            except KeyboardInterrupt:
                print("\n\nExiting application...")
                self._running = False
            except Exception as e:
                print(f"\n[ERROR] Unexpected error: {e}")
                if self._running:
                    input("\nPress Enter to continue...")
        
        self._running = False

