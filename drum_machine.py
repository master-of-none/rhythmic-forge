import tkinter as tk
import sounddevice as sd
from scipy.io import wavfile

from drum_beat import *


class DrumMachine:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Rhythmic Forge")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        window_width = int(screen_width / 2)
        window_height = int(screen_height / 2)
        window_position_x = int((screen_width - window_width) / 2)
        window_position_y = int((screen_height - window_height) / 2)

        self.root.geometry(f"{window_width}x{window_height}+{window_position_x}+{window_position_y}")

        self.duration = 150
        self.samplerate = 44100
        self.kick = Kick()
        self.snare = Snare()
        self.hi_hat = HiHat()
        self.open_hat = OpenHat()
        self.setup_gui()
        self.root.mainloop()
        # self.generate_beat = GenerateBeat()

    def setup_gui(self):
        self.play_button = tk.Button(self.root, text="Play Kick Sound", command=self.play_kick)
        self.play_button.pack()

        self.play_button = tk.Button(self.root, text="Play Snare Sound", command=self.play_snare)
        self.play_button.pack()

        self.play_button = tk.Button(self.root, text="Play HiHat Sound", command=self.play_hi_hat)
        self.play_button.pack()

        self.play_button = tk.Button(self.root, text="Play OpenHat Sound", command=self.play_open_hat)
        self.play_button.pack()

        self.play_button = tk.Button(self.root, text="Play Random Beat", command=self.play_beat)
        self.play_button.pack()

        self.quit_button = tk.Button(self.root, text="Quit", command=self.quit)
        self.quit_button.pack()

    def play_kick(self):
        frequency = 30
        sound = self.kick.generate_kick_sound(frequency, self.duration)
        # wavfile.write("kick.wav", 44100, sound)
        sd.play(sound, self.samplerate)
        sd.wait()

    def play_snare(self):
        frequency = 250
        snare_sound = self.snare.generate_snare_sound(frequency, self.duration)
        sd.play(snare_sound, self.samplerate)
        sd.wait()

    def play_hi_hat(self):
        hi_hat = self.hi_hat.generate_hi_hat(self.duration)
        sd.play(hi_hat, self.samplerate)
        sd.wait()

    def play_open_hat(self):
        open_hat = self.open_hat.generate_open_hat(self.duration)
        sd.play(open_hat, self.samplerate)
        sd.wait()

    def play_beat(self):
        generate_beat = GenerateBeat()
        beat = generate_beat.generate_sound()
        sd.play(beat, self.samplerate)
        sd.wait()

    def quit(self):
        self.root.destroy()
