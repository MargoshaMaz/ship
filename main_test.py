import pygame
import os
import random


pygame.init()

WIDTH = 900
HEIGHT = 500
SPACESHIP_WIDTH = 55
SPACESHIP_HEIGHT = 40
VELOCITY = 5
FPS = 60
HEALTH_FONT = pygame.font.SysFont('comiscans', 20)
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

clock = pygame.time.Clock()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Летающие прямоугольники")

KOSMOS_IMAGE = pygame.image.load(os.path.join('./assets', 'kosmos.jpg'))
KOSMOS_BG = pygame.transform.scale(KOSMOS_IMAGE, (WIDTH, HEIGHT))
BORDER = pygame.Rect(WIDTH//2 - 2, 0, 4, HEIGHT)

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('./assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('./assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

red = pygame.Rect(55, 130, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
yellow = pygame.Rect(500, 130, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

red_health = 10
yellow_health = 10

max_rectangles = 5
rectangles = []
red_bullets = []
yellow_bullets = []
rectangles_bullets = []
MAX_BULLETS = 3
BULLET_VEL = 7

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_a] and red.x - VELOCITY > 0:
        red.x -= VELOCITY
    if keys_pressed[pygame.K_d] and red.x + VELOCITY + red.width < BORDER.x:
        red.x += VELOCITY
    if keys_pressed[pygame.K_w] and red.y - VELOCITY > 0:
        red.y -= VELOCITY
    if keys_pressed[pygame.K_s] and red.y + VELOCITY + red.height < HEIGHT - 15:
        red.y += VELOCITY

def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_LEFT] and yellow.x - VELOCITY > BORDER.x + BORDER.width:
        yellow.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT] and yellow.x + VELOCITY + yellow.width < WIDTH:
        yellow.x += VELOCITY
    if keys_pressed[pygame.K_UP] and yellow.y - VELOCITY > 0:
        yellow.y -= VELOCITY
    if keys_pressed[pygame.K_DOWN] and yellow.y + VELOCITY + yellow.height < HEIGHT - 15:
        yellow.y += VELOCITY

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in red_bullets:
        bullet.x += BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            red_bullets.remove(bullet)
    for bullet in yellow_bullets:
        bullet.x -= BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x < 0:
            yellow_bullets.remove(bullet)

def handle_collisions(bullets):
    for bullet in bullets[:]:
        bullet_rect = pygame.Rect(bullet[0], bullet[1], 10, 10)
        for rect in rectangles:
            rect_rect = pygame.Rect(rect[0], rect[1], 50, 50)
            if bullet_rect.colliderect(rect_rect):
                bullets.remove(bullet)
                #rectangles.remove(rect)
                break


def draw_winner(text):
    WINNER_FONT = pygame.font.SysFont('comiscans', 60)
    draw_text = WINNER_FONT.render(text, 1, 'pink')
    screen.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                            2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(2000)

while True:
    clock.tick(FPS)

    screen.blit(KOSMOS_BG, (0, 0))

    pygame.draw.rect(screen, "PINK", BORDER)

    screen.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    screen.blit(RED_SPACESHIP, (red.x, red.y))

    red_health_text = HEALTH_FONT.render(
        "Health: " + str(red_health), 1, "pink")
    yellow_health_text = HEALTH_FONT.render(
        "Health: " + str(yellow_health), 1, "pink")
    screen.blit(red_health_text, (10, 10))
    screen.blit(yellow_health_text, (WIDTH - red_health_text.get_width() - 10, 10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.guit()

        if event.type == RED_HIT:
            red_health -= 1
        if event.type == YELLOW_HIT:
            yellow_health -= 1

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and len(red_bullets) < MAX_BULLETS:
                bullet = pygame.Rect(
                    red.x + red.width, red.y + red.height // 2 - 2, 10, 5)
                red_bullets.append(bullet)
            if event.key == pygame.K_RETURN and len(yellow_bullets) < MAX_BULLETS:
                bullet = pygame.Rect(
                    yellow.x, yellow.y + yellow.height // 2 - 2, 10, 5)
                yellow_bullets.append(bullet)

    keys_pressed = pygame.key.get_pressed()
    red_handle_movement(keys_pressed, red)
    yellow_handle_movement(keys_pressed, yellow)



    if len(rectangles) < max_rectangles and random.randint(0, 100) < 3:
        rect_width = random.randint(30, 30)
        rect_height = random.randint(30, 30)
        rect_x = random.randint(0, WIDTH - rect_width)
        rect_y = HEIGHT
        rectangles.append([rect_x, rect_y, rect_width, rect_height])


    for rect in rectangles:
        rect[1] -= 2
        pygame.draw.rect(screen, "pink", (rect[0], rect[1], rect[2], rect[3]))
        if rect[1] + 50 < 0:
            rectangles.remove(rect)


    for bullet in red_bullets:
        pygame.draw.rect(screen, "red", bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(screen, "yellow", bullet)

    handle_bullets(yellow_bullets, red_bullets, yellow, red)

    handle_collisions(red_bullets)
    handle_collisions(yellow_bullets)
    handle_collisions(rectangles_bullets)

    winner_text = ""
    if red_health <= 0:
        winner_text = "Yellow Wins!!!"
    if yellow_health <= 0:
        winner_text = "Red Wins!!!"
    if winner_text != "":
        draw_winner(winner_text)
        red_bullets.clear()
        yellow_bullets.clear()
        red_health = 10
        yellow_health = 10

    pygame.display.update()