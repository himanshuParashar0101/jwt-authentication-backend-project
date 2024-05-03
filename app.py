from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
import os


app = Flask(__name__)


# database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'secret-key'  # Replace with a strong secret key



db = SQLAlchemy(app)        # Initialize SQLAlchemy for db
jwt = JWTManager(app)       # Initialize JWTManager for tokens



# Initialize db structure
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Product {self.title}>'

with app.app_context():
    db.create_all()



# For creating a JWT access token (POST request)
@app.route('/login', methods=['POST'])
def login():
    access_token = create_access_token(identity='user')
    return jsonify(access_token=access_token)



# Fetch product information (GET request)
@app.route('/products', methods=['GET'])
@jwt_required()   # This route requires JWT (JSON Web Token) authentication
def get_products():
    limit = request.args.get('limit', 20, type=int)           # Default limit is 20 if not provided
    skip = request.args.get('skip', 0, type=int)              # Default skip is 0 if not provided
    products = Product.query.offset(skip).limit(limit).all()  # Query the database for products, applying limit and skip parameters
    product_list = [{'id': product.id, 'title': product.title, 'description': product.description, 'price': product.price} for product in products]    # Create a list of dictionaries containing product information
    return jsonify(product_list)


# Retrieve product details by product ID (GET request)
@app.route('/products/<int:product_id>', methods=['GET'])
@jwt_required()
def get_product(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify({'id': product.id, 'title': product.title, 'description': product.description, 'price': product.price})
    else:
        return jsonify({'error': 'Product not found'}), 404


# Create new product (POST request)
@app.route('/products', methods=['POST'])
@jwt_required()
def create_product():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No product data provided'}), 400
    title = data.get('title')
    description = data.get('description')
    price = data.get('price')
    if not title or not description or not price:
        return jsonify({'error': 'Missing required fields'}), 400
    product = Product(title=title, description=description, price=price)  # Create a new product and store it in db.

    db.session.add(product)
    db.session.commit()
    return jsonify({'id': product.id, 'title': product.title, 'description': product.description, 'price': product.price}), 201


# Updating product by its ID (PUT request)
@app.route('/products/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No product data provided'}), 400
    product.title = data.get('title', product.title)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    db.session.commit()
    return jsonify({'id': product.id, 'title': product.title, 'description': product.description, 'price': product.price})


# Deleting a product by its ID (DELETE request)
@app.route('/products/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'})



if __name__ == '__main__':
    app.run(debug=True)
