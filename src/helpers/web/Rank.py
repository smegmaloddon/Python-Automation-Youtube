# imports
from pathlib import Path

# functions
def __Score(
    post : dict
) -> float:

    upvotes : int = post.get(
        'ups', 0
    ) # fetch upvotes of post
    comments : int = post.get(
        'num_comments', 0
    ) # fetch number of comments
    ratio : float = post.get(
        'upvote_ratio', 1.0
    ) # fetch up /down vote ratio

    # create score
    score : float = upvotes *ratio

    # fetch posts with higher engagement
    score = score *(
        comments *2
    )

    return score

def Rank(
    posts : list[dict],
    requirement : int = 4
) -> list[dict]:
    
    # sort using 'ups' for best posts
    placeholder : list[dict] = sorted(
        posts,
        key=__Score, # lambda post: post.get('ups', 0), --old
        reverse=True
    )

    # fetch best posts using 'requirement'
    placeholder : list[dict] = placeholder[:requirement]

    return placeholder