
import numpy as np
from moviepy.editor import *
import utils
from skimage import color
import librosa
import glob
from natsort import natsorted
import pandas as pd
import math
from scipy.io.wavfile import read


"""
    Pre-processes data considering already spliced video and audio only
    Synchronize video and audio
    
    TODO: add emotion and text
"""


__author__ = "Gwena Cunha"


params = {
    'fps': 10,
    # 'root': '/media/ceslea/DATA/VideoEmotion/DataWithEmotionTags_noText_correctedAudio_hsio/',
    'root': utils.project_dir_name() + 'data/cognimuse_multimodal_robust_bert/',
    'new_size': 100,
    'sr': 16000,
    'audio_len': 48000,
    'results_dir': utils.project_dir_name() + 'data/cognimuse_multimodal_robust_bert/',
    'seconds': 10,
}


def load_video(filename, params_substitute=None):
    # To use in external scripts
    if params_substitute is not None:
        params = params_substitute
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


def save_npz(videos, type='train', audio_type='instrumental', emotion_dim='1D', emotion_root='emotion/',
             text_root='text/', data_type='with_incomplete', include_audio=True):
    """

    :param videos:
    :param type:
    :param audio_type:
    :param emotion_dim:
    :param emotion_root:
    :param text_root:
    :param data_type: related to text, whether to include samples with empty text (incomplete) or containing some text
        (complete). Options =['with_incomplete', 'only_complete'].
    :param include_audio:
    :return:
    """
    print(videos)
    seconds = params['seconds']
    frame_hsv_arr, audio_arr, emotion_arr, text_arr = [], [], [], []
    for v in videos:
        # data_path = params['root'] + "Video_emotion_" + v + "_noText/"
        data_path = params['root'] + v + "/"

        # Load video and corresponding audio
        # video_path = data_path + "selected_avi/*.avi"
        video_path = data_path + "video_splices_{}secs/*.mp4".format(seconds)
        video_filenames = glob.glob(video_path)
        video_filenames = natsorted(video_filenames)

        # Load corresponding audio
        # audio_path = data_path + "selected_wav_eq/*.wav"
        if audio_type == 'orig':
            audio_path = data_path + "audio_splices_{}secs_16000_c1_16bits/*.wav".format(seconds)
        else:
            audio_path = data_path + "audio_splices_{}secs_wav2mid2wav_16000_c1_16bits/*.wav".format(seconds)
        audio_filenames = glob.glob(audio_path)
        audio_filenames = natsorted(audio_filenames)

        # Load corresponding emotion
        emotion_csv = pd.read_csv(data_path + "{}intended_1_{}_splices_{}secs.csv".format(emotion_root, emotion_dim, seconds))
        emotion_data = emotion_csv['emotion']

        # Load corresponding text
        text_csv = pd.read_csv(data_path + "{}text_splices_{}secs.csv".format(text_root, seconds))
        text_data = text_csv['text']

        for v_filename, a_filename, emotion, text in zip(video_filenames, audio_filenames, emotion_data, text_data):
            text = "" if isinstance(text, float) else text
            if data_type == 'with_incomplete' or (data_type == 'only_complete' and len(text) != 0):
                print('Video {}: {}, audio: {}, emotion: {}, text: {}'.
                      format(v, v_filename.split('/')[-1], a_filename.split('/')[-1], emotion, text))
                frame_hsv_arr.append(load_video(v_filename))
                # audio, _ = librosa.load(a_filename, sr=params['sr'])  # float numbers
                rate, audio = read(a_filename)  # int numbers -> necessary for SAMPLERNN and CNNSEQ2SEQ models
                # print(rate)  # 16000 OKAY
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
    data_type_prefix = '_' + data_type
    save_npz_filename_root = '{}video_feats_HSL_{}fps_{}secs'.format(params['results_dir'], params['fps'], seconds)
    if include_audio:
        if audio_type == 'orig':
            save_npz_filename = save_npz_filename_root + '_origAudio_intAudio_{}_{}{}.npz'.format(type, emotion_dim, data_type_prefix)
        else:
            save_npz_filename = save_npz_filename_root + '_intAudio_{}_{}{}.npz'.format(type, emotion_dim, data_type_prefix)
        np.savez_compressed(save_npz_filename, HSL_data=frame_hsv_arr_transpose, audio=audio_arr, emotion=emotion_arr,
                            text=text_arr)
    else:
        save_npz_filename = save_npz_filename_root + '_{}_{}{}_noAudio.npz'.format(type, emotion_dim, data_type_prefix)
        np.savez_compressed(save_npz_filename, HSL_data=frame_hsv_arr_transpose, emotion=emotion_arr, text=text_arr)

    # Padded audio
    if include_audio:
        if audio_type == 'orig':
            save_npz_filename = save_npz_filename_root + '_origAudio_intAudio_pad_{}_{}{}.npz'.format(type, emotion_dim, data_type_prefix)
        else:
            save_npz_filename = save_npz_filename_root + '_intAudio_pad_{}_{}{}.npz'.format(type, emotion_dim, data_type_prefix)
        np.savez_compressed(save_npz_filename, HSL_data=frame_hsv_arr_transpose, audio=audio_arr_padded,
                            emotion=emotion_arr, text=text_arr)


if __name__ == '__main__':

    audio_type = 'orig'
    # audio_type = 'instrumental'

    print(audio_type)

    # videos = ['test']
    # save_npz(videos, type='test', audio_type=audio_type)

    # videos = ['BMI']
    # save_npz(videos, type='test', audio_type=audio_type)

    videos = ['BMI', 'CHI', 'FNE', 'GLA', 'LOR']
    # save_npz(videos, type='train', audio_type=audio_type, emotion_dim='1D', data_type='only_complete', include_audio=False)
    save_npz(videos, type='train', audio_type=audio_type, emotion_dim='1D', data_type='with_incomplete', include_audio=False)
    save_npz(videos, type='train', audio_type=audio_type, emotion_dim='2D', data_type='only_complete', include_audio=False)
    save_npz(videos, type='train', audio_type=audio_type, emotion_dim='2D', data_type='with_incomplete', include_audio=False)

    videos = ['CRA', 'DEP']
    save_npz(videos, type='test', audio_type=audio_type, emotion_dim='1D', data_type='only_complete', include_audio=False)
    save_npz(videos, type='test', audio_type=audio_type, emotion_dim='1D', data_type='with_incomplete', include_audio=False)
    save_npz(videos, type='test', audio_type=audio_type, emotion_dim='2D', data_type='only_complete', include_audio=False)
    save_npz(videos, type='test', audio_type=audio_type, emotion_dim='2D', data_type='with_incomplete', include_audio=False)
