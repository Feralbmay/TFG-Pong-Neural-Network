import numpy as np

class Network(object):

    def __init__(self, sizes):
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.biases = [np.random.randn(y, 1) for y in sizes[1:]]
        self.weights = [np.random.randn(y, x)
                        for x, y in zip(sizes[:-1], sizes[1:])]


    def feedforward(self, a):
        """Return the output of the network if "a" is input."""
        for b, w in zip(self.biases, self.weights):
            a = sigmoid(np.dot(w, a)+b)
        return a

    def generate_child(self):
        #Genera una xarxa fill de la xarxa pare.
        child = Network(self.sizes)
        # Recalcula els biaxos de la xarxa fill
        for i, b in enumerate(self.biases):
            child.biases[i] = b + child.biases[i] * 0.1

        #Recalcula els pesos de la xarxa fill
        for i, w in enumerate(self.weights):
            child.weights[i] = w + child.weights[i] * 0.1

        return child


def sigmoid(z):
    return 1.0/(1.0+np.exp(-z))
