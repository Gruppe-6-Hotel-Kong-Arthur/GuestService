from db.db import init_db, db_get_guest_by_id, db_get_guests, db_add_guest, db_get_countries
from flask import Flask, jsonify, request

app = Flask(__name__)

# Retrieve a specific guest by their ID
@app.route('/api/v1/guests/<int:id>', methods=['GET'])
def get_guest_by_id(id):
    guest = db_get_guest_by_id(id)
    if guest:
        return jsonify(guest), 200
    return jsonify({"error": "Guest not found"}), 404

# Retrieve all guests from the database
@app.route('/api/v1/guests', methods=['GET'])
def get_guests():
    guests = db_get_guests()
    if guests:
        return jsonify(guests), 200
    return jsonify({"error": "No guests found"}), 404

# Add a new guest to the database
@app.route('/api/v1/guests', methods=['POST'])
def add_guest():
    data = request.get_json()
    
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    country_id = data.get('country_id') 

    if db_add_guest(first_name, last_name, country_id): 
        return jsonify({"message": "Guest added successfully"}), 201
    
    return jsonify({"error": "Failed to add guest"}), 500

# Retrieve all countries from the database
@app.route('/api/v1/countries', methods=['GET'])
def get_countries():
    countries = db_get_countries()
    if countries:
        return jsonify(countries), 200
    return jsonify({"error": "No countries found"}), 404

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5001)
