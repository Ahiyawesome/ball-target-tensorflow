import pygame as pg


class Ball:
    def __init__(self, x, y, radius, speed, color):
        self.x = self.orX = x
        self.y = self.orY = y
        self.radius = radius
        self.speed = speed
        self.color = color

    def draw(self, win):
        pg.draw.circle(win, self.color, (self.x, self.y), self.radius)

    def move(self, state):
        if state == 0:                                  # right
            self.x += self.speed
        elif state == 1:                                # left
            self.x -= self.speed
        elif state == 2:                                # up
            self.y -= self.speed
        elif state == 3:                                # down
            self.y += self.speed
        elif state == 4:                                # right up
            self.x += self.speed
            self.y -= self.speed
        elif state == 5:                                # right down
            self.x += self.speed
            self.y += self.speed
        elif state == 6:                                # left up
            self.x -= self.speed
            self.y -= self.speed
        elif state == 7:                                # left down
            self.x -= self.speed
            self.y += self.speed

    def reset_position(self):
        self.x = self.orX
        self.y = self.orY
