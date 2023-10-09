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

Threads_running = True

def play_audio(audio_file_path):
    global Threads_running

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
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    audio_playing = True

def get_input(foo, channel):
    while Threads_running:
        response = input()
        channel.put(response)

def Respond(response):
    global Threads_running

    print(response)
    response_audio = gTTS(text=response, lang='en')

    # Save the response audio as an MP3 file
    response_audio.save('responseFile.mp3')

    # Convert the MP3 audio to WAV format using pydub
    audio = AudioSegment.from_mp3('responseFile.mp3')
    audio.export('responseFile.wav', format='wav')
    os.remove('responseFile.mp3')
    timeout = librosa.get_duration(path='responseFile.wav')

    # Specify the path to your audio file
    audio_file_path = "responseFile.wav"

    # Create a thread for audio playback
    audio_thread = threading.Thread(target=play_audio, args=(audio_file_path,), daemon=True)
    audio_thread.start()
    
    # Start awaiting input on seperate thread
    channel = queue.Queue()
    input_thread = threading.Thread(target=get_input, args=("", channel), daemon=True)
    input_thread.start()

    # Wait for either an input or the duration to expire
    try:
        channel.get(True, timeout)
    except queue.Empty:
        pass

    Threads_running = False
    audio_thread.join()
    os.remove('responseFile.wav')