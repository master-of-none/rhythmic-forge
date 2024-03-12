import random
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
        kick_sound = filtered * 10
        kick_sound_int16 = (kick_sound * np.iinfo(np.int16).max).astype(np.int16)
        wavfile.write('generatedSounds/kick.wav', self.sample_rate, kick_sound_int16)
        return kick_sound_int16



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
        snare_sound_int16 = (snare_sound * np.iinfo(np.int16).max).astype(np.int16)
        wavfile.write("generatedSounds/snare_sound.wav", self.sample_rate, snare_sound_int16)
        return snare_sound_int16


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
        hi_hat_sound_int16 = (hi_hat_sound * np.iinfo(np.int16).max).astype(np.int16)
        wavfile.write('generatedSounds/hi_hat_sound.wav', self.sample_rate, hi_hat_sound_int16)
        return hi_hat_sound_int16


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
        open_hat_sound_int16 = (open_hat_sound * np.iinfo(np.int16).max).astype(np.int16)
        wavfile.write('generatedSounds/open_hat_sound.wav', self.sample_rate, open_hat_sound_int16)
        return open_hat_sound_int16


# Wood Block
# This sound seems difficult to generate, I have no clue as if now how to work on this
# I have to use sine or square tone to generate. Probably need to watch YouTube to understand more about woodblock

class WoodBlock:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate

    def generate_a_wave(self, frequency, duration):
        normalized_time = np.linspace(0, 1, int((self.sample_rate / 1000) * duration))
        envelope = np.power(0.5, 25 * normalized_time)
        actual_time = np.arange(int((self.sample_rate / 1000) * duration)) / self.sample_rate
        oscillation = np.sin(2 * np.pi * frequency * actual_time)
        return envelope * oscillation

    def generate_woodblock(self, frequency, ratio, amount, duration):
        frequency_modulation = frequency + self.generate_a_wave(frequency * ratio, duration) * amount
        normalized_time = np.linspace(0, 1, int((self.sample_rate / 1000) * duration))
        envelope = np.power(0.5, 25 * normalized_time)
        actual_time = np.arange(int((self.sample_rate / 1000) * duration)) / self.sample_rate
        woodblock = 1 * np.sin(2 * np.pi * frequency_modulation * actual_time) * envelope
        woodblock_int16 = (woodblock * np.iinfo(np.int16).max).astype(np.int16)
        wavfile.write('generatedSounds/woodblock.wav', self.sample_rate, woodblock_int16)
        return woodblock_int16


# Mid-Tom
# It took me 2 days to figure out woodblock and Mid-Tom and finally an algorithm kicked in after hours of debugging.
class MidTom:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate

    def generate_noise(self, duration):
        noise = np.random.random_sample(int((self.sample_rate / 1000) * duration)) * 2 - 1
        return noise

    def create_filter(self):
        sos_high_pass = butter(10, 70, 'hp', fs=1000, analog=False, output='sos')
        sos_low_pass = butter(2, 30, 'lp', fs=1000, analog=False, output='sos')
        return sos_high_pass, sos_low_pass

    def generate_sine_sweep(self, duration, start_frequency, end_frequency):
        normalized_time = np.linspace(0, 1, int((self.sample_rate / 1000) * duration))
        sweep = (np.sqrt(start_frequency) + (np.sqrt(end_frequency) - np.sqrt(start_frequency)) * normalized_time)
        sweep = np.power(sweep, 2)
        actual_time = np.arange(int((self.sample_rate / 1000) * duration)) / self.sample_rate
        return np.sin(2 * np.pi * sweep * actual_time)

    def generate_mid_tom_sound(self, frequency, duration):
        time = np.linspace(1, 0, int((self.sample_rate / 1000) * duration))
        time = np.power(time, 2.5)
        noise = self.generate_noise(duration)
        sos_high_pass, sos_low_pass = self.create_filter()
        sine_sweep = self.generate_sine_sweep(duration, frequency + (frequency * 0.5), frequency)
        sine_sweep = sine_sweep * time * 2.5
        filtered_noise = sosfilt(sos_high_pass, noise)
        filtered_noise_2 = sosfilt(sos_low_pass, filtered_noise)
        mid_tom = sine_sweep + (filtered_noise_2 * time) * 0.085
        mid_tom_int16 = (mid_tom * np.iinfo(np.int16).max).astype(np.int16)
        wavfile.write('generatedSounds/mid_tom_sound.wav', self.sample_rate, mid_tom_int16)
        return mid_tom_int16


class Clap:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate

    def generate_noise(self, duration):
        noise = np.random.random_sample(int((self.sample_rate / 1000) * duration)) * 2 - 1
        return noise

    def create_filter(self):
        sos_high_pass = butter(10, 1000, 'hp', fs=self.sample_rate, analog=False, output='sos')
        sos_low_pass = butter(4, 5000, 'lp', fs=self.sample_rate, analog=False, output='sos')
        return sos_high_pass, sos_low_pass

    def generate_clap_sound(self, duration):
        time = np.linspace(1, 0, int((self.sample_rate / 1000) * duration))
        time = np.power(time, 1.5)
        noise = self.generate_noise(duration)
        sos_high_pass, sos_low_pass = self.create_filter()
        filtered_noise = sosfilt(sos_high_pass, noise)
        filtered_noise = sosfilt(sos_low_pass, filtered_noise)
        clap_sound = filtered_noise * time * 2
        clap_sound_int16 = (clap_sound * np.iinfo(np.int16).max).astype(np.int16)
        wavfile.write("generatedSounds/clap_sound.wav", self.sample_rate, clap_sound_int16)
        return clap_sound_int16


