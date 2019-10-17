[![DOI](https://zenodo.org/badge/152549677.svg)](https://zenodo.org/badge/latestdoi/152549677)

## About
Pre-processing of annotated music video, namely COGNIMUSE
Pre-processing of COGNIMUSE dataset

### Contents
[Requirements](#requirements) • [How to Use](#how-to-use) • [How to Cite](#acknowledgement)

## Requirements
Tested with Python 2.7 and Ubuntu 16.04
```
pip install -r requirements.txt
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
      +-- GLA
      |   +-- intended_1.dat
      |   +-- subtitle.srt
      |   +-- video.mp4 
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
