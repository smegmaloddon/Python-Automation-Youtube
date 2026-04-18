# imports
from pathlib import Path
import numpy

# user imports
from src.utils.data import Temporary, Configuration
from src.utils.io import FFMPEG, JSON5, Directory
from src.helpers.audio import ScoreAudio
from src.helpers.video import ScoreVideo

def FindBestMoment(audio, delta, motion, frame_seconds=0.25, window_seconds=4):

    min_len = min(len(audio), len(motion), len(delta))

    audio = numpy.array(audio[:min_len])
    motion = numpy.array(motion[:min_len])
    delta = numpy.array(delta[:min_len])

    # normalize safely
    audio = audio / (numpy.max(audio) + 1e-6)
    motion = motion / (numpy.max(motion) + 1e-6)
    delta = delta / (numpy.max(delta) + 1e-6)

    score = audio * 1.2 + motion * 0.7 + delta * 1.5
    score = numpy.convolve(score, numpy.ones(5)/5, mode='same')

    window = int(window_seconds / frame_seconds)
    pad = window // 2

    # remove edge bias
    score[:pad] = 0
    score[-pad:] = 0

    best_index = 0
    best_value = -1

    for i in range(len(score) - window):

        window_score = numpy.mean(score[i:i + window])  # IMPORTANT FIX

        if window_score > best_value:
            best_value = window_score
            best_index = i + pad

    start = max(0, best_index - pad) * frame_seconds
    end = min(len(score), best_index + pad) * frame_seconds

    # ensure minimum clip length
    if end - start < 2:
        end = start + 4

    return start, end

def Select(
    path : Path
) -> list[float]:
    
    audio, delta = ScoreAudio.Run(
        path=path
    )
    motion = ScoreVideo.Run(
        path=path
    )

    start, end = FindBestMoment(audio, delta, motion)

    return [start, end]