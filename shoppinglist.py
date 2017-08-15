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
        self.quantity = 0
        self.status = False  # false meaning the item has not been checked by t

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
        self.items = []  # list containing items as objects of ListItem

    def get_item(self, item_id):
        """
        This method returns a single item of a given id
        :param item_id: id of the item in the list
        :return: an object of type ListItem
        """
        return self.items[item_id-1]

    def view_items(self):
        """
        This method returns all Items on a shopping list
        :return: dictionary
        """
        list_of_items = {}
        for item in self.items:
            list_of_items[item.id] = [item.name, item.quantity, item.description]
        return list_of_items

    def add_item(self, name="", description="", quantity=0):
        """
        This method adds an item to the shopping list
        :param name: name of item
        :param description: short description about the item
        :param quantity: an integer
        :return: null
        """
        # item id should be greater than 0
        num_of_items = len(self.items)
        # create an instance of ListItem
        item = ListItem()
        item.id = num_of_items + 1
        item.name = name
        item.description = description
        item.quantity = quantity
        # add the object to the list of items
        self.items.append(item)

    def update_item(self, item_id, name="", description="", quantity=0):
        """
        This method updates an item on a shopping list
        :param item_id: of the type ListItem
        :param name:
        :param description:
        :param quantity: an integer
        :return: null
        """
        # todo check if item id is greater than zero
        select_item = self.items[item_id-1]  # this is an object of type ListItem
        select_item.quantity = quantity
        if name != "":
            select_item.name = name
        if description != "":
            select_item.description = description

    def delete_item(self, item_id):
        """
        This method deletes an item from the shopping list
        :param item_id: id of item
        :return: null
        """
        del self.items[item_id-1]


class User(object):
    def __init__(self):
        self.username = ""  # this is supposed to be unique for every user
        self.password = ""
        self.email = ""
        self.firstname = ""
        self.lastname = ""
        self.description = ""  # short description about the user
        self.shopping_lists = []

    def get_shopping_list(self, list_id):
        """
        This method returns a single shopping list of a given id
        :param list_id: id of the item in the list
        :return: an object of type ShoppingList
        """
        return self.shopping_lists[list_id-1]

    def get_user_full_name(self):
        """
        This method returns the full names of the user, that is the first name and last name as
        one string
        :return: string
        """
        return "{0} {1}".format(self.firstname, self.lastname)

    def create_shopping_list(self, list_name="", description="", items={}):
        """
        This method creates a shopping list for a user and populates it with items
        :param list_name: name of the list the user chooses to use
        :param description: short description about the list
        :param items: items to add to the list and this is a dictionary with keys as int and values as
        a list with ['name_of_item','desc_of_item', qty_as_int] see example below
        :return: null

        example of items dictionary passed to this method:
        items = {1:['mac book','apple', 1]}
        """
        # get length of user's shopping list
        list_length = len(self.shopping_lists)
        # create an instance of shopping list object
        shopping_list = ShoppingList()
        shopping_list.id = list_length + 1
        shopping_list.name = list_name
        shopping_list.description = description
        # iterate through the items and add them to shopping list created
        for key in items:
            shopping_list.add_item(items[key][0], items[key][1], items[key][2])

        self.shopping_lists.append(shopping_list)

    def delete_shopping_list(self, shopping_list_id):
        """
        This method deletes a shopping list that belongs to a user
        :param shopping_list_id: integer
        :return: null
        """
        del self.shopping_lists[shopping_list_id-1]

    def update_shopping_list(self, shopping_list_id, list_name="", description="", items={}):
        """
        This method updates a users shopping list
        :param shopping_list_id:
        :param list_name:
        :param description:
        :param items:
        :return:
        """
        # get the list to update
        the_list = self.shopping_lists[shopping_list_id-1]  # this is an object of ShoppingList
        if list_name != "":
            the_list.name = list_name
        if description != "":
            the_list.description = description
        # iterate through the items and update them to shopping list created
        position = 0
        for key in items:
            position += 1
            the_list.update_item(item_id=position, name=items[key][0], description=items[key][1], quantity=items[key][2])

    def view_shopping_lists(self):
        """
        This method returns the user's shopping lists
        :return: dictionary
        """
        user_shopping_lists = {}
        for the_list in self.shopping_lists:
            user_shopping_lists[the_list.id] = [the_list.name, the_list.description]
        return user_shopping_lists


class ShoppingListApp(object):
    def __init__(self):
        self.users = []  # list of objects of type User
        self.user_dict = {}  # this acts as my quick reference to map user name and password

    def register_user(self, username, password1, password2):
        """
        This function is used to register a user who signs up for an account in the shopping list app.
        :param username: preferred username and it should be 4 chars or longer
        :param password1: preferred password and it should be 4 chars or longer
        :param password2: password1 is entered again to confirm it, so password2 is the same as password1
        :return: bool to indicate if it was successful or not
        """
        # todo check if username exists in user_dict variable to prevent duplicates
        is_registered = False
        if len(username) >= 4 and password1 == password2 and len(password1) >= 4:
            # create an instance of User
            user = User()
            user.username = username
            user.password = password1
            self.user_dict[user.username] = user.password
            self.users.append(user)
            is_registered = True

        return is_registered

    def login_user(self, username, password):
        """
        This method logs in a user if they have already registered for a user account
        :param username: set by user at signup and it should be 4 chars or longer
        :param password: set by user at signup and it should be 4 chars or longer
        :return: bool to indicate if the login was successful or not
        """
        login_this_user = False
        if self.user_dict[username] == password:
            login_this_user = True  # user found, login this user

        return login_this_user

    def get_user(self, username):
        """
        This method returns a single user specified by username
        :param username: username
        :return: object of the type User
        """
        return self.users[self.user_dict.keys().index(username)]
