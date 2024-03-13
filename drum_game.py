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
RED = (255, 0, 0)
FPS = 60
INSTRUMENTS = 6
BEATS = 8
BPM = 240

# Pygame initialize
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Custom Beat Maker")
clock = pygame.time.Clock()
label_font = pygame.font.Font('freesansbold.ttf', size=28)

running = True
clicked = [[-1 for _ in range(BEATS)] for _ in range(INSTRUMENTS)]

mixer.init()
sounds = {
    0: mixer.Sound('generatedSounds/kick_sound.wav'),
    1: mixer.Sound('generatedSounds/snare_sound.wav'),
    2: mixer.Sound('generatedSounds/hi_hat_sound.wav'),
    3: mixer.Sound('generatedSounds/open_hat_sound.wav'),
    4: mixer.Sound('generatedSounds/wood_block_sound.wav'),
    5: mixer.Sound('generatedSounds/mid_tom_sound.wav')
}

active_beat = 0
beat_change = True
is_playing = True
active_beat_length = 0


def play_notes():
    for i in range(INSTRUMENTS):
        if clicked[i][active_beat] == 1:
            sounds[i].play()


def draw_grid(clicks, beat):

    for i in range(INSTRUMENTS):
        pygame.draw.line(screen, RED, (0, (i * 100) + 100), (200, (i * 100) + 100), 2)

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

    pygame.draw.rect(screen, BLUE, [beat * ((WIDTH - 200) // BEATS) + 200, 0, ((WIDTH - 200) // BEATS),
                                    INSTRUMENTS * 100], 5, 3)

    return all_box


while running:
    clock.tick(FPS)
    screen.fill(BLACK)

    total_box = draw_grid(clicked, active_beat)

    # Play and Pause
    play_pause = pygame.draw.rect(screen, GREY, [30, HEIGHT - 80, 250, 80], 0, 5)
    play_text = label_font.render('Play and Pause', True, WHITE)
    screen.blit(play_text, (50, HEIGHT - 80))

    if is_playing:
        play_text_2 = label_font.render("Playing", True, WHITE)
    else:
        play_text_2 = label_font.render("Pause", True, WHITE)

    screen.blit(play_text_2, (70, HEIGHT - 50))

    clear_button = pygame.draw.rect(screen, GREY, [1150, HEIGHT - 80, 250, 80], 0, 5)
    clear_text = label_font.render("Clear Board", True, WHITE)
    screen.blit(clear_text, (1160, HEIGHT - 50))
    if beat_change:
        play_notes()
        beat_change = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle button state when clicked
            for box, coordinates in total_box:
                if box.collidepoint(event.pos):
                    x, y = coordinates
                    clicked[y][x] *= -1

        if event.type == pygame.MOUSEBUTTONUP:
            if play_pause.collidepoint(event.pos):
                if is_playing:
                    is_playing = False
                elif not is_playing:
                    is_playing = True

            elif clear_button.collidepoint(event.pos):
                clicked = [[-1 for _ in range(BEATS)] for _ in range(INSTRUMENTS)]

    beat_len = 3600 // BPM
    if is_playing:
        if active_beat_length < beat_len:
            active_beat_length += 1
        else:
            active_beat_length = 0
            if active_beat < BEATS - 1:
                active_beat += 1
                beat_change = True
            else:
                active_beat = 0
                beat_change = True
    pygame.display.flip()

pygame.quit()
