from app import app
from flask import render_template, request, redirect, url_for
from app import models

# Initialise the model that will hold the non persistent data for the application
Shopping_List_App = models.ShoppingListApp()


@app.route('/', methods=['GET', 'POST'])
#@app.route('/index', methods=['GET'])
def index():
    """
    This route will return a login page to enable an already existing users to login and
    will be redirected to dashboard
    :return:
    """
    global Shopping_List_App
    error_message = None
    if request.method == 'POST':
        app.logger.debug("Index: POST data {}".format(request.form))
        # get the form data and store it in local variables
        username = request.form['username']
        password = request.form['password']
        if Shopping_List_App.login_user(username=username, password=password):
            # redirect user to the dashboard
            app.logger.debug(
                'successfully logged in user with username: %s and now redirecting user to dashboard' % username)
            return redirect(url_for('dashboard'))
        else:
            error_message = "failed to login user with username: {0}".format(username)
            app.logger.error(error_message)
    return render_template('index.html', error=error_message)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    This route will return a login page to enable new users to register accounts in the
    shopping list application
    :return:
    """
    global Shopping_List_App
    error_message = ""
    if request.method == 'POST':
        app.logger.debug("Signup: POST data {}".format(request.form))
        # get the form data and store it in local variables
        username = request.form['username']
        email = request.form['username']
        password1 = request.form['password1']
        password2 = request.form['password2']
        # next check if the user exists in the shopping list application non persistent data store
        if Shopping_List_App.user_dict.has_key(username):
            error_message = "username: {0} is already in user".format(username)
        else:
            # register the user and redirect the user to the login page
            if Shopping_List_App.register_user(username=username, password1=password1, password2=password2):
                # redirect user to login page
                app.logger.debug('user with username %s registered successfully' % username)
                return redirect(url_for('index'))
            else:
                error_message = "failed to register user. Ensure you enter your twice password correctly"
                app.logger.error(error_message)
    return render_template('signup.html', error=error_message)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template('dashboard.html')


@app.route('/list', methods=['GET', 'POST'])
def shopping_list():
    return render_template('shoppinglist.html')


@app.route('/items', methods=['GET', 'POST'])
def shopping_list_item():
    return render_template('shoppinglistitem.html')


