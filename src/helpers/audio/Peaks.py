# imports
from pathlib import Path
import librosa
import numpy

# user imports
from src.utils.io import FFMPEG
from src.utils.data import Configuration, Temporary

# functions
def Run(
    path : Path,
    frame : float = 0.25
) -> list:
    
    # create audio-extract.wav
    file : Path = Configuration.TEMPORARY /'audio-extract.wav'
    FFMPEG.ExtractAudio(
        path=path,
        output=file
    )
    
    # load audio
    __y, __sr = librosa.load(
        file,
        sr=None, # keep original sample rate
        mono=True
    )

    # samples per chunk
    size : int = int(
        __sr *frame
    )

    # init audio list
    audio : list = []

    # split into chunks
    for number in range(
        0,
        len(
            __y
        ),
        size
    ):

        chunk = __y[
            number:number +size
        ]
        if len(
            chunk
        ) == 0:
            
            continue

        # RMS = loudness
        value = float(
            numpy.max(
                numpy.abs(chunk)
            )
        )

        # 🔥 ignore quiet chunks
        if value <= 0.08:
            value = 0.0

        audio.append(
            value
        )

    # delta == change between frames 
    delta = numpy.diff(
        audio,
        prepend=audio[0]
    )

    return audio, delta