## @title File for testing purposes only.
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
bounce = pygame.mixer.Sound('pongTestFiles/sounds/bbal.wav')

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

    def scoreGoal(self):
        if self.rect.top <= 0 or self.rect.bottom >= height:
            bounce.play()
            self.movement[1] = -1*self.movement[1]
        if self.rect.left <= 0:
            self.resetBall()
            self.score = 1
        if self.rect.right >= width:
            self.resetBall()
            self.score = -1

        self.rect = self.rect.move(self.movement)

    def resetBall(self):
        self.rect.centerx = int(width/2)
        self.rect.centery = int(height/2)
        self.movement = [random.randrange(-1,2,2)*6,random.randrange(-1,2,2)*6]

    def draw(self):
        pygame.draw.circle(self.image,self.color,(int(self.rect.width/2),int(self.rect.height/2)),int(self.size/2))
        screen.blit(self.image,self.rect)