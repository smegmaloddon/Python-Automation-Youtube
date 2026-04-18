# imports
import requests
from pathlib import Path

# user imports
from src.utils.io import FFMPEG

# functions
def Playlist(
    url : str, # .mpd file url
    output : Path
) -> None:
    
    print(output)