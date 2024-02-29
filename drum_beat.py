import numpy as np
import sounddevice as sd
from scipy.signal import butter, sosfilt


def kick(frequency, duration):
    sample_rate = 44100
    time = np.linspace(0, 1, int(sample_rate * duration / 1000))
    exponential_decay = np.power(0.5, 25 * time)
    envelope = frequency * np.sqrt(time) - 0.15
    oscillation = exponential_decay * np.cos(envelope)
    sos = butter(2, 300, 'low', fs=sample_rate, output='sos')
    filtered = sosfilt(sos, oscillation)
    return filtered * 3


if __name__ == '__main__':
    frequency = 30
    duration = 150
    sound = kick(frequency, duration)
    sd.play(sound, samplerate=44100)
    sd.wait()
