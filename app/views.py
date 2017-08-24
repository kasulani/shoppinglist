from app import app
from flask import render_template, request, redirect, url_for
import requests
import json
from app import models

# Initialise the model that will hold the non persistent data for the application
# Shopping_List_App = models.ShoppingListApp()
# current_user = None
auth_token = None


@app.route('/', methods=['GET', 'POST'])
# @app.route('/index', methods=['GET'])
def index():
    """
    This route will return a login page to enable an already existing users to login and
    will be redirected to dashboard
    :return:
    """
    # global Shopping_List_App, current_user
    global auth_token
    error_message = None
    if request.method == 'POST':
        app.logger.debug("Index: POST data {}".format(request.form))
        # get the form data and store it in local variables
        username = request.form['username']
        password = request.form['password']
        data = {"username": username, "password": password}
        # handle exception in case api server is not reachable
        try:
            # call the endpoint to login
            reply = requests.post(app.config['LOGIN'], json=data)
            content = json.loads(reply.content)
            if 'token' in content:
                auth_token = content['token']
                return redirect(url_for('dashboard'))
            if content['status'] == 'fail':
                error_message = content['message']
            app.logger.debug("API response: %s" % content)
        except Exception as ex:
            app.logger.error(ex.message)
    return render_template('index.html', error=error_message)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    This route will return a login page to enable new users to register accounts in the
    shopping list application
    :return:
    """
    # global Shopping_List_App
    global auth_token
    error_message = None
    if request.method == 'POST':
        app.logger.debug("Signup: POST data {}".format(request.form))
        # get the form data and store it in local variables
        username = request.form['username']
        email = request.form['email']
        password1 = request.form['password1']
        password2 = request.form['password2']
        if password1 == password2 and email is not None:
            # password entered is the same, go ahead and create the user
            app.logger.debug('user with username %s registered successfully' % email)
            data = {"email": email, "password": password1}
            # handle exception in case api server is not reachable
            try:
                # call the endpoint to login
                reply = requests.post(app.config['REGISTER'], json=data)
                content = json.loads(reply.content)
                if content['status'] == 'pass':
                    return redirect(url_for('index'))
                else:
                    error_message = content['message']
                    app.logger.error("API response: %s" % error_message)
                app.logger.debug("API response: %s" % content)
            except Exception as ex:
                app.logger.error(ex.message)
    return render_template('signup.html', error=error_message)


@app.route('/dashboard', methods=['GET'])
def dashboard():
    # get the logged in user lists
    #
    return render_template('dashboard.html')


@app.route('/view/list', methods=['GET'])
def shopping_list():
    global auth_token
    if auth_token is not None:
        try:
            bearer = "Bearer {}".format(auth_token)
            headers = {'Authorization': bearer}
            app.logger.debug("Authorization Header: %s" % headers)
            reply = requests.get(app.config['LISTS'], headers=headers)
            content = json.loads(reply.content)
            lists = content
            num = len(lists)
            if lists is not None:
                return render_template('shoppinglist.html', num=num, lists=lists)
            app.logger.debug("API response: %s " % lists)
        except Exception as ex:
            app.logger.error(ex.message)

        return render_template('shoppinglist.html')
    return redirect(url_for('index'))


@app.route('/add/list', methods=['POST'])
def add_list():
    """
    This route will create a new shopping list for a particular user
    :return:
    """
    global auth_token
    if auth_token is not None:
        if request.method == 'POST':
            app.logger.debug("Create List: POST data {}".format(request.form))
            # get the form data and store it in local variables
            bearer = "Bearer {}".format(auth_token)
            headers = {'Authorization': bearer, 'content-type': 'application/json'}
            try:
                name = request.form['title']
                description = request.form['description']
                # a shopping list for user with out any items on it
                data = {"title": name, "description": description}
                app.logger.debug("data : %s " % json.dumps(data))
                reply = requests.post(app.config['LISTS'], headers=headers, data=json.dumps(data))
                content = json.loads(reply.content)
                app.logger.debug("API response: %s " % content)
                return redirect(url_for('shopping_list'))
            except Exception as ex:
                app.logger.error(ex.message)
        return render_template('shoppinglist.html')
    return redirect(url_for('index'))


@app.route('/edit/list/<list_id>', methods=['POST', 'GET'])
def edit_list(list_id):
    """
    This route will update a shopping list for a particular user
    :return:
    """
    # todo: template for edit needs styling
    global auth_token
    if auth_token is not None:
        bearer = "Bearer {}".format(auth_token)
        headers = {'Authorization': bearer, 'content-type': 'application/json'}
        # get the list by id
        url = app.config['LISTS'] + "/{}".format(list_id)
        reply = requests.get(url, headers=headers)
        content = json.loads(reply.content)
        # form the list for rendering on page
        a_list = [content['id'], content['title'], content['description']]
        return render_template('editshoppinglist.html', a_list=a_list)
    return redirect(url_for('index'))


@app.route('/delete/list/<list_id>', methods=['GET'])
def delete_list(list_id):
    """
    This route will delete a shopping list for a particular user
    :return:
    """
    global auth_token
    if auth_token is not None:
        app.logger.debug("Deleting List with id: {}".format(list_id))
        # get the form data and store it in local variables
        bearer = "Bearer {}".format(auth_token)
        headers = {'Authorization': bearer, 'content-type': 'application/json'}
        url = app.config['LISTS'] + "/{}".format(list_id)
        reply = requests.delete(url, headers=headers)
        content = json.loads(reply.content)
        app.logger.debug("API response: %s " % content)
        # redirect user to view list
        return redirect(url_for('shopping_list'))
    return redirect(url_for('index'))


@app.route('/items/<list_id>', methods=['GET', 'POST'])
def shopping_list_items(list_id):
    global auth_token
    if auth_token is not None:
        app.logger.debug("Items on List with id: {}".format(list_id))
        # fetch items on this list for view
        bearer = "Bearer {}".format(auth_token)
        headers = {'Authorization': bearer, 'content-type': 'application/json'}
        url = app.config['LISTS'] + "/{}".format(list_id)
        reply = requests.get(url, headers=headers)
        content = json.loads(reply.content)

        return render_template('shoppinglistitem.html', list_name=content['title'], list_id=content['id'])
    return redirect(url_for('index'))


@app.route('/add/item', methods=['POST'])
def add_item():
    """
    This route will create a new shopping list for a particular user
    :return:
    """
    global auth_token
    if auth_token is not None:
        if request.method == 'POST':
            app.logger.debug("Create List: POST data {}".format(request.form))
            bearer = "Bearer {}".format(auth_token)
            headers = {'Authorization': bearer, 'content-type': 'application/json'}
            try:
                list_id = request.form['list_id']
                item_name = request.form['item_name']
                description = request.form['description']
                # a shopping list for user with out any items on it
                data = {"name": item_name, "description": description}
                app.logger.debug("data : %s " % json.dumps(data))
                url = app.config['LISTS'] + "/{}".format(list_id) + "/items"
                app.logger.debug("Calling endpoint: %s " % url)
                reply = requests.post(url, headers=headers, data=json.dumps(data))
                content = json.loads(reply.content)
                app.logger.debug("API response: %s " % content)
                return redirect(url_for('shopping_list'))
            except Exception as ex:
                app.logger.error(ex.message)
        return render_template('shoppinglistitem.html')
    return redirect(url_for('index'))
