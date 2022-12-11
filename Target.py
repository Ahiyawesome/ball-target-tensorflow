import pygame as pg
import random


class Target:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

    def draw(self, win):
        pg.draw.circle(win, self.color, (self.x, self.y), self.radius)

    def change_position(self, width, height):
        new_position_x = random.randrange(0, width-self.radius)
        new_position_y = random.randrange(0, height-self.radius)
        self.x = new_position_x
        self.y = new_position_y

