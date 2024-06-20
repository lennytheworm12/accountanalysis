from flask import render_template
from app import app

# Define a route for the root URL
@app.route('/')
def index():
    # Render the 'index.html' template
    return render_template('index.html')
