from app.neuralnetwork.three_layer_ann import run_net, classify
from app.ling_prepro_hrishi.core import fingerprint_word
import numpy as np

def convert_fingerprint(words):
    return map(fingerprint_word, words)

def convert_to_x(fingerprints):
    arrs = [np.array([int(d) for d in fingerprint]) for fingerprint in fingerprints]
    return np.array(arrs)

def convert_to_y(length, classification):
    arrs = np.array([[classification] for i in range(length)])
    return arrs

def convert_from_positives_and_negatives(positives, negatives):
    p_length, n_length = len(positives), len(negatives)
    x = np.concatenate(convert_to_x(convert_fingerprint(positives)), convert_to_x(convert_fingerprint(negatives)))
    y = np.concatenate(convert_to_y(p_length, 1), convert_to_y(negatives, 0))
    return x, y

def get_class(positives, negatives, to_classify):
    """
    to_classify should be a word
    """
    x, y = convert_from_positives_and_negatives(positives, negatives)
    return classify(x, y, to_classify)
