# imports
from pathlib import Path
import shutil
import requests

# user imports
from src.utils.data import Configuration, Temporary
from src.utils.io import Directory, JSON5

from src.services.web import Posts

# functions
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

def Run(
) -> None:
    
    # fetch posts
    # (pre-ranked, pre-video : bool)
    posts : list[dict] = __Posts()

    