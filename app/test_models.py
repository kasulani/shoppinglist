"""
    Shopping List Application
    Created: 14-August-2017
    Author: Emmanuel King Kasulani
    Email: kasulani@gmail.com

    This file contains all the tests for the classes in the shopping list application
"""
import unittest
from app.models import ListItem, ShoppingList, User, ShoppingListApp


class ListItemTest(unittest.TestCase):
    """Tests for the ListItem class"""
    def setUp(self):
        self.list_item = ListItem()

    def test_listItem_property_initialization(self):
        self.assertEquals(self.list_item.id, 0, msg="initial value of id should be zero")
        self.assertEquals(self.list_item.status, False, msg="initial value of item status should be false")

    def test_get_status_of_listItem(self):
        self.assertFalse(self.list_item.status)


class ShoppingListTest(unittest.TestCase):
    """Tests for the ShoppingList class"""
    def setUp(self):
        self.shopping_list = ShoppingList()
        # self.list_item = ListItem()

    def test_shoppingList_property_initialization(self):
        self.assertEquals(self.shopping_list.id, 0, msg="initial value of id should be zero")
        self.assertIsInstance(self.shopping_list.items, list, msg="items is not a list")

    def test_add_item_to_shopping_list(self):
        self.shopping_list.add_item(name="mac book", description="apple", quantity=1)
        self.assertIsInstance(self.shopping_list.items[0], ListItem, msg="item was not added to shopping list")

    def test_get_item_on_shopping_list(self):
        self.shopping_list.add_item(name="mac book", description="apple", quantity=1)
        item = self.shopping_list.get_item(1)
        self.assertEquals(item.id, 1, msg="failed to get item from the list")

    def test_update_item_on_shopping_list(self):
        self.shopping_list.add_item(name="mac book", description="apple", quantity=1)
        self.shopping_list.update_item(item_id=1, quantity=2)
        item = self.shopping_list.get_item(1)
        self.assertEquals(item.quantity, 2, msg="item was not updated on the shopping list")

    def test_delete_item_from_shopping_list(self):
        self.shopping_list.add_item(name="mac book", description="apple", quantity=1)
        self.shopping_list.delete_item(1)
        self.assertEquals(len(self.shopping_list.items), 0, msg="item was not deleted from shopping list")

    def test_view_items_on_shopping_list(self):
        self.shopping_list.add_item(name="mac book", description="apple", quantity=1)
        items = self.shopping_list.view_items()
        self.assertEquals(items[1][0], "mac book", "view all shopping list items added failed")


class UserTest(unittest.TestCase):
    """Tests for the User class"""
    def setUp(self):
        self.user = User()

    def test_get_full_names(self):
        self.user.firstname = "Emmanuel"
        self.user.lastname = "Kasulani"
        self.assertEquals(self.user.get_user_full_name(), "Emmanuel Kasulani",
                          msg="method get_full_name failed")

    def test_create_shopping_list(self):
        self.user.create_shopping_list("gadgets", "cool gadgets for every gizmo",
                                       items={1: ['mac book', 'apple', 1]})
        self.assertIsInstance(self.user.shopping_lists[0], ShoppingList,
                              msg="shopping list was not created for this user")

    def test_update_shopping_list(self):
        self.user.create_shopping_list("gadgets", "cool gadgets for every gizmo",
                                       items={1: ['mac book', 'apple', 1]})
        self.user.update_shopping_list(1, "my gadgets", "my cool gadgets", items={1: ['mac book', 'apple', 2]})
        shopping_list = self.user.get_shopping_list(1)
        self.assertEquals(shopping_list.items[0].quantity, 2,
                          msg="the user's shopping list was not updated")

    def test_delete_shopping_list(self):
        self.user.create_shopping_list("gadgets", "cool gadgets for every gizmo",
                                       items={1: ['mac book', 'apple', 1]})
        self.user.delete_shopping_list(1)
        self.assertEquals(len(self.user.shopping_lists), 0, msg="shopping list was not deleted")

    def test_view_items_on_shopping_list(self):
        self.user.create_shopping_list("gadgets", "cool gadgets for every gizmo",
                                       items={1: ['mac book', 'apple', 1]})
        my_shopping_lists = self.user.view_shopping_lists()
        self.assertEquals(my_shopping_lists[1][0], "gadgets", "view all shopping lists failed")


class ShoppingListAppTest(unittest.TestCase):
    """Tests for the ShoppingListApp class"""
    def setUp(self):
        self.app = ShoppingListApp()

    def test_register_user(self):
        self.assertTrue(
            self.app.register_user(username="king", password1="root", password2="root"),
            msg="failed to register a user"
        )

    def test_login_user(self):
        self.app.register_user(username="king", password1="root", password2="root")
        self.assertTrue(self.app.login_user(username="king", password="root"),
                        msg="failed to login user")

    def test_get_user(self):
        self.app.register_user(username="king", password1="root", password2="root")
        self.assertIsInstance(self.app.get_user("king"), User, "failed to get a user")

if __name__ == '__main__':
    unittest.main()
