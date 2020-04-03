#!/usr/bin/env python
# -*- coding: utf-8 -*-

import arcade
from ENV.cfg import *

'''bee class'''
class Bee(arcade.Sprite):

    """Docstring for Bee. """

    # def __init__(self):
        # """TODO: to be defined. """
        # arcade.Sprite.__init__(self)
        # self.action = action
    def update(self, action):
        """TODO: Update the position of the sprite by action.

        :action: TODO
        :returns: TODO
        """
        
        # Move the sprite
        #super().update()
        

        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH:
            self.right = SCREEN_WIDTH

        # action control game
        """
        :action: 
        0 --> left
        1 --> right
        2 --> None
        :returns: TODO
        """

        if action == 0:
            self.change_y = BALL_JUMP_SPEED
            self.change_x = -BALL_MOVEMENT_SPEED

        elif action == 1:
            self.change_y = BALL_JUMP_SPEED
            self.change_x = BALL_MOVEMENT_SPEED
        else:
            pass

        



