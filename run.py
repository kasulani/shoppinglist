# coding=utf-8
from app import app, base_url

app.logger.info("Starting Shopping List application...\n")
app.logger.info("Base url for api requests is %s...\n" % base_url)
app.run(host='127.0.0.1',
        port=app.config['PORT'],
        use_reloader=False,
        debug=app.config['DEBUG'])
