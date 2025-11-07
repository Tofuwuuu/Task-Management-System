# Task Management Application

A Python command-line application for managing daily tasks, demonstrating core Python fundamentals, object-oriented programming (OOP) principles, problem-solving skills, and database interaction with MongoDB.

## Features

- **Add Tasks**: Create new tasks with title, description, due date, priority, and status
- **List Tasks**: View all tasks with customizable sorting options
- **Filter Tasks**: Filter tasks by priority, status, or due date
- **Update Tasks**: Modify task details
- **Mark Complete**: Mark tasks as completed
- **Delete Tasks**: Remove tasks from the system
- **Data Persistence**: All tasks are stored in MongoDB and persist across application restarts
- **Multithreading**: Background operations for concurrent task processing

## Project Structure

```
Task-Management/
├── task_manager/          # Main application package
│   ├── __init__.py
│   ├── task.py            # Task entity class
│   ├── task_manager.py    # TaskManager class with business logic
│   ├── database_handler.py # MongoDB database operations
│   ├── validators.py      # Input validation utilities
│   └── cli.py             # Command-line interface
├── main.py                # Application entry point
├── config.py              # Configuration settings
├── setup_database.py      # Database setup script
├── requirements.txt        # Python dependencies
├── .gitignore            # Git ignore file
└── README.md             # This file
```

## Requirements

- Python 3.7 or higher
- pip (Python package manager)
- **MongoDB Atlas account** (cloud MongoDB) - No local MongoDB installation needed!

## Quick Start (Cloud MongoDB)

Since this application uses **MongoDB Atlas** (cloud database), setup is simple:

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Task-Management
```

### 2. Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `pymongo` - MongoDB driver for Python

### 4. Run the Application

```bash
python main.py
```

**That's it!** The application is pre-configured to connect to MongoDB Atlas. The database connection string is already set in `config.py`, and the database will be automatically initialized on first run.

## Optional: Configure Database Connection

If you want to use a different MongoDB Atlas cluster, edit `config.py`:

```python
MONGODB_CONNECTION_STRING = "mongodb+srv://username:password@cluster.mongodb.net/"
MONGODB_DATABASE_NAME = "task_management"
```

Or set environment variables:
```bash
# Windows
set MONGODB_CONNECTION_STRING=mongodb+srv://username:password@cluster.mongodb.net/
set MONGODB_DATABASE_NAME=task_management

# macOS/Linux
export MONGODB_CONNECTION_STRING=mongodb+srv://username:password@cluster.mongodb.net/
export MONGODB_DATABASE_NAME=task_management
```

## Optional: Manual Database Setup

If you want to manually verify database setup:

```bash
python setup_database.py
```

**Note:** This is optional since the database is automatically initialized when you first run the application.

This will create the necessary database and collection with indexes.

## Usage

### Starting the Application

```bash
python main.py
```

### Application Menu

Once started, you'll see a menu with the following options:

1. **Add a new task** - Create a new task with all required details
2. **List all tasks** - View all tasks with sorting options
3. **Filter tasks** - Filter tasks by various criteria
4. **Update a task** - Modify existing task details
5. **Mark task as completed** - Change task status to "Completed"
6. **Delete a task** - Remove a task from the system
7. **View task details** - View detailed information about a specific task
8. **Exit** - Close the application

### Example Workflow

1. **Adding a Task:**
   ```
   Enter task title: Complete project documentation
   Enter task description: Write comprehensive README and code comments
   Enter due date (YYYY-MM-DD): 2024-12-31
   Enter priority (Low/Medium/High): High
   Enter status (Pending/In Progress/Completed): Pending
   ```

2. **Listing Tasks:**
   - Choose from sorting options (by date, priority, status, etc.)
   - Select ascending or descending order

3. **Filtering Tasks:**
   - Filter by priority: High, Medium, or Low
   - Filter by status: Pending, In Progress, or Completed
   - Filter by due date: exact date, before date, or after date

4. **Updating a Task:**
   - Enter the task ID
   - Update any fields you want to change (press Enter to keep current value)

## Technical Details

### Object-Oriented Design

The application follows OOP principles with the following classes:

- **Task**: Represents a single task entity with encapsulation
- **TaskManager**: Manages task operations and business logic
- **DatabaseHandler**: Handles all database operations
- **CLI**: Provides the command-line interface
- **Validators**: Static utility class for input validation

### Data Structures & Algorithms

- **Dictionary (Hash Map)**: Used for O(1) task lookups by ID
- **List**: Maintains task order and enables efficient iteration
- **Custom Sorting Algorithm**: Implements stable sorting with custom key functions
- **Custom Filtering Algorithm**: Uses list comprehension for efficient filtering

### Database Schema

The MongoDB collection `tasks` stores documents with the following structure:

```json
{
  "task_id": "unique-uuid-string",
  "title": "Task title",
  "description": "Task description",
  "due_date": ISODate("2024-12-31T00:00:00Z"),
  "priority": "High|Medium|Low",
  "status": "Pending|In Progress|Completed",
  "created_at": ISODate("2024-01-01T00:00:00Z")
}
```

Indexes:
- `task_id`: Unique index for fast lookups

### Multithreading

The application uses a background thread for concurrent operations:
- Background task cleanup and maintenance
- Demonstrates multithreading capabilities

### Error Handling

- Input validation for all user inputs
- Try-except blocks for database operations
- Meaningful error messages for users
- Graceful handling of connection failures

## Code Style

- Follows PEP 8 style guide
- Comprehensive docstrings for all classes and methods
- Clear comments explaining complex logic
- Type hints for better code clarity

## Testing the Application

1. **Run the application**:
   ```bash
   python main.py
   ```

   The application will automatically connect to MongoDB Atlas cloud database.

3. **Test operations**:
   - Add several tasks with different priorities and statuses
   - List and sort tasks
   - Filter tasks by different criteria
   - Update task details
   - Mark tasks as completed
   - Delete tasks
   - Restart the application to verify data persistence

## Troubleshooting

### MongoDB Connection Issues

If you encounter connection errors:

1. **Check if MongoDB is running:**
   ```bash
   # Windows
   Check Services (services.msc) for MongoDB

   # macOS/Linux
   sudo systemctl status mongodb
   ```

2. **Verify connection string** in `config.py`

3. **Check MongoDB logs** for detailed error messages

### Import Errors

If you see import errors:

1. Ensure you're in the project root directory
2. Activate your virtual environment
3. Verify all dependencies are installed: `pip list`

### Permission Errors

If you encounter permission errors:

1. Ensure MongoDB has proper permissions
2. Check file/directory permissions in your project folder

## Future Enhancements

Potential improvements for the application:

- User authentication and multiple user support
- Task categories/tags
- Task reminders and notifications
- Export/import functionality (JSON, CSV)
- Web interface
- Task dependencies and subtasks
- Search functionality
- Statistics and reporting

## License

This project is created for educational purposes.

## Author

Developed as a demonstration of Python programming skills, OOP principles, and database interaction.

## Contact

For questions or issues, please refer to the repository's issue tracker.
