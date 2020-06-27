[![DOI](https://zenodo.org/badge/152549677.svg)](https://zenodo.org/badge/latestdoi/152549677)

## About
Pre-processing of annotated music video datasets:
* [COGNIMUSE dataset](http://cognimuse.cs.ntua.gr/database)
* [DEAP dataset](https://www.eecs.qmul.ac.uk/mmv/datasets/deap/index.html)

### Contents
[Requirements](#requirements) • [How to Use](#how-to-use) • [How to Cite](#acknowledgement)

## Requirements
Tested with Python 2.7 and Ubuntu 16.04
```
pip install -r requirements.txt
sudo apt-get install -y sox
```
> See [more details](./README_notes.md)

## How to Use
### COGNIMUSE
0. Download [COGNIMUSE dataset](http://cognimuse.cs.ntua.gr/database):
    * [Download annotations](http://cognimuse.cs.ntua.gr/sites/default/files/COGNIMUSEdatabase_v0.1.zip)
        * Emotion: 2D (valence-arousal) with ranges between [-1, 1]
        * 2 emotions = {Neg: 0, Pos: 1}
        * 4 emotions = {NegHigh: 0, NegLow: 1, PosLow: 2, PosHigh: 3}
    * Download videos, extract the last 30 minutes of each video, and copy them to `data/`
    * The final directory structure should be as follow:
       ```
      .data
      +-- BMI
      |   +-- emotion
      |   |   +-- intended_1.dat
      |   +-- text
      |   |   +-- subtitle.srt
      |   +-- video.mp4
      ...
      ```

1. Splice full video (with subtitle information) into S seconds each -> video, emotion, audio, text
    * Run: `python video2splice.py`
    * Output: 
      ```
      .data_test
      +-- BMI
      |   +-- audio_splices_Xsecs
      |   |   0.wav
      |   ...
      |   |   N.wav
      |   +-- emotion
      |   |   +-- intended_1.dat
      |   |   +-- intended_1_[1D/2D].csv
      |   |   +-- intended_1_[1D/2D]_splices_Xsecs.csv
      |   +-- text
      |   |   +-- subtitle.srt
      |   |   +-- text.csv
      |   |   +-- text_splices_Xsecs.csv
      |   +-- video_splices_Xsecs
      |   |   0.mp4
      |   ...
      |   |   N.mp4
      ...
      ```

2. (Optional) Transform audio to instrumental piano audio
    * Run: `python audio2piano.py`
      > [More info](https://github.com/gcunhase/wav2midi2wav), needs Python 2.7

3. Save spliced data in Python's *npz* format
    * Run: `python splices2npz.py`
    * Run after full video has been spliced accordingly
    * Full: 7 annotated music videos divided into splices of S seconds stored in *data_test/*
    <p align="left">
    <img src="https://github.com/gcunhase/AnnotatedMV-PreProcessing/blob/master/assets/dataset.png" width="300" alt="Dataset">
    </p>   
    * Test: Single *.avi* or *.mp4* file in *data_test/*

4. Results will be a train and test dataset with the *npz* extension in the same root directory containing the data folders

### DEAP
0. [Download dataset](https://www.eecs.qmul.ac.uk/mmv/datasets/deap/download.html) (need to sign EULA form):
    * Train data:
        * Choose a video option: `highlights` (1 minute videos) or `raw video` (original music videos of varying lengths)
        * Convert `$DEAP_DATA/Video/highlights/*.wmv` files to `mp4`
        * Copy videos to `./data/deap/mp4/`
        * Open `$DEAP_DATA/metadata_xls/participatn_ratings.XLS`, save as `$DEAP_DATA/metadata_xls/participatn_ratings.CSV` and copy it to `./data/deap/`
    * Test data (same for `highlights` or `raw video`):
        * Extract the first 11 seconds of each train video
        * Copy it in `./data/deap/test_data/`
    * The final directory structure should be as follow:
       ```
      .data/deap/
      +-- mp4
      |   +-- 1.mp4
      |   +-- 2.mp4
      |   ...
      +-- participatn_ratings.csv
      +-- test_data
      |   +-- 1.mp4
      |   +-- 2.mp4
      |   ...
      ...
      ```
1. Get average of emotion scores
    * Run: `python deap_1_average_emotion_scores.py`
2. Splice video, audio, emotion and dummy text files
    > Dummy text is necessary in order to ensure compatibility with the COGNIMUSE script
    * Run: `python deap_2_video2splice.py`
3. (Optional) Transform audio to instrumental piano audio
    * Run: `python deap_3_audio2piano.py`
4. Save spliced data in Python's *npz* format
    * Run: `python deap_4_splices2npz.py`

## Acknowledgement
Please star or fork if this code was useful for you. If you use it in a paper, please cite as:
```
@software{cunha_sergio2019preprocessing_cognimuse,
    author       = {Gwenaelle Cunha Sergio},
    title        = {{gcunhase/AnnotatedMV-PreProcessing: Pre-Processing of COGNIMUSE Annotated Music Video Corpus}},
    month        = oct,
    year         = 2019,
    doi          = {10.5281/zenodo.3496807},
    version      = {v1.0},
    publisher    = {Zenodo},
    url          = {https://github.com/gcunhase/AnnotatedMV-PreProcessing}
    }
```

If you use the COGNIMUSE database:
```
@article{zlatintsi2017cognimuse,
  title={COGNIMUSE: A multimodal video database annotated with saliency, events, semantics and emotion with application to summarization},
  author={Zlatintsi, Athanasia and Koutras, Petros and Evangelopoulos, Georgios and Malandrakis, Nikolaos and Efthymiou, Niki and Pastra, Katerina and Potamianos, Alexandros and Maragos, Petros},
  journal={EURASIP Journal on Image and Video Processing},
  volume={2017},
  number={1},
  pages={54},
  year={2017},
  publisher={Springer}
}
```

If you use the DEAP database:
```
@article{koelstra2011deap,
  title={Deap: A database for emotion analysis; using physiological signals},
  author={Koelstra, Sander and Muhl, Christian and Soleymani, Mohammad and Lee, Jong-Seok and Yazdani, Ashkan and Ebrahimi, Touradj and Pun, Thierry and Nijholt, Anton and Patras, Ioannis},
  journal={IEEE transactions on affective computing},
  volume={3},
  number={1},
  pages={18--31},
  year={2011},
  publisher={IEEE}
}
```
