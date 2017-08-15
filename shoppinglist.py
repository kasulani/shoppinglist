"""
    Shopping List Application
    Created: 14-August-2017
    Author: Emmanuel King Kasulani
    Email: kasulani@gmail.com

    This file contains all the classes for the shopping list
"""


class ListItem(object):
    """
    Class for an item on the shopping list. The shopping list contains Items which are objects
    of the class ListItem
    """
    def __init__(self):
        self.id = 0
        self.name = ""
        self.description = ""
        self.status = False

    def get_status(self):
        """
        This function returns the status of item on the list. the status is either True if item has
        been bought or False if it has not yet been bought
        :return: bool
        """
        return self.status


class ShoppingList(object):
    """
    Class for shopping list. A user creates a shopping list and instance of this class is created.
    A shopping list contains items which are objects of the instance ListItem
    """
    def __init__(self):
        self.id = 0  # shopping list id
        self.name = ""  # shopping list name
        self.description = ""  # brief description of the shopping list
        self.items = {}  # dictionary containing items as keys of type ListItem and the value being quantity

    def view_items(self):
        """
        This method returns all Items on a shopping list
        :return: dictionary
        """
        return self.items

    def add_item(self, item, quantity):
        """
        This method adds an item to the shopping list
        :param item: of the type ListItem
        :param quantity: an integer
        :return: null
        """
        # item id should be greater than 0
        self.items[item.id] = quantity

    def update_item(self, item, quantity):
        """
        This method updates an item on a shopping list
        :param item: of the type ListItem
        :param quantity: an integer
        :return: null
        """
        self.items[item.id] = quantity

    def delete_item(self, item_id):
        """
        This method deletes an item from the shopping list
        :param item_id: id of item
        :return: null
        """
        del self.items[item_id]


