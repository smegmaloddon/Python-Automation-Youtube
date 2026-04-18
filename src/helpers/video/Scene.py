# imports
from pathlib import Path
import numpy
import librosa
import random
import cv2
import math

# user imports
from src.utils.data import Configuration, Temporary
from src.utils.io import FFMPEG
from src.utils import Math

def __FetchAudio(
    path : Path,
    duration : float = 0.25
) -> list:
    
    y, sr = librosa.load(
        path=path
    )
    
    size : int = int(sr * duration)

    energies = []

    for number in range(0, len(y), size):
        
        chunk = y[number:number + size]
        if len(chunk) == 0:
            continue

        calculation : float = numpy.sqrt(numpy.mean(chunk ** 2))
        energies.append(calculation)

    return energies


def __FetchMotion(
    path : Path,
    duration : float = 0.25
) -> list:

    cap = cv2.VideoCapture(str(path))

    fps : float = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 30.0

    step : int = max(1, int(fps * duration))

    motion_scores : list = []

    frame_idx : int = 0

    ret, prev = cap.read()
    if not ret:
        cap.release()
        return []

    prev_gray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)
    prev_gray = cv2.GaussianBlur(prev_gray, (5, 5), 0)

    while True:

        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx % step != 0:
            frame_idx += 1
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)

        diff = cv2.absdiff(prev_gray, gray)

        _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

        motion : float = thresh.mean()
        motion_scores.append(motion)

        prev_gray = gray
        frame_idx += 1

    cap.release()

    return motion_scores


def Run(
    videos : list = None,
    between : float = 4
) -> None:
    
    assert videos is not None and len(videos) != 0

    placeholder : list = []

    for path in videos:

        length : float = FFMPEG.Length(path=path)

        boolean : bool = FFMPEG.Audio(path=path)

        if not boolean:

            start : float = random.uniform(0, max(0.1, length - between * 2))
            end : float = start + (between * 2)

            placeholder.append({
                'path': path,
                'start': start,
                'end': end 
            })

            continue

        FFMPEG.ExtractAudio(
            path=path,
            output=Configuration.TEMPORARY /'audio-extract.wav'
        )

        energies : list[float] = __FetchAudio(
            path=Configuration.TEMPORARY /'audio-extract.wav'
        )

        motion = __FetchMotion(path)

        min_len = min(len(energies), len(motion))
        if min_len == 0:
            continue

        energies = numpy.array(energies[:min_len])
        motion = numpy.array(motion[:min_len])

        eps = 1e-6

        audio_norm = energies / (numpy.max(energies) + eps)
        motion_norm = motion / (numpy.max(motion) + eps)

        combined = audio_norm + motion_norm

        delta = numpy.diff(audio_norm, prepend=audio_norm[0])
        combined += delta * 0.5

        kernel = numpy.ones(5) / 5
        combined = numpy.convolve(combined, kernel, mode='same')

        best_index = int(numpy.argmax(combined))

        # 🔥 FIX: convert chunk index → seconds properly
        frame_seconds = 0.25
        best_time = best_index * frame_seconds

        start : float = Math.Clamp(
            number=best_time - between,
            lowest=0.0,
            highest=length
        )

        end : float = Math.Clamp(
            number=best_time + between,
            lowest=0.0,
            highest=length
        )

        placeholder.append(
            {
                'path': path,
                'start': start,
                'end': end
            }
        )

    extract : Path = Configuration.TEMPORARY / 'audio-extract.wav'
    if extract.exists():
        extract.unlink()

    return placeholder