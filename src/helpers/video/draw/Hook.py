# imports
from pathlib import Path
import random

# user imports
from src.utils.data import Configuration, Temporary
from src.utils.io import Directory, FFMPEG
from src.utils.characters import UUID, Hex

# constants
HOOKS_LIST: list[str] = [
    'Wait till #1',
    '#1 is insane',
    'Watch #1 carefully',
    '#1 will shock you',
    'Starting from #5',
    '#3 is crazy',
    '#2 gets worse',
    '#1 is next level',
    'Don’t skip #2',
    'Wait for #1',
    'Ending changes everything',
    'Stay till end',
    'It escalates fast',
    'Final one hits hard',
    'Only #1 matters',
    'Most miss #1',
    'Watch till end',
    'Last one wins',
    'This is insane',
    'You missed #1',
    'Ranking from worst',
    'Best saved for #1',
    'Keep watching #1',
    'Top one is wild',
    'Final is shocking',
    'You wont expect #1',
    'Wait for ending',
    'This is crazy',
    'Don’t miss last',
    'Last one best',
    'Number one hits',
    'Watch carefully #1',
    'Ending goes hard',
    'This gets intense',
    'Only legends reach #1',
    'Last one insane',
    'Wait until #1'
]
FONT : str = 'C\\:/Windows/Fonts/arial.ttf'
FONT_SIZE : int = 48

def Run(
) -> None:
    
    # fetch random hook
    text : str = random.choice(
        seq=HOOKS_LIST
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

    # build output
    output : Path = Configuration.TEMPORARY /f'{UUID.Create()}.mp4'

    # open & write to file --> bypass ffmpeg issues
    with open(
        file=Configuration.TEMPORARY /'title.txt',
        mode='w',
        encoding='utf-8'
    ) as file:
        
        file.write(
            text.upper()
        )
        file.close()

    # fetch path
    path : str = FFMPEG.ConvertPath(
        path=Configuration.TEMPORARY /'title.txt'
    )

    # init start & end
    start : float = 0
    end : float = 5

    # colors & fetch color
    colors : list[str] = [

        "#3CFF42", "#FF5050", "#5D68FF", "#FF4AF0", "#FFFB00"
    ]
    color : str = random.choice(
        seq=colors
    )

    # create accent
    accent : str = Hex.Darken(
        color=color,
        factor=0.5
    )

    # create animation
    animation: str = (
        f"drawtext="
        f"fontfile='{font}':"
        f"textfile='{path}':"
        f"fontcolor='{color}':"
        f"fontsize=w/16:"
        f"box=1:"
        f"boxcolor={color}@0.9:"
        f"boxborderw=14:"
        f"x=(w-text_w)/2:"
        f"y=(h*0.65)-th/2-20*sin(t*2):"
        f"borderw=5:bordercolor='{accent}':"
        f"alpha='if(lt(t,{end}-0.5),1,if(lt(t,{end}),({end}-t)/0.5,0))':"
        f"enable='between(t,{start},{end})'"
    )
        
    # fetch process
    process : list = [
        Configuration.FFMPEG,
        '-i', str(Configuration.TEMPORARY /'video.mp4'),
        '-vf',
        animation,
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-crf', '23',
        '-c:a', 'aac',
        '-b:a', '192k',
        str(
            output
        )
    ]

    FFMPEG.Run(
        process=process
    )

    # replace files
    Directory.Replace(
        old=Configuration.TEMPORARY /'video.mp4',
        new=output
    )