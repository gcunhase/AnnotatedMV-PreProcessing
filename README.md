[![DOI](https://zenodo.org/badge/152549677.svg)](https://zenodo.org/badge/latestdoi/152549677)

## About
Pre-processing of [COGNIMUSE dataset](http://cognimuse.cs.ntua.gr/database) (annotated music video)

### Contents
[Requirements](#requirements) • [How to Use](#how-to-use) • [How to Cite](#acknowledgement)

## Requirements
Tested with Python 2.7 and Ubuntu 16.04
```
pip install -r requirements.txt
sudo apt-get install -y sox
```

In more details:
```
pip install --upgrade pip
pip install numpy requests moviepy
pip install scikit-image librosa natsort
pip install pydub vamp jams midiutil
apt-get install ffmpeg bpm-tools
apt-get install timidity timidity-interfaces-extra
sudo apt-get install python3-tk
```

## How to Use
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
      |   +-- intended_1.dat
      |   +-- subtitle.srt
      |   +-- video.mp4
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

### Code notes
   * In `ImageSequenceClip.py`, change *isinstance(sequence, list)* in line 62 for *isinstance(sequence, list) or isinstance(sequence, np.ndarray)*
   * For *avi* use *png* codec

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
