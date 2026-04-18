# imports
from pathlib import Path
import shutil

# user imports
from src.utils.data import Configuration, Temporary
from src.utils.io import FFMPEG, Directory
from src.utils.characters import UUID
from src.services.video import Trim, Ratio, Normalise

# constants
DEFAULT_START : float = 1

# create separator & neccessary components
def Run(
) -> None:
    
    # fetch configuration & variables
    configuration : dict = Temporary.Content['video'].get(
        'separator-config', {}
    )
    
    # fetch video & check it exists
    video : str = configuration.get(
        'video', None
    )
    video : Path = Configuration.ASSETS /'videos' /'separators' /f'{video}'

    if not video.exists():

        raise FileNotFoundError()
    
    # copy file to temporary
    file : Path = Configuration.TEMPORARY /'separator.mp4'
    shutil.copy2(
        str(video),
        str(file)
    )

    # normalise
    Normalise.Normalise(
        path=file
    )
    
    # fetch length & trim
    length : float = configuration.get(
        'length', 0.75
    )
    Trim.Run(
        path=file,
        start=DEFAULT_START,
        end=length +DEFAULT_START
    )

    # detect if shorts & format aspect ratio
    Ratio.Run(
        videos=[file],
        ratio='9x16' if Temporary.Shorts else '16x9'
    )

    # create separator directory
    Directory.Create(
        directory=Configuration.TEMPORARY /'separators'
    )

    # create separators
    for number, video in enumerate(
        (
            Configuration.TEMPORARY /'videos'
        ).iterdir()
    ):
        
        # copy & rename
        shutil.copy2(
            str(
                file
            ),
            str(
                Configuration.TEMPORARY /'separators' /f'separator-{number}.mp4'
            )
        )
