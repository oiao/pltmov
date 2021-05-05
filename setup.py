from setuptools import setup, find_packages
from os.path import join as opj

NAME = 'pltmov'
DESCR = 'FFmpeg wrapper for pyplot for easy animation'
packages = [NAME]+[f'{NAME}.'+i for i in find_packages(NAME)]

with open(opj(NAME, '_version.py')) as f:
    exec(f.read())

setup(
    name             = NAME,
    version          = __version__,
    author           = 'Leo Komissarov',
    url              = f'https://github.com/oiao/{NAME}',
    download_url     = f'https://github.com/oiao/{NAME}/archive/master.zip',
    description      = DESCR,
    classifiers      = [
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python :: 3.6',
    ],
    keywords         = ['animation', 'ffmpeg', 'plotting', 'visualization', 'pyplot', 'matplotlib'],
    python_requires  = '>=3.6',
    install_requires = ['matplotlib'],
    packages         = packages,
    package_dir      = {NAME : NAME},
    package_data     = {NAME : ['tests/*']},
#     scripts          = [opj('scripts', NAME)],
)
