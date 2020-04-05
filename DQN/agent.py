#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import skimage
import skimage.color
import skimage.exposure
import skimage.transform
from skimage import io
import numpy as np
img_size = [80,80]
class DQNagent():

    """Docstring for DQNagent. """


    """Preprocess the image"""
    def preprocess(image_name,image):
        image = skimage.color.rgb2gray(image)
        image = skimage.transform.resize(image, img_size, mode = 'constant')
        image = skimage.exposure.rescale_intensity(image, out_range=(0,255))
        #io.imshow(image)
        #io.show()
        io.imsave(image_name,image)


# if __name__ == "__main__":
    # A = DQNagent()
    # image_path = '/Users/kevin/Pictures/pap.er/ZzUbvqIkwhU.jpg'
    # image_size = [80,80]
    # img = A.preprocess(image_path, image_size)
    # print(img)
