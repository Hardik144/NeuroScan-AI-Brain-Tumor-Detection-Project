import argparse, torch, os
device = 'cuda' if torch.cuda.is_available() else 'cpu'