class Tambourine:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate

    def generate_smooth_noise(self, duration):
        num_samples = int((self.sample_rate / 1000) * duration)
        noise = np.random.normal(0, 0.3, num_samples)
        return noise

    def generate_jingle(self, frequency, duration):
        num_samples = int((self.sample_rate / 1000) * duration)
        time = np.linspace(0, duration / 1000, num_samples)
        envelope = np.exp(-10 * time)
        jingle_signal = np.sin(2 * np.pi * frequency * time) * envelope
        return jingle_signal

    def create_filter(self):
        sos_band_pass = butter(4, [1000, 8000], 'band', fs=self.sample_rate, output='sos')
        return sos_band_pass

    def generate_tambourine_sound(self, duration):
        noise = self.generate_smooth_noise(duration)
        jingle = self.generate_jingle(3000, duration)
        tambourine_sound = noise + jingle
        sos_band_pass = self.create_filter()
        filtered_tambourine_sound = sosfilt(sos_band_pass, tambourine_sound)
        tambourine_sound = filtered_tambourine_sound * 1.5
        tambourine_sound_int16 = (tambourine_sound * np.iinfo(np.int16).max).astype(np.int16)
        wavfile.write("generatedSounds/tambourine.wav", self.sample_rate, tambourine_sound_int16)
        return tambourine_sound_int16


class Bongo:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate

    def generate_tone(self, frequency, duration):
        num_samples = int((self.sample_rate / 1000) * duration)
        time = np.linspace(0, duration / 1000, num_samples)
        envelope = np.exp(-10 * time)
        tone_signal = np.sin(2 * np.pi * frequency * time) * envelope
        return tone_signal

    def create_filter(self):
        sos_band_pass = butter(4, [100, 2000], 'band', fs=self.sample_rate, output='sos')
        return sos_band_pass

    def generate_bongo_sound(self, duration):
        low_tone = self.generate_tone(200, duration)
        high_tone = self.generate_tone(400, duration)
        bongo_sound = low_tone + high_tone
        sos_band_pass = self.create_filter()
        filtered_bongo_sound = sosfilt(sos_band_pass, bongo_sound)
        bongo_sound = filtered_bongo_sound / np.max(np.abs(filtered_bongo_sound))
        bongo_sound_int16 = (bongo_sound * np.iinfo(np.int16).max).astype(np.int16)
        wavfile.write('generatedSounds/bongo.wav', self.sample_rate, bongo_sound_int16)
        return bongo_sound_int16


class Tabla:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate

    def generate_drum_sound(self, frequency, duration):
        num_samples = int((self.sample_rate / 1000) * duration)
        time = np.linspace(0, duration / 1000, num_samples)
        bass_wave = np.sin(2 * np.pi * frequency * time)
        treble_wave = np.sin(2 * np.pi * (frequency * 1.6) * time)

        noise = np.random.normal(0, 0.05, len(time))
        tabla_sound = (bass_wave + treble_wave) * (1 - 0.4 * time) + noise * (1 - 0.5 * time)

        sos = butter(4, 1000, 'lp', fs=self.sample_rate, output='sos')
        tabla_sound = sosfilt(sos, tabla_sound)

        tabla_sound /= np.max(np.abs(tabla_sound))
        tabla_sound_int16 = (tabla_sound * np.iinfo(np.int16).max).astype(np.int16)
        wavfile.write('generatedSounds/tabla.wav', self.sample_rate, tabla_sound_int16)

        return tabla_sound_int16


# Next I will try to implement a sequencer.
# One way is to generate a random sequence and play the sound
# Before that I found a way while browsing online that I can implement a panning algorithm and then make sure the sound
# is played correctly.

class Panning:
    def pann(self, x, angle):
        cos_a = np.cos(angle)
        sin_a = np.sin(angle)
        stereo_factor = np.sqrt(2) / 2.0

        left = stereo_factor * (cos_a - sin_a) * x
        right = stereo_factor * (cos_a + sin_a) * x

        return np.column_stack((left, right))

    def generate_random_sequence(self, length):
        sequence = ''.join(random.choice(['^', '_']) for _ in range(length))
        return sequence


