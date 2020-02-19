#!/usr/bin/env python
# -*- coding: utf-8 -*-


import arcade
import random


SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Amazing Brick"
SCALING = 0.5
# image size: 128x128
IMAGE_SIZE = 128
PIPE_SOURCE = ":resources:images/tiles/lavaTop_low.png"
BALL_SOURCE = ":resources:images/enemies/bee.png"
ENEMY_SOURCE = ":resources:images/space_shooter/meteorGrey_big3.png"
PIPE_MAXINUM = 300
PIPE_MININUM = 200
PIPE_INTERVAL = 250
PIPE_TWO_DISTANCE = 600
BALL_MOVEMENT_SPEED = 5
BALL_JUMP_SPEED = 20
GRAVITY = 1
SCORE = 0

# How many pixels to keep as a minium margin between character 
# and the edge of the screen
TOP_VIEW_MARGIN = 350

class AB(arcade.Window):

    """Docstring for AB. """

    def __init__(self):
        """TODO: to be defined. """
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        

        # Set the empty sprite lists
        self.ball_sprites = arcade.SpriteList()
        self.pipe_sprites = arcade.SpriteList()
        self.enemy_sprites = arcade.SpriteList()
        # physics engine
        self.physics_engine = None
        # the left pipe's right position
        self.pipe_position = 0

        self.enemy_position = 0

        # Used to keep track of our scrolling
        self.view_bottom = 0

        # Keep track of the Score
        self.score = 0

    def setup(self):
        """TODO: Docstring for setup.
        :returns: TODO

        """
        arcade.set_background_color(arcade.color.WHITE)
        self.player = arcade.Sprite(BALL_SOURCE, SCALING)
        self.player.center_y = SCREEN_HEIGHT - TOP_VIEW_MARGIN
        self.player.center_x = SCREEN_WIDTH / 2
        self.ball_sprites.append(self.player)
        # check hit, but it's a useless parameter
        self.wall = arcade.SpriteList()

        # Keep track of the Score
        self.score = 0

        
        # Create the pipe
        for y in range(int(SCREEN_HEIGHT + IMAGE_SIZE), 100000, PIPE_TWO_DISTANCE):
            self.pipe_position = random.randint(PIPE_MININUM, PIPE_MAXINUM)
            for x in range(0, self.pipe_position, int(IMAGE_SIZE * SCALING)):
                pipe = arcade.Sprite(PIPE_SOURCE, SCALING)
  
                pipe.center_x = x
                pipe.center_y = y
                self.pipe_sprites.append(pipe)

                pipe = arcade.Sprite(PIPE_SOURCE, SCALING)
                pipe.center_x = x + PIPE_INTERVAL + self.pipe_position - self.pipe_position % (IMAGE_SIZE * SCALING)
                pipe.center_y = y
                self.pipe_sprites.append(pipe)

            for x in range(0, 2):
                self.enemy_position = random.randint(self.pipe_position + 25, self.pipe_position + PIPE_INTERVAL - 25)
                enemy = arcade.Sprite(ENEMY_SOURCE, SCALING)
                enemy.center_x = self.enemy_position
                enemy.center_y = y + 150 + x * 250
                self.enemy_sprites.append(enemy)
                

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
        :returns: TODO:resources:images/tiles/lavaTop_low.png

        """
        if (self.player.collides_with_list(self.pipe_sprites) 
            or self.player.collides_with_list(self.enemy_sprites)
            or self.player.bottom < 0):
            arcade.close_window()
            #self.setup()
        SCORE = 0
        self.physics_engine.update()
        
        # Cal score
        if self.player.center_y > SCREEN_HEIGHT + IMAGE_SIZE:
            
            SCORE = int((self.player.center_y - (SCREEN_HEIGHT + IMAGE_SIZE) ) / PIPE_TWO_DISTANCE) + 1
        #self.score = Score
        if self.score < SCORE:
            self.score = SCORE
        else:
            self.score = self.score


        # Manage Scrolling

        changed = False

        # Scrolling up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEW_MARGIN
        if self.player.top > top_boundary:
            self.view_bottom += self.player.top - top_boundary
            changed = True

        if changed:
            # Only scroll to integers. -> Make sure we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            
            # Do the scrolling
            arcade.set_viewport(0, SCREEN_WIDTH, self.view_bottom, SCREEN_HEIGHT + self.view_bottom)


    def on_draw(self):
        """TODO: Docstring for on_drew.
        :returns: TODO

        """
        arcade.start_render()
        self.ball_sprites.draw()
        self.pipe_sprites.draw()
        self.enemy_sprites.draw()
        #print(len(self.pipe_sprites))

        # Draw score on the screen
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10 , self.view_bottom + 10, arcade.csscolor.BLACK, 18, font_name = "FreeSans")


if __name__ == "__main__":
    AB = AB()
    AB.setup()
    arcade.run()
        
        
        
