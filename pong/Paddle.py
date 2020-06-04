## @file Paddle.py
# @title Creating a Paddle for a player.
# @author Arshan Khan
# @date 28 March 2020
import os
import pygame
import sys
import math
import random
from pygame.locals import *

scrSize = (width, height) = (1280,800)
screen = pygame.display.set_mode((scrSize))

## @brief A paddle class which represents a real world Paddle. The class is initialized by passing 5 parameters.
# @details This class is only called twice for each player when the game starts.
# @param x The x coordinate of the paddle to determine its position, weighted at the top-left.
# @param y The y coordinate of the paddle to determine its position, weighted at the top-left.
# @param sizex The width of the paddle which determines its size.
# @param sizex The height of the paddle which determines its size.
# @param color The color of the paddle in (R,G,B) format.
class Paddle(pygame.sprite.Sprite):
    def __init__(self,x,y,sizex,sizey,color):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.sizex = sizex
        self.sizey = sizey
        self.color = color
        self.image = pygame.Surface((sizex,sizey),pygame.SRCALPHA,32)
        self.image = self.image.convert_alpha()
        pygame.draw.rect(self.image,self.color,(0,0,sizex,sizey))
        self.rect = self.image.get_rect()
        self.rect.left = self.x
        self.rect.top = self.y
        self.points = 0
        self.movement = [0,0]

    ## @brief An update function which updates the state and position of the paddle.
    def movePaddle(self):
        self.rect = self.rect.move(self.movement)
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > height:
            self.rect.bottom = height

    ## @brief A draw function which draws the paddle onto the screen.
    def drawPaddle(self):
        screen.blit(self.image,self.rect)