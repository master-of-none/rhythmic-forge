import numpy as np
import sounddevice as sd
from scipy.signal import butter, sosfilt

def kick(frequency, duration):
    sample_rate = 44100
    time = np.linspace(0, duration, sample_rate)
    exponential_decay = np.exp(-20 * time)
    oscillation = np.cos(2 * np.pi * frequency * time)
    envelope = np.sqrt(time) * oscillation * exponential_decay
    sos = butter(2, 300, 'low', fs=sample_rate, output='sos')
    filtered = sosfilt(sos, envelope)
    return filtered * 3

if __name__ == '__main__':
    frequency = 30
    duration = 150
    sound = kick(frequency, duration)
    sd.play(sound, samplerate=44100)
    sd.wait()