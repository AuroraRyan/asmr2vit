# asmr2vit
convert your asmrs to vits datasets

asmr处理流程：
1、demucs去除噪音和背景音乐https://github.com/facebookresearch/demucs，个人偷懒没去研究直接导入python的使用方法，可使用命令行或者makefile文件管理
2、Slicer(VAD静音检测切片，把1h长音频切成几秒钟的短音频)

#以上集成在asmr_extract.py，愿意的话可以重新打包

3、使用whisper将wav转为srt字幕文件https://github.com/AlexandaJerry/whisper-vits-japanese

4、使用srt2txt.py，将srt字幕文件转化为
