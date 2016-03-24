import numpy as np

def nonlin(x, deriv=False):
    if deriv == True:
        return x*(1-x)

    return 1 / (1 + np.exp(-x))

x = np.array([  [5, 3, 0, 0, 1],
                [2, 2, 4, 5, 3],
                [2, 1, 2, 4, 3],
                [4, 3, 1, 1, 1]])

y = np.array([  [0],
                [1],
                [1],
                [0]])

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

syn0, l1, syn1, l2 = run_net(x, y)

print "End training"
print syn0
print l1
print "============"
print syn1
print l2
print "============"
new_input = np.array([[1, 1, 3, 3, 3]])
print nonlin(np.dot(nonlin(np.dot(new_input, syn0)), syn1))
