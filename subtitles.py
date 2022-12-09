import os
import re
import shutil
import json
from datetime import datetime , timedelta
import pysrt

import sox

path = "./global-subtitles.json"

def exportSubtitles():
    result={}
    with open(path, 'r', encoding="utf-8") as file:
        for one in json.load(file).values():
            # print(one)
            if "zh-cnFemaleVariant" not in one:
                continue
            if "zh-cnFemaleResPath" not in one:
                continue
            
            key = one["zh-cnFemaleResPath"].split("/")[-1].split(".")[0]
            result[key] = "V:" + one["zh-cnFemaleVariant"]
    # print(result)
    with open('./output.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False)

def exportSft():
    file = pysrt.SubRipFile()
    i = 1
    sub = pysrt.SubRipItem(i, start='00:02:04,000', end='00:02:08,000', text="Hello World!")
    file.append(sub)
    file.save('my_movie.srt')

def sox_length(path):
    try:
        length = sox.file_info.duration(path)
        return length
    except:
        return None

def mp3Length():
    filename = "1208.txt"
    time = datetime.strptime("2020-01-01T00:00:00", '%Y-%m-%dT%H:%M:%S')

    with open("output.json", 'r', encoding="utf-8") as file:
        subtitles = json.load(file)
        print(subtitles)

    srt = pysrt.SubRipFile()
    i = 1

    with open(filename) as file:
        for line in file:
            mp3filename = line.rstrip().split("'")[1]
            mp3 = os.path.join("mp3_files",mp3filename)
            tfrom = time.strftime("%H:%M:%S,%f")[:-3]
            time = time + timedelta(milliseconds=sox_length(mp3) * 1000)
            tto = time.strftime("%H:%M:%S,%f")[:-3]
            srt.append(pysrt.SubRipItem(i, start=tfrom, end=tto, text=subtitles.get(mp3filename.split(".")[0], "")))
            i+=1
    
    srt.save('my_movie.srt')
mp3Length()