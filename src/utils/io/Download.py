# imports
import requests
from pathlib import Path

# user imports
from src.utils.io import FFMPEG
from src.utils.data import Configuration, Temporary

from src.services.video import Normalise

# functions
def Playlist(
    url : str, # .mpd file url
    output : Path
) -> None:
    
    # build process[]
    process : list = [
        Configuration.FFMPEG,
        '-i', url,
        '-c', 'copy',
        str( 
            output
        )
    ]

    # run ffmpeg
    FFMPEG.Run(
        process=process
    )

    # normalise video
    Normalise.Normalise(
        path=output
    )