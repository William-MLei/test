## @title File for testing purposes only.
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

    def movePaddle(self):
        self.rect = self.rect.move(self.movement)
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > height:
            self.rect.bottom = height

    def drawPaddle(self):
        screen.blit(self.image,self.rect)