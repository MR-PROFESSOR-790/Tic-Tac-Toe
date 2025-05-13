from flask import Flask
import os
from .routes import main

def create_app():
    app = Flask(__name__, template_folder='../templates')
    app.secret_key = 'super_secret_key_for_ctf'
    app.register_blueprint(main)
    
    # Configure static folder
    app.static_folder = '../static'
    
    return app