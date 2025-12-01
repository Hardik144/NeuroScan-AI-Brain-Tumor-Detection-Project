import flask, os, torch
app = flask.Flask(__name__, template_folder='templates')
@app.route('/api/predict', methods=['POST'])
def api_predict():
    return flask.jsonify({'status': 'online'})
