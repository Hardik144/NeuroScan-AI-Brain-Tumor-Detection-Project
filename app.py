import flask, os
app = flask.Flask(__name__, template_folder='templates')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
@app.errorhandler(500)
def server_error(e):
    return flask.render_template('error.html'), 500
