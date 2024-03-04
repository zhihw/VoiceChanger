import pyaudio
import numpy as np
import keyboard
import sounddevice as sd
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
    
    return 44100, audio_data  
def wav_generater(data):
    pass #生成wav

def remove_noise(data):
    pass #预处理，消除噪音，返回处理后的声音数据

def analyze_audio(data):
    pass #分析声音性别，返回性别通过bool

def change_gender(data):
    pass #改变声音性别

def play_audio(data):
    pass #播放音频，实现进度条
rate, data = record_voice()  
sd.play(data, rate) 
sd.wait()  