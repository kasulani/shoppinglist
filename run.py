# coding=utf-8
from app import app

app.logger.info("Starting Shopping List application...\n")
app.run(host='127.0.0.1',
        port=app.config['PORT'],
        use_reloader=False,
        debug=app.config['DEBUG'])
