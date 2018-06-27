#!/usr/bin/python3
import urllib.request
import os
from pydub import AudioSegment
import requests
import json
import config

url = config.test_url


startMin = 2
startSec = 29
file_name = os.path.basename(url)
startTime = startMin*60*1000+startSec*1000
endTime = startTime + 15000

def download_podcast(url):
    urllib.request.urlretrieve(url, file_name)

def get_clip():
    clip = AudioSegment.from_mp3(os.path.join(os.getcwd(), file_name))
    extract = clip[startTime:endTime]
    extract.export(file_name+'-extract.mp3', format="wav")
    file_clip = file_name + '-extract.mp3'
    return file_clip


def get_transcript(clip):
    data = open(clip, 'rb').read()

    key = config.key
    headers = {'Accept':'application/json;text/xml',
               'Ocp-Apim-Subscription-Key' : key,
               'Host':'speech.platform.bing.com',
               'Content-type' : 'audio/mpeg; codec=audio/pcm; samplerate=16000'}

    r = requests.post("https://speech.platform.bing.com/speech/recognition/interactive/cognitiveservices/v1?language=en-US&format=detailed",
                      headers=headers,
                      data=data)
    return r


download_podcast(url)
clip = get_clip()
r = json.loads(get_transcript(clip).text)
text = r['NBest'][0]['Display']

