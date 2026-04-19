# imports
from pathlib import Path

# user imports
from src.helpers.video.draw import Descriptions, Numbers, Hook
from src.utils.data import Configuration, Temporary
from src.utils.characters import UUID
from src.utils.io import FFMPEG, Directory

# functions
def Run(
    videos : list[Path],
    posts : list[dict],
    path : Path = (Configuration.TEMPORARY /'video.mp4')
) -> None:
    
    # add numbers to video & save
    ranks : list[str] = Numbers.Run(
        path=path,
        videos=videos
    )

    # add descriptions to video numbers & save
    filters : list[str] = Descriptions.Run(
        videos=videos,
        posts=posts
    )

    # combine filters
    filters.append(
        ranks
    )

    # create -vf string
    placeholder : str = ','.join(
        filters
    )

    # build output
    output : Path = Configuration.TEMPORARY /f'{UUID.Create()}.mp4'

    # build process
    process = [
        Configuration.FFMPEG,
        '-y',

        # 🔥 FIX TIMESTAMP + INPUT SAFETY
        '-fflags', '+genpts+discardcorrupt',
        '-avoid_negative_ts', 'make_zero',
        '-i', str(Configuration.TEMPORARY / 'video.mp4'),

        # 🔥 VIDEO FILTERS
        '-vf', placeholder,

        # 🔥 FORCE CLEAN FRAME PIPELINE
        '-fps_mode', 'cfr',
        '-r', '30',

        # 🔥 VIDEO ENCODING (stable + widely compatible)
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-crf', '18',
        '-pix_fmt', 'yuv420p',

        # 🔥 AUDIO (FULL RE-ENCODE, NO GLITCHES)
        '-c:a', 'aac',
        '-b:a', '192k',
        '-ar', '48000',
        '-ac', '2',

        # 🔥 AUDIO FIX (this is the key you were missing)
        '-af', 'aresample=async=1:first_pts=0',

        # 🔥 SYNC SAFETY (prevents drift / freeze audio issues)
        '-async', '1',

        # 🔥 FINAL MP4 FIX
        '-movflags', '+faststart',

        str(output)
    ]

    # run process
    FFMPEG.Run(
        process=process
    )

    # replace files
    Directory.Replace(
        old=Configuration.TEMPORARY /'video.mp4',
        new=output
    )

    # add hook
    Hook.Run()