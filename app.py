import flask, os
app = flask.Flask(__name__, template_folder='templates')
@app.route('/api/sample/<filename>')
def api_sample(filename):
    return flask.send_from_directory('Brain-Tumor-Test-Images', filename)
