
import unittest
import utils
import os
import pandas as pd
from collections import defaultdict

"""
    Handles .dat emotion information
"""

__author__ = "Gwena Cunha"


params = {
    'root': utils.project_dir_name() + 'data_test/BMI/',
    'seconds': 10
}


class DatEmotionHandler:
    def __init__(self, root_dir, dat_filename='intended_1.dat'):
        self.root_dir = root_dir
        self.dat_filename = dat_filename
        self.dat_file = utils.get_file(self.root_dir, self.dat_filename)
        self.dat_sentences = self.dat_file.read().splitlines()
        self.csv_data = None

    def dat_to_csv(self, csv_filename='intended_1.csv'):
        """
        Transform .dat files into .csv files with time, valence_score_raw, and valence_score emotion information

        :param csv_filename: filename where dataframe will be saved to in csv format
        :return:
        """
        self.csv_data = defaultdict(list)
        for i in range(0, len(self.dat_sentences)):
            time, valence_score, arousal_score = self.dat_sentences[i].split()
            self.csv_data['time'].append(float(time))
            self.csv_data['valence_score_raw'].append(float(valence_score))
            self.csv_data['arousal_score_raw'].append(float(arousal_score))
            if float(valence_score) >= 0:  # range between -1 and 1
                self.csv_data['valence_score'].append(1)
            else:
                self.csv_data['valence_score'].append(0)
            if float(arousal_score) >= 0:  # range between -1 and 1
                self.csv_data['arousal_score'].append(1)
            else:
                self.csv_data['arousal_score'].append(0)
        df = pd.DataFrame(self.csv_data, columns=['time', 'valence_score_raw', 'valence_score', 'arousal_score_raw', 'arousal_score'])
        df.to_csv(self.root_dir + csv_filename, index=False)

    def emotion_between_times(self, init_time, final_time, verbose=False, raw=False):
        """
        Returns valence and arousal emotions between initial and final time

        :param init_time: initial time in seconds
        :param final_time: final time in seconds
        :param verbose: if print is allowed or not
        :return: Integer (emotion, the first emotion score that is between init_time and final_time)
        """
        time = self.csv_data['time']
        valence_scores = self.csv_data['valence_score_raw'] if raw else self.csv_data['valence_score']
        arousal_scores = self.csv_data['arousal_score_raw'] if raw else self.csv_data['arousal_score']
        count = 0
        while time[count] <= init_time and time[count] <= final_time:
            count += 1
        valence = valence_scores[count-1]
        arousal = arousal_scores[count-1]
        if verbose:
            print("Emotion between {} and {}s: {}/{}".format(init_time, final_time, valence, arousal))
        return valence, arousal

    def mean_emotion_between_times(self, init_time, final_time, verbose=False, raw=False):
        """
        Returns mean valence and arousal emotion between initial and final time

        :param init_time: initial time in seconds
        :param final_time: final time in seconds
        :param verbose: if print is allowed or not
        :return: Float (emotion, the first emotion score that is between init_time and final_time)
                 Integer (1 if float >= 0 else 0)
        """
        time = self.csv_data['time']
        valence_scores = self.csv_data['valence_score_raw'] if raw else self.csv_data['valence_score']
        arousal_scores = self.csv_data['arousal_score_raw'] if raw else self.csv_data['arousal_score']
        count = 0
        while count < len(time) and time[count] <= init_time and time[count] <= final_time:
            count += 1
        count -= 1
        valence, arousal = 0, 0
        em_count = 0
        while count < len(time) and time[count] < final_time:
            em_count += 1
            valence += valence_scores[count]
            arousal += arousal_scores[count]
            count += 1
        if em_count != 0:
            valence /= em_count
            valence = round(valence, 3)
            arousal /= em_count
            arousal = round(arousal, 3)
        valence_round = 1 if valence >= 0 else 0
        arousal_round = 1 if arousal >= 0 else 0
        if verbose:
            print("Emotion between {} and {}s: {}/{}".format(init_time, final_time, valence, arousal))
        return valence, valence_round, arousal, arousal_round


class TestSrtTextHandler(unittest.TestCase):

    def setUp(self):
        print("\nSet up")
        self.root_dir = params['root']
        self.dat_filename = 'intended_1.dat'
        self.datEmotionHandler = DatEmotionHandler(self.root_dir, dat_filename=self.dat_filename)

        self.seconds = params['seconds']

    def test_dat_to_csv(self):
        print("Testing dat_to_csv")
        csv_filename = 'intended_1.csv'
        self.datEmotionHandler.dat_to_csv(csv_filename=csv_filename)
        self.assertTrue(os.path.isfile(self.root_dir + csv_filename))

    def test_emotion_between_times(self):
        print("Testing valence_between_times")
        csv_filename = 'intended_1.csv'
        self.datEmotionHandler.dat_to_csv(csv_filename=csv_filename)
        valence, arousal = self.datEmotionHandler.valence_between_times(init_time=0, final_time=0.16, verbose=True, raw=True)
        self.assertEqual(valence, 0.028)
        valance, arousal = self.datEmotionHandler.valence_between_times(init_time=0.96, final_time=1.0, verbose=True, raw=True)
        self.assertEqual(valence, 0.023)

    def test_mean_emotion_between_times(self):
        print("Testing MEAN valence_between_times")
        csv_filename = 'intended_1.csv'
        self.datEmotionHandler.dat_to_csv(csv_filename=csv_filename)
        valence, _, _, _ = self.datEmotionHandler.mean_valence_between_times(init_time=0, final_time=0.16, verbose=True, raw=True)
        self.assertEqual(valence, 0.028)
        valence, _, _, _ = self.datEmotionHandler.mean_valence_between_times(init_time=0.9, final_time=1, verbose=True, raw=True)
        self.assertEqual(valence, 0.026)  # (0.028+0.028+0.023)/3
        valence, _, _, _ = self.datEmotionHandler.mean_valence_between_times(init_time=0.99, final_time=1, verbose=True, raw=True)
        self.assertEqual(valence, 0.023)
        valence, _, _, _ = self.datEmotionHandler.mean_valence_between_times(init_time=0.99, final_time=1.02, verbose=True, raw=True)
        self.assertEqual(valence, 0.017)


if __name__ == '__main__':
    unittest.main()
