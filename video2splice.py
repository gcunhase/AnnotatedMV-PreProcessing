
import numpy as np
from moviepy.editor import *
import utils
from timeit import default_timer as timer
from SrtTextHandler import SrtTextHandler
from DatEmotionHandler import DatEmotionHandler
from collections import defaultdict
from scipy.io import wavfile
import pandas as pd


"""
    Splice video into S seconds each -> video, emotion, audio, text (?)
    Start splicing video from the beginning (if more than 1 time is shown, it means we ran the code more than once)
            3 seconds BMI: 625 (0: 608, 1: 17) 1224.92secs, 1736.98secs
                      CHI: 602 (0: 0, 1: 602) 1199.21secs, 1618.33secs
                      CRA: 532 (0: 527, 1: 5) 1035.77secs, 1383.56secs
                      DEP: 609 (0: 245, 1: 364) 1210.28secs, 1655.11secs
                      FNE: 605 (0: 114, 1: 491) 1662.55secs
                      GLA: 600 (0: 125, 1: 475) 1641.90secs
                      LOR: 750 (0: 557, 1: 193) 2018.05secs
            10 seconds BMI: 187 (0: 182, 1: 5) 900secs, 1040.52secs (script run)
                       CHI: 180 (0: 0, 1: 180) 932.82secs, 1021.42secs
                       CRA: 159 (0: 158, 1: 1) 806.36secs, 874.45secs
                       DEP: 182 (0: 75, 1: 107) 925.69secs, 1009.31secs
                       FNE: 181 (0: 35, 1: 146) 947.94secs, 1014.08secs
                       GLA: 180 (0: 38, 1: 142) 923.03secs, 975.29secs
                       LOR: 225 (0: 168, 1: 57) 1271.24secs, 1262.19secs
"""


__author__ = "Gwena Cunha"


params = {
    # 'root': utils.project_dir_name() + 'data/cognimuse_multimodal_robust_bert/',
    'root': utils.project_dir_name() + 'data/cognimuse/',
    'sr': 16000,
    'seconds': 10,
    'num_samples': -1  # default = -1 for all samples. Use different to test code
}


def splice_video(video_clip, num_samples=-1):
    # Load videos (fps = 30)
    vid_fps = round(video_clip.fps)
    vid_num_frames = round(vid_fps * video_clip.duration)
    vid_frames_per_splice = params['seconds'] * vid_fps
    print("Video - num frames: {}, size: {}, fps: {}, frames_per_splice: {}".
          format(vid_num_frames, video_clip.size, vid_fps, vid_frames_per_splice))

    # Extract video splices
    video_splices = defaultdict(list)
    splice = 0
    for f, frame in enumerate(video_clip.iter_frames()):
        if f != 0 and f % vid_frames_per_splice == 0:
            print("Splice {} of size {}".format(splice, len(video_splices[splice])))
            splice += 1
            if splice == num_samples:
                break
        video_splices[splice].append(frame)
    if num_samples == -1:
        del video_splices[splice]  # last splice has different size
    print("Video - Num of video splices: {}".format(splice))

    # Save video splices in folder
    video_splices_dir = '{}video_splices_{}secs'.format(params['root'], params['seconds'])
    utils.ensure_dir(video_splices_dir)
    for k, v in video_splices.items():
        print("Video {}".format(k))
        clip = ImageSequenceClip(v, fps=vid_fps)
        clip.write_videofile('{}/{}.mp4'.format(video_splices_dir, k))
        del clip
    # return video_clip


def splice_audio(audio_clip, num_samples=-1):
    # Extract audio
    audio_fps = audio_clip.fps
    audio_frames_per_splice = params['seconds'] * audio_fps
    audio_num_frames = round(audio_fps * audio_clip.duration)
    print("Audio - num_frames: {}, fps: {}, duration: {}, frames_per_splice: {}".
          format(audio_num_frames, audio_fps, audio_clip.duration, audio_frames_per_splice))

    audio_splices = defaultdict(list)
    splice = 0
    for f, frame in enumerate(audio_clip.iter_frames()):
        if f != 0 and f % audio_frames_per_splice == 0:
            # print("Splice {} of size {}".format(splice, len(audio_splices[splice])))
            splice += 1
            if splice == num_samples:
                break
        audio_monochannel = frame[0]
        audio_splices[splice].append(audio_monochannel)
    if num_samples == -1:
        del audio_splices[splice]  # last splice has different size
    print("Splices: {}".format(splice))

    # Downsample to sr
    # print("Downsampling audio from {} to {}".format(audio_clip.fps, params['sr']))
    # audio_splices_down = utils.downsample_audio(audio_splices, audio_fps, params['sr'], params['seconds'])
    audio_splices_down = audio_splices

    # Save audio splices in folder
    print("Saving audio splices in folder + changing to 16kHz, 1 channel, 16 bits")
    audio_splices_dir = '{}audio_splices_{}secs'.format(params['root'], params['seconds'])
    utils.ensure_dir(audio_splices_dir)
    sr_dir = audio_splices_dir + '_16000_c1_16bits'
    utils.ensure_dir(sr_dir)

    for kd, vald in audio_splices_down.items():
        print("Writing k: {}, val: {} to wav".format(kd, len(vald)))
        # wavfile.write('{}/{}.wav'.format(audio_splices_dir, kd), params['sr'], np.array(vald))
        wavfile.write('{}/{}.wav'.format(audio_splices_dir, kd), audio_clip.fps, np.array(vald))
        # Change sample rate to 16000, 1 channel, 16 bits. The -G option fixes clipping issue
        os.system('sox {rec_dir}/{filename}.wav -c1 -b16 -r16000 -G {sr_dir}/{filename}.wav'.
                  format(filename=kd, rec_dir=audio_splices_dir, sr_dir=sr_dir))


