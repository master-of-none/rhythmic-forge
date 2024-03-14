import unittest
import numpy as np
from drum_beat import Kick, Snare, HiHat, OpenHat, WoodBlock, MidTom, Clap, Tambourine, Bongo, Tabla, GenerateBeat


class TestGenerateBeat(unittest.TestCase):
    def test_generate_sound(self):
        generate_beat = GenerateBeat(repetition=2)
        beat1, beat2 = generate_beat.generate_sound()

        self.assertIsInstance(beat1, np.ndarray)
        self.assertIsInstance(beat2, np.ndarray)

        min_non_zero_samples = int(0.1 * len(beat1))
        self.assertGreater(np.count_nonzero(beat1), min_non_zero_samples)
        self.assertGreater(np.count_nonzero(beat2), min_non_zero_samples)

    def test_sound_generation(self):
        duration = 150
        sample_rate = 44100

        kick = Kick(sample_rate)
        kick_sound = kick.generate_kick_sound(30, duration)
        self.assertIsInstance(kick_sound, np.ndarray)
        self.assertEqual(kick_sound.shape, (duration * sample_rate // 1000,))

        snare = Snare(sample_rate)
        snare_sound = snare.generate_snare_sound(250, duration)
        self.assertIsInstance(snare_sound, np.ndarray)
        self.assertEqual(snare_sound.shape, (duration * sample_rate // 1000,))

        hihat = HiHat(sample_rate)
        hihat_sound = hihat.generate_hi_hat(duration)
        self.assertIsInstance(hihat_sound, np.ndarray)
        self.assertEqual(hihat_sound.shape, (duration * sample_rate // 1000,))

        open_hat = OpenHat(sample_rate)
        open_hat_sound = open_hat.generate_open_hat(duration)
        self.assertIsInstance(open_hat_sound, np.ndarray)
        self.assertEqual(open_hat_sound.shape, (duration * sample_rate // 1000,))

        woodblock = WoodBlock(sample_rate)
        woodblock_sound = woodblock.generate_woodblock(880, 2.25, 80, duration)
        self.assertIsInstance(woodblock_sound, np.ndarray)
        self.assertEqual(woodblock_sound.shape, (duration * sample_rate // 1000,))

        mid_tom = MidTom(sample_rate)
        mid_tom_sound = mid_tom.generate_mid_tom_sound(175, duration)
        self.assertIsInstance(mid_tom_sound, np.ndarray)
        self.assertEqual(mid_tom_sound.shape, (duration * sample_rate // 1000,))

        clap = Clap(sample_rate)
        clap_sound = clap.generate_clap_sound(duration)
        self.assertIsInstance(clap_sound, np.ndarray)
        self.assertEqual(clap_sound.shape, (duration * sample_rate // 1000,))

        tambourine = Tambourine(sample_rate)
        tambourine_sound = tambourine.generate_tambourine_sound(duration)
        self.assertIsInstance(tambourine_sound, np.ndarray)
        self.assertEqual(tambourine_sound.shape, (duration * sample_rate // 1000,))

        bongo = Bongo(sample_rate)
        bongo_sound = bongo.generate_bongo_sound(duration)
        self.assertIsInstance(bongo_sound, np.ndarray)
        self.assertEqual(bongo_sound.shape, (duration * sample_rate // 1000,))

        tabla = Tabla(sample_rate)
        tabla_sound = tabla.generate_drum_sound(150, duration)
        self.assertIsInstance(tabla_sound, np.ndarray)
        self.assertEqual(tabla_sound.shape, (duration * sample_rate // 1000,))


if __name__ == '__main__':
    unittest.main()
