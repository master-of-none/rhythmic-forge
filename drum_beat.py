import numpy as np
import sounddevice as sd
from scipy.signal import butter, sosfilt
from scipy.io import wavfile


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

    def generate_noise(self, duration):
        time = np.linspace(0, 1, int((self.sample_rate / 1000) * duration))
        noise = np.random.random_sample(int((self.sample_rate / 1000) * duration)) * 2 - 1
        envelope = np.power(0.5, 12.5 * time)
        # wavfile.write('noise.wav', self.sample_rate, noise * envelope)
        return noise * envelope

    def generate_sine(self, frequency, duration):
        num_samples = int((self.sample_rate / 1000) * duration)
        normalized_time = np.linspace(0, duration / 1000, num_samples)
        envelope = np.power(0.5, 25 * normalized_time)
        actual_time = np.arange(num_samples) / self.sample_rate
        oscillation = 1 * np.sin(2 * np.pi * frequency * actual_time) * envelope
        return oscillation

    def create_filter(self):
        sos_high_pass = butter(4, 20, 'hp', fs=1000, analog=False, output='sos')
        sos_band_pass = butter(1, [5, 40], 'bp', fs=1000, output='sos')
        return sos_high_pass, sos_band_pass

    def generate_snare_sound(self, frequency, duration):
        noise = self.generate_noise(duration)
        sine = self.generate_sine(frequency, duration)
        sos_high_pass, sos_band_pass = self.create_filter()
        filtered_noise = sosfilt(sos_high_pass, noise)
        filtered_sine = sosfilt(sos_band_pass, sine)
        snare_sound = (filtered_noise + filtered_sine) * 4
        # wavfile.write("snare_sound.wav", self.sample_rate, snare_sound)
        return snare_sound


# Third step is to generate the hi hat sound Steps here are nearly same as snare. First generate the noise,
# Hi hat uses square tone hence can generate square wave, create a filter and finally figure out what to do with
# filtered signals

class HiHat:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate

    def generate_noise(self, duration):
        noise = np.random.random_sample(int((self.sample_rate / 1000) * duration))
        return noise

    def generate_square_tone(self, frequency, duration):
        time = np.linspace(0, 1, int((self.sample_rate / 1000) * duration))
        envelope = np.power(0.5, 25 * time)
        oscillation = np.sin(2 * np.pi * frequency * time)
        square_tone = np.where(oscillation > 0, 1, -1) * envelope
        return square_tone

    def create_filter(self):
        sos_high_pass_1 = butter(10, 100, 'hp', fs=1000, analog=False, output='sos')
        sos_high_pass_2 = butter(2, 100, 'hp', fs=1000, analog=False, output='sos')
        return sos_high_pass_1, sos_high_pass_2

    def generate_hi_hat(self, duration):
        time = np.linspace(1, 0, int((self.sample_rate / 1000) * duration))
        time = np.power(time, 4)
        high_noise = self.generate_square_tone(350, duration) + self.generate_square_tone(800, duration) + \
                     (self.generate_noise(duration) / 4)
        sos_high_pass_1, sos_high_pass_2 = self.create_filter()
        filtered_wave_1 = sosfilt(sos_high_pass_1, high_noise)
        filtered_wave_2 = sosfilt(sos_high_pass_2, filtered_wave_1)
        hi_hat_sound = filtered_wave_2 * time * 4
        # wavfile.write('hi_hat_sound.wav', self.sample_rate, hi_hat_sound)
        return hi_hat_sound


# Open Hat is similar as Hi hat with some variations in the creating the filter
# Most functions are same with some variations, implementing initial version

class OpenHat:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate

    def generate_noise(self, duration):
        noise = np.random.random_sample(int((self.sample_rate / 1000) * duration))
        return noise

    def generate_square_tone(self, frequency, duration):
        time = np.linspace(0, 1, int((self.sample_rate / 1000) * duration))
        envelope = np.power(0.5, 25 * time)
        oscillation = np.sin(2 * np.pi * frequency * time)
        square_tone = np.where(oscillation > 0, 1, -1) * envelope
        return square_tone

    def create_filter(self):
        sos_high_pass_1 = butter(10, 50, 'hp', fs=1000, analog=False, output='sos')
        sos_high_pass_2 = butter(2, 50, 'hp', fs=1000, analog=False, output='sos')
        return sos_high_pass_1, sos_high_pass_2

    def generate_open_hat(self, duration):
        time = np.linspace(1, 0, int((self.sample_rate / 1000) * duration))
        time = np.power(time, 0.1)
        high_noise = self.generate_square_tone(350, duration) + self.generate_square_tone(800, duration) + \
                     (self.generate_noise(duration) / 4)
        sos_high_pass_1, sos_high_pass_2 = self.create_filter()
        filtered_wave_1 = sosfilt(sos_high_pass_1, high_noise)
        filtered_wave_2 = sosfilt(sos_high_pass_2, filtered_wave_1)
        open_hat_sound = filtered_wave_2 * time * 4
        #wavfile.write('open_hat_sound.wav', self.sample_rate, open_hat_sound)
        return open_hat_sound


# Wood Block
# This sound seems difficult to generate, I have no clue as if now how to work on this
# I have to use sine or square tone to generate. Probably need to watch YouTube to understand more about woodblock

class WoodBlock:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate

    def generate_a_wave(self, frequency, duration):
        normalized_time = np.linspace(0, 1, int((self.sample_rate / 1000) * duration))
        envelope = np.power(0.5, 25*normalized_time)
        actual_time = np.arange(int((self.sample_rate / 1000) * duration)) / self.sample_rate
        oscillation = np.sin(2 * np.pi * frequency * actual_time)
        return envelope * oscillation

    def generate_woodblock(self, frequency, ratio, amount, duration):
        frequency_modulation = frequency + self.generate_a_wave(frequency*ratio, duration) * amount
        normalized_time = np.linspace(0, 1, int((self.sample_rate / 1000) * duration))
        envelope = np.power(0.5, 25 * normalized_time)
        actual_time = np.arange(int((self.sample_rate / 1000) * duration)) / self.sample_rate
        woodblock = 1 * np.sin(2 * np.pi * frequency_modulation * actual_time) * envelope
        wavfile.write('woodblock.wav', self.sample_rate, woodblock)


if __name__ == '__main__':
    woodblock = WoodBlock()
    woodblock.generate_woodblock(880, 2.25, 80,duration=150)
