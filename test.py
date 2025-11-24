import torch
import torch.nn.functional as F
from torch.nn import Sequential, Linear, SELU, Dropout, LogSigmoid
from torchvision.models import resnet50
LABELS = ['None', 'Meningioma', 'Glioma', 'Pitutary']
def predict_probs(output):
    probs = torch.exp(output)
    return probs / probs.sum(dim=1, keepdim=True)
