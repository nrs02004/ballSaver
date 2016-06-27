import pygame
from defs import *
from objects import * 

pygame.init()

screen = Screen(width,height)
world = World([Ball(8,10,-5,-5), Ball(20,20,5,5)], width, height)


for step in range(0,num_steps):
    world.update(dt)
    if step % steps_per_flip == 0:
        screen.draw_stuff(world.balls)


pygame.quit()
