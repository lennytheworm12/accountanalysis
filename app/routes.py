from flask import render_template
from app import app

# Define a route for the root URL
@app.route('/')
def home():
    #the homepage
    return render_template('index.html')