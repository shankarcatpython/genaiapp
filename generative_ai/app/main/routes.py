from flask import Blueprint, render_template

# Define the blueprint
main = Blueprint('main', __name__)

# Define the route within the blueprint
@main.route('/')
def home():
    return render_template('home.html')