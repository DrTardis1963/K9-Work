from __future__ import print_function
from watson_developer_cloud import ConversationV1
from watson_developer_cloud import SpeechToTextV1
from watson_developer_cloud.websocket import RecognizeCallback
from time import sleep

import os, sys, subprocess, threading, time, re, base64, json, ssl, signal

STTusername = os.environ['WTTSusername']
STTpassword = os.environ['WTTSpassword']
os.environ['WCpassword'] = 'xxxxxx'
os.environ['WCusername'] = 'xxxxxx'
os.environ['WCworkspace'] = 'xxxxxxx'

conversation = ConversationV1(
    username=os.environ['WCusername'],
    password=os.environ['WCpassword'],
    version='2018-02-16')

workspace_id = os.environ['WCworkspace']

speech_to_text = SpeechToTextV1(
    username=STTusername,
    password=STTpassword,
    url='https://stream.watsonplatform.net/speech-to-text/api')

print ("Username: " + str(STTusername))
print ("Password: " + str(STTpassword))

# Example using websockets
class MyRecognizeCallback(RecognizeCallback):
    def __init__(self):
        RecognizeCallback.__init__(self)

    def on_transcription(self, transcript):
        print(transcript)

    def on_connected(self):
        print('Connection was successful')

    def on_error(self, error):
        print('Error received: {}'.format(error))

    def on_inactivity_timeout(self, error):
        print('Inactivity timeout: {}'.format(error))

    def on_listening(self):
        print('Service is listening')

    def on_transcription_complete(self):
        print('Transcription completed')
        finished = True
        

    def on_hypothesis(self, hypothesis):
        print(hypothesis)

finished = False
print ('speak now')
record = "arecord voicedata.wav -d 15 -f S16_LE -r 44100 -t wav"
transcript = "silence"
mycallback = MyRecognizeCallback()
p = subprocess.Popen(record, shell=True)
time.sleep(10)
with open('voicedata.wav') as f:
    speechtext = speech_to_text.recognize_with_websocket(audio=f,content_type='audio/l16; rate=44100', recognize_callback=mycallback)
print ('Audio Transcribed')
response = conversation.message(workspace_id=workspace_id, input={'text':transcript})  # this one
results = re.search('\], u\'text\': \[u\'(.*)\'\]\}, u\'alt', str(response)) # this one
answer = results.group(1) # this one
speak = './tts ' + answer #this one 
subprocess.call(speak, shell=True) # and this one
while not finished:
    time.sleep(0.1)



