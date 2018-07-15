#!/usr/bin/python3
import urllib.request
import os
from pydub import AudioSegment
from pydub.silence import detect_silence
import requests
import json
import config

url = config.test_url


def download_podcast(url):
    urllib.request.urlretrieve(url, file_name)

def get_clip(startTime,endTime,cntr):
    clip = AudioSegment.from_mp3(os.path.join(os.getcwd(), file_name))
    extract = clip[startTime:endTime]
    extract.export(cntr+'-extract.mp3', format="wav")
    file_clip = cntr + '-extract.mp3'
    return file_clip


def get_transcript(clip):
    data = open(clip, 'rb').read()

    key = config.key
    headers = {'Accept':'application/json;text/xml',
               'Ocp-Apim-Subscription-Key' : key,
               'Host':'speech.platform.bing.com',
               'Content-type' : 'audio/mpeg; codec=audio/pcm; samplerate=16000'}

    r = requests.post("https://speech.platform.bing.com/speech/recognition/conversation/cognitiveservices/v1?language=en-US&format=simple",
                      headers=headers,
                      data=data)
    return r

file_name = os.path.basename(url)
clip_size = 8000

startMin = 26
startSec = 57

startTime = (startMin*60*1000+startSec*1000) - clip_size
endTime = startTime + (clip_size*8)


download_podcast(url)
text = ''

cnt = 0
for c in range(startTime,endTime,clip_size):
    cnt += 1
    clip = get_clip(c, c+clip_size,str(cnt))
    r = json.loads(get_transcript(clip).text)
    with open(str(cnt)+".txt", "w") as text_file:
        text_file.write(str(r))
    print(r['DisplayText'])
    text += r['DisplayText']

