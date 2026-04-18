# imports
from pathlib import Path

# user imports
from src.utils.data import Temporary, Configuration

from src.helpers.web import Fetch, Filter, Rank

# constants
PLACEHOLDER_LENGTH : float = 256

# functions
def Run(
    archive : list[str],
    boolean : bool = False, # videos only?
    requirement : int = 8
) -> list[dict]:
    
    # verify 'archive'
    assert archive is not None and len(
        archive
    ) != 0

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
        posts : list[dict] = Fetch.Run(
            archive=archive
        )

        # filter towards videos & non-video posts
        posts : list[dict] = Filter.Videos(
            posts=posts,
            boolean=boolean
        )

        # filter depending on length
        if boolean is True:

            length : float = Temporary.Content.get(
                'web', {}
            ).get(
                'length', PLACEHOLDER_LENGTH
            )
            posts : list[dict] = Filter.Lengths(
                posts=posts,
                number=length
            )

        # filter duplicate videos
        posts : list[dict] = Filter.Duplicates(
            posts=posts,
            duplicates=duplicates
        )

        # fetch best posts & return
        posts : list[dict] = Rank.Rank(
            posts=posts
        )

        # fetch posts 'id' & merge
        temporary : list[str] = [

            post[
                'id'
            ] for post in posts
        ]
        duplicates = duplicates +temporary
        
        # merge tables
        saveables = saveables +posts

    # remove last items from list
    saveables = saveables[:requirement]

    # send filtered posts back
    return saveables