from app.neuralnetwork.three_layer_ann import run_net, classify
from app.ling_prepro_hrishi.core import fingerprint_word
import numpy as np

def convert_fingerprint(words):
    return map(fingerprint_word, words)

def train(x, y):
    run_net(x, y)
