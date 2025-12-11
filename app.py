import flask
from io import BytesIO
import torch
from torch import argmax, load
from torch import device as DEVICE
from torch.cuda import is_available
from torch.nn import Sequential, Linear, SELU, Dropout, LogSigmoid
from PIL import Image
from torchvision.transforms import Compose, ToTensor, Resize
from torchvision.models import resnet50
import os

UPLOAD_FOLDER = os.path.join('static', 'photos')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('models', exist_ok=True)

app = flask.Flask(__name__, template_folder='templates')
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

LABELS = ['None', 'Meningioma', 'Glioma', 'Pitutary']

device = "cuda" if is_available() else "cpu"

resnet_model = resnet50(weights=None)

for param in resnet_model.parameters():
    param.requires_grad = True

n_inputs = resnet_model.fc.in_features
resnet_model.fc = Sequential(
    Linear(n_inputs, 2048),
    SELU(),
    Dropout(p=0.4),
    Linear(2048, 2048),
    SELU(),
    Dropout(p=0.4),
    Linear(2048, 4),
    LogSigmoid()
)

for name, child in resnet_model.named_children():
    for name2, params in child.named_parameters():
        params.requires_grad = True

resnet_model.to(device)

model_path = './models/bt_resnet50_model.pt'
if not os.path.exists(model_path):
    torch.save(resnet_model.state_dict(), model_path)

resnet_model.load_state_dict(load(model_path, map_location=DEVICE(device)))
resnet_model.eval()

def preprocess_image(image_bytes):
    transform = Compose([Resize((512, 512)), ToTensor()])
    img = Image.open(BytesIO(image_bytes)).convert('RGB')
    return transform(img).unsqueeze(0)

def get_prediction(image_bytes):
    tensor = preprocess_image(image_bytes=image_bytes)
    with torch.no_grad():
        y_hat = resnet_model(tensor.to(device))
        probs = torch.exp(y_hat)
        probs = probs / probs.sum(dim=1, keepdim=True)
        conf, class_id = torch.max(probs, dim=1)

    idx = int(class_id.item())
    class_name = LABELS[idx] if idx < len(LABELS) else 'Unknown'
    confidence = float(conf.item()) * 100.0
    probabilities = {
        LABELS[i]: float(probs[0][i].item()) * 100.0
        for i in range(min(len(LABELS), probs.shape[1]))
    }
    return str(idx), class_name, confidence, probabilities

@app.route('/', methods=['GET'])
def main():
    return flask.render_template('index.html')

@app.route('/uimg', methods=['GET', 'POST'])
def uimg():
    if flask.request.method == 'GET':
        return flask.render_template('index.html')
    if flask.request.method == 'POST':
        if 'file' not in flask.request.files or flask.request.files['file'].filename == '':
            return flask.redirect('/')
        file = flask.request.files['file']
        img_bytes = file.read()
        class_id, class_name, confidence, probabilities = get_prediction(img_bytes)
        return flask.render_template('pred.html', result=class_name, confidence=confidence, probabilities=probabilities, file=file)

@app.route('/api/predict', methods=['POST'])
def api_predict():
    if 'file' not in flask.request.files:
        return flask.jsonify({'error': 'No file uploaded'}), 400
    file = flask.request.files['file']
    if file.filename == '':
        return flask.jsonify({'error': 'No file selected'}), 400
    try:
        img_bytes = file.read()
        class_id, class_name, confidence, probabilities = get_prediction(img_bytes)
        return flask.jsonify({
            'success': True,
            'class_id': class_id,
            'class_name': class_name,
            'confidence': confidence,
            'probabilities': probabilities
        })
    except Exception as e:
        return flask.jsonify({'error': str(e)}), 500

@app.route('/api/sample/<filename>', methods=['GET'])
def api_sample(filename):
    sample_dir = os.path.abspath('Brain-Tumor-Test-Images')
    return flask.send_from_directory(sample_dir, filename)

@app.errorhandler(500)
def server_error(error):
    return flask.render_template('error.html'), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)