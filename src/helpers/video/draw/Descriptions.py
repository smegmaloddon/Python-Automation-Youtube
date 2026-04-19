# imports
from pathlib import Path
import random

# user imports
from src.utils.data import Configuration, Temporary
from src.utils.io import FFMPEG
from src.utils.characters import Keywords

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
    posts : list[dict],
    videos : list[Path]
) -> str:
    
    # fetch ranking numbers, != 1
    numbers : list[int] = [
        number for number, _ in enumerate(
            videos, 1
        ) if number != 1
    ]

    # fetch font size
    size : int = Temporary.Content['video'].get(
        'font-size', FONT_SIZE
    )

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

    # fetch separator length
    separator : dict = Temporary.Content['video'].get(
        'separator-config', None
    )
    separator : float = separator.get(
        'length', 0
    ) if separator != None else 0 # fetch separator length with fallback

    # init filters & duration
    filters : list = []
    duration : float = 0

    # fetch total length
    total : float = FFMPEG.Length(
        path=Configuration.TEMPORARY /'video.mp4'
    )

    # loop through videos
    for number, video in enumerate(
        videos
    ):
        
        # fetch rank & remove
        rank : int = 1

        # check that it shouldn't use rank 1
        if len(
            numbers
        ) != 0:
            
            rank : int = random.choice(
                seq=numbers
            )
            numbers.remove(
                rank
            )        

        # fetch keywords & keyword
        keywords : list = Keywords.Keywords(
            text=posts[number]['title']
        )
        keyword : str = keywords[0] if len(
            keywords
        ) >=1 else 'huh, hey there!'

        # fetch color
        color = COLORS[rank -1] if rank -1 <len(
            COLORS # rank -1 since rank is integer too high 
        ) else 'white'

        # fetch vertical
        vertical : int = Temporary.Content['video']['rank-config'].get(
            'vertical-pixels', DEFAULT_PIXEL_VERTICAL_GAP
        )
        vertical = (
            rank *vertical
        ) +START_PIXEL_GAP # add start pixel position2

        # fetch horizontal
        horizontal : int = Temporary.Content['video']['rank-config'].get(
            'horizontal-pixels', DEFAULT_PIXEL_HORIZONTAL_GAP
        )

        # fetch gap
        gap : int = Temporary.Content['video']['rank-config'].get(
            'horizontal-pixel-gap', TEXT_GAP_ACROSS_PIXELS
        )

        # fetch length of video
        length : float = FFMPEG.Length(
            path=video
        )

        # add filters
        filters.append(
            "drawtext="
            f"fontfile='{font}':"
            f"text='{keyword.upper()}':"
            f"x={horizontal +gap} + 2*sin(10*(t-{duration})):"
            f"y={vertical} + 1*sin(12*(t-{duration})):" # wobble effect
            f"fontcolor={color}:"
            f"borderw=2:"
            f"bordercolor=black:"
            # f"box=1:" # overlaps too much & creates z-index issues
            # f"boxcolor=black@0.25:"
            # f"boxborderw=14:"

            # 🔥 animation block (0.4s pop)
            f"fontsize='if(lt(t,{duration}+0.4),"
            f"h/{size}*pow((t-{duration})/0.4,0.35),"
            f"h/{size})':"

            f"enable='between(t,{duration},{total})'"
        )

        # set duration
        duration = duration +length +separator

    # return filters
    return filters