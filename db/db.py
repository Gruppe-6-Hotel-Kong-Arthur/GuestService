import sqlite3
import pandas as pd
import os

# Create or connect to the SQLite database (guests_service.db)
def create_connection():
    connection = sqlite3.connect('db/guests_service.db')
    # Return rows as dictionaries for easier access
    connection.row_factory = sqlite3.Row
    return connection


# Initialize the database and create necessary tables
def init_db():
    connection = create_connection()
    cursor = connection.cursor()
    
    # Create Countries table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Countries (
            id INTEGER PRIMARY KEY,
            name VARCHAR(45) NOT NULL
        )
    """)
    
    # Create Guests table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Guests (
            id INTEGER PRIMARY KEY,
            first_name VARCHAR(45) NOT NULL,
            last_name VARCHAR(45) NOT NULL,
            countries_id INTEGER NOT NULL,
            FOREIGN KEY (countries_id)
                REFERENCES Countries (id)
        )
    """)

    # Commit changes and close the connection for setup
    connection.commit()
    connection.close()

    # Define path to the CSV file containing guest data
    csv_path = os.path.join(os.path.dirname(__file__), '../csv/international_names_with_rooms_1000.csv')
    read_data_from_csv(csv_path)


# Retrieve the country ID. Insert a new country if it doesn't exist
def get_country_id(connection, country_name):
    cursor = connection.cursor()

    # Query to check if the country already exists
    cursor.execute("SELECT id FROM Countries WHERE name = ?", (country_name,))
    result = cursor.fetchone()
    
    if result:
        return result['id']
    else:
        # Insert new country and return the ID
        cursor.execute("INSERT INTO Countries (name) VALUES (?)", (country_name,))
        connection.commit()
        return cursor.lastrowid

def read_data_from_csv(path):
    # Load only the needed columns and rename them to match the database table
    data_frame = pd.read_csv(path, usecols=['First Name', 'Family Name', 'Country'])
    data_frame.rename(columns={'First Name': 'first_name', 'Family Name': 'last_name', 'Country': 'country'}, inplace=True)

    # Get DB connection for inserting data
    connection = create_connection()
    
    # Prepare to add each guest with their country ID
    guests_to_insert = []
    for _, row in data_frame.iterrows():
        country_id = get_country_id(connection, row['country'])
        guests_to_insert.append((row['first_name'], row['last_name'], country_id))

    # Insert guests into the Guests table
    connection.executemany("INSERT INTO Guests (first_name, last_name, countries_id) VALUES (?, ?, ?)", guests_to_insert)

    # Commit changes and close the connection
    connection.commit()
    connection.close()

# Run the init_db function
init_db()