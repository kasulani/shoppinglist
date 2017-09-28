# coding=utf-8
"""
    Front End Tests for the shopping list web application
    24-September-2017
"""
import unittest
import urllib2
import time
from flask_testing import LiveServerTestCase
from flask import url_for
from selenium import webdriver
from app import app


class TestShopListBase(LiveServerTestCase):
    def create_app(self):
        app.config.update(LIVESERVER_PORT=8943)
        return app

    def setUp(self):
        self.driver = webdriver.Firefox(capabilities=dict(acceptInsecureCerts=False))
        self.driver.get(self.get_server_url())

    def tearDown(self):
        self.driver.quit()

    def login_into_app(self, username, password):
        """
        Method to login into application before tests are run that require login
        :param username:
        :param password:
        :return:
        """
        # fill in the login form
        self.driver.find_element_by_id("username").send_keys(username)
        self.driver.find_element_by_id("password").send_keys(password)
        self.driver.find_element_by_id("sign_in_btn").click()
        time.sleep(1)

    def register_account_in_app(self, username, password, confirm_password):
        """
        Method to register an account in the shopping list app before running test
        :param username:
        :param password:
        :param confirm_password:
        :return:
        """
        # fill in the sign up form
        self.driver.find_element_by_id("email").send_keys(username)
        self.driver.find_element_by_id("password").send_keys(password)
        self.driver.find_element_by_id("confirm_password").send_keys(confirm_password)
        self.driver.find_element_by_id("submit_btn").click()
        time.sleep(1)

    @unittest.skip("Skipping test server is up and running")
    def test_01_server_is_up_and_running(self):
        response = urllib2.urlopen(self.get_server_url())
        self.assertEqual(response.code, 200)

    #@unittest.skip("Skipping test register a new user")
    def test_02_register_new_user(self):
        """
        Test registering a new user using the web front end app
        :return:
        """
        # click on the sign up button on the index page
        self.driver.find_element_by_id("sign_up_btn").click()
        time.sleep(1)
        self.register_account_in_app("testuser@mail.com", "testuser123", "testuser123")
        msg = self.driver.find_element_by_id("feedback").text
        assert url_for('signup') in self.driver.current_url
        assert "Well done! user account created successfully" in msg

    #@unittest.skip("Skipping test")
    def test_03_register_existing_user(self):
        """
        Test registering an existing user using the web front end app
        :return:
        """
        # click on the sign up button on the index page
        self.driver.find_element_by_id("sign_up_btn").click()
        time.sleep(1)
        self.register_account_in_app("testuser@mail.com", "testuser123", "testuser123")
        msg = self.driver.find_element_by_id("error").text
        assert url_for('signup') in self.driver.current_url
        assert "Error! user already exists" in msg

    #@unittest.skip("Skipping test")
    def test_04_login_with_a_fake_account(self):
        """
        Test logging in a non existing user with a fake account
        :return:
        """
        self.login_into_app("fakeuser@mail.com", "fakeuser123")
        msg = self.driver.find_element_by_id("error").text
        assert url_for('dashboard') not in self.driver.current_url
        assert "Error! wrong password or username or may be user does't exist" in msg

    #@unittest.skip("Skipping test")
    def test_05_login_a_user_with_an_account(self):
        """
        Test logging in a user with an account
        :return:
        """
        self.login_into_app("testuser@mail.com", "testuser123")
        assert url_for('dashboard') in self.driver.current_url

    #@unittest.skip("Skipping test")
    def test_06_create_a_list(self):
        """
        Test creating a list
        :return:
        """
        self.login_into_app("testuser@mail.com", "testuser123")
        self.driver.find_element_by_id("add_list_btn").click()
        time.sleep(1)
        self.driver.find_element_by_id("listName").send_keys("House party")
        self.driver.find_element_by_id("listDescription").send_keys("My house party shopping list")
        self.driver.find_element_by_id("create_list_btn").click()
        time.sleep(1)
        msg = self.driver.find_element_by_id("feedback_msg").text
        assert "Shopping List: list created successfully" in msg
        time.sleep(1)

    #@unittest.skip("Skipping test")
    def test_07_add_an_item(self):
        """
        Test adding an item to a list
        :return:
        """
        self.login_into_app("testuser@mail.com", "testuser123")
        self.driver.find_element_by_id("list_item").click()
        time.sleep(1)
        self.driver.find_element_by_id("add_item_btn").click()
        time.sleep(1)
        self.driver.find_element_by_id("itemName").send_keys("Beers")
        self.driver.find_element_by_id("itemDescription").send_keys("Some lagers for the guests")
        self.driver.find_element_by_id("create_item_btn").click()
        time.sleep(1)
        msg = self.driver.find_element_by_id("feedback_msg").text
        assert "Shopping List: item added to list" in msg
        time.sleep(1)

    #@unittest.skip("Skipping test")
    def test_08_edit_a_list(self):
        """
        Test editing a list name and description
        :return:
        """
        self.login_into_app("testuser@mail.com", "testuser123")
        self.driver.find_element_by_id("edit_list_btn").click()
        time.sleep(1)
        self.driver.find_element_by_id("editListName").send_keys("-edited")
        self.driver.find_element_by_id("editListDescription").send_keys("-edited")
        self.driver.find_element_by_id("save_list_edit").click()
        time.sleep(1)
        msg = self.driver.find_element_by_id("feedback_msg").text
        assert "Shopping List: list updated" in msg

    def test_09_edit_an_item(self):
        """
        Test editing an item
        :return:
        """
        self.login_into_app("testuser@mail.com", "testuser123")
        self.driver.find_element_by_id("list_item").click()
        time.sleep(1)
        self.driver.find_element_by_id("edit_item_btn").click()
        self.driver.find_element_by_id("editItemName").send_keys("-edited")
        self.driver.find_element_by_id("editItemDescription").send_keys("-edited")
        self.driver.find_element_by_id("save_item_edit").click()
        time.sleep(1)
        msg = self.driver.find_element_by_id("feedback_msg").text
        assert "Shopping List: item updated" in msg

    #@unittest.skip("Skipping test")
    def test_10_edit_profile(self):
        """
        Test editing user profile
        :return:
        """
        self.login_into_app("testuser@mail.com", "testuser123")
        self.driver.find_element_by_id("profile_tab").click()
        self.driver.find_element_by_id("firstName").send_keys("Test")
        self.driver.find_element_by_id("lastName").send_keys("User")
        self.driver.find_element_by_id("aboutMe").send_keys("I am a test user")
        self.driver.find_element_by_id("save_profile").click()
        self.driver.find_element_by_id("profile_tab").click()  # go back to profile tab and confirm changes
        time.sleep(2)  # allow some 2 seconds to see feedback message and other changes
        msg = self.driver.find_element_by_id("feedback_msg").text
        assert "Shopping List: user updated" in msg

    #@unittest.skip("Skipping test")
    def test_11_change_password_and_logout(self):
        """
        Test changing a user password and logout feature
        :return:
        """
        self.login_into_app("testuser@mail.com", "testuser123")  # login into web app
        self.driver.find_element_by_id("profile_tab").click()  # click on the profile tab
        time.sleep(1)
        self.driver.find_element_by_id("reset_pass_btn").click()  # click on the reset password button to launch modal
        time.sleep(1)
        self.driver.find_element_by_id("oldpass").send_keys("testuser123")  # enter the old password
        self.driver.find_element_by_id("newpass1").send_keys("testuser1234")  # enter the new password
        self.driver.find_element_by_id("newpass2").send_keys("testuser1234")  # confirm the new password
        self.driver.find_element_by_id("reset_btn").click()  # click on the reset password button to call API
        time.sleep(1)
        msg = self.driver.find_element_by_id("feedback_msg").text
        assert "Shopping List: password was changed successfully" in msg
        time.sleep(1)
        # navigate to the log out link and log out
        self.driver.find_element_by_id("logout").click()
        assert url_for('index') in self.driver.current_url  # assert that logout takes you back to the login page

    #@unittest.skip("Skipping test")
    def test_12_delete_item_and_list(self):
        """
        Test deleting items and their list
        :return:
        """
        self.login_into_app("testuser@mail.com", "testuser1234")  # login into web app
        self.driver.find_element_by_id("list_item").click()  # click on the name of the list in the table to view items
        self.driver.find_element_by_id("delete_item_btn").click()  # go to item in table and click on the delete button
        time.sleep(1)
        #msg = self.driver.find_element_by_id("feedback_msg").text
        #assert "Shopping List: item deleted" in msg
        # navigate back to view all lists and select a list to delete
        self.driver.find_element_by_id("link_to_dashboard").click()  # click on breadcrumb link to view all lists
        time.sleep(2)
        self.driver.find_element_by_id("delete_list_btn").click()  # click on delete button to remove list
        time.sleep(1)
        msg = self.driver.find_element_by_id("feedback_msg").text
        assert "Shopping List: list deleted" in msg

if __name__ == '__main__':
    unittest.main()
