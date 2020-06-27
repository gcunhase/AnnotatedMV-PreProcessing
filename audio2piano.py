import os
import glob
import argparse
from timeit import default_timer as timer
from pydub import AudioSegment
import utils

"""
Based on audio_to_midi_melodia/main_wav2mid2wav.py
"""


if __name__ == '__main__':

    # 10 seconds splices: 44.86 min
    parser = argparse.ArgumentParser()
    parser.add_argument("--script_dir", default="/media/ceslea/DATA/PycharmProjects/audio_to_midi_melodia-master",
                        help="Path to audio2midi project directory.")
    parser.add_argument("--folder", default="data_test/", help="Path to input audio file.")
    # parser.add_argument("--subfolders", type=list, default=['BMI', 'CHI', 'FNE', 'GLA', 'LOR'],
    parser.add_argument("--subfolders", nargs='+', default=['BMI', 'CHI', 'CRA', 'DEP', 'FNE', 'GLA', 'LOR'],
                        help="Path to subfolders containing input audio file.")
    parser.add_argument("--bpm", type=int, default=146, help="Tempo of the track in BPM.")
    parser.add_argument("--smooth", type=float, default=0.25,
                        help="Smooth the pitch sequence with a median filter "
                             "of the provided duration (in seconds).")
    parser.add_argument("--minduration", type=float, default=0.1,
                        help="Minimum allowed duration for note (in seconds). "
                             "Shorter notes will be removed.")
    parser.add_argument("--jams", action="store_const", const=True,
                        default=False, help="Also save output in JAMS format.")
    parser.add_argument("--duration", type=int, default=10, help="Duration of audio files in seconds.")

    args = parser.parse_args()

    init_time = timer()

    FOLDER = args.folder + "*"

    IFS = ".wav"  # delimiter
    BPM = args.bpm
    size_audio_files = args.duration  # in seconds

    subdirs = []
    for s in args.subfolders:
        # subdirs.append(args.folder + s + '/audio_splices_3secs_16000_c1_16bits')
        subdirs.append(args.folder + s + '/audio_splices_{}secs'.format(size_audio_files))

    for sub in subdirs:
        files = glob.glob(sub + "/*{}".format(IFS))
        mid_dir = sub + "_mid/"
        utils.ensure_dir(mid_dir)
        save_dir = sub + "_wav2mid2wav/"
        utils.ensure_dir(save_dir)
        sr_dir = sub + "_wav2mid2wav_16000_c1_16bits/"
        utils.ensure_dir(sr_dir)
        for f in files:
            filename = f.split('/')[-1]
            filename = filename.split(IFS)[0]
            sound = AudioSegment.from_file(f)
            size_audio_files = len(sound)
            print("{}, {}, {}".format(f, filename, size_audio_files))

            # wav to mid
            command_str = 'python {script_dir}/audio_to_midi_melodia.py {sub}/{filename}{ifs} {mid_dir}{filename}.mid' \
                          ' {bpm} --smooth {smooth} --minduration {mindur}'.format(script_dir=args.script_dir, sub=sub,
                                                                                   filename=filename, bpm=BPM, ifs=IFS,
                                                                                   smooth=args.smooth,
                                                                                   mindur=args.minduration,
                                                                                   mid_dir=mid_dir)

            if args.jams:
                command_str += ' --jams'
            os.system(command_str)

            # mid to wav
            os.system('timidity {mid_dir}{filename}.mid -Ow -o {rec_dir}{filename}.wav'.
                      format(filename=filename, rec_dir=save_dir, mid_dir=mid_dir))

            # change sample rate to 16000, 1 channel, 16 bits
            os.system('sox {rec_dir}{filename}.wav -c1 -b16 -r16000 -G {sr_dir}/{filename}.wav'.
                      format(filename=filename, rec_dir=save_dir, sr_dir=sr_dir))

    '''
    # Normalize data length (all audio samples must have the same duration)
    subdirs = []
    for s in args.subfolders:
        subdirs.append(args.folder + s + '/audio_splices_3secs_wav2mid2wav_16000_c1_16bits')
    splice_seconds = size_audio_files * 1000  # ms
    for sub in subdirs:
        files = glob.glob("{}/*{}".format(sub, IFS))
        sr_dir = '{}_eq/'.format(sub)
        utils.ensure_dir(sr_dir)
        for f in files:
            # print(f)
            f_base = f.split(IFS)[0]
            filename = f_base.split('/')[-1]

            sound = AudioSegment.from_file(f)
            sound_chunks = len(sound)

            first_x_seconds = sound[:splice_seconds]
            first_x_seconds.export("{}{}.wav".format(sr_dir, filename), format="wav")
    '''

    end_time = timer()
    print("Program took {} minutes".format((end_time - init_time) / 60))
    # COGNIMUSE: 47 minutes, minutes
