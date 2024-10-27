import sqlite3

# Create or connect to SQLite database
def create_connection():
    connection = sqlite3.connect('db/guests_service.db')
    connection.row_factory = sqlite3.Row  # Rows as dictionaries
    return connection
