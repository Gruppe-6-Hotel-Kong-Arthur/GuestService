from .connection import create_connection

# Get or create country ID for a given country name
def db_get_country_id(connection, country_name):
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

# Delete a guest from the database
def _db_delete_guest(id):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        
        cursor.execute("DELETE FROM Guests WHERE id = ?", (id,))
        connection.commit()
        connection.close()
        return True
    except Exception as e:
        print(f"Error deleting guest: {e}")
        return False
    