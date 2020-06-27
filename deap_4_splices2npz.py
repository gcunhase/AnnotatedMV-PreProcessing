
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
from splices2npz import load_video, process_audio

"""
    Pre-processes data considering already spliced video and audio only
    Synchronize video and audio
"""


__author__ = "Gwena Cunha"


is_test = True
if is_test:
    ROOT = utils.project_dir_name() + 'data/deap/test_data2/'
else:
    ROOT = utils.project_dir_name() + 'data/deap_raw/mp4/'
params = {
    'fps': 10,
    'root': ROOT,
    'new_size': 100,  # new frame size (100x100)
    'sr': 16000,
    'audio_len': 48000,
    'results_dir': ROOT,
    'seconds': 3,
}


def save_npz(videos, type='train', audio_type='instrumental', emotion_dim='1D', emotion_root='emotion/',
             text_root='text/', include_audio=True):
    print(videos)
    seconds = params['seconds']
    frame_hsv_arr, audio_arr, emotion_arr, text_arr = [], [], [], []
    for v_int in videos:
        v = str(v_int)
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
        emotion_csv = pd.read_csv(data_path + "{}participant_ratings_{}_splices_{}secs.csv".format(emotion_root, emotion_dim, seconds))
        emotion_data = emotion_csv['emotion']

        # Load corresponding text
        text_csv = pd.read_csv(data_path + "{}text_splices_{}secs.csv".format(text_root, seconds))
        text_data = text_csv['text']

        for v_filename, a_filename, emotion, text in zip(video_filenames, audio_filenames, emotion_data, text_data):
            text = "" if isinstance(text, float) else text
            print('Video {}: {}, audio: {}, emotion: {}, text: {}'.
                  format(v, v_filename.split('/')[-1], a_filename.split('/')[-1], emotion, text))
            frame_hsv = load_video(v_filename, params_substitute=params)
            if 'deap_raw' in ROOT:
                # Make sure the max frame is 25 (for splices of 3 secs with 10fps)
                frame_hsv_container = np.zeros( (25, params['new_size'], params['new_size'], 3) )
                frame_hsv_container[:np.shape(frame_hsv)[0], :, :, :] = np.array(frame_hsv[:25])
                frame_hsv = frame_hsv_container
                #frame_hsv = frame_hsv[:25]  # np.array(frame_hsv)[:25, :, :, :]
            frame_hsv_arr.append(frame_hsv)
            rate, audio = read(a_filename)  # int numbers -> necessary for SAMPLERNN and CNNSEQ2SEQ models
            # print(rate)  # 16000 OKAY
            audio_arr.append(audio)
            emotion_arr.append(emotion)
            text_arr.append(text)

    # Transpose from (N, 30, 100, 100, 3) to (N, 30, 3, 100, 100)
    # frame_hsv_arr = np.array(frame_hsv_arr)
    #if 'deap_raw' in ROOT:
    #    #frame_hsv_arr = np.concatenate(frame_hsv_arr, axis=0)
    #    frame_hsv_arr = np.stack(frame_hsv_arr, axis=0)
    #    # frame_hsv_arr = list(map(list, zip(*frame_hsv_arr)))  # (16, N, 100, 100, 3)
    #    s = np.shape(frame_hsv_arr)
    #    if s.__len__ == 1:
    #        frame_hsv_arr = frame_hsv_arr[0]  #np.squeeze(frame_hsv_arr, axis=0)
    #    frame_hsv_arr_transpose = np.transpose(frame_hsv_arr, (1, 0, 4, 2, 3))
    #else:
    frame_hsv_arr_transpose = np.transpose(frame_hsv_arr, (0, 1, 4, 2, 3))
    # Pad audio to audio_len if not already
    audio_arr_padded = process_audio(audio_arr, pad_size=params['audio_len'])
    print("Shapes - video: {}/{}, audio: {}/{}".format(np.shape(frame_hsv_arr), np.shape(frame_hsv_arr_transpose),
                                                       np.shape(audio_arr), np.shape(audio_arr_padded)))

    # Save in .npz
    utils.ensure_dir(params['results_dir'])
    save_npz_filename_root = '{}video_feats_HSL_{}fps_{}secs'.format(params['results_dir'], params['fps'], seconds)
    if include_audio:
        if audio_type == 'orig':
            save_npz_filename = save_npz_filename_root + '_origAudio_intAudio_{}_{}.npz'.format(emotion_dim, type)
        else:
            save_npz_filename = save_npz_filename_root + '_intAudio_{}_{}.npz'.format(emotion_dim, type)
        np.savez_compressed(save_npz_filename, HSL_data=frame_hsv_arr_transpose, audio=audio_arr, emotion=emotion_arr,
                            text=text_arr)
    else:
        save_npz_filename = save_npz_filename_root + '_{}_{}_noAudio.npz'.format(emotion_dim, type)
        np.savez_compressed(save_npz_filename, HSL_data=frame_hsv_arr_transpose, emotion=emotion_arr, text=text_arr)

    # Padded audio
    if include_audio:
        if audio_type == 'orig':
            save_npz_filename = save_npz_filename_root + '_origAudio_intAudio_pad_{}_{}.npz'.format(emotion_dim, type)
        else:
            save_npz_filename = save_npz_filename_root + '_intAudio_pad_{}_{}.npz'.format(emotion_dim, type)
        np.savez_compressed(save_npz_filename, HSL_data=frame_hsv_arr_transpose, audio=audio_arr_padded,
                            emotion=emotion_arr, text=text_arr)


if __name__ == '__main__':

    # audio_type = 'orig'
    audio_type = 'instrumental'
    type = 'test' if is_test else 'train'

    videos = np.concatenate((range(1, 16+1), range(19, 40+1)))
    #videos = range(3, 5 + 1)
    save_npz(videos, type=type, audio_type=audio_type, emotion_dim='1D', include_audio=True,
             emotion_root='', text_root='')
