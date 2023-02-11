import pandas as pd
import os
import io
import re
from glob import glob
import re
import numpy as np
import sys

def change_encoding(srt, save_path):
    with io.open(srt, 'r', encoding= "utf-8") as f:
        text = f.read()
        # process Unicode text
    with io.open(save_path, 'w', encoding= 'utf-8-sig') as f:
        f.write(text)

def convert_srt_to_csv(file):
    with open(file, 'r',encoding= 'utf-8') as h:
        sub = h.readlines()   #returns list of all lines

    re_pattern = r'[0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3} --> [0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3}'
    regex = re.compile(re_pattern)
    # Get start times
    times = list(filter(regex.search, sub))
    end_times = [time.split('--> ')[1] for time in times] #returns a list
    start_times = [time.split(' ')[0] for time in times]  #returns a list

    # Get lines
    lines = [[]]
    for sentence in sub:
        if re.match(re_pattern, sentence):
            lines[-1].pop()
            lines.append([])
        else:
            lines[-1].append(sentence)

    lines = lines[1:]   #all text in lists
    text_list = [] #只留日文和数字和标点
    text_only_list = [] #只留日文
    for diag in lines:
        text_only = re.sub(u"([^\u30a0-\u30ff\u3040-\u309f\u4e00-\u9fa5])", "", diag[0])#只留日文和汉字
        #消除括号内内容
        while re.match('【.*?】', diag[0]):
            no_braket = re.sub('【.*?】', '', diag[0])
            print(no_braket+",原句为”"+diag[0])
            diag[0] = no_braket

        #消除分段重复

        if text_only in text_only_list:
            print(text_only+"，为重复字段")
            return None
        else:
            text_only_list.append(text_only)
        diag[0] = re.sub(u"([^\u30a0-\u30ff\u3040-\u309f\u4e00-\u9fa5\u3000-\u303f\ufb00-\ufffd0-9])", "", diag[0])#只留日文和数字和标点
        if len(diag[0]) < 2:
            return None
        if diag[0][-2] not in ["。","、","?","!","…"]:
            text_list.append(diag[0].replace("\n", "。") )  #去掉换行符合并所有文本
        #如果换行符前面没有标点加上句号
        else:
            if diag[0][-2] == "?":
                diag[0] = diag[0].replace("?", "？")
            elif diag[0][-2] == "!":
                diag[0] = diag[0].replace("!", "！")
            text_list.append(diag[0].replace("\n", ""))
    final_text = ''.join(text_list)

    #确认没有重复，如果仍有大段重复直接舍弃
    if repeat_judge(final_text):
        return None
    if katagana_judge(final_text): #全是片假也舍弃
        return None

    return NG_judge(final_text)
    
    
def NG_judge(text):
    NGword = ["","ん。"]
    NGmode = ["ぁぁぁぁ","赤い赤い赤い赤い赤い","高評価","チャンネル","登録","コメントをお願いします","ふぅぅ","字幕辞聴者","字幕をご覧いただ","ご視聴頂き","ご視聴ありがとうございました","ご視聴ありがとうございます","ん。ん。","はぁ、","はぁ。","はぁー","はぁはぁ","んんん"]
    if len(text) < 4:
        return None
    for mode in NGmode:
        if re.match(".*"+mode+".*", text):
            return None
    if text not in NGword:
        return text
    else:
        return None
def katagana_judge(text): #判断是否全是片假
    japan_only = re.sub(u"([^\u30a0-\u30ff\u3040-\u309f\u4e00-\u9fa5])", "", text)#只留日文体系
    katagana_only = re.sub(u"([^\u30a0-\u30ff])", "", text)#只留片假
    if len(katagana_only) == len(japan_only):
        return True
    else:
        return False

#判断字符串是否含有大量重复字段
def repeat_judge(text):

    clip_number = 5
    mid_text_spot = int(len(text)//2)
    if (len(text)<(clip_number*2-2)):
        return False #足够长度字符串才进行判断
    
    head = text[0:clip_number] #5个字符为一组检测是否有重复字符
    if re.match(".*"+head+".*", text[clip_number:]):
        return True #有重复返回true

    mid = text[(mid_text_spot-2):(mid_text_spot+3)]
    mid_clip =  text[0:mid_text_spot-2] + text[mid_text_spot+3:]
    if re.match(".*"+mid+".*", mid_clip):
        return True #有重复返回true
    
    mid_clip2 =  text[0:mid_text_spot-2] + text[mid_text_spot+2:] #这个加上是因为9字符的刚好无法判断
    mid2 = text[(mid_text_spot-2):(mid_text_spot+2)]
    if re.match(".*"+mid2+".*", mid_clip2):
        return True #有重复返回true

    tail = text[(clip_number*-1):] #5个字符为一组检测是否有重复字符
    if re.match(".*"+tail+".*", text[0:(clip_number*-1)]):
        return True #有重复返回true
    
    return False



if __name__ == "__main__":
    character_name = "asami"
    srt_path = "F:\\vit model audio\\44100\\"+character_name+"\\srt" #字幕文件夹
    save_path = "F:\\vit model audio\\44100\\"+character_name #txt filelist导出地址
    srt_list = os.listdir(srt_path)
    character_number = str(6)
    with open(os.path.join(save_path,(character_name+"_list.txt")),"w+", encoding= "utf-8") as w:
        text_combination = []
        for srt_file in glob(srt_path + "\\*.srt"):
            text_each = convert_srt_to_csv(srt_file)
            if (text_each != None) & (text_each not in text_combination): #消除重复文本文件
                text_combination.append(text_each)
                srt_filename = srt_file[(len(srt_path)+1):]
                wav_filename = srt_filename[0:-3] + "wav"
                if len(text_each) < 25:
                    w.write("wavs/{}|{}|{}\n".format(wav_filename, character_number, text_each))
    