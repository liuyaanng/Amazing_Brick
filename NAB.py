#!/usr/bin/env python
# -*- coding: utf-8 -*-


import arcade
import random


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Amazing Brick"
SCALING = 1.0
BALL_SOURCE = "images/ship.bmp"

BALL_SWING = 5
BALL_SLIDE = 1
BALL_UP_SPEED = 75
BALL_DOWN_SPEED = 6
CONTINUE_TIME1 = 0.7
CONTINUE_TIME2 = 5.0


class AB(arcade.Window):

    """Docstring for AB. """

    def __init__(self):
        """TODO: to be defined. """
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        

        # Set the empty sprite lists
        self.all_sprites = arcade.SpriteList()
        self.ball_sprites = arcade.SpriteList()
    def setup(self):
        """TODO: Docstring for setup.
        :returns: TODO

        """
        arcade.set_background_color(arcade.color.WHITE)
        self.player = arcade.Sprite(BALL_SOURCE, SCALING)
        self.player.bottom = SCREEN_HEIGHT /2
        self.player.center_x = SCREEN_WIDTH / 2
        self.ball_sprites.append(self.player)
        #self.all_sprites.append(self.player)

        self.player.change_y = -BALL_DOWN_SPEED
        self.player.jumpleft = False
        self.player.jumpright = False
        #self.player.change_x = 0.1
        #self.player.change_y = 0
        self.player.delta_times = 0.0
    def on_key_press(self, symbol, modifiers):
        """TODO: Docstring for on_key_press.

        :symbol: TODO
        :modifiers: TODO
        :returns: TODO

        """
        if symbol == arcade.key.Q:
            arcade.close_window()
        
        if symbol == arcade.key.N or symbol == arcade.key.LEFT:
            #self.player.jumpleft = True
            #self.player.jumpright = False
            self.player.change_y = BALL_UP_SPEED
            self.player.change_x = -BALL_SWING

            #self.player.change_x *= -BALL_JUMP_SPEED * 100
            #self.player.change_y *= BALL_JUMP_SPEED / 2
            #self.player.change_y = 10
        if symbol == arcade.key.I or symbol == arcade.key.RIGHT:
            #self.player.jumpright = True
            #self.player.jumpleft = False
            self.player.change_y = BALL_UP_SPEED
            self.player.change_x = BALL_SWING
            #print(type(self.player.center_x))


    def on_key_release(self, symbol: int, modifiers: int):
        """TODO: Docstring for on_key_release(self, symbol, modifiers):.
        :returns: TODO

        """
        if (
            symbol == arcade.key.N
            #or symbol == arcade.key.I
            #or symbol == arcade.key.LEFT
            or symbol == arcade.key.RIGHT
        ):
            self.player.change_x = -BALL_SLIDE
            self.player.change_y = -BALL_DOWN_SPEED
            self.player.delta_times = 0.0
        else:
            self.player.change_x = BALL_SLIDE
            self.player.change_y = -BALL_DOWN_SPEED
            self.player.delta_times = 0.0


    def on_update(self, delta_time: float):
        """TODO: Docstring for on_update.

        :delta_time: TODO
        :returns: TODO

        """
        #print(delta_time)
        #print(self.player.change_x)
        #print(self.player.delta_times)
        #print(self.player.change_y)
        self.player.delta_times += delta_time

        self.player.change_y -=  self.player.delta_times
        self.ball_sprites.update()
        if self.player.jumpleft:
            self.player.change_x = -100
            self.player.delta_times += delta_time
            if self.player.delta_times <= CONTINUE_TIME1:
                self.player.change_y = GRAVITY * 50
                self.player.change_x += -15
                print(self.player.change_x)
            elif self.player.delta_times <= CONTINUE_TIME2:
                self.player.change_x += 60
                self.player.change_y += -GRAVITY * 10
            else:
                self.player.jumpleft = False
                self.player.delta_times = 0.0
                self.player.change_x = 5
        if self.player.jumpright:
            self.player.change_x = 100
            self.player.delta_times += delta_time
            if self.player.delta_times <= CONTINUE_TIME1:
                self.player.change_y += GRAVITY * 50
                self.player.change_x += 15
            elif self.player.delta_times <= CONTINUE_TIME2:
                self.player.change_x -= 60
                self.player.change_y += -GRAVITY * 10
            else:
                self.player.jumpright = False
                self.player.delta_time = 0.0
                self.player.change_x = 5

        if self.player.bottom < 0:
            self.player.bottom = 0
        #self.player.center_x += self.player.change_x * delta_time
        #self.player.center_y += self.player.change_y * delta_time
        
        #self.player.change_y = -GRAVITY * 10


        #self.player.center_x = int( self.player.center_x + delta_time * self.player.change_x )
        #self.player.center_y = int( self.player.center_y - 10 * delta_time * delta_time * GRAVITY )


    def on_draw(self):
        """TODO: Docstring for on_drew.
        :returns: TODO

        """
        arcade.start_render()
        self.ball_sprites.draw()


if __name__ == "__main__":
    AB = AB()
    AB.setup()
    arcade.run()
        
        
        
