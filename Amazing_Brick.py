#!/usr/bin/env python
# -*- coding: utf-8 -*-

import arcade
import skimage
import ENV.env_amazing_brick as game
import numpy as np
import random
def play_Amazing_Brick():
    # Step1: init BrainDQN
    #brain = BrainDQN()

    # Step2: init Amazing Brick game
    amazingbrick = game.ENV()
    amazingbrick.setup()
    arcade.run()

def main():
    play_Amazing_Brick()

if __name__ == "__main__":
    main()
