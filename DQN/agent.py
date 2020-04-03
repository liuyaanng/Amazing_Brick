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
        #image = skimage.exposure.rescale_intensity(image, out_range=(0,255))
        io.imshow(image)
        io.show()
        image = image / 255.0
        return image


if __name__ == "__main__":
    A = DQNagent()
    image_path = '/Users/kevin/Github/Myrep/Amazing_Brick/test.png'
    image_size = [80,80]
    img = A.preprocess(image_path, image_size)
    print(img)
