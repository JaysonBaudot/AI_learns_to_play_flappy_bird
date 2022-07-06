import pygame
import neat
import time
import os
import random

class Base:
    # represents the moving floor of the game

    BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
    VEL =  5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        # Initialize the object
        # :param y: int
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH
    
    
    def move(self):
        # move the floor so it looks like its scrolling
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        # once one base image is off the screen it resets to a position offscreen behind the image still on the screen
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 +self.WIDTH
    
    def draw(self, win):
        # Draw the floor. This is two images that move together.
        # :param win: the pygame surface/window
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))
