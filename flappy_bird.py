
from distutils.command.config import config
from operator import ge
import pygame
import neat
import time
import os
import random
from bird import Bird
from pipe import Pipe
from base import Base
pygame.font.init()

WIN_WIDTH = 500
WIN_HEIGHT = 800
GEN = 0

BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

STAT_FONT = pygame.font.SysFont("comicsans", 30)

DRAW_LINES = True




def draw_window(win, birds, pipes, base, score, gen):
    # draws the windows for the main game loop
    # :param win: pygame window surface
    # :param bird: a Bird object
    # :param pipes: List of pipes
    # :param score: score of the game (int)
    # :param gen: current generation

    win.blit(BG_IMG, (0, 0))

    for pipe in pipes:
        pipe.draw(win)  

    base.draw(win)
    for bird in birds:
        # draw lines from bird to pipe
        if DRAW_LINES:
            try:
                pygame.draw.line(win, (255,0,0), (bird.x+bird.img.get_width()/2, bird.y + bird.img.get_height()/2), (pipes[pipe_ind].x + pipes[pipe_ind].PIPE_TOP.get_width()/2, pipes[pipe_ind].height), 5)
                pygame.draw.line(win, (255,0,0), (bird.x+bird.img.get_width()/2, bird.y + bird.img.get_height()/2), (pipes[pipe_ind].x + pipes[pipe_ind].PIPE_BOTTOM.get_width()/2, pipes[pipe_ind].bottom), 5)
            except:
                pass
        # draw bird
        bird.draw(win)
    # display score
    text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    # display generations 
    text = STAT_FONT.render("Gen: " + str(gen), 1, (255, 255, 255))
    win.blit(text, (10, 10))

    # display number of alive birds
    score_label = STAT_FONT.render("Alive: " + str(len(birds)),1,(255,255,255))
    win.blit(score_label, (10, 50))

    pygame.display.update()



def main(genomes, config):
    global GEN
    GEN += 1
    # start by creating lists holding the genome itself, the
    # neural network associated with the genome and the
    # bird object that uses that network to play
    nets = []
    ge = []
    birds = []
    

    # assigning neural network to each genome and creation of all the birds
    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230,350))
        g.fitness = 0 # start with a fitness level of 0
        ge.append(g)


    base = Base(730)
    pipes = [Pipe(600)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    score = 0

    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
        
        # makes sure that bird only looks at one pipe at a time
        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1 
        else:
            run = False
            break   

        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1 # gives bird fitness points for every frame it moves forward/stays alive

            # send bird location, top pipe location, and bottom pipe location and determine from network whether to jump or not
            output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom))) 

            if output[0] > 0.5: # uses a tanh activation function so result will be between -1 and 1. if over 0.5 jump
                bird.jump()
        
        # bird.move()

        # creates multiple pipes on screen
        add_pipe = False
        rem = []
        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)
                    

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x +pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)
            
            pipe.move()

        # increments fitness score for passing a pipe and creates new pipe
        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(600))
        
        for r in rem:
            pipes.remove(r)
        
        # check for floor collision
        for x, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)                
        
        if score > 50:
            break

        base.move()
        draw_window(win, birds, pipes, base, score, GEN)
    




def run(config_path):
    # runs the neat algorithm to traina neural network to play flappy bird.
    # :param config_file: loation of config file
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    
    # create the population, which is the top-level object for a NEAT run
    p = neat.Population(config) 

    # adds a stdout reporter which shows progewss in the terminal
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main,50)

if __name__ == "__main__": 
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)