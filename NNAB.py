#!/usr/bin/env python
# -*- coding: utf-8 -*-


import arcade
import random


SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Amazing Brick"
SCALING = 0.7
BALL_SOURCE = ":resources:images/enemies/bee.png"
PIPE_MAXINUM = 300
PIPE_MININUM = 200
PIPE_INTERVAL = 220
BALL_MOVEMENT_SPEED = 5
BALL_JUMP_SPEED = 20
GRAVITY = 1
class AB(arcade.Window):

    """Docstring for AB. """

    def __init__(self):
        """TODO: to be defined. """
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        

        # Set the empty sprite lists
        self.ball_sprites = arcade.SpriteList()
        self.pipe_sprites = arcade.SpriteList()
        # physics engine
        self.physics_engine = None
        # the left pipe's right position
        self.pipe_position = 0
    def setup(self):
        """TODO: Docstring for setup.
        :returns: TODO

        """
        arcade.set_background_color(arcade.color.WHITE)
        self.player = arcade.Sprite(BALL_SOURCE, SCALING)
        self.player.bottom = SCREEN_HEIGHT / 3
        self.player.center_x = SCREEN_WIDTH / 2
        self.ball_sprites.append(self.player)
        # check hit, but it's a useless parameter
        self.wall = arcade.SpriteList()
        
        # Create the pipe
        for y in range(int(self.player.bottom) + 100, 900, 300):
            self.pipe_position = random.randint(PIPE_MININUM, PIPE_MAXINUM)
            for x in range(0, self.pipe_position, 64):
                pipe = arcade.Sprite(":resources:images/tiles/lavaTop_low.png", SCALING)
                pipe.center_x = x
                pipe.center_y = y
                self.pipe_sprites.append(pipe)

                pipe = arcade.Sprite(":resources:images/tiles/lavaTop_low.png", SCALING)
                pipe.center_x = x + PIPE_INTERVAL + self.pipe_position
                pipe.center_y = y
                self.pipe_sprites.append(pipe)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, self.wall, GRAVITY)
    def on_key_press(self, symbol, modifiers):
        """TODO: Docstring for on_key_press.

        :symbol: TODO
        :modifiers: TODO
        :returns: TODO

        """
        if symbol == arcade.key.Q:
            arcade.close_window()
        
        if symbol == arcade.key.N or symbol == arcade.key.LEFT:
            self.player.change_y = BALL_JUMP_SPEED
            self.player.change_x = -BALL_MOVEMENT_SPEED

        if symbol == arcade.key.I or symbol == arcade.key.RIGHT:
            self.player.change_y = BALL_JUMP_SPEED
            self.player.change_x = BALL_MOVEMENT_SPEED


    def on_key_release(self, symbol: int, modifiers: int):
        """TODO: Docstring for on_key_release(self, symbol, modifiers):.
        :returns: TODO

        """
        if (
            symbol == arcade.key.N
            or symbol == arcade.key.RIGHT
        ):
            self.player.change_x = -BALL_MOVEMENT_SPEED * 0.5
        if (
            symbol == arcade.key.I
            or symbol == arcade.key.LEFT
        ):
            self.player.change_x = BALL_MOVEMENT_SPEED * 0.5


    def on_update(self, delta_time: float):
        """TODO: Docstring for on_update.

        :delta_time: TODO
        :returns: TODO

        """
        #print(delta_time)
        #print(self.player.change_x)
        #print(self.player.delta_times)
        #print(self.player.change_y)
        self.physics_engine.update()
        if self.player.bottom < 0:
            self.player.bottom = 0


    def on_draw(self):
        """TODO: Docstring for on_drew.
        :returns: TODO

        """
        arcade.start_render()
        self.ball_sprites.draw()
        self.pipe_sprites.draw()
        print(len(self.pipe_sprites))

if __name__ == "__main__":
    AB = AB()
    AB.setup()
    arcade.run()
        
        
        
