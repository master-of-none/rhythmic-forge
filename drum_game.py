import pygame
from pygame import mixer

pygame.init()

WIDTH, HEIGHT = 1400, 800
black = (0, 0, 0)
white = (255, 255, 255)
grey = (128, 128, 128)
green = (0, 255, 0)
gold = (212, 175, 55)
blue = (0, 255, 255)

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Custom Beat Maker")
label_font = pygame.font.Font('freesansbold.ttf', 28)

fps = 60
timer = pygame.time.Clock()
beats = 8
instruments = 6
all_box = []
clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]
bpm = 240
playing = True
active_length = 0
active_beat = 0
beat_changed = True

running = True


def draw_grid(clicks, beat):
    left_side = pygame.draw.rect(screen, grey, [0, 0, 200, HEIGHT - 200], 5)
    bottom_side = pygame.draw.rect(screen, grey, [0, HEIGHT - 200, WIDTH, 200], 5)
    all_box = []
    colors = [grey, white, grey]
    kick_text = label_font.render("Kick", True, white)
    screen.blit(kick_text, (30, 30))
    snare_text = label_font.render("Snare", True, white)
    screen.blit(snare_text, (30, 130))
    snare_text = label_font.render("Hi Hat", True, white)
    screen.blit(snare_text, (30, 230))
    snare_text = label_font.render("Open Hat", True, white)
    screen.blit(snare_text, (30, 330))
    snare_text = label_font.render("Wood Block", True, white)
    screen.blit(snare_text, (30, 430))
    snare_text = label_font.render("Mid Tom", True, white)
    screen.blit(snare_text, (30, 530))

    for i in range(instruments):
        pygame.draw.line(screen, grey, (0, (i * 100) + 100), (200, (i * 100) + 100), 2)

    for i in range(beats):
        for j in range(instruments):
            if clicks[j][i] == -1:
                color = grey
            else:
                color = green

            rect = pygame.draw.rect(screen, color,
                                    [i * ((WIDTH - 200) // beats) + 205, (j * 100) + 5, ((WIDTH - 200) // beats) - 10,
                                     ((HEIGHT - 200) // instruments) - 10], 0, 3)

            pygame.draw.rect(screen, gold,
                             [i * ((WIDTH - 200) // beats) + 200, (j * 100), ((WIDTH - 200) // beats),
                              ((HEIGHT - 200) // instruments)], 5, 5)

            pygame.draw.rect(screen, black,
                             [i * ((WIDTH - 200) // beats) + 200, (j * 100), ((WIDTH - 200) // beats),
                              ((HEIGHT - 200) // instruments)], 2, 5)
            all_box.append((rect, (i, j)))

        active = pygame.draw.rect(screen, blue, [beat * ((WIDTH - 200) // beats) + 200, 0, ((WIDTH - 200) // beats),
                                                 instruments * 100], 5, 3)
    return all_box


while running:
    timer.tick(fps)
    screen.fill(black)
    all_box = draw_grid(clicked, active_beat)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(all_box)):
                if all_box[i][0].collidepoint(event.pos):
                    co_ordinate = all_box[i][1]
                    clicked[co_ordinate[1]][co_ordinate[0]] *= -1

    beat_len = 3600 // bpm

    if playing:
        if active_length < beat_len:
            active_length += 1
        else:
            active_length = 0
            if active_beat < beats - 1:
                active_beat += 1
                beat_changed = True

            else:
                active_beat = 0
                beat_changed = True

    pygame.display.flip()
pygame.quit()
