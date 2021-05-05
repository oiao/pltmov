import os
import shutil
import unittest
import numpy as np
import matplotlib.pyplot as plt
from pltmov import Movie

mov = Movie()

class TestMovie(unittest.TestCase):
    def test01_init(self):
        self.assertEqual(mov.args, [])
        self.assertEqual(mov.count, 0)
        self.assertEqual(mov.command, '-c:v libx264')
        self.assertIsNone(mov.f)

    def test02_record(self):
        @mov.record
        def plot(xmax, text):
            x = np.linspace(0, xmax, 100)
            plt.plot(x, np.sin(x))
            plt.text(0.1, 0.1, str(text), transform=plt.gca().transAxes, size=18)
            plt.tight_layout()

        ranges = np.linspace(0.1,  100, 99)
        texts  = [f"frame {i}" for i in range(1, len(ranges)+1)]
        for r, t in zip(ranges,texts):
            plot(r, t)

        self.assertEqual(len(mov.args), 99)
        self.assertEqual(mov.args[0], (ranges[0], texts[0], 0))
        self.assertEqual(mov.count, 99)

    def test03_write_temp(self):
        mov.write('movie.mp4', dpi=120, fps=32, crf=20, processes=3, tempdir=None, silent=False)
        self.assertTrue( os.path.exists('movie.mp4') )

    def test04_write_temp(self):
        mov.write('movie.mp4', dpi=120, fps=32, crf=20, processes=3, tempdir='tempdir', silent=False)
        self.assertTrue( os.path.exists('movie.mp4') )
        self.assertTrue( os.path.exists('tempdir') )
        self.assertEqual( len(os.listdir('tempdir')), 99)

    @classmethod
    def tearDownClass(self):
        for i in ['movie.mp4', 'tempdir']:
            if os.path.isdir(i):
                shutil.rmtree(i)
            elif os.path.isfile(i):
                os.remove(i)
