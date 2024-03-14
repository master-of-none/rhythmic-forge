import random
import numpy as np
import sounddevice as sd
from scipy.signal import butter, sosfilt
from scipy.io import wavfile


class Kick:
    """
     A class for generating kick drum sounds.

     Attributes:
         sample_rate (int): The sample rate of the sound.

     Methods:
         generate_kick_sound(frequency, duration): Generate a kick drum sound.
     """

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
        return kick_sound


class Snare:
    """
    A class for generating snare drum sounds.

    Attributes:
        sample_rate (int): The sample rate of the sound.

    Methods:
        generate_noise(duration): Generate noise for the snare.
        generate_sine(frequency, duration): Generate a sine wave for the snare.
        create_filter(): Create filters for processing snare sounds.
        generate_snare_sound(frequency, duration): Generate a snare drum sound.
    """

    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate

    def generate_noise(self, duration):
        time = np.linspace(0, 1, int((self.sample_rate / 1000) * duration))
        noise = np.random.random_sample(int((self.sample_rate / 1000) * duration)) * 2 - 1
        envelope = np.power(0.5, 12.5 * time)
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
        return snare_sound


class HiHat:
    """
     A class for generating hi-hat sounds.

     Attributes:
         sample_rate (int): The sample rate of the sound.

     Methods:
         generate_noise(duration): Generate noise for the hi-hat.
         generate_square_tone(frequency, duration): Generate a square tone for the hi-hat.
         create_filter(): Create filters for processing hi-hat sounds.
         generate_hi_hat(duration): Generate a hi-hat sound.
     """

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
        return hi_hat_sound


class OpenHat:
    """
      A class for generating open hi-hat sounds.

      Attributes:
          sample_rate (int): The sample rate of the sound.

      Methods:
          generate_noise(duration): Generate noise for the open hi-hat.
          generate_square_tone(frequency, duration): Generate a square tone for the open hi-hat.
          create_filter(): Create filters for processing open hi-hat sounds.
          generate_open_hat(duration): Generate an open hi-hat sound.
      """

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
        return open_hat_sound


class WoodBlock:
    """
       A class for generating woodblock sounds.

       Attributes:
           sample_rate (int): The sample rate of the sound.

       Methods:
           generate_a_wave(frequency, duration): Generate a sine wave.
           generate_woodblock(frequency, ratio, amount, duration): Generate a woodblock sound.
       """

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
        return woodblock


class MidTom:
    """
    A class for generating mid-tom sounds.

    Attributes:
        sample_rate (int): The sample rate of the sound.

    Methods:
        generate_noise(duration): Generate noise for the mid-tom.
        create_filter(): Create filters for processing mid-tom sounds.
        generate_sine_sweep(duration, start_frequency, end_frequency): Generate a sine sweep.
        generate_mid_tom_sound(frequency, duration): Generate a mid-tom sound.
    """

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
        return mid_tom


class Clap:
    """
     A class for generating clap sounds.

     Attributes:
         sample_rate (int): The sample rate of the sound.

     Methods:
         generate_noise(duration): Generate noise for the clap.
         create_filter(): Create filters for processing clap sounds.
         generate_clap_sound(duration): Generate a clap sound.
     """

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
        return clap_sound_int16


class Tambourine:
    """
     A class for generating tambourine sounds.

     Attributes:
         sample_rate (int): The sample rate of the sound.

     Methods:
         generate_smooth_noise(duration): Generate smooth noise for the tambourine.
         generate_jingle(frequency, duration): Generate a jingle sound.
         create_filter(): Create filters for processing tambourine sounds.
         generate_tambourine_sound(duration): Generate a tambourine sound.
     """

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
        return tambourine_sound_int16


class Bongo:
    """
       A class for generating bongo sounds.

       Attributes:
           sample_rate (int): The sample rate of the sound.

       Methods:
           generate_tone(frequency, duration): Generate a tone for the bongo.
           create_filter(): Create filters for processing bongo sounds.
           generate_bongo_sound(duration): Generate a bongo sound.
       """

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
        return bongo_sound_int16


class Tabla:
    """
       A class for generating tabla sounds.

       Attributes:
           sample_rate (int): The sample rate of the sound.

       Methods:
           generate_drum_sound(frequency, duration): Generate a tabla drum sound.
       """

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
        return tabla_sound_int16


