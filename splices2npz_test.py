
import numpy as np
from moviepy.editor import *
import utils
from skimage import color
import librosa
import pandas as pd
import math

"""
    Test steps: takes a movie file, resizes, downsamples, does RGB2HSV color transformation and saves data in .npz,
        saves new video, loads that video for testing, loads .npz, converts from HSV2RGB, saves in restored video for 
        testing. 
        
    DONE: add emotion and text
"""


__author__ = "Gwena Cunha"


params = {
    'fps': 10,
    'root': utils.project_dir_name() + 'data_test/',
    'new_size': 100,
    'sr': 16000
}


def load_video(filename):
    # Load videos (fps = 30)
    clip = VideoFileClip(filename)

    # Resize to 100 x 100
    clip_resized = clip.resize(newsize=(params['new_size'], params['new_size']))
    print("clip: {}, resized: {}".format(clip.size, clip_resized.size))

    # Downsample
    downsampled_frames, new_filename = utils.downsample_video(clip_resized, params, save_downsampled=True)

    # Load video for testing
    clip = VideoFileClip(new_filename)
    num_frames = round(clip.fps * clip.duration)
    print("Number of frames: {}, size: {}, fps: {}".format(num_frames, clip.size, clip.fps))

    # Frames colour conversion
    frame_hsv_arr = []
    for frame in downsampled_frames:
        frame_hsv = color.rgb2hsv(frame)
        frame_hsv_arr.append(frame_hsv)
    return frame_hsv_arr


if __name__ == '__main__':

    # Load video
    params['root'] += 'BMI/'
    sample_idx = 0
    video_filename = "{}video_splices_3secs/{}.mp4".format(params['root'], sample_idx)
    frame_hsv_arr = load_video(video_filename)

    # Load corresponding audio
    audio, sr = librosa.load("{}audio_splices_3secs_16000_c1_16bits/{}.wav".format(params['root'], sample_idx), sr=params['sr'])
    print("audio: {}, sr: {}".format(np.shape(audio), sr))

    # Load corresponding emotion
    emotion_csv = pd.read_csv(params['root'] + "intended_1_splices_3secs.csv")
    emotion_data = emotion_csv['emotion']
    emotion = emotion_data[sample_idx]
    print("emotion: {}, {}: {}".format(np.shape(emotion_data), sample_idx, emotion))

    # Load corresponding text
    text_csv = pd.read_csv(params['root'] + "text_splices_3secs.csv")
    text_data = text_csv['text']
    text = text_data[sample_idx]
    text = "" if math.isnan(text) else text
    print("text: {}, {}: {}".format(np.shape(text_data), sample_idx, text))

    # Save in .npz
    save_npz_filename = '{}video_feats_HSL.npz'.format(params['root'])
    # np.savez_compressed(save_npz_filename, HSL_data=frame_hsv_arr, audio=audio)
    np.savez_compressed(save_npz_filename, HSL_data=frame_hsv_arr, audio=audio, emotion=emotion, text=text)

    # Load from .npz, convert to RGB and save in recovered (movie)
    data = np.load(save_npz_filename)
    hsl_frames = data['HSL_data']
    frame_rgb_arr = []
    for frame in hsl_frames:
        frame_rgb = color.hsv2rgb(frame)
        frame_rgb_arr.append(frame_rgb * 255)

    scaled = np.ascontiguousarray(frame_rgb_arr)
    clip = ImageSequenceClip(np.array(scaled), fps=params['fps'])
    new_filename = '{root}1_{new_size}x{new_size}_{fps}fps_recovered.mp4'.format(root=params['root'],
                                                                                 new_size=params['new_size'],
                                                                                 fps=params['fps'])
    clip.write_videofile(new_filename, fps=params['fps'])

    # Load audio and save as recovered
    audio = data['audio']
    new_filename = '{root}BMI_1_recovered.wav'.format(root=params['root'])
    librosa.output.write_wav(new_filename, y=audio, sr=sr)
