import os
import pandas as pd
from .connection import create_connection
from db.guest_repository import db_get_country_id

# Initialize database with tables and data
def init_db():
    _create_tables()
    
    # If data does not exist in database, read CSV data
    if not _check_data_exists():
        _read_csv_data()
    
    print("Database initialized successfully.")

# Creates the necessary database tables if needed
def _create_tables():
    connection = create_connection()
    cursor = connection.cursor()
    
    # Create Countries table with unique names
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Countries (
            id INTEGER PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE
        )
    """)
    
    # Create Guests table with foreign key to Countries
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Guests (
            id INTEGER PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            country_id INTEGER NOT NULL,
            FOREIGN KEY (country_id) REFERENCES Countries (id)
        )
    """)

    connection.commit()
    connection.close()

# Check if data is already present in Guests table
def _check_data_exists():
    connection = create_connection()
    cursor = connection.cursor()
    
    cursor.execute("SELECT COUNT(*) AS count FROM Guests")
    result = cursor.fetchone()
    
    connection.close()
    return result['count'] > 0

# Read initial guest data from CSV file
def _read_csv_data():
    csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                           'csv/international_names_with_rooms_1000.csv')
    
    data = pd.read_csv(csv_path, usecols=['First Name', 'Family Name', 'Country'])
    data.rename(columns={
        'First Name': 'first_name',
        'Family Name': 'last_name',
        'Country': 'country'
    }, inplace=True)

    connection = create_connection()
    
    for _, row in data.iterrows():
        country_id = db_get_country_id(connection, row['country'])
        connection.execute("""
            INSERT INTO Guests (first_name, last_name, countries_id) 
            VALUES (?, ?, ?)
        """, (row['first_name'], row['last_name'], country_id))

    connection.commit()
    connection.close()
