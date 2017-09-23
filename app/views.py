# coding=utf-8
from app import app, utility
from flask import render_template, request, redirect, url_for, session
import requests
import json

# Global Variables
auth_token = None
logged_in_user = None
global_err_msg = None
global_feedback_msg = None
# ----------------------------------------------------------------------------------------------------------


@app.route('/', methods=['GET', 'POST'])
# @app.route('/index', methods=['GET'])
def index():
    """
    This route will return a landing page with a login form and a link to a signup page.
    :return: html page
    """
    global auth_token
    error_message = None
    if request.method == 'POST':
        app.logger.debug("index controller: POST data {}".format(request.form))
        # get the form data and store it in local variables
        username = request.form['username']
        password = request.form['password']
        data = {"username": username, "password": password}
        if username != '' and password != '':  # make sure the data in the field is not empty
            # handle exception in case api server is not reachable
            try:
                # call the endpoint to login
                reply = requests.post(utility.get_url(app.config['LOGIN']), json=data)
                content = json.loads(reply.content)
                if 'token' in content:
                    auth_token = content['token']
                    session['logged_in'] = True
                    session['username'] = username
                    return redirect(url_for('dashboard'))
                if content['status'] == 'fail':
                    error_message = content['message']
                app.logger.debug("API response: %s" % content)
            except Exception as ex:
                error_message = "Connection refused"
                app.logger.error(ex.message)
        else:
            error_message = "blank field(s) found"
    return render_template('index.html', error=error_message)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    This route will return a signup page for a new user to register an account
    :return: html page
    """
    error_message, msg = None, None

    if request.method == 'POST':
        # get the form data and store it in local variables
        email = request.form['email']
        password1 = request.form['password1']
        password2 = request.form['password2']
        if password1 == password2 and email != '' and password1 != '' and password2 != '':
            # password entered is the same, go ahead and create the user
            data = {"username": email, "password": password1}
            # handle exception in case api server is not reachable
            try:
                # call the endpoint to login
                reply = requests.post(utility.get_url(app.config['REGISTER']), json=data)
                content = json.loads(reply.content)
                if content['status'] == 'pass':
                    app.logger.debug('user with username %s registered successfully' % email)
                    msg = content['message']
                else:
                    error_message = content['message']
                    app.logger.error("API response: %s" % error_message)
                app.logger.debug("API response: %s" % content)
            except Exception as ex:
                error_message = "Connection refused"
                app.logger.error(ex.message)
        else:
            error_message = "blank field(s) found"
    return render_template('signup.html', error=error_message, feedback=msg)


@app.route('/logout', methods=['GET'])
def logout():
    """
    This method logs out a user
    :return:
    """
    global auth_token
    # API call
    reply = requests.get(app.config['LOGOUT'])
    content = json.loads(reply.content)
    app.logger.debug("API response: %s" % content)
    # reset auth token
    auth_token = None
    # reset session
    session['logged_in'] = False
    return redirect(url_for('index'))


@app.route('/dashboard', methods=['GET'])
def dashboard():
    """
    This method will return a dashboard for the login access area, which gives a user a snap shot summary
    of their account in the shopping list application
    :return:
    """
    global auth_token, logged_in_user, global_feedback_msg, global_err_msg
    if auth_token is not None and session['logged_in']:
        try:
            # read-in the global messages and reset them to None
            error_message = global_err_msg
            msg = global_feedback_msg
            global_err_msg, global_feedback_msg = None, None
            # get the logged in user lists
            reply = requests.get(utility.get_url(app.config['LISTS']), headers=utility.set_headers())
            content = json.loads(reply.content)
            lists = None
            if content['status'] == 'pass':  # if the status is pass, lists have been found
                lists = content['lists']
            # get the user details
            utility.get_user_status()
            return render_template('dashboard.html',
                                   feedback=msg, error=error_message, lists=lists, user=logged_in_user)
        except Exception as ex:
            app.logger.error(ex.message)
            return render_template('dashboard.html')
    return redirect(url_for('index'))


@app.route('/add/list', methods=['POST'])
def add_list():
    """
    This route will create a new shopping list for a particular user
    :return:
    """
    global auth_token
    if auth_token is not None and session['logged_in']:
        if request.method == 'POST':
            try:
                # a shopping list for user with out any items on it
                data = {"title": request.form['title'], "description": request.form['description']}
                app.logger.debug("data : %s " % json.dumps(data))
                reply = requests.post(utility.get_url(app.config['LISTS']), headers=utility.set_headers(), data=json.dumps(data))
                content = json.loads(reply.content)
                utility.show_view_message(content['status'], content['message'])
                app.logger.debug("API response: %s " % content)
            except Exception as ex:
                app.logger.error(ex.message)
        return redirect(url_for('dashboard'))
    return redirect(url_for('index'))


@app.route('/edit/list/<list_id>', methods=['GET'])
def edit_list(list_id):
    """
    This route will update a shopping list for a particular user
    :return:
    """
    global auth_token
    if auth_token is not None and session['logged_in']:
        try:
            # get the list by id
            url = utility.get_url(app.config['LISTS'] + "/{}".format(list_id))
            reply = requests.get(url, headers=utility.set_headers())
            content = json.loads(reply.content)
            utility.show_view_message(content['status'], content['message'])
            app.logger.debug("API response: %s " % content)
            return render_template('editlist.html', id=list_id, list=content["list"], user=logged_in_user)
        except Exception as ex:
            app.logger.error(ex.message)
            return render_template('editlist.html', id=list_id, list=None, user=logged_in_user)
    return redirect(url_for('index'))


@app.route('/update/list', methods=['POST'])
def update_list():
    """
    This method will update a list details
    :return:
    """
    global auth_token
    if auth_token is not None and session['logged_in']:
        try:
            list_id = request.form['id']
            name = request.form['title']
            description = request.form['description']
            url = utility.get_url(app.config['LISTS'] + "/{}".format(list_id))
            data = {"title": name, "description": description}
            app.logger.debug("data : %s " % json.dumps(data))
            reply = requests.put(url, headers=utility.set_headers(), data=json.dumps(data))
            content = json.loads(reply.content)
            utility.show_view_message(content['status'], content['message'])
            app.logger.debug("API response: %s " % content)
            return redirect(url_for('dashboard'))
        except Exception as ex:
            app.logger.error(ex.message)
            return render_template('editlist.html')
    return redirect(url_for('index'))


@app.route('/delete/list/<list_id>', methods=['GET'])
def delete_list(list_id):
    """
    This method will delete a shopping list for a particular user
    :return:
    """
    global auth_token
    if auth_token is not None:
        try:
            url = utility.get_url(app.config['LISTS'] + "/{}".format(list_id))
            reply = requests.delete(url, headers=utility.set_headers())
            content = json.loads(reply.content)
            utility.show_view_message(content['status'], content['message'])
            app.logger.debug("API response: %s " % content)
        except Exception as ex:
            app.logger.error(ex.message)
        # redirect user to view list
        return redirect(url_for('dashboard'))
    return redirect(url_for('index'))


@app.route('/items/list/<list_id>', methods=['GET'])
def view_items(list_id):
    """
    This method will render a view of all items on a particular list
    :param list_id:
    :return:
    """
    global auth_token, logged_in_user, global_err_msg, global_feedback_msg
    if auth_token is not None:
        try:
            # read-in the global messages and reset them to None
            error_message = global_err_msg
            msg = global_feedback_msg
            global_err_msg, global_feedback_msg = None, None
            # get the name of the list using the id
            url = utility.get_url(app.config['LISTS'] + "/{}".format(list_id))
            reply = requests.get(url, headers=utility.set_headers())
            content = json.loads(reply.content)
            app.logger.debug("API response: %s " % content)
            list_name = content["list"]["title"]
            # fetch items on this list for view
            url = utility.get_url(app.config['LISTS'] + "/{}".format(list_id) + "/items")
            reply = requests.get(url, headers=utility.set_headers())
            content = json.loads(reply.content)
            return render_template('viewitems.html',
                                   list_name=list_name, list_id=list_id,
                                   user=logged_in_user, items=content['items'], feedback=msg, error=error_message)
        except Exception as ex:
            app.logger.error(ex.message)
            return render_template('viewitems.html', list_name=list_name, list_id=list_id, user=logged_in_user)
    return redirect(url_for('index'))


@app.route('/add/item', methods=['POST'])
def add_item():
    """
    Add an item to a shopping list
    :return:
    """
    global auth_token, logged_in_user, global_feedback_msg, global_err_msg
    if auth_token is not None and session['logged_in']:
        try:
            list_id = request.form['list_id']
            item_name = request.form['item_name']
            description = request.form['description']
            # a shopping list for user with out any items on it
            data = {"name": item_name, "description": description}
            url = utility.get_url(app.config['LISTS'] + "/{}".format(list_id) + "/items")
            app.logger.debug("Calling endpoint: %s " % url)
            reply = requests.post(url, headers=utility.set_headers(), data=json.dumps(data))
            content = json.loads(reply.content)
            # set global messages
            utility.show_view_message(content['status'], content['message'])
            app.logger.debug("API response: %s " % content)
            # update the global user object, new item has been added
            utility.get_user_status()
        except Exception as ex:
            app.logger.error(ex.message)
        return redirect(url_for('view_items', list_id=list_id))
    return redirect(url_for('index'))


@app.route('/edit/item/<item_id>/list/<list_id>', methods=['GET'])
def edit_item(item_id, list_id):
    """
    This route will render a page for editing a shopping list item
    :return:
    """
    global auth_token, logged_in_user
    if auth_token is not None and session['logged_in']:
        try:
            # get the item by id
            url = app.config['LISTS'] + "/{}".format(list_id) + "/items/{}".format(item_id)
            reply = requests.get(url, headers=utility.set_headers())
            content = json.loads(reply.content)
            utility.show_view_message(content['status'], content['message'])
            app.logger.debug("API response: %s " % content)
            return render_template('edititem.html', list_id=list_id, item_id=item_id,
                                   item=content["item"], user=logged_in_user)
        except Exception as ex:
            app.logger.error(ex.message)
            return render_template('edititem.html', user=logged_in_user)
    return redirect(url_for('index'))


@app.route('/update/item', methods=['POST'])
def update_item():
    """
    This method will update an item
    :return:
    """
    global auth_token
    if auth_token is not None and session['logged_in']:
        try:
            list_id = request.form['list_id']
            item_id = request.form['item_id']
            name = request.form['name']
            description = request.form['description']
            url = app.config['LISTS'] + "/{}".format(list_id) + "/items/{}".format(item_id)
            data = {"name": name, "description": description}
            app.logger.debug("data : %s " % json.dumps(data))
            reply = requests.put(url, headers=utility.set_headers(), data=json.dumps(data))
            content = json.loads(reply.content)
            utility.show_view_message(content['status'], content['message'])
            app.logger.debug("API response: %s " % content)
            return redirect(url_for('view_items', list_id=list_id))
        except Exception as ex:
            app.logger.error(ex.message)
            return render_template('edititem.html')
    return redirect(url_for('index'))


@app.route('/delete/item/<item_id>/list/<list_id>', methods=['GET'])
def delete_item(item_id, list_id):
    """
    This method will delete a shopping list item for a particular user
    :return:
    """
    global auth_token
    if auth_token is not None:
        app.logger.debug("Deleting item with id: {}".format(item_id))
        try:
            url = app.config['LISTS'] + "/{}".format(list_id) + "/items/{}".format(item_id)
            reply = requests.delete(url, headers=utility.set_headers())
            content = json.loads(reply.content)
            utility.show_view_message(content['status'], content['message'])
            app.logger.debug("API response: %s " % content)
        except Exception as ex:
            app.logger.error(ex.message)
        # redirect user to view list items
        return redirect(url_for('view_items', list_id=list_id))
    return redirect(url_for('index'))


@app.route('/update/profile', methods=['POST'])
def update_profile():
    """
    This method will update user's profile
    :return:
    """
    global auth_token, global_err_msg, global_feedback_msg
    if auth_token is not None and session['logged_in']:
        try:
            url = app.config['USERS']
            data = {"firstname": request.form['firstname'],
                    "lastname": request.form['lastname'],
                    "description": request.form['description']}
            reply = requests.put(url, headers=utility.set_headers(), data=json.dumps(data))
            content = json.loads(reply.content)
            utility.show_view_message(content['status'], content['message'])
            app.logger.debug("API response: %s " % content)
        except Exception as ex:
            global_err_msg = ex.message
            app.logger.error(ex.message)
        return redirect(url_for('dashboard'))
    return redirect(url_for('index'))


@app.route('/reset-password', methods=['POST'])
def reset_password():
    """
    This method will reset the user's password who's logged in
    :return:
    """
    global auth_token, global_err_msg, global_feedback_msg
    if auth_token is not None and session['logged_in']:
        try:
            oldpass = request.form['oldpass']
            newpass1 = request.form['newpass1']
            newpass2 = request.form['newpass2']
            username = session['username']
            if newpass1 == newpass2 and newpass1 != '' and newpass2 != '':  # the new password has to match
                url = app.config['RESET']
                data = {"username": username, "old_password": oldpass, "new_password": newpass1}
                app.logger.debug("data : %s " % json.dumps(data))
                reply = requests.post(url, headers=utility.set_headers(), data=json.dumps(data))
                content = json.loads(reply.content)
                utility.show_view_message(content['status'], content['message'])
                app.logger.debug("API response: %s " % content)
            else:
                utility.show_view_message(status='fail',
                                          message="Password reset failed because of a password mismatch")
                app.logger.error("Password mismatch")
        except Exception as ex:
            global_err_msg = ex.message
            app.logger.error(ex.message)
        return redirect(url_for('dashboard'))
    return redirect(url_for('index'))
