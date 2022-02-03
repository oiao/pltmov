from .movie import Movie
from shutil import which

if which('ffmppeg') is None:
    raise ImportError(f"This package requires the 'ffmpeg' binary to be installed.")
    
__all__ = ['Movie']
