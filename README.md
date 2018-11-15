
### About
Pre-processing of annotated music video, namely COGNIMUSE

### Run Code
1. *video2splice.py*: splice video into S seconds each -> video, emotion, audio, text
2. (Optional) *audio2piano.py* ([source](https://github.com/gcunhase/wav2midi2wav)): transform audio to instrumental piano audio, needs Python 2.7
3. *splices2npz.py*: to run after full video has been spliced accordingly
4. Results will be a train and test dataset with the *npz* extension in the same root directory containing the data folders

### Data
1. *video2splice.py*: full videos with emotion and subtitle information.

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
    
3. *splices2npz.py*
    * Full: 7 annotated music videos divided into splices of S seconds stored in *data_test/*
    <p align="left">
    <img src="https://github.com/gcunhase/AnnotatedMV-PreProcessing/blob/master/assets/dataset.png" width="300" alt="Dataset">
    </p>
    
    * Test: Single *.avi* or *.mp4* file in *data_test/*

### Requirements
```
pip install --upgrade pip
pip install numpy requests moviepy
pip install scikit-image librosa natsort
pip install pydub vamp jams midiutil
apt-get install ffmpeg bpm-tools
apt-get install timidity timidity-interfaces-extra
sudo apt-get install python3-tk
```

### Note
* In *ImageSequenceClip.py*, change *isinstance(sequence, list)* in line 62 for *isinstance(sequence, list) or isinstance(sequence, np.ndarray)*
* For *avi* use *png* codec and for *mp4* use **