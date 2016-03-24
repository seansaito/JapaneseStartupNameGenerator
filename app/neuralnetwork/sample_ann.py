"""
Sample implementation of ANN
"""

import numpy as np

# Sigmoid
def sigmoid(x, deriv=False):
    if (deriv==True):
        return x*(1-x)
    return 1/(1 + np.exp(-x))

# input dataset
x = np.array([  [0,0,0],
                [0,1,0],
                [1,0,1],
                [1,1,1] ])

# output dataset
y = np.array([[0,0,1,1]]).T

np.random.seed(1)

syn0 = 2*np.random.random((3,1)) - 1

for i in xrange(10000):

    # forward prop
    l0 = x
    l1 = sigmoid(np.dot(l0, syn0))

    # error calc
    l1_error = y - l1

    l1_delta = l1_error * sigmoid(l1, True)

    # update weights
    syn0 += np.dot(l0.T, l1_delta)

print "Output after training"
print syn0
print l1

print "Sample using l1"
new_input = np.array([[0, 1, 0]])
print sigmoid(np.dot(new_input, syn0))
