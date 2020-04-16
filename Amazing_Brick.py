#!/usr/bin/env python
# -*- coding: utf-8 -*-

import arcade
import os
import skimage
import ENV.env_amazing_brick as game
import numpy as np
import random
import argparse
from DQN.agent import *

def ParseArgs():
    """ Set friendly interface to users.
    :returns: TODO

    """
    parser = argparse.ArgumentParser(description = 'Choose mode what you want.')
    parser.add_argument('--mode', dest = 'mode', help = 'Choose an action between train and test(default is train)', default = 'train', type = str)
    parser.add_argument('--resume', dest = 'resume', help = 'If mode is trian and use --continue, check and load the training history', action = 'store_true')
    args = parser.parse_args()
    return args
def play_Amazing_Brick():
    # Step1: init BrainDQN
    #brain = BrainDQN()

    args = ParseArgs()
    mode = args.mode.lower()

    # Make sure mode is train or test
    assert mode in ['train', 'test']

    # modelpath
    if not os.path.exists('checkpoints'):
        os.mkdir('checkpoints')
    model_path = 'checkpoints/dqn.h5'
    agent = DQNagent(mode, model_path)
    if os.path.isfile(model_path):
        if mode == 'test' or (mode == 'train' and args.resume):
            agent.LoadModel(model_path)
    # Step2: init Amazing Brick game

    amazingbrick = game.ENV(agent)
    amazingbrick.setup()
    arcade.run()

def main():
    play_Amazing_Brick()

if __name__ == "__main__":

    main()
