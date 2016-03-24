from app.neuralnetwork.three_layer_ann import run_net, classify, nonlin
from app.ling_prepro_hrishi.core import fingerprint_word
from app.nlp.loadword import getBadWords, getGoodWords
import numpy as np

def convert_fingerprint(words):
    return map(fingerprint_word, words)

def convert_to_input(word):
    f = fingerprint_word(word)
    input = np.array([[int(d) for d in f]])
    return input

def convert_to_x(fingerprints):
    arrs = [np.array([int(d) for d in fingerprint]) for fingerprint in fingerprints]
    return np.array(arrs)

def convert_to_y(length, classification):
    arrs = np.array([[classification] for i in xrange(length)])
    return arrs

def convert_from_positives_and_negatives(positives, negatives):
    p_length, n_length = len(positives), len(negatives)
    x = np.concatenate((convert_to_x(convert_fingerprint(positives)), convert_to_x(convert_fingerprint(negatives))))
    y = np.concatenate((convert_to_y(p_length, 1), convert_to_y(n_length, 0)))
    return x, y

def get_class(to_classify):
    """
    to_classify should be an array of words
    """
    positives = getGoodWords()
    negatives = getBadWords()
    x, y = convert_from_positives_and_negatives(positives, negatives)
    print x
    print y
    syn0, l1, syn1, l2 = run_net(x, y)
    res = [nonlin(np.dot(nonlin(np.dot(convert_to_input(word), syn0)), syn1))[0, 0] for word in to_classify]

    return res
