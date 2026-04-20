# imports
from pathlib import Path
import json

# functions
def Read(
    path : Path
) -> dict[any]:
    
    # verify 'path' is correct
    assert path is not None and path.exists(), 'Failed to pass verity checks'

    # init dictionary
    dictionary : dict[any] = {}

    # open file & read contents to dictionary
    with open(
        file=path,
        mode='r', # 'r' mode to not overwrite /or modify
        encoding='utf-8'
    ) as file:
        
        dictionary = json.load(
            file
        )
        file.close()

    return dictionary

def Write(
    path : Path,
    contents : dict[any]
) -> None:
    
    # verify parameters are correct
    assert path is not None, 'Parameters do not fit the requirements'

    # open file & save
    with open(
        file=path,
        mode='w',
        encoding='utf-8'
    ) as file:
        
        json.dump(
            contents, file, indent=4
        )
        file.close()