def splice_text(text_root='text/', srt_filename='subtitle.srt'):
    # Extract dialogue
    srtTextHandler = SrtTextHandler(params['root']+text_root, srt_filename=srt_filename)
    srtTextHandler.srt_to_csv(csv_filename='text.csv')
    text_splices = {}
    for e, t in enumerate(range(0, int(audio_clip.duration)-params['seconds'], params['seconds'])):
        text_splices[e] = srtTextHandler.text_between_times(t, t+params['seconds'])
        # print("i: {}, f: {}, t: {}".format(t, t+params['seconds'], text_splices[e]))

    # Save text splices in csv file
    text_csv_data = defaultdict(list)
    for kd, vald in text_splices.items():
        # print("k: {}, val: {}".format(kd, vald))
        text_csv_data['splice'].append(kd)
        text_csv_data['text'].append(vald)
    df = pd.DataFrame(text_csv_data, columns=['splice', 'text'])
    df.to_csv('{}text_splices_{}secs.csv'.format(params['root']+text_root, params['seconds']), index=False)
    print("Text - Num of text splices: {}".format(e+1))


def splice_emotion(emotion_root='emotion/', dat_filename='intended_1.dat', emotion_dim='1D'):
    # Extract emotion
    datEmotionHandler = DatEmotionHandler(params['root']+emotion_root, dat_filename=dat_filename)
    datEmotionHandler.dat_to_csv(csv_filename='intended_1_{}.csv'.format(emotion_dim))
    emotion_splices = {}
    for e, t in enumerate(range(0, int(audio_clip.duration) - params['seconds'], params['seconds'])):
        _, valence, _, arousal = datEmotionHandler.mean_emotion_between_times(t, t + params['seconds'], raw=True)
        emotion_splices[e] = [valence, arousal]
        # print("i: {}, f: {}, em: {}".format(t, t+params['seconds'], emotion_splices[e]))

    # Save emotion splices in csv file
    emotion_csv_data = defaultdict(list)
    emotion_counter = defaultdict(lambda: 0)
    for kd, vald in emotion_splices.items():
        # print("k: {}, val: {}".format(kd, vald))
        emotion = utils.get_emotion_score(vald, emotion_dim)
        emotion_csv_data['splice'].append(kd)
        emotion_csv_data['emotion'].append(emotion)
        emotion_counter[emotion] += 1

    df = pd.DataFrame(emotion_csv_data, columns=['splice', 'emotion'])
    df.to_csv('{}intended_1_{}_splices_{}secs.csv'.format(params['root']+emotion_root, emotion_dim, params['seconds']), index=False)
    print("Emotion - Num of emotion splices: {} ({})".format(e + 1, emotion_counter.items()))


if __name__ == '__main__':

    tic = timer()

    video_name = "BMI"  # BMI, CHI, CRA, DEP, FNE, GLA, LOR
    num_samples = params['num_samples']

    # Splice
    params['root'] = params['root'] + video_name + '/'
    video_filename = "{}video.mp4".format(params['root'])
    video_clip = VideoFileClip(video_filename)
    splice_video(video_clip, num_samples=num_samples)

    audio_clip = video_clip.audio  # audio_file_clip = AudioFileClip(audio_clip, fps=audio_clip.fps)
    del video_clip
    splice_audio(audio_clip, num_samples=num_samples)
    del audio_clip

    splice_text(srt_filename='subtitle.srt')

    # 1D and 2D emotion splicing
    splice_emotion(dat_filename='intended_1.dat', emotion_dim='1D')
    splice_emotion(dat_filename='intended_1.dat', emotion_dim='2D')

    toc = timer()
    print("Program ran for {:.2f} seconds".format(toc-tic))
