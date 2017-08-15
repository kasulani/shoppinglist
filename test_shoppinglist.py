"""
    Shopping List Application
    Created: 14-August-2017
    Author: Emmanuel King Kasulani
    Email: kasulani@gmail.com

    This file contains all the tests for the classes in the shopping list application
"""
import unittest
from shoppinglist import ListItem, ShoppingList


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
    """Test for the ShoppingList class"""
    def setUp(self):
        self.shopping_list = ShoppingList()
        self.list_item = ListItem()

    def test_shoppingList_property_initialization(self):
        self.assertEquals(self.shopping_list.id, 0, msg="initial value of id should be zero")
        self.assertIsInstance(self.shopping_list.items, dict, msg="items is not a dictionary")

    def test_add_item_to_shopping_list(self):
        self.list_item.id = 1
        self.list_item.name = "mac book"
        self.shopping_list.add_item(self.list_item, 1)
        self.assertEquals(self.shopping_list.items[1], 1, msg="item was not added to shopping list")

    def test_update_item_on_shopping_list(self):
        self.list_item.id = 1
        self.list_item.name = "mac book"
        self.shopping_list.update_item(self.list_item, 2)
        self.assertEquals(self.shopping_list.items[1], 2, msg="item was not updated to shopping list")

    def test_delete_item_from_shopping_list(self):
        self.list_item.id = 1
        self.list_item.name = "mac book"
        self.shopping_list.add_item(self.list_item, 1)
        self.shopping_list.delete_item(1)
        self.assertTrue(self.shopping_list.items, msg="item was not deleted from shopping list")

    def test_view_items_on_shopping_list(self):
        self.list_item.id = 1
        self.list_item.name = "mac book"
        self.shopping_list.add_item(self.list_item, 1)
        self.assertIsInstance(self.shopping_list.items, dict, msg="items is not a dictionary")
        self.assertEquals(self.shopping_list.items[1], 1, msg="no items on the shopping list")

if __name__ == '__main__':
    unittest.main()
