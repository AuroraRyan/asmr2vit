from demucs import vocal_extract
import os
import librosa  # Optional. Use any library you like to read audio files.
import soundfile  # Optional. Use any library you like to write audio files.

from audio_slicer.slicer2 import Slicer
import shutil

def slicer_use(filepath):
    wav_list = [e for e in os.listdir(filepath) if os.path.isfile(os.path.join(filepath,e))]

    for wav in wav_list:
        audio, sr = librosa.load(os.path.join(filepath,wav) , sr=None, mono=False)  # Load an audio file with librosa.
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
            filename = os.path.join(filepath,wav[0:-11]+"_{}.wav".format(i))
            soundfile.write(filename, chunk, sr)  # Save sliced audio files with soundfile.
        os.remove(os.path.join(filepath,wav))

if __name__ == '__main__':
    wav_path = "E:\\asmr"
    vocal_extract(wav_path)
    slicer_use(wav_path)

