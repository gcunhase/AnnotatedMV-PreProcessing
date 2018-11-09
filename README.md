
### About
Pre-processing of annotated music video, namely COGNIMUSE

### Run Code
1. *video2splice.py*: splice video into S seconds each -> video, emotion, audio, text (?)
    
2. *splices2npz.py*: to run after full video has been spliced accordingly

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
    
2. *splices2npz.py*
    * Full: 7 annotated music videos divided into splices of S seconds stored in *data/*
    TODO: change table to splices 3 seconds and splices 10 seconds
    <p align="left">
    <img src="https://github.com/gcunhase/AnnotatedMV-PreProcessing/blob/master/assets/dataset.png" width="300" alt="Dataset">
    </p>
    
    * Test: Single *.avi* file in *data_test/*

### Requirements
```
pip install --upgrade pip
pip install numpy requests moviepy
pip install scikit-image librosa natsort
```

### Note
* In *ImageSequenceClip.py*, change *isinstance(sequence, list)* in line 62 for *isinstance(sequence, list) or isinstance(sequence, np.ndarray)*
