import pyaudio
import numpy as np
import keyboard
import sounddevice as sd
import scipy.signal as ss
from datetime import datetime
from scipy.io import wavfile
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
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    audio_data = np.concatenate(frames)
    
    return audio_data  

def wav_generater(data):
    data = data.astype(np.int16)
    current_time = datetime.now().strftime("%Y%m%d-%H%M")
    filename = f"vc_{current_time}.wav"
    wavfile.write(filename, 44100, data) #The wav files generated each time are in vc_currenttime format
    print(f"File saved as vc_current time")

def remove_noise(data):
    data = data / np.max(np.abs(data))#normalized data
    
    sos = ss.butter(4, [300,3400], btype='band', fs=44100, output='sos')
    data = ss.sosfilt(sos, data)#Use bandpass filters to reduce noise

    data = data * np.max(np.abs(data))
    return data.astype(np.int16)
    #后续可以添加谱减法继续降噪

def analyze_audio(data):
    pass #分析声音性别，返回性别通过bool

def change_gender(data):
    pass #改变声音性别

def play_audio(data):
    pass #播放音频，实现进度条
data = record_voice() 
data = remove_noise(data) 
sd.play(data) 
sd.wait()  
wav_generater(data)