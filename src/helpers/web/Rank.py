# imports
from pathlib import Path

# functions
def Rank(
    posts : list[dict],
    requirement : int = 4
) -> list[dict]:
    
    # sort using 'ups' for best posts
    placeholder : list[dict] = sorted(
        posts,
        key=lambda post: post.get('ups', 0),
        reverse=True
    )

    # fetch best posts using 'requirement'
    placeholder : list[dict] = placeholder[:requirement]

    return placeholder