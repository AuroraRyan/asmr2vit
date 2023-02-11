import os
import uuid
from ffmpy import FFmpeg







# for file in os.listdir(wav_dir):
#     complete_dir = os.path.join(wav_dir, file)

#     cmd = "ffmpeg -i "+"\""+complete_dir+"\"" +" -af loudnorm=I=-16:TP=-1.5:LRA=11:print_format=json -f null -"
#     cmd_return = os.system(cmd)
#     n += 1
#     if n == 3:
#         exit()
def raise_by_decibel(audio_path: str, output_dir: str, decibel):
    ext = os.path.basename(audio_path).strip().split('.')[-1]
    file_name = os.path.basename(audio_path)
    if ext not in ['wav', 'mp3']:
        raise Exception('format error')
    temp_name =  os.path.join(
                output_dir, '{}.{}'.format(
                    uuid.uuid4(), ext))
    ff = FFmpeg(
        inputs={
            '{}'.format(audio_path): None}, outputs={
            temp_name: '-filter:a "volume={}dB"'.format(decibel)})
    print(ff.cmd)
    ff.run()
    os.remove(audio_path)
    os.rename(temp_name, audio_path)
    return os.path.join(output_dir, file_name)


if __name__ == "__main__":
    # wav_dir = "F:\\vit model audio\\wavs\\wavs"
    wav_dir2 = "F:\\vit model audio\\uma"
    wav_dir3 = "F:\\vit model audio\\uma\\story\\data\\09"
    for root,dirs,files_list in os.walk(wav_dir2):
        for wav_file in files_list:
            if wav_file[-4:] == ".wav":
                complete_dir = os.path.join(root,wav_file)
                raise_by_decibel(complete_dir,root,-7.8) #降低分贝数

    for root,dirs,files_list in os.walk(wav_dir3):
        for wav_file in files_list:
            if wav_file[-4:] == ".wav":
                complete_dir = os.path.join(root,wav_file)
                raise_by_decibel(complete_dir,root,-3) #降低分贝数

