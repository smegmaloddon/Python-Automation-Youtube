# voice /tiktok
import tiktoktts
from pathlib import Path

# constants
PLACEHOLDER_VOICE     = 'en_us_006' # voice

# run func
def Run( 
    
    text : str = None,
    voice : str = PLACEHOLDER_VOICE,

    output : Path = None
) -> None:

    # init client
    client : object = tiktoktts.TTS(
        output_file_name=output,
        voice=voice
    )

    # create
    client.New(
        text=text,
        voice=voice
    )