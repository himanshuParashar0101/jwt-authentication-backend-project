# Product API

## Overview

This Flask-based API allows you to manage products in a database.

## Setup

### 1. Clone the Repository

git clonehttps://github.com/himanshuParashar0101/birdvision-backend-assignment.git

### 2. Navigate to the Project Directory

cd birdvision


### 3. Install Dependencies

pip install -r requirements.txt


### 4. Set up the Database

- By default, the API uses SQLite as the database backend. The database file (`products.db`) will be created automatically.
- If you wish to use a different database system (e.g., PostgreSQL, MySQL), modify the `SQLALCHEMY_DATABASE_URI` configuration in `app.py` accordingly.


### 5. Set the JWT Secret Key

- Open `app.py` and replace `'secret-key'` in the line `app.config['JWT_SECRET_KEY'] = 'secret-key'` with your own secret key.
- Ensure that the secret key is kept secure and not shared publicly.


### 6. Run the API

- Start the Flask development server by running `python app.py`.
- Once the server is running, you can access the API endpoints as described in the Usage section.


### 7. Accessing API Endpoints

- Utilize HTTP methods (e.g., POST, GET, PUT, DELETE) to interact with the API endpoints.
- Ensure to include required parameters in the request payload for POST and PUT requests.
- Handle the API responses appropriately based on the status codes returned.
