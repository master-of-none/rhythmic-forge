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
        time = np.linspace(0, duration / 1000, num_samples)
        envelope = np.power(0.5, 25 * time)
        t = np.arange(num_samples) / self.sample_rate
        oscillation = 1 * np.sin(2 * np.pi * frequency * t) * envelope
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
        #wavfile.write('hi_hat_sound.wav', self.sample_rate, hi_hat_sound)
        return hi_hat_sound


if __name__ == '__main__':
    hi_hat = HiHat()
    duration = 150
    hi_hat.generate_hi_hat(duration)

    #     kick = Kick()
    #     frequency = 30
    #     duration = 150
    #     sound = kick.generate_kick_sound(frequency, duration)
    #     # sd.play(sound, kick.sample_rate)
    #     # sd.wait()
    #     frequency = 250
    #     snare = Snare()
    #     snare.generate_snare_sound(frequency, duration)
