import time
import boto3
from snipper import PodcastSnippet
import config
from io import BytesIO
import re, json, uuid, os
import requests

def transcribe(job_name, clip_url):
    transcribe = boto3.client('transcribe')
    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': clip_url},
        MediaFormat='mp3',
        LanguageCode='en-US'
    )
    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        print("Not ready yet...")
        time.sleep(5)
        
    print(status)
    return status

def get_clip_save_to_s3(url):
    ep_snip = PodcastSnippet(url)
    start_seconds = int(re.findall('t=\d*', config.test_url)[0][2:])
    ep_snip.get_clip(ep_snip.download(), start_seconds, start_seconds + 120)

    output_file = BytesIO()
    ep_snip.extract.export(output_file)
    output_file.seek(0)

    s3 = boto3.resource('s3')
    file_name = os.path.basename(ep_snip.url) + str(uuid.uuid4().hex[:4])
    s3.meta.client.put_object(Key=file_name, Body=output_file, Bucket=config.bucket_name)
    
    return file_name


def get_transcription_text(job_name):
    transcribe = boto3.client('transcribe')
    r = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    transcript_uri = r['TranscriptionJob']['Transcript']['TranscriptFileUri']
    transcript_text = json.loads(requests.get(transcript_uri).text)['results']['transcripts'][0]['transcript']
    return transcript_text

def name_job():
    return 'job_' + str(uuid.uuid4().hex)

    
if __name__ == '__main__':
    clip = get_clip_save_to_s3('https://pca.st/V2Al#t=116')
    clip_url = config.bucket_url + clip

    transcription_job = name_job()
    
    transcribe(transcription_job, clip_url)
    text = get_transcription_text(transcription_job)







    
