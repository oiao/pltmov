from shutil import which
if which('ffmpeg') is None:
    raise ImportError(f"This package requires the 'ffmpeg' binary to be installed.")
del which    

from .movie import Movie
__all__ = ['Movie']
