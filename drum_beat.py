import numpy as np
import sounddevice as sd
from scipy.signal import butter, sosfilt


class Kick:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate

    def generate_kick_sound(self, frequency, duration):
        time = np.linspace(0, 1, int(self.sample_rate * duration / 1000))
        exponential_decay = np.power(0.5, 25 * time)
        envelope = frequency * np.sqrt(time) - 0.15
        oscillation = exponential_decay * np.cos(envelope)
        sos = butter(2, 300, 'low', fs=self.sample_rate, output='sos')
        filtered = sosfilt(sos, oscillation)
        return filtered * 3

# Next is to generate snare sound
# For this what I can do is generate a noise with an envelope, generate a sine wave with an envelope
# Make 2 high pass filters (Must think more about this), pass noise and sine to filter,
# Add up the filtered noises for generating snare sound. OOFF!!!


class Snare:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate

    def generate_noise(self):
        pass

    def generate_sine(self):
        pass

    def create_filter(self):
        pass

    def generate_snare_sound(self):
        pass


if __name__ == '__main__':
    kick = Kick()
    frequency = 30
    duration = 150
    sound = kick.generate_kick_sound(frequency, duration)
    sd.play(sound, kick.sample_rate)
    sd.wait()
