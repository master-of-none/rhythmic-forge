import tkinter as tk
import sounddevice as sd
from scipy.io import wavfile

from drum_beat import Kick


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

        self.kick = Kick()
        self.setup_gui()
        self.root.mainloop()

    def setup_gui(self):
        self.play_button = tk.Button(self.root, text="Play", command=self.play_drum)
        self.play_button.pack()

        self.quit_button = tk.Button(self.root, text="Quit", command=self.quit)
        self.quit_button.pack()

    def play_drum(self):
        frequency = 30
        duration = 150
        sound = self.kick.generate_kick_sound(frequency, duration)
        wavfile.write("kick.wav", 44100, sound)
        sd.play(sound, samplerate=44100)
        sd.wait()

    def quit(self):
        self.root.destroy()
