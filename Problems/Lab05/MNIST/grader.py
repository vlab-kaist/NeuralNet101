import numpy as np
import torchvision.datasets as dsets
import torchvision.transforms as transforms


class NeuronAbstract:
    def __init__(self):
        raise Exception("Not implemented constructor")

    def forward(self, x):
        raise Exception("Not implemented forward")

    def loss(self, t):
        raise Exception("Not implemented loss")

    def backward(self, d_out, lr):
        raise Exception("Not implemented backward")


class ModelAbstract:
    def __init__(self, learning_rate):
        self.layer = []
        self.error = None
        self.learning_rate = learning_rate

    def add(self, layer):
        self.layer.append(layer)

    def getLoss(self, t):
        self.error = self.layer[-1].loss(t)
        return self.error

    def forward(self, x):
        raise Exception("Not implemented forward")

    def backward(self):
        raise Exception("Not implemented backward")


def sigmoid(x):
    np.clip(x, -100, 100, out=x)
    return 1 / (1 + np.exp((-1) * x))


def softmax(x):
    e = np.exp(x - np.max(x, axis=1, keepdims=True))
    return e / np.sum(e, axis=1, keepdims=True)


def mean_squared_error(y, t):
    return np.mean((y - t) ** 2)


def cross_entropy_error(y, t):
    return -np.sum(t * np.log(y + 1e-7)) / y.shape[0]


def get_data(encoding):
    mnist_train = dsets.MNIST(root="MNIST_data/", train=True, transform=transforms.ToTensor(), download=True)
    x_train = np.array(mnist_train.data.view(-1, 28 * 28).float()) / 255
    y_train = np.array([encoding[i] for i in mnist_train.targets])
    return x_train, y_train


if __name__ == '__main__':
    from mnist import get_model

    nb_epochs = 120
    nb_inner_epochs = 100
    batch_size = 1000

    encoding = np.eye(10)
    x_train, y_train = get_data(encoding)

    train_size = x_train.shape[0]
    model = get_model()

    for epoch in range(nb_epochs):
        X = x_train[((epoch * batch_size) % train_size):((epoch * batch_size) % train_size + batch_size)]
        Y = y_train[((epoch * batch_size) % train_size):((epoch * batch_size) % train_size) + batch_size]

        for inner_epoch in range(nb_inner_epochs):
            hypothesis = model.forward(X)
            loss = model.getLoss(Y)
            model.backward()

        print("Epoch : %d/%d, loss : %.7f" % (epoch + 1, nb_epochs, loss))
