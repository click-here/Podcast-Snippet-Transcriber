#!/usr/bin/python3
import urllib.request
import os, re, json
from pydub import AudioSegment
from pydub.silence import detect_silence
import requests
import config
import urllib.parse as urlparse
from lxml import html

def get_podcast_file_url(pocketcasts_custom_url):
    r = requests.get(pocketcasts_custom_url)
    tree = html.fromstring(r.content)
    audio_player_path = '//*[@id="audio_player"]'
    audio_elem = tree.xpath(audio_player_path)[0]
    podcast_url = audio_elem.attrib['src']
    return podcast_url

def download_podcast(url):
    urllib.request.urlretrieve(url, file_name)

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

if __name__ == "__main__":
    pcast_url = config.test_url
    url = get_podcast_file_url(pcast_url)
    start_seconds = int(re.findall('t=\d*', pcast_url)[0][2:])
    file_name = os.path.basename(url)
    
    startTime = start_seconds * 1000
    endTime = startTime + 60000

    download_podcast(url)

    clip_size = 15000

    text = ''
    cnt = 0
    for c in range(startTime,endTime,clip_size):
        cnt += 1
        clip = get_clip(c, c+clip_size,str(cnt))
        r = json.loads(get_transcript(clip).text)
        print(r['DisplayText'])
        text += r['DisplayText']


