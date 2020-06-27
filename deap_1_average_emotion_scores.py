
import numpy as np
from moviepy.editor import *
import utils
from timeit import default_timer as timer
from SrtTextHandler import SrtTextHandler
from DatEmotionHandler import DatEmotionHandler
from collections import defaultdict
from scipy.io import wavfile
import pandas as pd
import csv

"""
    DEAP has scores from 32 participants for 40 videos. This script will output a .csv file with the average emotion scores from all 32 participants.
    Valence: 1 (most negative) - 9 (most positive) -> 5 is right in the middle
            [1, 5) = neg
            [5, 9] = pos

    DEAP scale: valence, arousal (continuous 1-9) - Russell's scale ( J. A. Russell, “A circumplex model of affect,” Journal of Personality and Social Psychology, vol. 39, no. 6, pp. 1161–1178, 1980)
    "Arousal can range from inactive (e.g. uninterested, bored) to active (e.g. alert, excited), whereas valence ranges from unpleasant (e.g. sad, stressed) to pleasant (e.g. happy, elated)"
    Source: http://www.eecs.qmul.ac.uk/mmv/datasets/deap/doc/tac_special_issue_2011.pdf
"""


__author__ = "Gwena Cunha"


ROOT = utils.project_dir_name() + 'data/deap/'


def get_emotion_score_dictionary(filename='data/deap/participant_ratings.csv'):
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        # Fieldnames: Participant_id,Trial,Experiment_id,Start_time,Valence,Arousal,Dominance,Liking,Familiarity
        valence_dict = defaultdict(lambda: [])
        arousal_dict = defaultdict(lambda: [])
        for row in reader:
            # print(row['Trial'], row['Valence'], row['Arousal'])
            valence_dict[row['Trial']].append(float(row['Valence']))
            arousal_dict[row['Trial']].append(float(row['Arousal']))
        dict = {'valence': valence_dict, 'arousal': arousal_dict}
        return dict


def get_emotion_score_mean_1D(dict):
    valence_dict = dict['valence']
    valence_mean_dict = defaultdict(lambda: 0)
    valence_mean_dict_1D = defaultdict(lambda: 0)
    count_emotion = defaultdict(lambda: 0)
    for k, v in valence_dict.items():
        valence_mean_dict[k] = np.mean(v)
        valence_mean_dict_1D[k] = 0 if valence_mean_dict[k] < 5 else 1
        count_emotion[valence_mean_dict_1D[k]] += 1
    print('Emotion count: {}'.format(count_emotion))
    return valence_mean_dict_1D


def save_emotion_score_mean_1D(dict, csv_filename):
    # Save 1D emotion in csv file
    csv_filename = csv_filename.split('.csv')[0] + '_1D.csv'
    with open(csv_filename, 'w', newline='') as csvfile:
        fieldnames = ['video_id', 'emotion']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for k, v in dict.items():
            writer.writerow({'video_id': k, 'emotion': v})


if __name__ == '__main__':
    csv_filename = ROOT + 'participant_ratings.csv'
    dict = get_emotion_score_dictionary(filename=csv_filename)
    valence_mean_dict_1D = get_emotion_score_mean_1D(dict)
    save_emotion_score_mean_1D(valence_mean_dict_1D, csv_filename)