class GenerateBeat:
    def __init__(self, repetition, duration=150):
        self.duration = duration
        self.repetition = repetition
        self.panning_values = [0.03, 0, -15, 15, -35, 35]
        self.volume_mix_values = [1, 1, 0.4, 0.35, 0.6, 0.6]
        self.pann = Panning()

    def pause(self, note):
        paused = np.zeros_like(note)
        return paused

    def generate_sound(self):

        length = random.randint(5, 15)
        kick_pat = self.pann.generate_random_sequence(length)
        snare_pat = self.pann.generate_random_sequence(length)
        hihat_pat = self.pann.generate_random_sequence(length)
        open_hat_pat = self.pann.generate_random_sequence(length)
        wood_block_pat = self.pann.generate_random_sequence(length)
        mid_tom_pat = self.pann.generate_random_sequence(length)

        # Next set of instruments
        clap_pat = self.pann.generate_random_sequence(length)
        tambourine_pat = self.pann.generate_random_sequence(length)
        bongo_pat = self.pann.generate_random_sequence(length)
        tabla_pat = self.pann.generate_random_sequence(length)

        kick_sound = Kick().generate_kick_sound(30, self.duration)
        snare_sound = Snare().generate_snare_sound(250, self.duration)
        hihat_sound = HiHat().generate_hi_hat(self.duration)
        open_hat_sound = OpenHat().generate_open_hat(self.duration)
        wood_block_sound = WoodBlock().generate_woodblock(880, 2.25, 80, self.duration)
        mid_tom_sound = MidTom().generate_mid_tom_sound(175, self.duration)

        # Next set of sounds
        clap_sound = Clap().generate_clap_sound(self.duration)
        tambourine_sound = Tambourine().generate_tambourine_sound(self.duration)
        bongo_sound = Bongo().generate_bongo_sound(self.duration)
        tabla_sound = Tabla().generate_drum_sound(150, self.duration)

        kick_seq = np.concatenate([kick_sound if char == '^' else self.pause(kick_sound) for char in kick_pat])
        snare_seq = np.concatenate([snare_sound if char == '^' else self.pause(snare_sound) for char in snare_pat])
        hihat_seq = np.concatenate([hihat_sound if char == '^' else self.pause(hihat_sound) for char in hihat_pat])
        open_hat_seq = np.concatenate(
            [open_hat_sound if char == '^' else self.pause(open_hat_sound) for char in open_hat_pat])
        wood_block_seq = np.concatenate(
            [wood_block_sound if char == '^' else self.pause(wood_block_sound) for char in wood_block_pat])
        mid_tom_seq = np.concatenate(
            [wood_block_sound if char == '^' else self.pause(mid_tom_sound) for char in mid_tom_pat])

        # Next set
        clap_seq = np.concatenate([clap_sound if char == '^' else self.pause(clap_sound) for char in clap_pat])
        tambourine_seq = np.concatenate(
            [tambourine_sound if char == '^' else self.pause(tambourine_sound) for char in tambourine_pat])
        bongo_seq = np.concatenate([bongo_sound if char == '^' else self.pause(bongo_sound) for char in bongo_pat])
        tabla_seq = np.concatenate([tabla_sound if char == '^' else self.pause(tabla_sound) for char in tabla_pat])

        instrument_seq = [kick_seq, snare_seq, hihat_seq, open_hat_seq, wood_block_seq, mid_tom_seq]
        # print(instrument_seq)
        random.shuffle(instrument_seq)
        # print(instrument_seq)
        beats = self.panning_mixture(instrument_seq)

        instrument_seq_2 = [clap_seq, tambourine_seq, bongo_seq, tabla_seq, bongo_seq, tambourine_seq]
        random.shuffle(instrument_seq_2)
        beats_2 = self.panning_mixture(instrument_seq_2)
        return beats, beats_2

    def panning_mixture(self, instrument_seq):
        #print(instrument_seq)
        panned_instruments = []
        for inst, pan_val in zip(instrument_seq, self.panning_values):
            panned_instruments.append(self.pann.pann(inst, pan_val))

        vol_pan_inst = []
        for inst, vol_mix in zip(panned_instruments, self.volume_mix_values):
            tiled_sequence = np.tile(inst * vol_mix, (self.repetition, 1))
            vol_pan_inst.append(tiled_sequence)

        beats = sum(vol_pan_inst)
        return beats


class Reverb(object):
    def __init__(self, length):
        self.length = length
        self.buffer = [0] * length
        self.head = 0
        self.tail = 0
        self.empty = True

    def enqueue(self, s):
        assert self.empty or self.head != self.tail
        self.buffer[self.tail] = s
        self.tail = (self.tail + 1) % self.length
        self.empty = False

    def dequeue(self):
        assert not self.empty
        s = self.buffer[self.head]
        self.head = (self.head + 1) % self.length
        self.empty = self.head == self.tail
        return s

    def is_empty(self):
        return self.empty


class Reverb_apply:
    @staticmethod
    def apply_reverb(signal, delay, wet, reverb):
        buffer = Reverb(delay)
        out_signal = []
        for i, s in enumerate(signal):
            if i < delay:
                sdelay = 0
            else:
                sdelay = buffer.dequeue()
            out_signal.append((1 - wet) * s + wet * sdelay)
            buffer.enqueue((1 - reverb) * s + reverb * sdelay)
        return np.array(out_signal)


if __name__ == '__main__':
    pass
    # generate_beat = GenerateBeat(repetition=2)
    # beat1, beat2 = generate_beat.generate_sound()
    # sd.play(beat1.astype(np.int16), samplerate=44100)
    # sd.wait()
