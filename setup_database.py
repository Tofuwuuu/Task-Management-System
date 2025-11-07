"""
Database setup script for initializing MongoDB database and collections.
"""

from task_manager.database_handler import DatabaseHandler
import config


def setup_database():
    """
    Set up the database by creating necessary collections and indexes.
    """
    print("Setting up database...")
    
    db_handler = DatabaseHandler(
        connection_string=config.MONGODB_CONNECTION_STRING,
        database_name=config.MONGODB_DATABASE_NAME
    )
    
    if not db_handler.connect():
        print("ERROR: Could not connect to MongoDB.")
        print("Please ensure MongoDB is running and accessible.")
        print(f"Connection string: {config.MONGODB_CONNECTION_STRING}")
        return False
    
    print("[OK] Database connection established.")
    print("[OK] Database setup completed.")
    print(f"  Database: {config.MONGODB_DATABASE_NAME}")
    print("  Collection: tasks")
    print("  Index: task_id (unique)")
    
    db_handler.disconnect()
    return True


if __name__ == "__main__":
    setup_database()

