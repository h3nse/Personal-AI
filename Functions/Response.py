import os
import sys
from sys import stdout
import wave
import pyaudio
import threading
import io
from pydub import AudioSegment
from gtts import gTTS
import queue
import time

# Play audio
audio_playing = True

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
    
    stream.stop_stream()
    stream.close()
    p.terminate()

def get_input(message, channel):
    response = input(message)
    channel.put(response)

def input_with_timeout(message, timeout, audio_thread):
    global audio_playing

    channel = queue.Queue()
    thread = threading.Thread(target=get_input, args=(message, channel))
    # by setting this as a daemon thread, python won't wait for it to complete
    thread.daemon = True
    thread.start()

    try:
        channel.get(True, timeout)
        audio_playing = False
        audio_thread.join()
        os.remove('responseFile.wav')
    except queue.Empty:

        pass
    return None

def respond(response):
    print(response)

    response_audio = gTTS(text=response, lang='en')

    # Save the response audio as an MP3 file
    response_audio.save('responseFile.mp3')

    # Convert the MP3 audio to WAV format using pydub
    audio = AudioSegment.from_mp3('responseFile.mp3')
    audio.export('responseFile.wav', format='wav')
    os.remove('responseFile.mp3')

    # Play audio 
    # Specify the path to your audio file
    audio_file_path = "responseFile.wav"

    # Create a thread for audio playback
    audio_thread = threading.Thread(target=play_audio, args=(audio_file_path,))
    audio_thread.start()

    input_with_timeout("Press enter to skip", 5, audio_thread)

    sys.stdout.write("\033[F")
    sys.stdout.write("\033[K")
    print('')

respond("Hello, Test, Test Test. Test. Test. Test")