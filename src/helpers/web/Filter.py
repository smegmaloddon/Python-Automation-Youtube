# imports
from pathlib import Path

# user imports
from src.utils.data import Configuration, Temporary

# functions
def Videos(
    posts : list[dict],
    boolean : bool = True
) -> list[dict]:
    
    # fetch limited to boolean
    placeholder : list[dict] = [

        post for post in posts if post[
            'is_video'
        ] == boolean
    ]

    return placeholder

def Duplicates(
    posts : list[dict],
    duplicates : list[str]
) -> list[dict]:
    
    # remove duplicates & cleanse posts
    placeholder : list[dict] = [

        post for post in posts if not post[
            'id'
        ] in duplicates
    ]

    return placeholder

def Lengths(
    posts : list[dict],
    number : float
) -> list[dict]:
    
    def __Fetch(
        post : dict
    ) -> float:
        
        # fetch duration & return
        duration : int = (
            post.get('media', {})
                .get('reddit_video', {})
                .get('duration', 0)
        )

        return duration
    
    # filter depending on length of videos
    placeholder : list[dict] = [

        post for post in posts if __Fetch(
            post=post
        ) <=number
    ]

    return placeholder