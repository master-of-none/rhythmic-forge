import pygame
from pygame import mixer

pygame.init()
WIDTH, HEIGHT = 1400, 800
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
GREEN = (0, 255, 0)
GOLD = (212, 175, 55)
BLUE = (0, 255, 255)
FPS = 60

# Pyagame intialize
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Custom Beat Maker")
clock = pygame.time.Clock()
label_font = pygame.font.Font('freesansbold.ttf', size=28)

running = True

while running:
    clock.tick(FPS)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()