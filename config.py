"""
Configuration file for database settings.
"""

import os

# MongoDB Configuration
MONGODB_CONNECTION_STRING = os.getenv(
    "MONGODB_CONNECTION_STRING",
    "mongodb+srv://example:sA62bqN5Yp89Yion@cluster0.9pt586g.mongodb.net/?appName=Cluster0"
)

MONGODB_DATABASE_NAME = os.getenv(
    "MONGODB_DATABASE_NAME",
    "task_management"
)

# Application Settings
APP_NAME = "Task Management Application"
APP_VERSION = "1.0.0"

