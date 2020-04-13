#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import skimage
import skimage.color
import skimage.exposure
import skimage.transform
from skimage import io
import numpy as np
import random
from collections import deque
from tensorflow.keras.optimizers import Adam
from DQN.DQN import *
class DQNagent():

    """Docstring for DQNagent. """

    def __init__(self, **kwargs):
        """TODO: to be defined. """
        
        self.discount_factor = 0.99
        self.epsilon = 0.1
        self.init_epsilon = 0.1
        self.final_epsilon = 1e-4

        self.num_observes = 3200
        self.num_explores = 3e6
        self.num_iters = 0

        self.num_actions = 3
        self.num_input_frames = 4
        self.replay_memory_record = deque()
        self.replay_memory_size = 5e4
        self.image_size = (80, 80)
        self.input_image = None

        self.batch_size = 32


        # create q network
        self.DQN_model = Build_Q_network(image_size = self.image_size, channels = self.num_input_frames, num_actions = self.num_actions)

        self.optimizer = Adam(lr = 1e-4)
        self.DQN_model.compile(loss = 'mse', optimizer = self.optimizer)

    def NextAction(self, reward):
        """TODO: Docstring for NextAction.

        :reward: TODO
        :returns: TODO

        """
        # As the training progresses, ε control of actions becomes less and less important
        if self.epsilon > self.final_epsilon and self.num_iters > self.num_observes:
            self.epsilon -= (self.init_epsilon - self.final_epsilon ) / self.num_explores
        self.num_iters += 1

        # Make decision
        # ε-greddy
        if random.random() <= self.epsilon:
            action = random.choice([0, 1, 2])
        else:
            q = self.DQN_model.predict(self.input_image)
            action = np.argmax(q)

        # Train model
        loss = 0
        if self.num_iters > self.num_observes:
            # Sample values
            minibatch = random.sample(self.replay_memory_record, self.batch_size)

            # Find every label list
            states, actions, rewards, states_next, is_game_running = zip(*minibatch)
            # Concatenate arrays
            states = np.concatenate(states)
            states_next = np.concatenate(states_next)
            targets = self.DQN_model.predict(states_next)
            targets[range[32], action] = rewards + self.discount_factor *np.max(self.DQN_model.predict(states_next), axis = 1) * is_game_running
            loss = self.DQN_model.train_on_batch(states, targets)

            if self.num_iters % self.save_interval == 0:
                self.SaveModel(self.backup_path)





    def record(self, action, reward, score, is_game_running, image):
        """TODO: Docstring for record.

        :action: TODO
        :reward: TODO
        :score: TODO
        :image: TODO
        :returns: TODO

        """

        # preprocess the image. image: 80x80
        image = self.preprocess(image, self.image_size)
        
        # record the scene and corresponding info
        if self.input_image is None:
            # set image: 80x80x4
            self.input_image = np.stack((image, )*self.num_input_frames, axis = 2)
            # set image: 1x80x80x4
            self.input_image = self.input_image.reshape(1, self.input_image.shape[0], self.input_image.shape[1], self.input_image.shape[2])
        else:
            # set image frame equal (the current image + the last 3 images)
            # set image: 1x80x80x1
            image = image.reshape(1, image.shape[0], image.shape[1], 1)
            # current image + the last 3 images
            next_input_image = np.append(image, self.input_image[:, :, :, :self.num_input_frames - 1], axis = 3)
            self.replay_memory_record.append((self.input_image, np.array([action]), np.array([reward]), next_input_image, np.array([int(is_game_running)])))
            self.input_image = next_input_image

        if len(self.replay_memory_record) > self.replay_memory_size:
            self.replay_memory_record.popleft()


    """Preprocess the image"""
    def preprocess(self, image, image_size):
        image = image.astype(np.uint8)
        image = skimage.color.rgb2gray(image)
        image = skimage.transform.resize(image, image_size, mode = 'constant')
        image = skimage.exposure.rescale_intensity(image, out_range=(0, 255))
        image = image / 255.0
        return image
        # return a ndarray with shape 2
