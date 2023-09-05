import os
import requests
from gtts import gTTS
from playsound import playsound
from elevenlabs import generate, play

# Create mp3 file from text
response = "meow"
language = 'en'

response_audio = gTTS(text=response, lang=language)
response_audio.save('responseFile.mp3')

# Play audio with playsound
playsound('responseFile.mp3')