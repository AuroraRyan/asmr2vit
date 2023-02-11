import os
import shutil
import time

def vocal_extract(filepath): #filepath like"F:\\vit model audio\\44100\\asami\\"
    wav_dir=filepath
    output_path = wav_dir
    wav_list = [e for e in os.listdir(wav_dir) if os.path.isfile(os.path.join(wav_dir,e))]

    for wav in wav_list:
        src_path = os.path.join(wav_dir,wav)
        wav_name = wav.replace(".wav","")
        new = src_path[0:-4]+"_no_bgm.wav"
        print(src_path)
        cmd = "demucs "+"\""+src_path+"\""+" -o "+ "\""+ output_path +"\"" + " -n mdx --two-stems=vocals"   
        print("执行"+cmd)
        cmd_return = os.system(cmd)
        print("返回值为{}已完成".format(cmd_return))
        old = os.path.join(wav_dir,"mdx",wav_name,"vocals.wav")
        shutil.move(old,new)
        time.sleep(2)
        shutil.rmtree(os.path.join(wav_dir,"mdx"))   #删除输出文件夹
        os.remove(os.path.join(wav_dir,wav)) #删除源文件

if __name__ == '__main__':
    wav_path = "F:\\vit model audio\\44100\\iwamimanaka"
    vocal_extract(wav_path)