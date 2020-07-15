
import numpy as np
from moviepy.editor import VideoFileClip
from ImageSequenceClip import ImageSequenceClip
import utils
from timeit import default_timer as timer
from SrtTextHandler import SrtTextHandler
from DatEmotionHandler import DatEmotionHandler
from collections import defaultdict
from scipy.io import wavfile
import pandas as pd
from video2splice import splice_video, splice_audio
import glob
import csv

"""
    DEAP scale: valence, arousal (continuous 1-9) - Russell's scale ( J. A. Russell, “A circumplex model of affect,” Journal of Personality and Social Psychology, vol. 39, no. 6, pp. 1161–1178, 1980)
    "Arousal can range from inactive (e.g. uninterested, bored) to active (e.g. alert, excited), whereas valence ranges from unpleasant (e.g. sad, stressed) to pleasant (e.g. happy, elated)"
    Source: http://www.eecs.qmul.ac.uk/mmv/datasets/deap/doc/tac_special_issue_2011.pdf
    
   A dummy text csv is also generated here but it's not used (generated so we can use splices2npz.py)
    
    Splice video into 3 seconds each -> video, emotion (1D), audio
    Start splicing video from the beginning (if more than 1 time is shown, it means we ran the code more than once)
            Test: Vid 1-16, 19-40 (3 splices each)
                  Em 1: 28 * 3 -> 84
                  Em 0: 10 * 3 -> 30
                  Program ran for 221.39 seconds
            Train (highlights): Vid 1-16, 19-40 (20 splices each)
                                Em 1: 1-7, 9-13, 15, 20, 22-25, 27, 29-32, 34-38 (7+5+2+4+1+4+5=28 -> 560 splices)
                                Em 0: 8, 14, 16, 19, 21, 26, 28, 33, 39, 40 (10 -> 200 splices)
                                Program ran for 1209.07 seconds
            Train (raw videos): same emotion as above, but number of splices per video is different:
                                Em 1 (total=2,069): Vid 1 (46), 2 (67), 3 (77), 4 (92), 5 (40), 6 (70), 7 (48), 9 (90), -> 530
                                                    10 (83), 11 (76), 12 (72), 13 (61), 15 (23), 20 (78), 22 (78), -> 471
                                                    23 (78), 24 (79), 25 (89), 27 (112), 29 (90), 30 (69), 31 (95), -> 612
                                                    32 (75), 34 (79), 35 (59), 36 (66), 37 (104), 38 (73) -> 456
                                Em 0 (total=781): Vid 8 (70), 14 (73), 16 (74), 19 (55), 21 (94), -> 366
                                                    26 (82), 28 (63), 33 (60), 39 (124), 40 (86) -> 415
                                P.S.: Raw 21, 23 have compromised frames and splicing doesn't work.
                                      Solved by converting to .mov and back to .mp4
"""


__author__ = "Gwena Cunha"

is_test = False
if is_test:
    ROOT = utils.project_dir_name() + 'data/deap/test_data/'
else:
    ROOT = utils.project_dir_name() + 'data/deap_raw/mp4/'
params = {
    'root': ROOT,
    'emotion_root': utils.project_dir_name() + 'data/deap_raw/',
    'sr': 16000,
    'seconds': 3,
    'num_samples': -1  # default = -1 for all samples. Use different to test code
}


def get_num_video_splices(video_splices_dir):
    return len(glob.glob(video_splices_dir+'*.mp4'))


def splice_emotion(video_name_int, csv_filename='participant_ratings_1D.csv'):
    n_splices = get_num_video_splices(params['root'] + 'video_splices_{}secs/'.format(params['seconds']))

    # Extract emotion
    with open(csv_filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        dict = {'video_id': []}
        for row in reader:
            dict['video_id'].append(row['emotion'])

    # DEAP dataset is annotated for each video, not per time in video.
    #  This means that the emotion score will be the same for every splice in 'video_name'.
    emotion_csv_data = defaultdict(lambda: [])
    text_csv_data = defaultdict(lambda: [])
    emotion_counter = defaultdict(lambda: 0)
    emotion = dict['video_id'][video_name_int-1]
    for e in range(0, n_splices):
        emotion_csv_data['splice'].append(e)
        emotion_csv_data['emotion'] = emotion
        text_csv_data['splice'].append(e)
        text_csv_data['text'].append("")
        emotion_counter[emotion] += 1

    # Save emotion splices in csv file
    df = pd.DataFrame(emotion_csv_data, columns=['splice', 'emotion'])
    df.to_csv('{}participant_ratings_1D_splices_{}secs.csv'.format(params['root'], params['seconds']), index=False)
    # Save dummy text csv
    df = pd.DataFrame(text_csv_data, columns=['splice', 'text'])
    df.to_csv('{}text_splices_{}secs.csv'.format(params['root'], params['seconds']), index=False)
    return "Vid {} - Num of emotion splices: {} ({})".format(video_name_int, e + 1, emotion_counter.items())


if __name__ == '__main__':

    tic = timer()

    # Test numbers 1-10
    # Train: 1-16, 19-40
    emotion_video_info_str = '\n'
    if is_test:
        # video_names_train = range(1, 10+1)
        video_names_train = np.concatenate((range(1, 16 + 1), range(19, 40 + 1)))
    else:
        video_names_train = np.concatenate((range(1, 16+1), range(19, 40+1)))
    for video_name_int in video_names_train:  #range(1, 16+1):
        video_name = str(video_name_int)
        num_samples = params['num_samples']

        # Splice video and audio
        video_filename = ROOT + video_name + '.mp4'
        params['root'] = ROOT + video_name + '/'
        utils.ensure_dir(params['root'])
        video_clip = VideoFileClip(video_filename)
        splice_video(video_clip, num_samples=num_samples, params_substitute=params)

        audio_clip = video_clip.audio  # audio_file_clip = AudioFileClip(audio_clip, fps=audio_clip.fps)
        del video_clip
        splice_audio(audio_clip, num_samples=num_samples, params_substitute=params)

        # Splice Emotion: 1D emotion splicing
        emotion_video_info_str += splice_emotion(video_name_int, csv_filename=params['emotion_root']+'participant_ratings_1D.csv') + '\n'

    toc = timer()
    print(emotion_video_info_str)
    print("Program ran for {:.2f} seconds".format(toc-tic))
