# imports
from pathlib import Path
import time

# user imports
from src.utils.data import Temporary, Configuration
from src.utils.io import JSON5, Directory

from src.services.upload import Authorisation
from src.workflows import Videos, Comments

# functions
def __Temporary(
    channel : str = None
) -> None:
    
    # verify 'channel'
    assert channel is not None, 'Channel must be valid'

    # fetch .json5
    dictionary : dict = JSON5.Read(
        path=Configuration.DATA /'configuration.json5'
    )

    # save new variables & verify
    Temporary.Channel = channel
    Temporary.Content = dictionary.get(
        channel, None
    )
    assert Temporary.Content is not None, 'Channel does not exist'

def Run(
    channel : str
) -> None:
    
    # error handling
    try:

        # cleanse temp/ file
        Directory.Cleanse(
            folder=Configuration.TEMPORARY
        )
        
        # fetch temporary data for channel
        __Temporary(
            channel=channel
        )

        Authorisation.Run()

        # run videos for debug
        Videos.Run()
    except:

        pass

# entry
if __name__ == '__main__':

    timestamp : float = time.time()
    Run(
        channel='placeholder-channel'
    )
    Run(
        channel='instant-karma-personified'
    )
    Run(
        channel='sports-clips-channel'
    )

    print(
        f'timestamp : {time.time() -timestamp}'
    )