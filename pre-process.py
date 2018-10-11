
import numpy as np
from moviepy.editor import *
import utils
from skimage import color
import librosa
import glob
from natsort import natsorted


"""
    Pre-processes data considering video and audio only
    Synchronize video and audio
"""


__author__ = "Gwena Cunha"


params = {
    'fps': 10,
    'root': utils.project_dir_name() + 'data/',
    'new_size': 100,
    'sr': 16000
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


def save_npz(videos, type='train'):
    print(videos)
    frame_hsv_arr = []
    audio_arr = []
    for v in videos:
        # Load video and corresponding audio
        video_path = params['root'] + v + "/selected_avi/*.avi"
        video_filenames = glob.glob(video_path)
        video_filenames = natsorted(video_filenames)
        # Load corresponding audio
        audio_path = params['root'] + v + "/selected_wav_eq/*.wav"
        audio_filenames = glob.glob(audio_path)
        audio_filenames = natsorted(audio_filenames)

        for v_filename, a_filename in zip(video_filenames, audio_filenames):
            print('Video: {}, audio: {}'.format(v_filename.split('/')[-1], a_filename.split('/')[-1]))
            frame_hsv_arr.append(load_video(v_filename))
            audio, _ = librosa.load(a_filename, sr=params['sr'])
            audio_arr.append(audio)

    # Transpose from (N, 30, 100, 100, 3) to (N, 30, 3, 100, 100)
    frame_hsv_arr_transpose = np.transpose(frame_hsv_arr, (0, 1, 4, 2, 3))
    print("Shapes - video: {}/{}, audio: {}".format(np.shape(frame_hsv_arr), np.shape(frame_hsv_arr_transpose),
                                                    np.shape(audio_arr)))

    # Save in .npz
    save_npz_filename = '{}video_feats_HSL_{}fps_{}.npz'.format(params['root'], params['fps'], type)
    np.savez_compressed(save_npz_filename, HSL_data=frame_hsv_arr_transpose, audio=audio_arr)


if __name__ == '__main__':

    videos = ['BMI', 'CHI', 'FNE', 'GLA', 'LOR']
    save_npz(videos, type='train')

    videos = ['CRA', 'DEP']
    save_npz(videos, type='test')
