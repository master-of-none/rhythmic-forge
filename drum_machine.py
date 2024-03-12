import tkinter as tk
import sounddevice as sd
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
        self.setup_gui()
        self.root.mainloop()
        # self.generate_beat = GenerateBeat()

    def setup_gui(self):
        self.play_button = tk.Button(self.root, text="Play Random Beat", command=self.play_beat_1)
        self.play_button.pack()

        self.play_button = tk.Button(self.root, text="Play Random Beat 2", command=self.play_beat_2)
        self.play_button.pack()

        self.play_button = tk.Button(self.root, text="Play Reverb Beat 1", command=self.play_reverb)
        self.play_button.pack()

        self.stop_button = tk.Button(self.root, text="Stop the Beat", command=self.stop_beat)
        self.stop_button.pack()

        self.quit_button = tk.Button(self.root, text="Quit", command=self.quit)
        self.quit_button.pack()

    def play_beat_1(self):
        generate_beat = GenerateBeat(repetition=2)
        beat1, beat2 = generate_beat.generate_sound()
        sd.play(beat1.astype(np.int16), self.samplerate)

    def play_beat_2(self):
        generate_beat = GenerateBeat(repetition=2)
        beat1, beat2 = generate_beat.generate_sound()
        sd.play(beat2.astype(np.int16), self.samplerate)

    def play_reverb(self):
        generate_beat = GenerateBeat(repetition=2)
        beat1, beat2 = generate_beat.generate_sound()
        reverb_delay = 100
        wetness = 0.5
        reverb_strength = 0.1
        reverb_sound = Reverb_apply()
        reverb_beat = reverb_sound.apply_reverb(beat1, reverb_delay, wetness, reverb_strength)
        sd.play(reverb_beat.astype(np.int16), self.samplerate)
    def stop_beat(self):
        sd.stop()

    def quit(self):
        self.root.destroy()
