# coding=utf-8
"""
    Utility Functions
"""
from app import app
import views
import requests
import json


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
    bearer = "Bearer {}".format(views.auth_token)
    headers = {'Authorization': bearer, 'content-type': 'application/json'}
    #
    reply = requests.get(app.config['USERS'], headers=headers)
    content = json.loads(reply.content)
    views.logged_in_user = content['user']
