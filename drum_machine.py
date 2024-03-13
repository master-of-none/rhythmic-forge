import tkinter as tk
import sounddevice as sd
from drum_beat import *
from threading import Thread
import subprocess
import os

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
        tk.Label(self.root, text="Select a Beat:").pack(pady=10)

        tk.Button(self.root, text="Play Random Beat", command=self.play_beat_1).pack(pady=5)

        tk.Button(self.root, text="Play Random Beat 2", command=self.play_beat_2).pack(pady=5)

        tk.Button(self.root, text="Play Reverb Beat 1", command=self.play_reverb).pack(pady=5)

        tk.Button(self.root, text="Stop the Beat", command=self.stop_beat).pack(pady=5)

        tk.Button(self.root, text="Open Pygame Window", command=self.open_pygame_window).pack(pady=5)

        tk.Button(self.root, text="Quit", command=self.quit).pack(pady=5)

    def play_beat_1(self):
        generate_beat = GenerateBeat(repetition=2)
        beat1, beat2 = generate_beat.generate_sound()
        sd.play(beat1, self.samplerate)

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
        sd.play(reverb_beat, self.samplerate)

    def stop_beat(self):
        sd.stop()

    def open_pygame_window(self):
        if not os.path.exists("generatedSounds"):
            os.makedirs("generatedSounds")

        required_sounds = [
            "generatedSounds/kick_sound.wav",
            "generatedSounds/snare_sound.wav",
            "generatedSounds/hi_hat_sound.wav",
            "generatedSounds/open_hat_sound.wav",
            "generatedSounds/wood_block_sound.wav",
            "generatedSounds/mid_tom_sound.wav"
        ]
        missing_sounds = [sound for sound in required_sounds if not os.path.exists(sound)]

        if missing_sounds:
            sound_file = SoundFile()
            sound_file.generate_sound_files()

        subprocess.Popen(["python", "drum_game.py"])

    def quit(self):
        self.root.destroy()
