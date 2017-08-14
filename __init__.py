"""
    Shopping List Application
    Created: 14-August-2017
    Author: Emmanuel King Kasulani
    Email: kasulani@gmail.com
"""

from flask import Flask

shoppinglist_app = Flask(__name__)

from shoppinglist import views