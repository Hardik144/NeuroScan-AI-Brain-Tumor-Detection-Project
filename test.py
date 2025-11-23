import torch
from torch.nn import Sequential, Linear, SELU, Dropout, LogSigmoid
from torchvision.models import resnet50
model = resnet50(weights=None)
n_inputs = model.fc.in_features
model.fc = Sequential(Linear(n_inputs, 2048), SELU(), Dropout(0.4), Linear(2048, 2048), SELU(), Dropout(0.4), Linear(2048, 4), LogSigmoid())
