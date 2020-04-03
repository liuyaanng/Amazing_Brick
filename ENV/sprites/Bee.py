#!/usr/bin/env python
# -*- coding: utf-8 -*-

import arcade
SCREEN_WIDTH = 600

'''bee class'''
class Bee(arcade.Sprite):

    """Docstring for Bee. """

    # def __init__(self):
        # """TODO: to be defined. """
        # arcade.Sprite.__init__(self)

    def update(self):
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

        



