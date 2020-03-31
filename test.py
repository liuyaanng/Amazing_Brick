#!/usr/bin/env python
# -*- coding: utf-8 -*-
import arcade
import random
import os
import pyglet
import Amazing_Brick
def get_action():
    """TODO: Docstring for get_action.
    :returns: TODO

    """
    
    action = random.randint(0,2)
    return action

if __name__ == "__main__":
    ABC = Amazing_Brick.AB()
    ABC.setup()
    image = arcade.run()
    print(image)
    print('Game over')
