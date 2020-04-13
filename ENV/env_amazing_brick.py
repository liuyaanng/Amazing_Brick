#!/usr/bin/env python
# -*- coding: utf-8 -*-


import arcade
import random
import time
import numpy as np
from ENV.sprites.Bee import *
from ENV.cfg import *

import sys
sys.path.append("..")
from DQN.agent import *
class ENV(arcade.Window):

    """Amazing Brick game environment. """

    def __init__(self):
        """TODO: to be defined. """
        super().__init__(SCREEN_WIDTH * RETINA_SCALING, SCREEN_HEIGHT * RETINA_SCALING, SCREEN_TITLE)
        
        # Set the empty sprite lists
        self.player_sprites =arcade.SpriteList()
        self.pipe_sprites = arcade.SpriteList()
        self.enemy_sprites = arcade.SpriteList()
        # Save all sprite
        self.all_sprites = arcade.SpriteList()

        self.MAX_SCORE = 0
        self.TOTAL_GAME_NUM = 0
        # for save image
        self.num = 0
        

        self.agent = DQNagent()
    def setup(self): 
        """TODO: Set up a new game.
        :returns: none

        """
        # remove all sprite
        self.player_sprites =arcade.SpriteList()
        self.pipe_sprites = arcade.SpriteList()
        self.enemy_sprites = arcade.SpriteList()
        self.all_sprites = arcade.SpriteList()

        # Set up a player
        self.player = Bee(BALL_SOURCE, SCALING)
        self.player.center_y = SCREEN_HEIGHT - TOP_VIEW_MARGIN
        self.player.center_x = SCREEN_WIDTH / 2
        self.player_sprites.append(self.player)

        # Create two pipes when set up the game.
        self.pipe_initial_position = SCREEN_HEIGHT - SCALING * IMAGE_HEIGHT
        self.create_pipe_and_enemy(self.pipe_initial_position)
        self.create_pipe_and_enemy(self.pipe_initial_position + PIPE_TWO_DISTANCE)

        # the left pipe's right position
        self.pipe_position = 0
        self.enemy_position = 0

        # Used to keep track of our scrolling
        self.view_bottom = 0

        self.is_add_pipe = True

        arcade.set_background_color(arcade.color.WHITE)
        
        # check hit, but it's a useless parameter
        self.wall = arcade.SpriteList()

        # Keep track of the Score. (for cal)
        self.score = 0
        
        # set SCORE = 0 when begin a new game. (for output)
        self.SCORE = 0

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, self.wall, GRAVITY)
        
        # DQN config
        # Set init action = None
        self.action = 2

        # Set init reward = 0
        self.reward = 0

        self.is_game_running = True

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
            or symbol == arcade.key.LEFT
        ):
            pass
            #self.player.change_x = -BALL_MOVEMENT_SPEED * 0.5
        if (
            symbol == arcade.key.I
            or symbol == arcade.key.RIGHT
        ):
            pass
            #self.player.change_x = BALL_MOVEMENT_SPEED * 0.5

    def action_update_game(self, action):
        """Use parameter action to update game.

        :action: 
        0 --> left
        1 --> right
        2 --> None
        :returns: TODO

        """
        if action == 0:
            self.player.change_y = BALL_JUMP_SPEED
            self.player.change_x = -BALL_MOVEMENT_SPEED

        elif action == 1:
            self.player.change_y = BALL_JUMP_SPEED
            self.player.change_x = BALL_MOVEMENT_SPEED
        else:
            pass

    def on_update(self, delay_time: float):
        """TODO: Update game 60 times per min.

        :returns: Obversition, reward, terminal

        """

        #self.action = Amazing_brick.get_action()
        #print(action)
        #self.action_update_game(self.action)

        # update physics engine
        self.physics_engine.update()
        
        reward = 0.1
        
        # get reward form cal score
        score, reward = self.cal_score()

        # action update game
        self.action_update_game(self.action)
        # Restart the game when collode
        if (self.player.collides_with_list(self.pipe_sprites) 
            or self.player.collides_with_list(self.enemy_sprites)
            or self.player.bottom < 0
            or self.view_bottom < 0):
            # time.sleep(0.5)
            self.setup()
            # self.TOTAL_GAME_NUM += 1
            is_game_running = False
            # Set reward
            reward = -1

        # Get image frame
        self.num += 1
        # 1s save 6 images
        if self.num % 10 == 0:
            image = np.array(arcade.get_image(0,0,width = int(SCREEN_WIDTH * RETINA_SCALING) , height = int(SCREEN_HEIGHT * RETINA_SCALING)))
            image_name = str(self.num) + '.png'
            # image.save(image_name,'PNG')
            #print('save',type(image), 'succeed')
            #return image
            #image = np.array(image)
            #image = DQNagent.preprocess(image)
        
            # record the action and corrsponding reward
            self.agent.record(self.action, reward, score, self.is_game_running, image)

            # make decision
            action = self.agent.NextAction(reward)

            # Update game with action
            self.player.update(action)
        self.all_sprites.update()
        # if self.player.left < 0:
            # self.player.left = 0
        # if self.player.right > SCREEN_WIDTH:
            # self.player.right = SCREEN_WIDTH
        

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
        
        # Create pipe sprites if they are already into the screen and delete pipe sprites if they are no langer on the screen.
        # If all sprites in the same position are delated, then flag = True
        flag = False
        pipe_list = self.get_pipe_y()

        for pipe in self.pipe_sprites:
            pipe_new = pipe.center_y + PIPE_TWO_DISTANCE

            if (top_boundary - pipe.center_y < PIPE_TWO_DISTANCE) and pipe_new not in pipe_list and self.is_add_pipe:
               self.create_pipe_and_enemy(int(pipe.center_y + PIPE_TWO_DISTANCE))

            if pipe.center_y < self.view_bottom:
                if (top_boundary - pipe.center_y < PIPE_TWO_DISTANCE) and pipe_new not in pipe_list:
                   self.create_pipe_and_enemy(int(pipe.center_y + PIPE_TWO_DISTANCE))
                self.pipe_sprites.remove(pipe)
                pipe_list = self.get_pipe_y()
                flag = True
            # Make sure destory all pipe in the same position
                if pipe.center_y in pipe_list: 
                    flag = False
        if flag: self.is_add_pipe = True

        for enemy in self.enemy_sprites:
            if enemy.center_y < self.view_bottom:
                enemy.kill()



        # print('num of pipe sprites:',len(self.pipe_sprites))
        # print('num of enemy sprites:',len(self.enemy_sprites))

    def on_draw(self):
        """TODO: Docstring for on_drew.
        :returns: TODO

        """
        arcade.start_render()
        self.player_sprites.draw()
        self.pipe_sprites.draw()
        self.enemy_sprites.draw()
        #self.all_sprites.draw()

        # Draw score on the screen
        score_text = f"Score: {self.score}"
        max_score_text = f"Max score:{self.MAX_SCORE}"
        total_game_num_text = f"Num of game:{self.TOTAL_GAME_NUM}"
        arcade.draw_text(score_text, 10 , self.view_bottom + SCREEN_HEIGHT - 30, arcade.csscolor.RED, 18, font_name = "FreeSans")
        arcade.draw_text(max_score_text, 10 , self.view_bottom + SCREEN_HEIGHT - 55, arcade.csscolor.RED, 18, font_name = "FreeSans")
        arcade.draw_text(total_game_num_text, 10 , self.view_bottom + SCREEN_HEIGHT - 80, arcade.csscolor.RED, 18, font_name = "FreeSans")

    def create_pipe_and_enemy(self, pipe_height):
        """TODO: Create pipe every runing time.
        :returns: TODO

        """
        # Require a random position for pipe every running time
        self.pipe_position = random.randint(PIPE_MININUM, PIPE_MAXINUM)

        # Cal the pipe center position depend on IMAGE_WIDTH
        pipe_position_left = self.pipe_position - (IMAGE_WIDTH * SCALING) // 2
        pipe_position_right = self.pipe_position + PIPE_INTERVAL + (IMAGE_WIDTH * SCALING) // 2

        # Create the left pipe
        pipe = arcade.Sprite(PIPE_SOURCE, SCALING)
        pipe.center_x = self.pipe_position - (IMAGE_WIDTH * SCALING) // 2
        pipe.center_y = pipe_height
        self.pipe_sprites.append(pipe)
        self.all_sprites.append(pipe)
        
        #Create the right pipe
        pipe = arcade.Sprite(PIPE_SOURCE, SCALING)
        pipe.center_x = pipe_position_right
        pipe.center_y = pipe_height
        self.pipe_sprites.append(pipe)
        self.all_sprites.append(pipe)

        self.is_add_pipe = False
        
        # Create two enemy
        for i in range(0, 2):

            # Require the enemy position with pipe
            self.enemy_position = random.randint(self.pipe_position + 25, self.pipe_position + PIPE_INTERVAL - 25)
            enemy = arcade.Sprite(ENEMY_SOURCE, SCALING)
            enemy.center_x = self.enemy_position
            enemy.center_y = pipe_height + 150 + i * 250
            self.enemy_sprites.append(enemy)
            self.all_sprites.append(enemy)
        
    def get_pipe_y(self):
        """TODO: Docstring for get_pipe_y.
        :returns: TODO

        """
        pipe_y_list = []
        for pipe in self.pipe_sprites:
            pipe_y_list.append(pipe.center_y)
        #print(pipe_y_list)
        return pipe_y_list

    def cal_score(self):
        """ Calulate current score and max score.
        :returns: TODO

        """
        # Cal score
        if self.player.center_y > self.pipe_initial_position:
            self.score = int((self.player.center_y - (self.pipe_initial_position) ) / PIPE_TWO_DISTANCE) + 1
        #self.score = Score
        if self.SCORE < self.score:
            self.SCORE = self.score
            self.reward = 1
        else:
            self.SCORE = self.SCORE
            self.reward = 0.1
        #print("score:", self.score)
        if self.MAX_SCORE < self.SCORE:
            self.MAX_SCORE = self.SCORE

        return self.SCORE, self.reward
