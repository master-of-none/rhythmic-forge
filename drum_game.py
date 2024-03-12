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
INSTRUMENTS = 6
BEATS = 8

# Pyagame intialize
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Custom Beat Maker")
clock = pygame.time.Clock()
label_font = pygame.font.Font('freesansbold.ttf', size=28)

running = True
clicked = [[-1 for _ in range(BEATS)] for _ in range(INSTRUMENTS)]


def draw_grid(clicks):
    # Draw grid lines and labels
    for i in range(INSTRUMENTS):
        pygame.draw.line(screen, GREY, (0, (i * 100) + 100), (200, (i * 100) + 100), 2)

        # Draw labels
    labels = ["Kick", "Snare", "Hi Hat", "Open Hat", "Wood Block", "Mid Tom"]
    for i, label in enumerate(labels):
        text = label_font.render(label, True, WHITE)
        screen.blit(text, (30, i * 100 + 30))

    all_box = []
    for i in range(BEATS):
        for j in range(INSTRUMENTS):
            color = GREEN if clicks[j][i] == 1 else GREY
            rect = pygame.draw.rect(screen, color,
                                    [i * ((WIDTH - 200) // BEATS) + 205, (j * 100) + 5, ((WIDTH - 200) // BEATS) - 10,
                                     ((HEIGHT - 200) // INSTRUMENTS) - 10], 0, 3)
            pygame.draw.rect(screen, BLACK,
                             [i * ((WIDTH - 200) // BEATS) + 200, (j * 100), ((WIDTH - 200) // BEATS),
                              ((HEIGHT - 200) // INSTRUMENTS)], 2, 5)

            all_box.append((rect, (i, j)))
    return all_box

while running:
    clock.tick(FPS)
    screen.fill(BLACK)

    all_box = draw_grid(clicked)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle button state when clicked
            for box, coordinates in all_box:
                if box.collidepoint(event.pos):
                    x, y = coordinates
                    clicked[y][x] *= -1

    pygame.display.flip()

pygame.quit()
