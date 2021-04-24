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

    def record(self,f):
        """
        Use as a wrapper around yor plotting funciton,
        then call it as many times as the number of frames you want
        to record. 
        """
        self.f = self.f or f
        def wrap(*a, **kw):
            assert not kw, "Can not take keyword arguments"
            self.args.append(a+(self.count,))
            self.count += 1
        return wrap

    def write(self, outfile, dpi=100, fps=30, crf=10, processes=None, tempdir=None, silent=True):
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
