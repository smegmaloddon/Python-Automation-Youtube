# imports
from pathlib import Path

# user imports
from src.utils.data import Configuration, Temporary
from src.utils.io import FFMPEG

# constants
COLORS : list[str] = [

    # gold
    "\#FFDC51",

    # silver
    "\#F1F1F1",

    # bronze
    "\#FF9152"
]
DEFAULT_PIXEL_VERTICAL_GAP : int = 26
DEFAULT_PIXEL_HORIZONTAL_GAP : int = 24
TEXT_GAP_ACROSS_PIXELS : int = 24
START_PIXEL_GAP : int = 48
FONT : str = 'C\\:/Windows/Fonts/arial.ttf'
FONT_SIZE : int = 48

# functions
def Run(
    path : Path,
    videos : list[Path]
) -> str:
    
    # init count
    count : int = len(
        videos
    )

    # init filters
    filters : list = []

    # fetch font
    font : str = Temporary.Content['video'].get(
        'font', FONT
    )
    if font != FONT:

        # if custom font, find & convert to ffmpeg safe path
        font : Path = Configuration.ASSETS /'fonts' /f'{font}'
        if not font.exists():

            raise FileNotFoundError(
                'Font.ttf file not found'
            )
        
        font : str = FFMPEG.ConvertPath(
            path=font
        )

    # loop through count
    for number in range(
        count
    ):
        
        # fetch color
        color = COLORS[number] if number <len(
            COLORS
        ) else 'white'

        # update number
        number = number +1

        # fetch pixels vertical
        pixels : int = Temporary.Content['video']['rank-config'].get(
            'vertical-pixels', DEFAULT_PIXEL_VERTICAL_GAP
        )

        # fetch vertical
        vertical : str = (
            number *pixels
        ) +START_PIXEL_GAP

        # fetch horizontal
        horizontal : int = Temporary.Content['video']['rank-config'].get(
            'horizontal-pixels', DEFAULT_PIXEL_HORIZONTAL_GAP
        )

        # fetch font size
        size : int = Temporary.Content['video'].get(
            'font-size', FONT_SIZE
        )

        # add filters
        filters.append(
            "drawtext="
            f"fontfile='{font}':"
            f"text='{number})':"
            f"x={horizontal}:y={vertical}:"
            f"fontsize=h/{size}:"
            f"fontcolor={color}:"
            f"borderw=2:"
            f"bordercolor=black:"
        )

    # create -vf string
    placeholder : str = ','.join(
        filters
    )
    return placeholder