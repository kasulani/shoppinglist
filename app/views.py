from app import app
from flask import render_template, request


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    """
    This route will return a login page to enable already existing users to login and
    will be redirected to dashboard
    :return:
    """
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def login():
    return render_template('signup.html')


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html')


@app.route('/shoppinglist', methods=['GET', 'POST'])
def shopping_list():
    return render_template('shoppinglist.html')

@app.route('/shoppinglistitem', methods=['GET', 'POST'])
def shopping_list_item():
    return render_template('shoppinglistitem.html')

