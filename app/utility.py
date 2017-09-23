# coding=utf-8
"""
    Utility Functions
"""
from app import app, base_url
import views
import requests
import json


def get_url(endpoint):
    """
    This utility function will return a url to be used in a request
    :param endpoint:
    :return:
    """
    if not isinstance(endpoint, str):
        raise Exception('endpoint has to be a string')
    return base_url + endpoint


def set_headers():
    """
    This utility function will set the authorization header for a request
    :return: http header
    """
    bearer = "Bearer {}".format(views.auth_token)
    headers = {'Authorization': bearer, 'content-type': 'application/json'}
    return headers


def show_view_message(status, message):
    """
    This utility function will set the global messages
    :param status:
    :param message:
    :return:
    """
    if status == 'pass':
        views.global_feedback_msg = message
    else:
        views.global_err_msg = message


def get_user_status():
    """
    This utility function will get the current status of the logged
    :return:
    """
    reply = requests.get(app.config['USERS'], headers=set_headers())
    content = json.loads(reply.content)
    views.logged_in_user = content['user']
