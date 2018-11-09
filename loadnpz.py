import numpy as np
from librosa.output import write_wav
from moviepy.editor import ImageSequenceClip
from skimage import color

"""
    Load npz and save test video and audio
"""

__author__ = "Gwena Cunha"


def normalize(arr, min=0, max=1):
    return min + (max - min) * (arr - np.amin(arr)) / (np.amax(arr) - np.amin(arr))


data = np.load('data_test/video_feats_HSL_10fps_pad_test.npz')
HSL_data = data['HSL_data']
audio = data['audio']
emotion = data['emotion']
text = data['text']

print("HSL_data {}, audio {}, emotion: {}, text: {}".format(np.shape(HSL_data), np.shape(audio), np.shape(emotion), np.shape(text)))
sample_idx = 1
test_video = np.array(HSL_data[sample_idx]).squeeze()
test_audio = audio[sample_idx]
test_emotion = emotion[sample_idx]
test_text = text[sample_idx]
print("Test HSL_data {}, audio {}, emotion {}, text {}".format(np.shape(test_video), np.shape(test_audio), test_emotion, test_text))

filename_target_audio = 'data_test/test.wav'
write_wav(filename_target_audio, test_audio, sr=16000, norm=True)

input_reshaped = np.array(test_video).squeeze()

frame_arr = []
for frame in input_reshaped:
    frame = np.swapaxes(np.swapaxes(frame, 0, 1), 1, 2)  # np.transpose(frame)  # 100, 100, 3
    frame = normalize(frame, min=0, max=1)
    frame_rgb = color.hsv2rgb(frame)
    frame_arr.append(frame_rgb * 255)

clip = ImageSequenceClip(np.array(frame_arr), fps=10)  # 3-second clip, .tolist()
filename = 'data_test/test.avi'
clip.write_videofile(filename, fps=10, codec='png', audio_fps=16000, audio=filename_target_audio)  # export as video
