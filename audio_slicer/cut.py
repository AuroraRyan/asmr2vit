import librosa  # Optional. Use any library you like to read audio files.
import soundfile  # Optional. Use any library you like to write audio files.

from slicer2 import Slicer
import os

wav_list = os.listdir("F:\\vit model audio\\44100\\asami\\")

for wav in wav_list:
    audio, sr = librosa.load('F:\\vit model audio\\44100\\asami\\'+ wav , sr=None, mono=False)  # Load an audio file with librosa.
    slicer = Slicer(
        sr=sr,
        threshold=-40,
        min_length=5000,
        min_interval=300,
        hop_size=10,
        max_sil_kept=500
    )
    chunks = slicer.slice(audio)
    for i, chunk in enumerate(chunks):
        if len(chunk.shape) > 1:
            chunk = chunk.T  # Swap axes if the audio is stereo.
        filename = "./clips/"+wav[0:-5]+"_{}.wav".format(i)
        soundfile.write(filename, chunk, sr)  # Save sliced audio files with soundfile.