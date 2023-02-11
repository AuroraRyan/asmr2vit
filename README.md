# asmr2vit
convert your asmrs to vits datasets

asmr处理流程：
1、demucs去除噪音和背景音乐https://github.com/facebookresearch/demucs，个人偷懒没去研究直接导入python的使用方法,可以使用仓库里的demucs.py（基于命令行）。也可使用makefile文件管理。时间较长。而且请一定先做。

2、Slicer(VAD静音检测切片，把1h长音频切成几秒钟的短音频)

#以上集成在asmr_extract.py，愿意的话可以重新打包，本人仓库https://github.com/AuroraRyan/asmr2vit

3、使用whisper将wav转为srt字幕文件https://github.com/AlexandaJerry/whisper-vits-japanese。愿意的话可以自己部署到本地集成

4、使用srt2txt.py，将srt字幕文件转化为filelist.txt，供vits训练用。相关文件夹结构为，以声优名字ueda为例，ueda-(srt,wavs,ueda_list.txt)，srt文件夹下存放whisper得到的srt文件，wavs文件夹下存放第2步得到音频切片

#srt2txt.py做了清洗文本操作，包括重复词检测，NG词检测（可能会把h部分过滤掉，不需要请手动修改）

5、降低第2步得到的音频切片采样率至22050（change_sample_rate.py），注意音频音量，可自行尝试匹配，也可以使用volume.py手动降低。

6、VITS训练，参考https://www.bilibili.com/read/cv18357171?from=search&spm_id_from=333.337.0.0

期待有能人士打包成ipynb笔记本，供谷歌colab使用。
