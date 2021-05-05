This package provides a wrapper around [ffmpeg](http://ffmpeg.org/), allowing for fast conversion of your pyplot plots into a movie file.


# Installation
  * `git clone https://github.com/oiao/pltmov.git`
  * `pip install -e pltmov`


# How to use

#### 1. Import and initialize a `Movie` instance
```python
from pltmov import Movie
movie = Movie()
````

#### 2. Define your plotting function as usual, but use the instance's `record` decorator
```python
import numpy as np
import matplotlib.pyplot as plt

@movie.record
def plot(xmax, text):
    x = np.linspace(0, xmax, int(np.sqrt(xmax)*100))
    plt.plot(x, np.sin(x))
    plt.text(0.1, 0.1, str(text), transform=plt.gca().transAxes, size=18)
    plt.tight_layout()
````
Make sure your plotting function does **not** save anything to disk

#### 3. Call the plotting function with as many arguments as the number of frames in your movie
```python
ranges = np.linspace(0.1,  100, 1000)
texts  = [f"frame {i}" for i in range(1, len(ranges)+1)]
for r, t in zip(ranges,texts):
    plot(r, t)
```

#### 4. Save your movie
```python
movie.write('movie.mp4', fps=60)
```

All arguments for `write()` are documented in the [docstring](https://github.com/oiao/pltmov/blob/master/pltmov/movie.py#L54).
