import queue
import threading
import wave
import pyaudio
from pydub import AudioSegment
from gtts import gTTS
import os
import librosa
from pynput.keyboard import Key, Controller
import keyboard
import msvcrt
import time

def play_audio(audio_file_path):
    global audio_playing

    wf = wave.open(audio_file_path, 'rb')
    p = pyaudio.PyAudio()
    
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    
    chunk_size = 1024
    data = wf.readframes(chunk_size)
    
    while data and audio_playing:
        stream.write(data)
        data = wf.readframes(chunk_size)
    
    audio_playing = False
    stream.stop_stream()
    stream.close()
    p.terminate()

def timer_callback():
    global audio_playing
    audio_playing = False

def Respond(response):
    global audio_playing
    audio_playing = True

    print(response)
    response_audio = gTTS(text=response, lang='en')

    # Save the response audio as an MP3 file
    response_audio.save('responseFile.mp3')

    # Convert the MP3 audio to WAV format using pydub
    audio = AudioSegment.from_mp3('responseFile.mp3')
    audio.export('responseFile.wav', format='wav')
    os.remove('responseFile.mp3')
    timeout = librosa.get_duration(path='responseFile.wav')

    # Specify the path to audio file
    audio_file_path = "responseFile.wav"

    # Create a thread for audio playback
    audio_thread = threading.Thread(target=play_audio, args=(audio_file_path,))
    audio_thread.start()

    timer_thread = threading.Timer(timeout, timer_callback)
    timer_thread.start()

    while audio_playing:
        if msvcrt.kbhit():
            msvcrt.getche()
            audio_playing = False

    audio_thread.join()
    timer_thread.join()
    os.remove('responseFile.wav')