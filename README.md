# ShoppingList
[![Build Status](https://travis-ci.org/kasulani/Shoppinglist.svg?branch=master)](https://travis-ci.org/kasulani/shoppinglist)
## About
This is an application that allows to record and share things they want
to spend money on and keep track of their shopping lists.
## Goal
The goal of this application is to enable users keep track of their shopping lists and further
provide an innovative and robust solution that will allow them share their
shopping lists with others.
## Features
- You can create a user account - Registration
- You can login and log out - Authorization and Authentication
- You can create, view, update, and delete a shopping list in your user account
- You can create, view, update, and delete an item in your shopping list under your account
- Extra: You can share your shopping list with your friends and have fun!
## Requirements
- Python 2.7.1x+. preferably use Python 3.x.x+
## Tools
Tools used during the development of this application are;
- [Balsamiq](https://balsamiq.com/) - this is a wire-framing tool
- [Flask](http://flask.pocoo.org/) - this is a python micro-framework
- [Bootstrap](http://getbootstrap.com/) - this is a HTML/CSS/JS framework
- [postgresql](https://www.postgresql.org/) - this is a database server
- [React](https://facebook.github.io/react/) - this is a java script library
to build user interfaces
## Tests
To run tests, go to your command line prompt and execute the following command
```sh
   $ cd shoppinglist/app
   $ python test_models.py
```
## Non-Persistent data
This branch of shopping list application implements a prototype that uses non persistent data so that
means that the data will be lost when the application is closed.
## Running the application
To run this application in linux, execute the following command
```sh
    $ cd shoppinglist
    $ nohup python run.py > logs/shop.log 2>&1>> logs/shop.log & disown
```
