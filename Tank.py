#PONG pygame

import random
import pygame, sys
from pygame.locals import *

pygame.init()
fps = pygame.time.Clock()

#colors
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,0)

#globals
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 80
PAD_HEIGHT = 8
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
ball_pos = [0,0]
ball_vel = [0,0]
paddle1_vel = 0
paddle2_vel = 0
l_score = 0
r_score = 0
rectangles = []
fired1 = []
fired2 = []
projectile_speed = 1
GameOver = False
p1_alive = True
p2_alive = True


#canvas declaration
window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('Hello World')

# helper function that spawns a ball, returns a position vector and a velocity vector
# if right is True, spawn to the right, else spawn to the left
def ball_init(right):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [int(WIDTH/2),int(HEIGHT/2)]
    horz = random.randrange(2,4)
    vert = random.randrange(1,3)

    if right == False:
        horz = - horz

    ball_vel = [horz,-vert]

# define event handlers
def init():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel,l_score,r_score  # these are floats
    global score1, score2  # these are ints
    global rectangles
    paddle1_pos = [int(WIDTH/2), int(HALF_PAD_HEIGHT +4)]
    paddle2_pos = [int(WIDTH/2), int(HEIGHT - 20 - HALF_PAD_HEIGHT)]
    l_score = 0
    r_score = 0
    j = 0
    for i in range(0, 18):
        if (i % 6 == 0):
           j += 1
           print(j)
        rectangles.append(pygame.Rect((((i %6)* 50 + 10*(i%6))+120),((HEIGHT/2) + 20 * j + 10*j - 75),50,20))

def fire_proj_1():
    global paddle1_pos, paddle2_pos, fired
    if(len(fired1)<= 15):
        fired1.append(pygame.Rect(paddle1_pos[0], paddle1_pos[1]+PAD_HEIGHT, 10, 10))

def fire_proj_2():
    global paddle1_pos, paddle2_pos, fired
    if(len(fired2)<= 15):
         fired2.append(pygame.Rect(paddle2_pos[0], paddle2_pos[1] - PAD_HEIGHT - 10, 10, 10))


