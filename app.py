import flask, os
app = flask.Flask(__name__, template_folder='templates')
UPLOAD_FOLDER = os.path.join('static', 'photos')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
