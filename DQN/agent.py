#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import skimage
import skimage.color
import skimage.exposure
import skimage.transform
from skimage import io
import numpy as np



class DQNagent():

    """Docstring for DQNagent. """

    def __init__(self, mode, backuppath, **kwargs):
        """TODO: to be defined. """
        self.num_input_frames = 4
        self.replay_memory_record = deque()
        self.replay_memory_size = 5e4
        self.img_size = (80, 80)
        self.input_image = None
    def record(self, action, reward, score, image):
        """TODO: Docstring for record.

        :action: TODO
        :reward: TODO
        :score: TODO
        :image: TODO
        :returns: TODO

        """

        # preprocess the image. image: 80x80
        image = self.preprocess(image, self.img_size)
        
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
            next_input_image = np.append(image, self.input_image[:, :, :, :self.num_input_frames - 1, axis = 3])
            self.replay_memory_record.append((self.input_image, np.array([action]), np.array([reward]), next_input_image, np.array([int(is_game_running)])))
            self.input_image = next_input_image

        if len(self.replay_memory_record) > self.replay_memory_size:
            self.replay_memory_record.popleft()


    """Preprocess the image"""
    def preprocess(image, image_size):
        image = image.astype(np.uint8)
        image = skimage.color.rgb2gray(image)
        image = skimage.transform.resize(image, img_size, mode = 'constant')
        image = skimage.exposure.rescale_intensity(image, out_range=(0, 255))
        image = image / 255.0
        return image
        # return a ndarray with shape 2
