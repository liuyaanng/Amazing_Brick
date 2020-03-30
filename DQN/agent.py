#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import skimage
import skimage.color
import skimage.exposure
import skimage.transform
import numpy as np
from skimage import io

class DQNagent():

    """Docstring for DQNagent. """

    def __init__(self):
        """TODO: to be defined. """

    """Preprocess the image"""
    def preprocess(self, image, imagesize):
        image = io.imread(image)
        image = skimage.color.rgb2gray(image)
        image = skimage.transform.resize(image, imagesize, mode = 'constant')
        io.imshow(image)
        io.show()
        image = skimage.exposure.rescale_intensity(image, out_range=(0,255))
        image = image / 255.0
        return image


if __name__ == "__main__":
    A = DQNagent()
    image_path = '/Users/kevin/Github/Myrep/Amazing_Brick/images/bee.png'
image_size = [160,80]
    A.preprocess(image_path, image_size)
