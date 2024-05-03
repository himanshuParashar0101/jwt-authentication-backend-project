from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_restx import Api, Resource, fields

app = Flask(__name__)

def apikey(func):
    return api.doc(security='apikey')(func)

# database configuration
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'secret-key'  # Replace with a strong secret key

db = SQLAlchemy(app)        # Initialize SQLAlchemy for db
jwt = JWTManager(app)       # Initialize JWTManager for tokens

# Initialize Flask-RESTX
api = Api(app, version='1.0', title='E-Commerce Product Management API',
          description='An API for managing products in an e-commerce application.',authorizations=authorizations)

# Product Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Product {self.title}>'

with app.app_context():
    db.create_all()

# Namespace for product routes
product_ns = api.namespace('products', description='Operations related to products')

# Product Model for Swagger documentation
product_model = api.model('Product', {
    'id': fields.Integer(description='Product ID'),
    'title': fields.String(required=True, description='Product title'),
    'description': fields.String(required=True, description='Product description'),
    'price': fields.Float(required=True, description='Product price')
})

# Add JWT authentication to Swagger
security = {'bearerAuth': {
    'type': 'apikey',
    'in': 'header',
    'name': 'Authorization'
}}

# For creating a JWT access token (POST request)
@api.route('/login')
class Login(Resource):
    def post(self):
        access_token = create_access_token(identity='user')
        return jsonify(access_token=access_token)

# Fetch product information (GET request)
@product_ns.route('/')

class ProductList(Resource):
    @api.doc(security='apiKey')  # Add security to the documentation
    @jwt_required()
    
    @api.marshal_with(product_model, as_list=True)
    def get(self):
        limit = request.args.get('limit', 20, type=int)
        skip = request.args.get('skip', 0, type=int)
        products = Product.query.offset(skip).limit(limit).all()
        return products

    @api.doc(security='bearerAuth')  # Add security to the documentation
    @jwt_required()
    @api.expect(product_model)
    @api.marshal_with(product_model, code=201)
    def post(self):
        data = request.get_json()
        title = data.get('title')
        description = data.get('description')
        price = data.get('price')
        if not title or not description or not price:
            return {'error': 'Missing required fields'}, 400
        product = Product(title=title, description=description, price=price)
        db.session.add(product)
        db.session.commit()
        return product, 201

# Retrieve product details by product ID (GET request)
@product_ns.route('/<int:product_id>')
class ProductResource(Resource):
    @api.doc(security='bearerAuth')  # Add security to the documentation
    @jwt_required()
    @api.marshal_with(product_model)
    def get(self, product_id):
        product = Product.query.get(product_id)
        if not product:
            return {'error': 'Product not found'}, 404
        return product

    @api.doc(security='bearerAuth')  # Add security to the documentation
    @jwt_required()
    @api.expect(product_model)
    @api.marshal_with(product_model)
    def put(self, product_id):
        product = Product.query.get(product_id)
        if not product:
            return {'error': 'Product not found'}, 404
        data = request.get_json()
        product.title = data.get('title', product.title)
        product.description = data.get('description', product.description)
        product.price = data.get('price', product.price)
        db.session.commit()
        return product

    @api.doc(security='bearerAuth')  # Add security to the documentation
    @jwt_required()
    @api.response(204, 'Product deleted')
    def delete(self, product_id):
        product = Product.query.get(product_id)
        if not product:
            return {'error': 'Product not found'}, 404
        db.session.delete(product)
        db.session.commit()
        return '', 204

if __name__ == '__main__':
    app.run(debug=True)
