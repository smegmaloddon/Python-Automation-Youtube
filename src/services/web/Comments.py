# imports
from pathlib import Path
import random

# user imports
from src.utils.data import Configuration, Temporary
from src.helpers.web import Rank, Filter, Fetch

# functions
def Run(
    post : dict = None,
    requirement : int = 8
) -> None:
    
    # verify 'post'
    assert post is not None, 'Post is None'

    # init saveables & flag
    saveables : list[dict] = []
    duplicates : list[str] = []
    flag : bool = True

    # init iteration
    while flag:

        # if requirements are met, end iteration
        if len(
            saveables
        ) >=requirement:
            
            flag = False
            break

        # fetch raw posts
        comments : list[dict] = Fetch.Comments(
            post=post
        )

        # filter towards videos & non-video posts
        comments : list[dict] = Filter.Videos(
            posts=comments,
            boolean=False
        )

        # filter duplicate comments
        comments : list[dict] = Filter.Duplicates(
            posts=comments,
            duplicates=duplicates
        )

        # fetch best posts & return
        comments : list[dict] = Rank.Rank(
            posts=comments
        )

        # fetch posts 'id' & merge
        temporary : list[str] = [

            post[
                'id'
            ] for post in comments
        ]
        duplicates = duplicates +temporary
        
        # merge tables
        saveables = saveables +comments

    # remove last items from list
    saveables = saveables[:requirement]

    # send filtered posts back
    return saveables