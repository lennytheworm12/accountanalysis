from flask import Flask

# Create an instance of the Flask class
app = Flask(__name__)

# Import the routes module to register the routes with the application
from app import routes
