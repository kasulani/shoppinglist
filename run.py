from app import app

app.logger.info("Starting Shopping List application...\n")
app.run(host='127.0.0.1',
        port=app.config['PORT'],
        use_reloader=True,
        debug=app.config['DEBUG'])
