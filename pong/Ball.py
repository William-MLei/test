## @file Ball.py
# @title Creating a Ball for the game.
# @author Arshan Khan
# @date 28 March 2020
import pygame
import sys
import os
import math
import random
from pygame.locals import *

scrSize = (width, height) = (1280,800)
screen = pygame.display.set_mode((scrSize))

pygame.mixer.init()
bounce = pygame.mixer.Sound('pong/sounds/bbal.wav')

## @brief a Ball class which represents a real world ball. The class is initialized by passing 5 parameters.
# @details This class is called once the game is running.
# @param x horizontal coordinate of where the ball is to be placed initially, weighted at the top-left.
# @param y vertical coordinate of where the ball is to be placed initially, weighted at the top-left.
# @param size The diameter of the ball.
# @param color The color of the ball in (R,G,B) format.
# @param movement This determines the speed of the ball in how many pixels the ball moves in [x,y] direction. It is [0, 0] by default.
class Ball(pygame.sprite.Sprite):
    def __init__(self,x,y,size,color,movement=[0,0]):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.movement = movement
        self.image = pygame.Surface((size,size),pygame.SRCALPHA,32)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image,self.color,(int(self.rect.width/2),int(self.rect.height/2)),int(size/2))
        self.rect.centerx = x
        self.rect.centery = y
        self.maxspeed = 10
        self.score = 0

    ## @brief This determines how the ball will move and stay within the boundary of the screen.
    def scoreGoal(self):
        if self.rect.top <= 0 or self.rect.bottom >= height: #reverses the vertical velocity on collision with top and bottom walls
            bounce.play()
            self.movement[1] = -1*self.movement[1]
        if self.rect.left <= 0: #resets the ball's position and notes that the point is scored by the ai
            self.resetBall()
            self.score = 1
        if self.rect.right >= width: #resets the position of the ball and notes that the point is scored by the user
            self.resetBall()
            self.score = -1

        self.rect = self.rect.move(self.movement)

    ## @brief Resets the ball to the center of the screen with a random trajectory.
    def resetBall(self):
        self.rect.centerx = int(width/2)
        self.rect.centery = int(height/2)
        self.movement = [random.randrange(-1,2,2)*6,random.randrange(-1,2,2)*6]

    ## @brief Redraw the ball on the screen.
    def draw(self):
        pygame.draw.circle(self.image,self.color,(int(self.rect.width/2),int(self.rect.height/2)),int(self.size/2))
        screen.blit(self.image,self.rect)