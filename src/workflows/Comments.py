# imports
from pathlib import Path
import random

# user imports
from src.services.web import Posts
from src.utils.data import Temporary, Configuration
from src.services.web import Comments

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

    # init count
    count : int = 8
    
    # fetch & save posts to variable
    posts : list[dict] = Posts.Run(
        archive=archive,
        boolean=False,
        requirement=count
    )

    post : dict = random.choice(
        seq=posts
    )

    # return posts to main func()
    return post

def __Comments(
    post : dict
) -> list[dict]:
    
    # init count (amount of comments)
    requirement : int = 8

    # fetch comments
    comments : list[dict] = Comments.Run(
        post=post,
        requirement=requirement
    )

    return comments

def Run(
) -> None:
    
    # fetch post
    post : dict = __Posts()

    # fetch comments from post
    comments : list[dict] = __Comments(
        post=post
    )

    print(comments)