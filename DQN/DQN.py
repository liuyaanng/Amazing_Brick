#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tensorflow as tf

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D, Activation

# create  net
def Build_Q_network(image_size, channels, num_actions, **kwargs):
    """TODO: Docstring for Build_Q_network.
    :returns: TODO

    """
    DQN_model = Sequential([Conv2D(32, (8, 8), strides = (4, 4), padding = 'same', input_shape = (*image_size, channels)),
                            Activation('relu'),
                            Conv2D(64, (4, 4), strides = (2, 2), padding = 'same'),
                            Activation('relu'),
                            Conv2D(64, (3, 3), strides = (1, 1), padding = 'same'),
                            Activation('relu'),
                            Flatten(),
                            Dense(512),
                            Activation('relu'),
                            Dense(num_actions)])
    return DQN_model

# network summary is showed by test.py

