import pygame
import neat
import time
import os
import random

class Pipe:
    PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
    GAP = 200
    VEL = 5

    def __init__(self, x):
        # initialize pipe object
        # :param x: int
        # :param y: int

        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(self.PIPE_IMG, False, True)
        self.PIPE_BOTTOM = self.PIPE_IMG

        self.passed = False
        self.set_height()
        
    
    def set_height(self):
        # sets random height of pipes from the top of the screen
        self.height = random.randrange(50,450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    
    def move(self):
        # moves pipes towards player based on vel
        self.x -= self.VEL
    
    
    def draw(self, win):
        # draw both the top and bottom of the pipe
        # :param win: pygame window/surface
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    
    def collide(self, bird):
        # returns if a point is colliding with the pipe
        # :param bird: Bird object
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x -bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True
        
        return False



    
