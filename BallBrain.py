import keras.callbacks
import tensorflow as tf
import numpy as np
from tensorflow.python.keras import Sequential


def check_and_resize(inp, targ):
    index = 0
    for i in range(0, 100):
        if inp[index][0] == np.inf:
            new_inp = inp[:index]
            new_targ = inp[:index]
            return new_inp, new_targ, index
        index += 1
    return inp, targ, index


class NeuralNet:
    def __init__(self, inputs, targets):
        self.model = None
        self.index = None
        self.output = np.zeros(8)
        self.inputs = inputs
        self.targets = targets

    def create(self):
        inputs = tf.keras.Input(shape=self.inputs.shape[1:])
        x = tf.keras.layers.Dense(9, activation='relu')(inputs)
        outputs = tf.keras.layers.Dense(8, activation='softmax')(x)
        model = tf.keras.Model(inputs=inputs, outputs=outputs)

        self.model = model
        self.model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    def update_values(self, new_inputs, new_targets):
        self.inputs = new_inputs
        self.targets = new_targets
        self.inputs, self.targets, self.index = check_and_resize(self.inputs, self.targets)
        print("Inputs: ")
        print(self.inputs)
        print("\n")

    def run(self):
        self.model.fit(self.inputs, self.targets, batch_size=self.index, epochs=30)

    def make_prediction(self, x):
        return self.model.predict(x, verbose='0')

