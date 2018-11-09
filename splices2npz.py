
import numpy as np
from moviepy.editor import *
import utils
from skimage import color
import librosa
import glob
from natsort import natsorted
import pandas as pd
import math


"""
    Pre-processes data considering already spliced video and audio only
    Synchronize video and audio
    
    TODO: add emotion and text
"""


__author__ = "Gwena Cunha"


params = {
    'fps': 10,
    # 'root': '/media/ceslea/DATA/VideoEmotion/DataWithEmotionTags_noText_correctedAudio_hsio/',
    'root': utils.project_dir_name() + 'data_test/',
    'new_size': 100,
    'sr': 16000,
    'audio_len': 48000,
    'results_dir': utils.project_dir_name() + 'data_test/'
}


def load_video(filename):
    # Load videos (fps = 30)
    clip = VideoFileClip(filename)

    # Resize to 100 x 100
    clip_resized = clip.resize(newsize=(params['new_size'], params['new_size']))

    # Downsample
    downsampled_frames, _ = utils.downsample_video(clip_resized, params, save_downsampled=False)

    # Frames colour conversion
    frame_hsv_arr = []
    for frame in downsampled_frames:
        frame_hsv = color.rgb2hsv(frame)
        frame_hsv_arr.append(frame_hsv)
    return frame_hsv_arr


def process_audio(audio_arr, pad_size=48000):
    # Check audio files size and pad
    audio_arr_padded = []
    for audio in audio_arr:
        f_length = len(audio)
        if f_length < pad_size:
            audio_pad = np.zeros([pad_size])
            audio_pad[0:f_length] = audio
            audio_arr_padded.append(audio_pad)
        else:
            audio_arr_padded.append(audio[0:pad_size])
    return audio_arr_padded


def save_npz(videos, type='train'):
    print(videos)
    frame_hsv_arr, audio_arr, emotion_arr, text_arr = [], [], [], []
    for v in videos:
        # data_path = params['root'] + "Video_emotion_" + v + "_noText/"
        data_path = params['root'] + v + "/"

        # Load video and corresponding audio
        # video_path = data_path + "selected_avi/*.avi"
        video_path = data_path + "video_splices_3secs/*.mp4"
        video_filenames = glob.glob(video_path)
        video_filenames = natsorted(video_filenames)

        # Load corresponding audio
        # audio_path = data_path + "selected_wav_eq/*.wav"
        audio_path = data_path + "audio_splices_3secs_16000_c1_16bits/*.wav"
        audio_filenames = glob.glob(audio_path)
        audio_filenames = natsorted(audio_filenames)

        # Load corresponding emotion
        emotion_csv = pd.read_csv(data_path + "intended_1_splices_3secs.csv")
        emotion_data = emotion_csv['emotion']

        # Load corresponding text
        text_csv = pd.read_csv(data_path + "text_splices_3secs.csv")
        text_data = text_csv['text']

        for v_filename, a_filename, emotion, text in zip(video_filenames, audio_filenames, emotion_data, text_data):
            text = "" if isinstance(text, float) else text
            print('Video: {}, audio: {}, emotion: {}, text: {}'.
                  format(v_filename.split('/')[-1], a_filename.split('/')[-1], emotion, text))
            frame_hsv_arr.append(load_video(v_filename))
            audio, _ = librosa.load(a_filename, sr=params['sr'])
            audio_arr.append(audio)
            emotion_arr.append(emotion)
            text_arr.append(text)

    # Transpose from (N, 30, 100, 100, 3) to (N, 30, 3, 100, 100)
    frame_hsv_arr_transpose = np.transpose(frame_hsv_arr, (0, 1, 4, 2, 3))
    # Pad audio to audio_len if not already
    audio_arr_padded = process_audio(audio_arr, pad_size=params['audio_len'])
    print("Shapes - video: {}/{}, audio: {}/{}".format(np.shape(frame_hsv_arr), np.shape(frame_hsv_arr_transpose),
                                                       np.shape(audio_arr), np.shape(audio_arr_padded)))

    # Save in .npz
    utils.ensure_dir(params['results_dir'])
    save_npz_filename = '{}video_feats_HSL_{}fps_{}.npz'.format(params['results_dir'], params['fps'], type)
    np.savez_compressed(save_npz_filename, HSL_data=frame_hsv_arr_transpose, audio=audio_arr, emotion=emotion_arr,
                        text=text_arr)

    save_npz_filename = '{}video_feats_HSL_{}fps_pad_{}.npz'.format(params['results_dir'], params['fps'], type)
    np.savez_compressed(save_npz_filename, HSL_data=frame_hsv_arr_transpose, audio=audio_arr_padded,
                        emotion=emotion_arr, text=text_arr)


if __name__ == '__main__':
    # videos = ['test']
    # save_npz(videos, type='test')

    videos = ['BMI', 'CHI', 'FNE', 'GLA', 'LOR']
    save_npz(videos, type='train')

    videos = ['CRA', 'DEP']
    save_npz(videos, type='test')
