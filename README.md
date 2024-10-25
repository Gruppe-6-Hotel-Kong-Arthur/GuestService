# Guest Service Microservice

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)

## Overview

The Guest Service Microservice is a crucial component of the Hotel Kong Arthur management system, designed to handle all guest-related operations efficiently. It provides robust APIs for guest registration, profile management, and country-based guest tracking. The service automatically seeds initial guest data from a CSV file and maintains a relational database structure for optimal data organization.

Key functionalities:
- Seamless guest registration and profile updates
- Country-based guest categorization and tracking
- Automated data seeding from CSV files
- RESTful API endpoints for easy integration
- Docker containerization for consistent deployment

## Project Structure

```
GuestService/
│
├── csv/
│   └── international_names_with_rooms_1000.csv  # Initial guest data
│
├── db/
│   ├── __init__.py
│   └── db.py                                    # Database operations
│
├── .dockerignore                                # Docker ignore rules
├── .gitignore                                   # Git ignore rules
├── app.py                                       # Main Flask application
├── Dockerfile                                   # Docker configuration
├── README.md                                    # Project documentation
└── requirements.txt                             # Python dependencies
```

## Prerequisites

Before running the service, ensure you have:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Python 3.x](https://www.python.org/downloads/) (for local development)
- [Postman](https://www.postman.com/downloads/) (for testing)

## Installation

### Docker Setup (Recommended)

1. Build the Docker image:
```bash
docker build -t guest-service .
```

2. Run the container:
```bash
docker run -d -p 5001:5001 --name guest-service guest-service
```

### Local Development Setup

1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

## Database Schema

```mermaid
erDiagram
    Guests ||--o{ Countries : belongs_to
    Guests {
        int id PK
        string first_name
        string last_name
        int countries_id FK
    }
    Countries {
        int id PK
        string name
    }
```

## API Documentation

| Method | Endpoint                | Description        | Request Body Example                                  | Response Example                              |
|--------|-------------------------|--------------------|------------------------------------------------------|-----------------------------------------------|
| GET    | `/api/v1/guests`       | Get all guests     | N/A                                                  | `[{"id": 1, "first_name": "John", "last_name": "Doe", "country": "Denmark"}]` |
| GET    | `/api/v1/guests/<id>`  | Get guest by ID    | N/A                                                  | `{"id": 1, "first_name": "John", "last_name": "Doe", "country": "Denmark"}`  |
| POST   | `/api/v1/guests`       | Add new guest      | `{"first_name": "Jane", "last_name": "Smith", "country": "Sweden"}` | `{"message": "Guest added successfully"}`     |


## Testing with Postman

1. Open Postman and create a new collection named "Guest Service"

2. Add the following requests:

### Get All Guests
- Method: GET
- URL: `http://localhost:5001/api/v1/guests`
- Expected Response: Array of guest objects

### Get Guest by ID
- Method: GET
- URL: `http://localhost:5001/api/v1/guests/1`
- Expected Response: Single guest object

### Add New Guest
- Method: POST
- URL: `http://localhost:5001/api/v1/guests`
- Headers: `Content-Type: application/json`
- Body (raw JSON):
```json
{
    "first_name": "Jane",
    "last_name": "Smith",
    "country": "Sweden"
}
```
- Expected Response: Success message

---

Created by Gruppe 6 Hotel Kong Arthur Team
