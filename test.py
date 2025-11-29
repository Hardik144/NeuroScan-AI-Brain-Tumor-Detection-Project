import os
import sys
import argparse
from PIL import Image
import torch
import torch.nn.functional as F
from torch.nn import Sequential, Linear, SELU, Dropout, LogSigmoid
from torchvision.transforms import Compose, ToTensor, Resize
from torchvision.models import resnet50

LABELS = ['None', 'Meningioma', 'Glioma', 'Pitutary']
ICONS = {'None': '🟢', 'Meningioma': '🟡', 'Glioma': '🔴', 'Pitutary': '🟣'}

def build_model(model_path, device):
    model = resnet50(weights=None)
    n_inputs = model.fc.in_features
    model.fc = Sequential(
        Linear(n_inputs, 2048),
        SELU(),
        Dropout(p=0.4),
        Linear(2048, 2048),
        SELU(),
        Dropout(p=0.4),
        Linear(2048, 4),
        LogSigmoid()
    )
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}. Please ensure the model weights are present.")
    
    state_dict = torch.load(model_path, map_location=device)
    model.load_state_dict(state_dict)
    model.to(device)
    model.eval()
    return model

def predict_image(image_path, model, device):
    transform = Compose([Resize((512, 512)), ToTensor()])
    img = Image.open(image_path).convert('RGB')
    tensor = transform(img).unsqueeze(0).to(device)
    
    with torch.no_grad():
        output = model(tensor)
        probs = torch.exp(output)  # output uses LogSigmoid
        probs = probs / probs.sum(dim=1, keepdim=True)
        conf, pred_id = torch.max(probs, dim=1)
        
    class_id = int(pred_id.item())
    class_name = LABELS[class_id] if class_id < len(LABELS) else "Unknown"
    confidence = float(conf.item()) * 100
    return class_name, confidence

def main():
    parser = argparse.ArgumentParser(description="Brain Tumor Detection CLI")
    parser.add_argument("--image", required=True, help="Path to input MRI scan image")
    parser.add_argument("--model", default="./models/bt_resnet50_model.pt", help="Path to model weights file")
    args = parser.parse_args()

    if not os.path.exists(args.image):
        print(f"Error: Image file not found: {args.image}", file=sys.stderr)
        sys.exit(1)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    try:
        model = build_model(args.model, device)
        result, confidence = predict_image(args.image, model, device)
        icon = ICONS.get(result, "⚪")

        print("┌──────────────────────────────────────────────────┐")
        print("│           🧠 Brain Tumor Classifier              │")
        print("│  ──────────────────────────────────────────────  │")
        print(f"│   Result:  {icon}  {result.upper():<29} │")
        print(f"│   Confidence:  {confidence:.1f}%{'':<28} │")
        print("│                                                  │")
        print("│   ⚠️  Please consult a medical professional.     │")
        print("└──────────────────────────────────────────────────┘")
    except Exception as e:
        print(f"Error during prediction: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
