# imports
import edge_tts as Voice
import asyncio
from pathlib import Path

# constants
PLACEHOLDER_VOICE     = 'en-AU-NatashaNeural' # placeholder voice
PLACEHOLDER_RATE      = '+0%' # rate of voice
PLACEHOLDER_PITCH     = '+0Hz' # pitch of voice
PLACEHOLDER_VOLUME    = '+0%' # volume of voice

# to create voice .wav file
def Run(
    
    text : str = None,
    voice : str = PLACEHOLDER_VOICE,
    rate : str = PLACEHOLDER_RATE,
    pitch : str = PLACEHOLDER_PITCH,
    volume : str = PLACEHOLDER_VOLUME,

    output : Path = None
) -> None:
    
    async def Communicate(
    ) -> None:
        
        # init class
        communication : object = Voice.Communicate(
            text=text,
            voice=voice,
            rate=rate,
            pitch=pitch,
            volume=volume
        )

        # save to file and delay thread
        await communication.save(
            str(
                output
            )
        )

    # halts thread
    asyncio.run(
        main=Communicate()
    )