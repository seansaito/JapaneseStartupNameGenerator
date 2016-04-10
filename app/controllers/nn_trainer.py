from app.neuralnetwork.three_layer_ann import run_net, classify, nonlin
from app.ling_prepro_hrishi.core import fingerprint_word
from app.nlp.loadword import getBadWords, getGoodWords
import numpy as np
import json, json_tricks, random
from global_vars import script_dir, weight_file

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

    This is the main function to call
    """
    # positives = random.sample(set(getGoodWords()), 20)
    # negatives = random.sample(set(getBadWords()), 20)
    # x, y = convert_from_positives_and_negatives(positives, negatives)
    # s0, l1, s1, l2 = run_net(x, y)
    # print s0
    # print s1
    print "[nn_trainer:get_class] Classying following words"
    print to_classify
    p = getGoodWords()
    n = getBadWords()
    s0, l1, s1, l2 = recursive_net(p, n)
    # print s0
    # print s1
    res = [nonlin(np.dot(nonlin(np.dot(convert_to_input(word), s0)), s1))[0, 0] for word in to_classify]

    return res

def nonlin(x, deriv=False):
    if deriv == True:
        return x*(1-x)

    return 1 / (1 + np.exp(-x))

def load_weights():
    """ Load cached weights from neuralnet_weight.json """
    fp = open(weight_file, "r+")
    try:
        store = json_tricks.np.load(fp)
    except:
        store = json.load(fp)
    fp.close()
    return (store["syn0"], store["syn1"])

def write_weights(syn0, syn1):
    fp = open(weight_file, "w+")
    store = {"syn0": syn0, "syn1": syn1}
    fp.write(json_tricks.np.dumps(store))
    fp.close()
    return

def recursive_net(p, n):
    np.random.seed(1)
    # randomly init weights with mean 0
    print "[nn_trainer:recursive_net] Loading weights"
    syn0, syn1 = load_weights()

    if syn0 == "" or syn1 == "":
        print "[nn_trainer:recursive_net] Initializing weights with random numbers"
        syn0 = 2 * np.random.random((6,4)) - 1
        syn1 = 2 * np.random.random((4,1)) - 1

    for i in xrange(1):
        positives = random.sample(set(p), 20)
        negatives = random.sample(set(n), 20)
        x, y = convert_from_positives_and_negatives(positives, negatives)

        for j in xrange(5000):

            # Feed fowrad through layers 0, 1, and 2
            l0 = x
            l1 = nonlin(np.dot(l0, syn0))
            l2 = nonlin(np.dot(l1, syn1))

            # calculate error
            l2_error = y - l2

            if (j % 1000) == 0:
                print "Error: " + str(np.mean(np.abs(l2_error)))

            l2_delta = l2_error * nonlin(l2, deriv=True)

            # how much did each l1 value contribute to the l2 error according to the weights?
            l1_error = l2_delta.dot(syn1.T)
            l1_delta = l1_error * nonlin(l1, deriv=True)

            syn1 += l1.T.dot(l2_delta)
            syn0 += l0.T.dot(l1_delta)

    print "[nn_trainer:recursive_net] Writing to json file"
    write_weights(syn0, syn1)

    return (syn0, l1, syn1, l2)

def run_net(x, y):

    np.random.seed(1)

    # randomly init weights with mean 0
    syn0 = 2 * np.random.random((x.shape[1],4)) - 1
    syn1 = 2 * np.random.random((4,1)) - 1

    for j in xrange(60000):

        # Feed fowrad through layers 0, 1, and 2
        l0 = x
        l1 = nonlin(np.dot(l0, syn0))
        l2 = nonlin(np.dot(l1, syn1))

        # calculate error
        l2_error = y - l2

        if (j % 10000) == 0:
            print "Error: " + str(np.mean(np.abs(l2_error)))



        l2_delta = l2_error * nonlin(l2, deriv=True)

        # how much did each l1 value contribute to the l2 error according to the weights?
        l1_error = l2_delta.dot(syn1.T)



        l1_delta = l1_error * nonlin(l1, deriv=True)

        syn1 += l1.T.dot(l2_delta)
        syn0 += l0.T.dot(l1_delta)

    return (syn0, l1, syn1, l2)

def classify(x, y, i):
    syn0, l1, syn1, l2 = run_net(x, y)
    res = nonlin(np.dot(nonlin(np.dot(i, syn0)), syn1))
    print res
    return res

def sample_run(num_pos, num_neg):
    """
    This function allows the user to test run the neural net.

    Args:
        num_pos (int)   : Number of words to sample from positive words
        num_neg (int)   : Number of words to sample from negative words
    """
    pos_sample = random.sample(getGoodWords(), num_pos)
    neg_sample = random.sample(getBadWords(), num_neg)

    pos_res = get_class(pos_sample)
    neg_res = get_class(neg_sample)

    print "========================================="
    print "===========Positive results=============="
    print "========================================="

    print pos_sample
    print pos_res

    print "========================================="
    print "===========Negative results=============="
    print "========================================="

    print neg_sample
    print neg_res

    return
