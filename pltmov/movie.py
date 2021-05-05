import os
from os.path import join as opj
import matplotlib.pyplot as plt
from multiprocessing import Pool
from tempfile import TemporaryDirectory
from subprocess import Popen, DEVNULL
from typing import Callable, List, Tuple

class Movie:
    def __init__(self):
        self.args = []
        self.f = None
        self.count = 0
        self.command = '-c:v libx264'

    def record(self,f:Callable):
        """
        Use as a wrapper around yor plotting funciton, then call it
        as many times as the number of frames you want to record.
        This method needs to be called at least once before `record()` can be called.

        Parameters
        ----------
        f: Callable
            The plotting function to be recorded

        Examples
        --------
            import numpy as np
            import matplotlib.pyplot as plt
            from pltmov import Movie

            movie = Movie()

            @movie.record
            def plot(xmax, text):
                x = np.linspace(0, xmax, int(np.sqrt(xmax)*100))
                plt.plot(x, np.sin(x))
                plt.text(0.1, 0.1, str(text), transform=plt.gca().transAxes, size=18)
                plt.tight_layout()

            ranges = np.linspace(0.1,  100, 1000)
            texts  = [f"frame {i}" for i in range(1, len(ranges)+1)]
            for r, t in zip(ranges,texts):
                plot(r, t)
        """
        self.f = self.f or f
        def wrap(*a, **kw):
            assert not kw, "Can not take keyword arguments"
            self.args.append(a+(self.count,))
            self.count += 1
        return wrap

    def write(self, outfile, dpi=100, fps=30, crf=10, processes=None, tempdir=None, silent=True):
        """
        Writes the recorded frames to an `outfile` movie file.
        The `record()` method must have been called before this method can be used.

        Parameters
        ----------
        outfile : str
            Location of the produced movie file
        dpi : int
            DPI for the resulting images and movie
        fps : int
            Frames per second for the resulting movie
        crf : 0 <= int <= 51
            This value will be passed to the `ffmpeg -crf` argument.
            Lower values mean better quality (0 is lossless, 51 is crap)
        processes : optional, int
            Number of MP workres to be used when writing all frames to disk.
            Defaults to `os.cpu_count()`
        tempdir : optional, str
            Temporary directory that stores all frames before passing them to `ffmpeg`.
            If set, the directory will not be removed after this method has been called.
        silent : bool
            Whether to suppress all `ffmpeg` input

        Examples
        --------
        Continued from `record()`:
        >>> movie.write('movie.mp4')
        """
        assert self.f is not None, f"Please record() your function's arguments before calling this method"
        td = None
        if tempdir is None:
            td = TemporaryDirectory()
            tempdir = td.name
        if not os.path.exists(tempdir):
            os.makedirs(tempdir)

        _globals.tempdir = tempdir
        _globals.dpi = dpi
        _globals.f = self.f

        with Pool(processes=processes) as p:
            p.starmap( _plot, self.args )
        cmd = ['ffmpeg', '-r', fps, '-i', opj(tempdir, '%07d.png'), '-crf', crf, '-y'] +  self.command.split() + [outfile]
        p = Popen([str(i) for i in cmd], stderr=DEVNULL if silent else None)
        p.communicate()

        if td is not None:
            td.cleanup()


# force the actual plot function to the global scope
class _globals:
    tempdir = None
    dpi = None
    f = None

def _plot(*args):
    _globals.f(*args[:-1])
    plt.savefig(opj(_globals.tempdir, f"{args[-1]:07d}.png"), dpi=_globals.dpi)
    plt.close()
