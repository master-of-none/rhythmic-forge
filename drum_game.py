import pygame
from pygame import mixer

pygame.init()

WIDTH, HEIGHT = 1400, 800
black = (0, 0, 0)
white = (255, 255, 255)
grey = (128, 128, 128)

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Custom Beat Maker")
label_font = pygame.font.Font('freesansbold.ttf', 28)

fps = 60
timer = pygame.time.Clock()

running = True

while running:
    timer.tick(fps)
    screen.fill(black)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
pygame.quit()
