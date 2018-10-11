import os
from moviepy.editor import ImageSequenceClip
import numpy as np


def project_dir_name():
    project_dir = os.path.abspath(os.path.dirname(__file__)) + "/"
    return project_dir


def ensure_dir(file_path):
    if not os.path.exists(file_path):
        os.mkdir(file_path)


def downsample_video(clip_resized, params, save_downsampled=False):
    num_frames = round(clip_resized.fps * clip_resized.duration)
    print("Number of frames: {}".format(num_frames))

    downsample = clip_resized.fps / params['fps']
    downsampled_frames = []
    counter = 0
    for i, frame in enumerate(clip_resized.iter_frames()):
        # We want 30 frames total, not 31
        if i % downsample == 0 and counter < downsample * params['fps'] - 1:
            downsampled_frames.append(frame)
            counter += 1

    new_filename = '{root}1_{new_size}x{new_size}_{fps}fps.mp4'.format(root=params['root'],
                                                                       new_size=params['new_size'],
                                                                       fps=params['fps'])
    if save_downsampled:
        clip_downsampled = ImageSequenceClip(np.array(downsampled_frames), fps=params['fps'])
        clip_downsampled.write_videofile(new_filename, fps=params['fps'])
    return downsampled_frames, new_filename
