
import unittest
import utils
import os
import pandas as pd
from collections import defaultdict

"""
    Handles .srt text information
    Transform it into .txt or .csv
"""

__author__ = "Gwena Cunha"


params = {
    'root': utils.project_dir_name() + 'data_test/BMI/',
    'seconds': 10
}


class SrtTextHandler:
    def __init__(self, root_dir, srt_filename='subtitle.srt'):
        self.root_dir = root_dir
        self.srt_filename = srt_filename
        self.srt_file = utils.get_file(self.root_dir, self.srt_filename)
        self.srt_sentences = self.srt_file.read().splitlines()
        self.csv_data = None

    def get_sec(self, time_str):
        """
        HH:MM:SS,sss to seconds

        :param time_str: time in HH:MM:SS,sss format
        :return:
        """
        h, m, s = time_str.split(':')
        ss, ms = s.split(',')
        return int(h) * 3600 + int(m) * 60 + int(ss) + int(ms) / 1000

    def srt_to_csv(self, csv_filename='text.csv'):
        """
        Transform .srt files into .csv files with start and end time, duration, and related text

        :param csv_filename: filename where dataframe will be saved to in csv format
        :return:
        """
        self.csv_data = defaultdict(list)
        count = 0
        sentence = ''
        for i in range(0, len(self.srt_sentences)):
            line = self.srt_sentences[i]
            if count == 0:  # ID
                self.csv_data['ID'].append(line)
                count += 1
            elif count == 1:  # initial and final times in seconds
                init_time, final_time = line.split('-->')
                init_time_sec = self.get_sec(init_time)
                final_time_sec = self.get_sec(final_time)
                self.csv_data['init_time'].append(init_time_sec)
                self.csv_data['final_time'].append(final_time_sec)
                self.csv_data['duration'].append(round(final_time_sec - init_time_sec, 3))
                count += 1
            else:
                if line.strip() != '':
                    sentence += line + ' '
                else:
                    self.csv_data['text'].append(sentence)
                    sentence = ''
                    count = 0
        df = pd.DataFrame(self.csv_data, columns=['ID', 'init_time', 'final_time', 'duration', 'text'])
        df.to_csv(self.root_dir + csv_filename, index=False)

    def srt_to_text(self, txt_filename='text.txt'):
        """
        Transform .srt files into .txt files

        :param txt_filename: filename where text will be saved to
        :return:
        """
        saved_filename = self.root_dir + txt_filename
        txt_file = open(saved_filename, 'w')

        count = 0
        sentence = ''
        for i in range(0, len(self.srt_sentences)):
            line = self.srt_sentences[i]
            if count != 2:
                count += 1
            else:
                if line.strip() != '':
                    sentence += line + ' '
                else:
                    txt_file.write(sentence + '\n')
                    sentence = ''
                    count = 0

    def text_between_times(self, init_time, final_time, verbose=False):
        """
        Returns text between initial and final time

        :param init_time: initial time in seconds
        :param final_time: final time in seconds
        :param verbose: if print is allowed or not
        :return: String (sentence)
        """
        if self.csv_data is not None:

            sentence = ''
            real_init_time = init_time
            real_final_time = final_time
            for i, f, text in zip(self.csv_data['init_time'], self.csv_data['final_time'], self.csv_data['text']):
                if init_time <= f and final_time >= i and ((init_time <= i and final_time <= f) or
                                                           (init_time <= i and f <= final_time) or
                                                           (i <= init_time and f <= final_time) or
                                                           (i <= init_time and final_time <= f)):
                    if verbose:
                        print("i: {}, f: {}, text: {}".format(i, f, text))
                    sentence += text
                    init_time = f
            if verbose:
                print("Text between {} and {}s: {}".format(real_init_time, real_final_time, sentence))
            return sentence
        else:
            return ''


class TestSrtTextHandler(unittest.TestCase):

    def setUp(self):
        print("\nSet up")
        self.root_dir = params['root']
        self.srt_filename = 'subtitle.srt'
        self.srtTextHandler = SrtTextHandler(self.root_dir, srt_filename=self.srt_filename)

        self.seconds = params['seconds']

    def test_srt_to_txt(self):
        print("Testing srt_to_text")
        txt_filename = 'text.txt'
        self.srtTextHandler.srt_to_text(txt_filename=txt_filename)
        self.assertTrue(os.path.isfile(self.root_dir + txt_filename))


    def test_text_between_times(self):
        print("Testing text_between_times")
        csv_filename = 'text.csv'
        self.srtTextHandler.srt_to_csv(csv_filename=csv_filename)
        text = self.srtTextHandler.text_between_times(init_time=27, final_time=29, verbose=True)
        self.assertEqual(text, 'Get in. Hurry. ')
        text = self.srtTextHandler.text_between_times(init_time=28, final_time=29, verbose=True)
        self.assertEqual(text, 'Get in. Hurry. ')
        text = self.srtTextHandler.text_between_times(init_time=28, final_time=30, verbose=True)
        self.assertEqual(text, 'Get in. Hurry. ')
        text = self.srtTextHandler.text_between_times(init_time=30, final_time=31, verbose=True)
        self.assertEqual(text, '')
        text = self.srtTextHandler.text_between_times(init_time=33, final_time=40, verbose=True)
        self.assertEqual(text, 'They\'re following us. Who\'s- Who\'s following us? ')
        text = self.srtTextHandler.text_between_times(init_time=34, final_time=40, verbose=True)
        self.assertEqual(text, 'They\'re following us. Who\'s- Who\'s following us? ')
        text = self.srtTextHandler.text_between_times(init_time=310.5, final_time=318, verbose=True)
        self.assertEqual(text, 'I told you attachments were dangerous. You chose to marry the girl. I did nothing to prevent it. ')
        text = self.srtTextHandler.text_between_times(init_time=310.5, final_time=310, verbose=True)
        self.assertEqual(text, '')


if __name__ == '__main__':
    unittest.main()