#draw function of canvas
def draw(canvas):
    global paddle1_pos, paddle2_pos, ball_pos, ball_vel, l_score, r_score, rectangles, p1_alive, p2_alive, GameOver

    canvas.fill(BLACK)
    for rect in rectangles:
        pygame.draw.rect(canvas, WHITE, rect, 0)


    for fire in fired1:
        fire[1] += projectile_speed
        if(fire[1] <= HEIGHT):
            pygame.draw.rect(canvas, RED, fire, 0)
        else:
            fired1.remove(fire)#


    for fire in fired2:
        fire[1] -= projectile_speed
        #pygame.draw.rect(canvas, RED, fire, 0)
        if(fire[1]>=0):
            pygame.draw.rect(canvas, RED, fire, 0)
        else:
            fired2.remove(fire)



    #pygame.draw.rect(canvas, WHITE, [WIDTH/2, HEIGHT/2, 50, 20], 0)
    # pygame.draw.line(canvas, WHITE, [WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1)
    # pygame.draw.line(canvas, WHITE, [PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1)
    # pygame.draw.line(canvas, WHITE, [WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1)
    # pygame.draw.circle(canvas, WHITE, [WIDTH//2, HEIGHT//2], 70, 1)

    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos[0] > HALF_PAD_WIDTH  and paddle1_pos[0] < WIDTH - HALF_PAD_WIDTH :
        paddle1_pos[0] += paddle1_vel
    elif paddle1_pos[0] <= HALF_PAD_WIDTH and paddle1_vel > 0:
        paddle1_pos[0] += paddle1_vel
    elif paddle1_pos[0] >= WIDTH - HALF_PAD_WIDTH and paddle1_vel < 0:
        paddle1_pos[0] += paddle1_vel

    if paddle2_pos[0] > HALF_PAD_WIDTH and paddle2_pos[0] < WIDTH - HALF_PAD_WIDTH:
        paddle2_pos[0] += paddle2_vel
    elif paddle2_pos[0] <= HALF_PAD_WIDTH and paddle2_vel > 0:
        paddle2_pos[0] += paddle2_vel
    elif paddle2_pos[0] >= WIDTH - HALF_PAD_WIDTH and paddle2_vel < 0:
        paddle2_pos[0] += paddle2_vel

    #update ball
    # ball_pos[0] += int(ball_vel[0])
    # ball_pos[1] += int(ball_vel[1])

    for fire in fired1:
        for rect in rectangles:
            if fire[1] == rect[1] -10 and fire[0] >= rect[0]  and (fire[0] <= rect[0] + 50):
                fired1.remove(fire)
                rectangles.remove(rect)
            if fire[1] == paddle2_pos[1] - 10   and (fire[0] >= paddle2_pos[0] - HALF_PAD_WIDTH) and (fire[0] <= paddle2_pos[0] + HALF_PAD_WIDTH):
                p2_alive = False
                GameOver = True


    for fire in fired2:
        for rect in rectangles:
            if fire[1] == rect[1] + 20  and fire[0] >= rect[0] and (fire[0] <= rect[0] + 50):
                fired2.remove(fire)
                rectangles.remove(rect)
            if (fire[1] == paddle1_pos[1] +10)   and (fire[0] >= paddle1_pos[0] - HALF_PAD_WIDTH) and (fire[0] <= paddle1_pos[0] + HALF_PAD_WIDTH):
                p1_alive = False
                GameOver = True

    #draw paddles and ball
    # pygame.draw.circle(canvas, RED, ball_pos, 20, 0)
    if p1_alive:
         pygame.draw.polygon(canvas, GREEN, [[paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT], [paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT], [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT], [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT]], 0)

    if p2_alive:
        pygame.draw.polygon(canvas, GREEN, [[paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT], [paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT], [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT], [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT]], 0)


     # if int(ball_pos[1]) <= BALL_RADIUS:
     #     ball_vel[1] = - ball_vel[1]
     # if int(ball_pos[1]) >= HEIGHT + 1 - BALL_RADIUS:
     #     ball_vel[1] = -ball_vel[1]






    #ball collison check on gutters or paddles
    # if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH and ball_pos[1] in range(int(paddle1_pos[1] - HALF_PAD_HEIGHT),int(paddle1_pos[1] + HALF_PAD_HEIGHT),1):
    #     ball_vel[0] = -ball_vel[0]
    #     ball_vel[0] *= 2
    #     ball_vel[1] *= 2
    # elif int(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH:
    #     r_score += 1
    #     ball_init(True)
    #
    # if ball_pos[0] >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH and ball_pos[1] in range(int(paddle2_pos[1] - HALF_PAD_HEIGHT),int(paddle2_pos[1] + HALF_PAD_HEIGHT),1):
    #     ball_vel[0] = -ball_vel[0]
    #     ball_vel[0] *= 2
    #     ball_vel[1] *= 2
    # elif int(ball_pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH:
    #     l_score += 1
    #     ball_init(False)

    #update scores
    # myfont1 = pygame.font.SysFont("Comic Sans MS", 20)
    # label1 = myfont1.render("Score "+str(l_score), 1, (255,255,0))
    # canvas.blit(label1, (50,20))
    #
    # myfont2 = pygame.font.SysFont("Comic Sans MS", 20)
    # label2 = myfont2.render("Score "+str(r_score), 1, (255,255,0))
    # canvas.blit(label2, (470, 20))


#keydown handler
def keydown(event):
    global paddle1_vel, paddle2_vel

    if event.key == K_LEFT:
        paddle2_vel = -8
    elif event.key == K_RIGHT:
        paddle2_vel = 8
    elif event.key == K_a:
        paddle1_vel = -8
    elif event.key == K_d:
        paddle1_vel = 8
    elif event.key == K_s:
        fire_proj_1()
    elif event.key == K_RETURN:
        fire_proj_2()

#keyup handler
def keyup(event):
    global paddle1_vel, paddle2_vel

    if event.key in (K_a, K_d):
        paddle1_vel = 0
    elif event.key in (K_LEFT, K_RIGHT):
        paddle2_vel = 0

init()


#game loop
while not GameOver:

    draw(window)

    for event in pygame.event.get():

        if event.type == KEYDOWN:
            keydown(event)
        elif event.type == KEYUP:
            keyup(event)
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    fps.tick(100)
