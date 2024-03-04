import pyaudio
import numpy as np
import keyboard

def record_voice():
    audio = pyaudio.PyAudio()
    
    stream = audio.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=44100,
                        input=True,
                        frames_per_buffer=1024)
    frames=[]
    print("Recording started. Press 'Esc' key to stop recording.")
    while True:
        if keyboard.is_pressed('esc'):  
            print("Recording stopped.")
            break
        data = stream.read(1024, exception_on_overflow=False)
        frames.append(np.frombuffer(data, dtype=np.int16))