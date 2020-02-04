import numpy as np
from librosa.output import write_wav
from moviepy.editor import ImageSequenceClip
from skimage import color
import utils
import os

"""
    Load npz and save test video and audio
"""

__author__ = "Gwena Cunha"


def normalize(arr, min=0, max=1):
    return min + (max - min) * (arr - np.amin(arr)) / (np.amax(arr) - np.amin(arr))


# data = np.load('data_test/video_feats_HSL_10fps_pad_test.npz')
data = np.load('data_test/video_feats_HSL_10fps_origAudio_3secs_intAudio_pad_train.npz')
HSL_data = data['HSL_data']
audio = data['audio']
emotion = data['emotion']
text = data['text']

num = 0
for i, a in enumerate(audio):
    if i == 0:
        num = np.shape(a)[0]
        print(np.shape(a))
    else:
        if np.shape(a)[0] != num:
            num = np.shape(a)[0]
            print(np.shape(a))

'''
print("HSL_data {}, audio {}, emotion: {}, text: {}".format(np.shape(HSL_data), np.shape(audio), np.shape(emotion), np.shape(text)))

recovered_dir = 'data_test/recovered/'
utils.ensure_dir(recovered_dir)

idx = -1  # 1
idx = np.shape(HSL_data)[0] if idx == -1 else idx
for sample_idx in range(0, idx):
    test_video = np.array(HSL_data[sample_idx]).squeeze()
    test_audio = audio[sample_idx]
    test_emotion = emotion[sample_idx]
    test_text = text[sample_idx]
    print("Test HSL_data {}, audio {}, emotion {}, text {}".format(np.shape(test_video), np.shape(test_audio), test_emotion, test_text))

    filename_target_audio = '{}{}.wav'.format(recovered_dir, sample_idx)
    write_wav(filename_target_audio, test_audio, sr=16000, norm=True)

    input_reshaped = np.array(test_video).squeeze()

    frame_arr = []
    for frame in input_reshaped:
        frame = np.swapaxes(np.swapaxes(frame, 0, 1), 1, 2)  # np.transpose(frame)  # 100, 100, 3
        frame = normalize(frame, min=0, max=1)
        frame_rgb = color.hsv2rgb(frame)
        frame_arr.append(frame_rgb * 255)

    clip = ImageSequenceClip(np.array(frame_arr), fps=10)  # 3-second clip, .tolist()
    filename = '{}{}.avi'.format(recovered_dir, sample_idx)
    clip.write_videofile(filename, fps=10, codec='png', audio_fps=16000, audio=filename_target_audio)  # export as video
    # os.system('ffmpeg -y -i {} {}{}.mp4'.format(filename, recovered_dir, sample_idx))
    # os.system('ffmpeg -y -i {} -c:v libx264 -c:a copy {}{}.mp4'.format(filename, recovered_dir, sample_idx))
'''
