import pygame
import random
import sys
from pygame.locals import *

pygame.init()

FPS = 30

FPSCLOCK = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

WIDTH = 800
HEIGHT = 600

BALL_RADIUS = 10
PAD_WIDTH = 10
PAD_HEIGHT = 100

ball_pos = [0, 0]
ball_vel = [1, 1]

paddle1_pos = [0, 0]
paddle2_pos = [WIDTH - PAD_WIDTH, 0]
paddle1_vel = 0
paddle2_vel = 0

l_score = 0
r_score = 0

DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")


def check_winner():
    global r_score, l_score

    if r_score == 5:
        return "Right Player Wins!"
    elif l_score == 5:
        return "Left Player Wins!"

    return


def ball_init():
    global ball_pos, ball_vel

    ball_pos = [WIDTH // 2, HEIGHT // 2]
    ball_vel = [0, 0]

    if random.randint(1, 3) == 1:
        ball_vel[0] = random.randrange(4, 6)
    else:
        ball_vel[0] = -(random.randrange(4, 6))

    if random.randint(1, 3) == 1:
        ball_vel[1] = random.randrange(3, 6)
    else:
        ball_vel[1] = -(random.randrange(3, 6))

def second_paddle_ai(ball):
    global paddle2_vel, paddle2_pos

    if paddle2_pos[1] + 50 > ball[1]:
        paddle2_vel = -5
    elif paddle2_pos[1] + 50 < ball[1]:
        paddle2_vel = 5


def draw(display):
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, ball_pos, ball_vel
    global BLACK, WHITE
    global PAD_WIDTH, PAD_HEIGHT, HEIGHT, WIDTH
    global l_score, r_score

    display.fill(BLACK)

    # update paddle position
    paddle1_pos[1] += paddle1_vel
    paddle2_pos[1] += paddle2_vel

    # keep paddles on screen
    if paddle1_pos[1] <= 0:
        paddle1_pos[1] = 0
    elif paddle1_pos[1] + PAD_HEIGHT >= HEIGHT:
        paddle1_pos[1] = HEIGHT - PAD_HEIGHT
    if paddle2_pos[1] <= 0:
        paddle2_pos[1] = 0
    elif paddle2_pos[1] + PAD_HEIGHT >= HEIGHT:
        paddle2_pos[1] = HEIGHT - PAD_HEIGHT

    # update ball position
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    ball_pos[0] = int(ball_pos[0])
    ball_pos[1] = int(ball_pos[1])

    # test roof/floor ball collision
    if ball_pos[1] - BALL_RADIUS <= 0:
        ball_vel[1] = -ball_vel[1]
        ball_pos[1] += 1
    elif ball_pos[1] + BALL_RADIUS >= HEIGHT:
        ball_vel[1] = -ball_vel[1]
        ball_pos -= 1

    # test left/right ball collision
    if ball_pos[0] - BALL_RADIUS - 1 <= PAD_WIDTH and ball_pos[1] in range(paddle1_pos[1], paddle1_pos[1] + 1 + PAD_HEIGHT):
        ball_vel[0] *= -1.15
        if paddle1_vel != 0:
            ball_vel[1] += paddle1_vel * 0.1
    elif ball_pos[0] + BALL_RADIUS + 1 >= WIDTH - PAD_WIDTH and ball_pos[1] in range(paddle2_pos[1], paddle2_pos[1] + 1 + PAD_HEIGHT):
        ball_vel[0] *= -1.15
        if paddle2_vel != 0:
            ball_vel[1] += paddle2_vel * 0.1
    elif ball_pos[0] - BALL_RADIUS - 1 <= PAD_WIDTH:
        r_score += 1
        ball_init()
    elif ball_pos[0] + BALL_RADIUS + 1 >= WIDTH - PAD_WIDTH:
        l_score += 1
        ball_init()

    pygame.draw.circle(display, WHITE, ball_pos, BALL_RADIUS, 0)

    pygame.draw.rect(display, WHITE, (paddle1_pos[0], paddle1_pos[1], PAD_WIDTH, PAD_HEIGHT), 0)

    pygame.draw.rect(display, WHITE, (paddle2_pos[0], paddle2_pos[1], PAD_WIDTH, PAD_HEIGHT), 0)

    pygame.draw.line(display, WHITE, [PAD_WIDTH, 0], [PAD_WIDTH, HEIGHT], 1)
    pygame.draw.line(display, WHITE, [WIDTH - PAD_WIDTH, 0], [WIDTH - PAD_WIDTH, HEIGHT], 1)

    myfont1 = pygame.font.SysFont("Times New Roman", 26)
    label1 = myfont1.render("Score: " + str(l_score), 1, (255, 255, 255))
    label2 = myfont1.render("Score: " + str(r_score), 1, (255, 255, 255))
    display.blit(label1, (WIDTH / 4, HEIGHT / 2))
    display.blit(label2, (int(WIDTH * 0.75), int(HEIGHT * 0.5)))


def keydown(event):
    global paddle1_vel, paddle2_vel

    # if event.key == K_UP:
        # paddle2_vel = -10
    # if event.key == K_DOWN:
        # paddle2_vel = 10
    if event.key == K_w:
        paddle1_vel = -10
    if event.key == K_s:
        paddle1_vel = 10


def keyup(event):
    global paddle1_vel, paddle2_vel

    # if event.key == K_UP:
        # paddle2_vel = 0
    # if event.key == K_DOWN:
        # paddle2_vel = 0
    if event.key == K_w:
        paddle1_vel = 0
    if event.key == K_s:
        paddle1_vel = 0


ball_init()
draw(DISPLAYSURF)


while True:

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            keydown(event)
        elif event.type == KEYUP:
            keyup(event)
        elif event.type == QUIT:
            pygame.quit()
            sys.exit()

    second_paddle_ai(ball_pos)

    draw(DISPLAYSURF)

    result = check_winner()
    if result:
        DISPLAYSURF.fill(BLACK)
        over_font = pygame.font.SysFont("Times New Roman", 36)
        over_label = over_font.render("Game Over!" + "" + result, 1, (255, 255, 255))
        DISPLAYSURF.blit(over_label, (WIDTH//4, HEIGHT//2))
        l_score = 0
        r_score = 0
        pygame.display.update()
        pygame.time.wait(4000)
        ball_init()
        draw(DISPLAYSURF)

    pygame.display.update()
    FPSCLOCK.tick(FPS)
