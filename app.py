from db.db import init_db, db_get_guest_by_id, db_get_guests, db_add_guest
from flask import Flask, jsonify, request
import requests
import os

app = Flask(__name__)

@app.route('/api/v1/guests/<int:id>', methods=['GET'])
def get_guest_by_id(id):
    guest = db_get_guest_by_id(id)

    if guest:
        return jsonify(guest), 200
    else:
        return jsonify({"Error" : "Guest not found"}), 404
    
@app.route('/api/v1/guests', methods=['GET'])
def get_guests():
    guests = db_get_guests()

    if guests:
        return jsonify(guests), 200
    else:
        return jsonify({"Error" : "Guests not found"}), 404

@app.route('/api/v1/guests',methods=['POST'])
def add_guest(first_name, last_name, country):
    data = request.get_json()
    first_name = data['first_name']
    last_name = data['last_name']
    country = data['country']

    if db_add_guest(first_name, last_name, country):
        return jsonify({"Success" : "Guest added"}), 201
    else:
        return jsonify({"Error" : "Guest not added"}), 500
    


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5001)