class Panning:
    """
       A class for panning audio signals.

       Methods:
           pann(x, angle): Apply panning to an audio signal.
           generate_random_sequence(length): Generate a random panning sequence.
       """

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
    """
       A class for generating beats.

       Attributes:
           repetition (int): Number of repetitions for each beat.
           duration (int): Duration of each beat.

       Methods:
           pause(note): Generate a pause in the beat.
           generate_sound(): Generate a beat sequence.
           panning_mixture(instrument_seq): Mix and pan instruments.
       """

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
        random.shuffle(instrument_seq)
        beats = self.panning_mixture(instrument_seq)

        instrument_seq_2 = [clap_seq, tambourine_seq, bongo_seq, tabla_seq, bongo_seq, tambourine_seq]
        random.shuffle(instrument_seq_2)
        beats_2 = self.panning_mixture(instrument_seq_2)
        return beats, beats_2

    def panning_mixture(self, instrument_seq):
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
    """
        A class representing a reverberation effect.

        Attributes:
            length (int): Length of the reverb buffer.
            buffer (list): The reverb buffer.
            head (int): Pointer to the head of the buffer.
            tail (int): Pointer to the tail of the buffer.
            empty (bool): Indicates if the buffer is empty.

        Methods:
            enqueue(s): Add a sample to the buffer.
            dequeue(): Remove a sample from the buffer.
            is_empty(): Check if the buffer is empty.
        """

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
    """
     A class for applying reverb to audio signals.

     Methods:
         apply_reverb(signal, delay, wet, reverb): Apply reverb to an audio signal.
     """

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


class SoundFile:
    """
       A class for generating sound files.

       Attributes:
           duration (int): Duration of the sound files.
           sample_rate (int): Sample rate of the sound files.

       Methods:
           generate_sound_files(): Generate sound files for various percussion instruments.
       """

    def __init__(self, duration=150):
        self.duration = duration
        self.sample_rate = 44100

    def generate_sound_files(self):
        kick_sound = Kick().generate_kick_sound(30, self.duration)
        kick_sound_int16 = (kick_sound * np.iinfo(np.int16).max).astype(np.int16)
        wavfile.write('generatedSounds/kick_sound.wav', self.sample_rate, kick_sound_int16)

        snare_sound = Snare().generate_snare_sound(250, self.duration)
        snare_sound_int16 = (snare_sound * np.iinfo(np.int16).max).astype(np.int16)
        wavfile.write('generatedSounds/snare_sound.wav', self.sample_rate, snare_sound_int16)

        hihat_sound = HiHat().generate_hi_hat(self.duration)
        hi_hat_sound_int16 = (hihat_sound * np.iinfo(np.int16).max).astype(np.int16)
        wavfile.write('generatedSounds/hi_hat_sound.wav', self.sample_rate, hi_hat_sound_int16)

        open_hat_sound = OpenHat().generate_open_hat(self.duration)
        open_hat_sound_int16 = (open_hat_sound * np.iinfo(np.int16).max).astype(np.int16)
        wavfile.write('generatedSounds/open_hat_sound.wav', self.sample_rate, open_hat_sound_int16)

        wood_block_sound = WoodBlock().generate_woodblock(880, 2.25, 80, self.duration)
        woodblock_int16 = (wood_block_sound * np.iinfo(np.int16).max).astype(np.int16)
        wavfile.write('generatedSounds/wood_block_sound.wav', self.sample_rate, woodblock_int16)

        mid_tom_sound = MidTom().generate_mid_tom_sound(175, self.duration)
        mid_tom_int16 = (mid_tom_sound * np.iinfo(np.int16).max).astype(np.int16)
        wavfile.write('generatedSounds/mid_tom_sound.wav', self.sample_rate, mid_tom_int16)

        # # Next set of sounds
        # clap_sound = Clap().generate_clap_sound(self.duration)
        # tambourine_sound = Tambourine().generate_tambourine_sound(self.duration)
        # bongo_sound = Bongo().generate_bongo_sound(self.duration)
        # tabla_sound = Tabla().generate_drum_sound(150, self.duration)


if __name__ == '__main__':
    pass
