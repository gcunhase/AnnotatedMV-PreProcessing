import numpy as np
from librosa.output import write_wav
from moviepy.editor import VideoFileClip
from ImageSequenceClip import ImageSequenceClip
from skimage import color
import utils
import os
from collections import defaultdict

"""
    Add audio to video without audio
"""

__author__ = "Gwena Cunha"


def normalize(arr, min=0, max=1):
    return min + (max - min) * (arr - np.amin(arr)) / (np.amax(arr) - np.amin(arr))


#root_dir = '../data/add_audio_to_video/cognimuse_10secs/'
root_dir = '../data/add_audio_to_video/deap_3secs/'
recovered_dir = '{}recovered_videos-mp4_500x500/'.format(root_dir)
corrected_videos_dir = '{}corrected_with_audio/'.format(root_dir)

emotion_type_arr = ['positive']  #, 'negative']
emotion_type_short_arr = ['pos']  #, 'neg']
sample_arr = [1]  #, 2, 3, 4, 5]
for emotion_type, emotion_type_short in zip(emotion_type_arr, emotion_type_short_arr):
    for sample in sample_arr:
        video_dir_filename = '{}{}{}.mp4'.format(recovered_dir, emotion_type_short, sample)
        if emotion_type_short == 'neg':
            save_dir_path = '{}{}/N{}/'.format(corrected_videos_dir, emotion_type, sample)
        else:
            save_dir_path = '{}{}/P{}/'.format(corrected_videos_dir, emotion_type, sample)
        utils.ensure_dir(save_dir_path)

        clip = VideoFileClip(video_dir_filename)
        frames = []
        for i, frame in enumerate(clip.iter_frames()):
            frames.append(frame)

        clip = ImageSequenceClip(np.array(frames), fps=10)
        for data_type in ['baseline', 'target', 'ours_scene2wav']:
            filename_audio = '{}{}{}_{}.wav'.format(save_dir_path, emotion_type_short, sample, data_type)
            filename_video = '{}{}{}_{}.avi'.format(save_dir_path, emotion_type_short, sample, data_type)
            # Export video with audio
            #   codec = png for avi, mpeg4 or libx264 for mp4
            clip.write_videofile(filename_video, fps=10, codec='png', audio_fps=16000, audio=filename_audio)
