import random
import pygame as pg
import numpy as np
import time
from Ball import Ball
from Target import Target
from BallBrain import NeuralNet

pg.init()

WIDTH = 1500
HEIGHT = 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

WIN = pg.display.set_mode((WIDTH, HEIGHT))
BALL_INITIAL_POS_X = WIDTH // 2
BALL_INITIAL_POS_Y = HEIGHT // 2
BALL_SPEED = 3

best_possible = np.array([0, 0, 0, 0, 0, 0, 0, 0])
inputs = np.zeros((1, 8))
outputs = np.array(8)
stored_inputs = np.full((100, 8), np.inf)
stored_targets = np.full((100, 8), np.inf)
reset_inputs = np.full((100, 8), np.inf)
reset_targets = np.full((100, 8), np.inf)


def collision_check(ballx, bally, ballrad, redx, redy):
    if ballx + ballrad >= WIDTH or ballx - ballrad <= 0 or bally + ballrad >= HEIGHT or bally - ballrad <= 0:
        return True
    if redx - 5 <= ballx <= redx + 5 and redy - 5 <= bally <= redy + 5:
        return True


def target_check(ballx, bally, ballrad, redx, redy):
    if redx - 5 <= ballx <= redx + 5 and redy - 5 <= bally <= redy + 5:
        return True


def best_possible_move(ballx, bally, ballrad, targx, targy, targrad, best, inp):       # LEFT OFF HERE: CHECK ORIGINAL
    for i in range(0, 8):
        inp[0][i] = 0
        best[i] = 0

    if ballx > targx:
        if (targy - targrad >= bally + ballrad >= targy + targrad) or (
                targy + targrad >= bally - ballrad >= targy - targrad):
            best[1] = 1
            inp[0][1] = 1                              # left
        elif targy < bally:
            best[6] = 1
            inp[0][6] = 1                              # left-up
        elif targy > bally:
            best[7] = 1
            inp[0][7] = 1                              # left-down
    elif ballx < targx:
        if targy > bally:
            best[5] = 1
            inp[0][5] = 1                              # right-down
        elif targy < bally:
            best[4] = 1
            inp[0][4] = 1                              # right-up
        elif (targy - targrad >= bally + ballrad >= targy + targrad) or (
                targy + targrad >= bally - ballrad >= targy - targrad):
            best[0] = 1
            inp[0][0] = 1                              # right
    else:
        if targy > bally:
            best[3] = 1
            inp[0][3] = 1                              # down
        elif targy < bally:
            best[2] = 1
            inp[0][2] = 1                              # up


def store_values(index, tempIn, tempTarg, storedIn, storedTarg):
    if index < 100:
        storedIn[index] = tempIn[0]
        storedTarg[index] = tempTarg


def reset(circle, s_inputs, s_targs, r_inputs, r_targs):
    circle.reset_position()
    s_inputs = r_inputs
    s_targs = r_targs


def move(output):
    best_index = -1.0
    best_value = -2.0
    for i in range(0, 8):
        if output[0][i] > best_value:
            best_value = output[0][i]
            best_index = i

    print(best_index)

    return best_index


def draw(win, agent, target):
    win.fill(BLACK)
    target.draw(win)
    agent.draw(win)
    pg.draw.rect(win, WHITE, (target.x-5, target.y-5, 10, 10), 2)

    pg.display.update()


def main():
    run = True
    first_run = True
    count = 0
    index = 0
    state = random.randrange(0, 7)

    agent = Ball(BALL_INITIAL_POS_X, BALL_INITIAL_POS_Y, 5, BALL_SPEED, WHITE)
    target = Target(100, HEIGHT//2, 5, RED)

    net = NeuralNet(stored_inputs, stored_targets)
    net.create()

    while run:
        pg.time.Clock().tick(60)

        best_possible_move(agent.x, agent.y, agent.radius, target.x, target.y, target.radius, best_possible, inputs)

        if not first_run and count % 5 == 0:
            output = net.make_prediction(inputs)
            state = move(output)
        elif first_run and count % 20 == 0:
            state = random.randrange(0, 7)

        agent.move(state)

        if collision_check(agent.x, agent.y, agent.radius, target.x, target.y) or count > 600:
            net.update_values(stored_inputs, stored_targets)
            net.run()
            time.sleep(2)           # idk how this fix worked, but it works
            reset(agent, stored_inputs, stored_targets, reset_inputs, reset_targets)
            count = 0
            index = 0
            if target_check(agent.x, agent.y, agent.radius, target.x, target.y):
                target.change_position(WIDTH, HEIGHT)
            if first_run:
                first_run = False

        if count % 10 == 0:
            store_values(index, inputs, best_possible, stored_inputs, stored_targets)
            index += 1

        draw(WIN, agent, target)
        count += 1
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
    pg.quit()


if __name__ == '__main__':
    main()
