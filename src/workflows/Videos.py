# imports
from pathlib import Path
import shutil
import requests

# user imports
from src.utils.data import Configuration, Temporary
from src.utils.io import Directory, JSON5, Download, FFMPEG
from src.utils import Threads

from src.helpers.video import Scene, Separators, Rank
from src.services.web import Posts
from src.services import Script
from src.services.upload import Upload
from src.services.video import Normalise, Trim, Merge, Speed, Ratio

# constants
PLACEHOLDER_LENGTH : list[float] = [256, 256]
PLACEHOLDER_MULTIPLIER : list[float] = [1, 1]
MAXIMUM_SCRIPT : int = 3

# functions
# used to fetch posts from www.reddit.com
def __Posts(
) -> list[dict]:
    
    # fetch & verify 'archive'
    archive : list[str] = Temporary.Content.get(
        'web', {}
    ).get(
        'archive', None
    )
    if archive is None:

        raise ValueError(
            'Variable \'archive\' is None'
        )

    # fetch & verify 'count'
    count : int = Temporary.Content.get(
        'video', {}
    ).get(
        'count', None
    )
    if count is None:

        raise ValueError(
            'Variable \'count\' is None'
        )
    
    # fetch short-form .v long-form config
    count : int = count[0] if Temporary.Shorts else count[1]

    # fetch & save posts to variable
    posts : list[dict] = Posts.Run(
        archive=archive,
        boolean=True,
        requirement=count
    )

    # return posts to main func()
    return posts

# func() to download retrieved posts
def __Download(
    posts : list[dict]
) -> None:
    
    # create directory & download videos
    path : Path = Configuration.TEMPORARY /'videos'
    Directory.Create(
        directory=path
    )

    # build arguments list[dict]
    arguments : list[dict] = []
    for number, post in enumerate(
        posts, 0
    ):

        # fetch .mpd url 
        url : str = post.get(
            'media', {}
        ).get(
            'reddit_video', {}
        ).get(
            'dash_url', None
        )

        # fallback
        if url is None:

            continue
        
        # add arguments to list
        arguments.append(

            {

                'url': url,
                'output': path /f'video-{number}.mp4'
            }
        )

    # thread func() & arguments
    # reset arguments[]
    Threads.Thread(
        func=Download.Playlist,
        items=arguments
    )

# func() to customise individual .mp4s
def __Filter(
    path : Path
) -> None:
    
    # init arguments
    arguments : list = []
    
    # fetch scene from video & trim
    timestamps : list[dict] = Scene.Run(
        videos=[
            video for video in path.iterdir()
        ], between=6
    )
    
    # thread the trim.py
    Threads.Thread(
        func=Trim.Run,
        items=timestamps
    )

    # fetch speed multiplier
    multiplier : float = Temporary.Content.get(
        'video', {} 
    ).get(
        'speed', PLACEHOLDER_MULTIPLIER
    )
    multiplier : float = multiplier[0] if Temporary.Shorts else multiplier[1]

    # build arguments[] for Speed.py
    for video in path.iterdir():

        arguments.append(

            {

                'path': video,
                'multiplier': multiplier,
                'ignore': True
            }
        )

    # run speed.py & reset arguments
    Threads.Thread(
        func=Speed.Speed,
        items=arguments
    )
    arguments = []

    # run ratio
    Ratio.Run(
        videos=[
            video for video in path.iterdir()
        ],
        ratio='9x16' if Temporary.Shorts else '16x9'
    )

# func() to merge all .mp4s
def __Merge(
    path : Path
) -> None:
    
    # create merge list[]
    mergeable : list[Path] = []
    useable : bool = Temporary.Content['video'].get(
        'separator-config', None
    ) != None

    # build mergeable list[]
    for number, video in enumerate(
        path.iterdir()
    ):
        
        mergeable.append(
            path /f'video-{number}.mp4'
        )

        # if not separators, continue
        if not useable:

            continue

        mergeable.append(
            Configuration.TEMPORARY /'separators' /f'separator-{number}.mp4'
        )

    # run merge.py
    Merge.Videos(
        videos=mergeable
    )

def __Save(
    posts : list[dict]
) -> None:
    
    # save posts
    saved : dict = JSON5.Read(
        path=Configuration.DATA /'posts.json5'
    )
    placeholder : list = saved.get(
        Temporary.Channel, []
    )

    # combine posts & save
    for post in posts:

        placeholder.append(
            post.get(
                'id', None
            )
        )

    saved[Temporary.Channel] = placeholder
    JSON5.Write(
        path=Configuration.DATA /'posts.json5',
        contents=saved
    )

def Run(
) -> None:
   
    # fetch posts --(pre-ranked, pre-video : bool)
    posts : list[dict] = __Posts()

    # save posts
    __Save(
        posts=posts
    )
    
    # download posts
    __Download(
        posts=posts
    )

    # videos path reference
    path : Path = Configuration.TEMPORARY /'videos'

    # create separator if required
    if Temporary.Content['video'].get(
        'separator-config', None
    ) != None:
        
        Separators.Run()

    # trim & select .etc
    __Filter(
        path=path
    )

    # merge & save filtered videos
    __Merge(
        path=path
    )

    # add ranking to video & save
    Rank.Run(
        posts=posts,
        videos=[
            video for video in path.iterdir()
        ]
    )

    # create prompt 
    prompt : str = str.format(
        Temporary.Content['script'].get(
            'upload-prompt', None
        ), posts
    )
    if not prompt:

        raise ValueError(
            'No prompt'
        )

    # create title & desciption
    dictionary : dict = None
    number : int = 0

    flag : bool = True
    while flag:

        if number >=MAXIMUM_SCRIPT:

            break

        dictionary = Script.Create(
            prompt=prompt
        )
        if dictionary != {} and dictionary != None:

            flag = False
            break

        number = number +1

    if flag:

        print(
            'error : script jsondecode'
        )
        return
    
    # upload to youtube
    Upload.Upload(
        title=dictionary.get(
            'Title', None
        ),
        description=dictionary.get(
            'Description', None
        )
    )