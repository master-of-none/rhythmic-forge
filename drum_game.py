# I will try to implement This using pygame
from drum_beat import *
import pygame
import sounddevice as sd

pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Custom Beat Generator")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY =(150, 150, 150)

button_positions = [(50, 100), (150, 100), (250, 100), (350, 100)]
button_texts = ["Kick", "Snare", "Hi-Hat", "Open Hat"]

button_width, button_height = 100, 50
button_rects = [pygame.Rect(pos[0], pos[1], button_width, button_height) for pos in button_positions]

running = True
instrument_sequence = []

while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button clicked
                for i, button_rect in enumerate(button_rects):
                    if button_rect.collidepoint(event.pos):
                        if i == 0:
                            beat = Kick().generate_kick_sound(30, 150)
                            instrument_sequence.append(beat)
                            sd.play(beat, samplerate=44100)
                            sd.wait()
                        elif i == 1:
                            beat = Snare().generate_snare_sound(250, 150)
                            instrument_sequence.append(beat)
                            sd.play(beat, samplerate=44100)
                            sd.wait()
                        elif i == 2:
                            beat = HiHat().generate_hi_hat(150)
                            instrument_sequence.append(beat)
                            sd.play(beat, samplerate=44100)
                            sd.wait()
                        else:
                            beat = OpenHat().generate_open_hat(150)
                            instrument_sequence.append(beat)
                            sd.play(beat, samplerate=44100)
                            sd.wait()

                        #instrument_sequence.append(beat)

                if play_button_rect.collidepoint(event.pos):
                    # print(instrument_sequence)
                    beats = GenerateBeat().panning_mixture(instrument_sequence)
                    #
                    # #print(beats)
                    # beats = sum(instrument_sequence)
                    sd.play(beats, samplerate=44100)
                    sd.wait()

    for button_rect, text in zip(button_rects, button_texts):
        pygame.draw.rect(screen, GRAY, button_rect)
        font = pygame.font.SysFont(None, 30)
        text_surface = font.render(text, True, BLACK)
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)

    play_button_rect = pygame.Rect(50, 300, 100, 50)
    pygame.draw.rect(screen, GRAY, play_button_rect)
    font = pygame.font.SysFont(None, 30)
    text_surface = font.render("Play", True, BLACK)
    text_rect = text_surface.get_rect(center=play_button_rect.center)
    screen.blit(text_surface, text_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()