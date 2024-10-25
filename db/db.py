import sqlite3
import pandas as pd
import os

# Create or connect to SQLite database
def create_connection():
    connection = sqlite3.connect('db/guests_service.db')
    connection.row_factory = sqlite3.Row  # Rows as dictionaries
    return connection

# Initialize database and create necessary tables
def init_db():
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

    # Check if data is already present in Guests table
    cursor.execute("SELECT COUNT(*) AS count FROM Guests")
    result = cursor.fetchone()

    if result['count'] == 0:
        # Adjusted CSV path to correctly point to the file
        csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'csv/international_names_with_rooms_1000.csv')
        read_data_from_csv(csv_path)

    connection.close()

# Get or create country ID for a given country name
def get_country_id(connection, country_name):
    cursor = connection.cursor()
    
    # Check if country exists
    cursor.execute("SELECT id FROM Countries WHERE name = ?", (country_name,))
    country_id = cursor.fetchone()
    
    if country_id:
        return country_id['id']
    
    # If country doesn't exist, create it
    cursor.execute("INSERT INTO Countries (name) VALUES (?)", (country_name,))
    connection.commit()
    
    # Get the ID of the newly inserted country
    cursor.execute("SELECT id FROM Countries WHERE name = ?", (country_name,))
    return cursor.fetchone()['id']

# Read initial guest data from CSV file
def read_data_from_csv(path):
    data = pd.read_csv(path, usecols=['First Name', 'Family Name', 'Country'])
    data.rename(columns={
        'First Name': 'first_name',
        'Family Name': 'last_name',
        'Country': 'country'
    }, inplace=True)

    connection = create_connection()
    
    for _, row in data.iterrows():
        country_id = get_country_id(connection, row['country'])
        connection.execute("""
            INSERT INTO Guests (first_name, last_name, countries_id) 
            VALUES (?, ?, ?)
        """, (row['first_name'], row['last_name'], country_id))

    connection.commit()
    connection.close()

# Retrieve a specific guest by ID with their country information
def db_get_guest_by_id(id):
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT 
            Guests.id, 
            Guests.first_name, 
            Guests.last_name, 
            Countries.name as country
        FROM Guests
        INNER JOIN Countries ON Guests.countries_id = Countries.id
        WHERE Guests.id = ?
    """, (id,))

    guest = cursor.fetchone()
    connection.close()
    
    return dict(guest) if guest else None

# Retrieve all guests with their country information
def db_get_guests():
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT 
            Guests.id, 
            Guests.first_name, 
            Guests.last_name, 
            Countries.name as country
        FROM Guests
        INNER JOIN Countries ON Guests.countries_id = Countries.id
    """)

    guests = cursor.fetchall()
    connection.close()
    
    if guests:
        return [dict(guest) for guest in guests]
    else:
        return None

# Retrieve all countries from the database
def db_get_countries():
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Countries")
    countries = cursor.fetchall()
    connection.close()
    
    if countries:
        return [dict(country) for country in countries]
    else:
        return None

# Add a new guest to the database
def db_add_guest(first_name, last_name, country_id):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        
        # Insert new guest using country_id directly
        cursor.execute("""
            INSERT INTO Guests (first_name, last_name, countries_id) 
            VALUES (?, ?, ?)
        """, (first_name, last_name, country_id))
        
        connection.commit()
        connection.close()
        return True
    except Exception as e:
        print(f"Error adding guest: {e}")
        return False