#!/usr/bin/env python
# -*- coding: utf-8 -*-
import arcade
import random
import time
import env_amazing_brick
def get_action():
    """TODO: Docstring for get_action.
    :returns: TODO

    """
    action = random.randint(0,3)
    return action

if __name__ == "__main__":
    ABC = Amazing_Brick.AB()
    ABC.setup()
    image = arcade.run()
    print(image)
    print('Game over')
