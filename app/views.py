from app import app
from flask import render_template, request, redirect, url_for
from app import models

# Initialise the model that will hold the non persistent data for the application
Shopping_List_App = models.ShoppingListApp()
current_user = None


@app.route('/', methods=['GET', 'POST'])
#@app.route('/index', methods=['GET'])
def index():
    """
    This route will return a login page to enable an already existing users to login and
    will be redirected to dashboard
    :return:
    """
    global Shopping_List_App, current_user
    error_message = None
    if request.method == 'POST':
        app.logger.debug("Index: POST data {}".format(request.form))
        # get the form data and store it in local variables
        username = request.form['username']
        password = request.form['password']
        if Shopping_List_App.login_user(username=username, password=password):
            # set the current user
            current_user = username
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


@app.route('/dashboard', methods=['GET'])
def dashboard():
    # get the logged in user lists
    #
    return render_template('dashboard.html')


@app.route('/view/list', methods=['GET'])
def shopping_list():
    # get all the lists for the logged in user and show them
    # list name, description, status
    # get the current user model
    global Shopping_List_App, current_user
    user = Shopping_List_App.get_user(current_user)
    lists = user.view_shopping_lists()
    app.logger.debug("View List data: ".format(lists))
    return render_template('shoppinglist.html', lists=lists)


@app.route('/add/list', methods=['POST'])
def add_list():
    """
    This route will create a new shopping list for a particular user
    :return:
    """
    global Shopping_List_App, current_user
    # get the user model
    user = Shopping_List_App.get_user(current_user)
    if request.method == 'POST':
        app.logger.debug("Create List: POST data {}".format(request.form))
        # get the form data and store it in local variables
        name = request.form['title']
        description = request.form['description']
        # a shopping list for user with out any items on it
        user.create_shopping_list(list_name=name, description=description)
        if len(user.shopping_lists) > 0:
            app.logger.debug("Successful created a list for user % s" % current_user)
        # redirect user to dashboard to see their list they have added
        return redirect(url_for('shopping_list'))
    return render_template('shoppinglist.html')


@app.route('/edit/list/<list_id>', methods=['GET'])
def edit_list(list_id):
    """
    This route will update a shopping list for a particular user
    :return:
    """
    global Shopping_List_App, current_user
    # get the user model
    user = Shopping_List_App.get_user(current_user)
    # get a list model
    the_list = user.get_shopping_list(list_id=int(list_id))
    a_list = [the_list.name, the_list.description]
    return render_template('shoppinglist.html', a_list=a_list)


@app.route('/delete/list/<list_id>', methods=['GET'])
def delete_list(list_id):
    """
    This route will delete a shopping list for a particular user
    :return:
    """
    global Shopping_List_App, current_user
    # get the user model
    user = Shopping_List_App.get_user(current_user)
    user.delete_shopping_list(shopping_list_id=int(list_id))
    # redirect user to view list
    return redirect(url_for('shopping_list'))


@app.route('/items', methods=['GET', 'POST'])
def shopping_list_item():
    return render_template('shoppinglistitem.html')


