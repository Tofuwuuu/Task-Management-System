"""
Main entry point for the Task Management Application.
"""

import sys
from task_manager.database_handler import DatabaseHandler
from task_manager.task_manager import TaskManager
from task_manager.cli import CLI
import config


def main():
    """Main function to start the application."""
    print("Initializing Task Management Application...")
    
    # Database configuration from config file
    connection_string = config.MONGODB_CONNECTION_STRING
    database_name = config.MONGODB_DATABASE_NAME
    
    # Initialize database handler
    db_handler = DatabaseHandler(
        connection_string=connection_string,
        database_name=database_name
    )
    
    # Connect to database
    print("Connecting to database...")
    if not db_handler.connect():
        print("ERROR: Could not connect to MongoDB.")
        print("Please ensure MongoDB is running and accessible.")
        print(f"Connection string: {connection_string}")
        sys.exit(1)
    
    print("[OK] Database connection established.")
    
    try:
        # Initialize task manager
        task_manager = TaskManager(db_handler)
        
        # Initialize and run CLI
        cli = CLI(task_manager)
        cli.run()
        
    except KeyboardInterrupt:
        print("\n\nApplication interrupted by user.")
    except Exception as e:
        print(f"\nFatal error: {e}")
        sys.exit(1)
    finally:
        # Cleanup
        print("\nClosing database connection...")
        db_handler.disconnect()
        print("Application terminated.")


if __name__ == "__main__":
    main()

