#!/usr/bin/python3
import urllib.request
import os, re, json
from pydub import AudioSegment
from pydub.silence import detect_silence
import requests
import config
import urllib.parse as urlparse
from lxml import html
from io import BytesIO

class PodcastSnippet:
    
    def __init__(self, pcast_url):
        self.pcast_url = pcast_url
        r = requests.get(self.pcast_url)
        tree = html.fromstring(r.content)
        audio_player_path = '//*[@id="audio_player"]'
        audio_elem = tree.xpath(audio_player_path)[0]
        self.url = audio_elem.attrib['src']

    def download(self):
        r = requests.get(self.url, stream=True)
        full_podcast = BytesIO(r.content)
        self.full_podcast = full_podcast
        return self.full_podcast

    def get_clip(self, file, startTime, endTime):
        clip = AudioSegment.from_mp3(file)
        extract = clip[startTime*1000:endTime*1000]
        self.extract = extract
