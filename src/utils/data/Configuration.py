# imports
from pathlib import Path
import time

# paths
DIRECTORY : Path = Path.cwd()
SOURCE : Path = DIRECTORY /'src'

DATA : Path = DIRECTORY /'data'
TEMPORARY : Path = DIRECTORY /'temp'
ASSETS : Path = DIRECTORY /'assets'
BIN : Path = DIRECTORY /'bin'

# ffmpeg executable paths
FFMPEG : Path = BIN /'video' /'bin' /'ffmpeg.exe'
FFPROBE : Path = BIN /'video' /'bin' /'ffprobe.exe'
FFPLAY : Path = BIN /'video' /'bin' /'ffplay.exe'

# keys for apis
ARTIFICIAL : list[str] = [

    'AIzaSyDaCiAERqkCVsLtugIHPATBtQ3HNGfW6fw', 
    'AIzaSyAxlCcoRfil6Yr061njkFwA2FcAT9jSveE', 
    'AIzaSyDJ72sXFO_47S8E3z8dgLKJmtLvEjQGXI4'
]
STOCK : str = '53636883-18dd4c5344673acec1a9a2a12'

# decorator time function
def Time(
    func : object
):
    
    def __func(
        *args, **kwargs
    ):
        
        # fetch start
        start = time.perf_counter()

        # result
        result = func(*args, **kwargs)

        # fetch end
        end = time.perf_counter()

        print(
            f'{func.__name__}() : {end - start:.4f}s'
        )

        return result

    return __func
    