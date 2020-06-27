# Optional: original audio to piano notes

# Test
#ARR=('1' '2' '3' '4' '5' '6' '7' '8' '9' '10')
#FOLDER=data/deap/test_data/
#ARR=( $(seq 1 10) )
# Train: 1.726 min (DEAP highlights), 62.12min (DEAP raw)
ARR=( $(seq 1 16) $(seq 19 40) )
FOLDER=data/deap/mp4/
# echo "${ARR[@]}"
python audio2piano.py --script_dir /media/ceslea/RESEARCH/PycharmProjects/audio_to_midi_melodia-master \
    --folder $FOLDER \
    --subfolders "${ARR[@]}" \
    --duration 3