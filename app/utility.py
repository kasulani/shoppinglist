# coding=utf-8
"""
    Utility Functions
"""

from app import views


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
