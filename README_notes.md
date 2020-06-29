
## Detailed Requirements
Tested with Python 2.7 and Ubuntu 16.04
```
pip install -r requirements.txt
sudo apt-get install -y sox
```

In more details:
```
pip install numba==0.43.0 llvmlite==0.32.1
pip install --upgrade pip
pip install numpy requests moviepy
pip install scikit-image librosa natsort
pip install pydub vamp jams midiutil
apt-get install ffmpeg bpm-tools
apt-get install timidity timidity-interfaces-extra
sudo apt-get install python3-tk
```

## Code notes
* In `ImageSequenceClip.py`, change *isinstance(sequence, list)* in line 62 for *isinstance(sequence, list) or isinstance(sequence, np.ndarray)*
* For *avi* use *png* codec
