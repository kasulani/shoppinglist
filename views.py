from shoppinglist import shoppinglist_app
from flask import render_template


@shoppinglist_app.route('/')
@shoppinglist_app.route('/index')
def index():
    render_template('UI/index.html')

