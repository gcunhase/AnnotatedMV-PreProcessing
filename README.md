
### About
Pre-processing of annotated music video, namely COGNIMUSE

### Data
* Full: 7 annotated music videos divided into splices of 3 seconds stored in *data/*
<p align="left">
<img src="https://github.com/gcunhase/AnnotatedMV-PreProcessing/blob/master/assets/dataset.png" width="300" alt="Dataset">
</p>

* Test: Single *.avi* file in *data_test/*

### Requirements
```
pip install --upgrade pip
pip install numpy requests moviepy
pip install scikit-image librosa
```

### Note
* In *ImageSequenceClip.py*, change *isinstance(sequence, list)* in line 62 for *isinstance(sequence, np.ndarray) or isinstance(sequence, list)*
