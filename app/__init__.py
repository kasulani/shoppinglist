"""
    Shopping List Application
    Created: 14-August-2017
    Author: Emmanuel King Kasulani
    Email: kasulani@gmail.com
"""

import logging
from logging.handlers import RotatingFileHandler
from flask import Flask

app = Flask(__name__, instance_relative_config=True)

# load the config file in instance folder, don't suppress errors (silent=false)
app.config.from_pyfile('config.cfg', silent=False)
logfile = app.config['LOGFILE']
log_level = app.config['LEVEL']
# set logging format
formatter = logging.Formatter("[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
# set up file handler for the logger
handler = RotatingFileHandler(logfile, maxBytes=10000000, backupCount=5)
# set logging level as set in the config file
if log_level == 'DEBUG':
    handler.setLevel(logging.DEBUG)
else:
    handler.setLevel(logging.INFO)

handler.setFormatter(formatter)
app.logger.setLevel(log_level)
app.logger.addHandler(handler)

from app import views