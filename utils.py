import os
from moviepy.editor import ImageSequenceClip
import numpy as np
from collections import defaultdict


def project_dir_name():
    project_dir = os.path.abspath(os.path.dirname(__file__)) + "/"
    return project_dir


def ensure_dir(file_path):
    if not os.path.exists(file_path):
        os.mkdir(file_path)


def get_file(root_dir, filename):
    try:
        full_filename = root_dir + filename
        if os.path.isfile(full_filename):
            return open(full_filename, 'r')
        else:
            raise FileNotFoundError("Exception: file not found!")
    except FileNotFoundError as error:
        print(error)
        return None


def downsample_video(clip_resized, params, save_downsampled=False, verbose=False):
    """
        Downsample video files from 30 fps to 10 fps
    """

    num_frames = round(clip_resized.fps * clip_resized.duration)
    # print("Original number of frames: {}".format(num_frames))

    downsample = clip_resized.fps / params['fps']
    downsampled_frames = []
    counter = 0
    for i, frame in enumerate(clip_resized.iter_frames()):
        # We want 30 frames total, not 31
        # if i % downsample == 0 and counter < downsample * params['fps'] - 1:
        if i % downsample == 0 and counter < downsample * params['fps']:
            downsampled_frames.append(frame)
            counter += 1

    new_filename = '{root}1_{new_size}x{new_size}_{fps}fps.mp4'.format(root=params['root'],
                                                                       new_size=params['new_size'],
                                                                       fps=params['fps'])
    if save_downsampled:
        clip_downsampled = ImageSequenceClip(np.array(downsampled_frames), fps=params['fps'])
        clip_downsampled.write_videofile(new_filename, fps=params['fps'])
    return downsampled_frames, new_filename


def downsample_audio(audio_splices, old_fps, new_sr, seconds, verbose=False):
    """
        Downsample audio files from 44100 fps to 16000 fps
    """

    downsample = round(old_fps / new_sr)
    if verbose:
        print("Downsampling ratio: {}".format(downsample))
    audio_splices_down = defaultdict(list)
    for k, val in audio_splices.items():
        counter = 0
        for i, frame in enumerate(val):
            if i % downsample == 0 and counter < seconds * new_sr:
                audio_splices_down[k].append(frame)
                counter += 1

    if verbose:
        for k, val in audio_splices_down.items():
            print("{}, {}".format(k, len(val)))

    return audio_splices_down
