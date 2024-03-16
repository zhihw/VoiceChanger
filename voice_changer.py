import pyaudio
import numpy as np
import keyboard
import sounddevice as sd
import scipy.signal as ss
import librosa as lr
import time
from datetime import datetime
from scipy.io import wavfile


def record_voice():
    try:
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16,
                            channels=1,
                            rate=44100,
                            input=True,
                            frames_per_buffer=1024)
        
        frames = []
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
    except Exception as e:
        print(f"An error occurred while recording: {str(e)}")

def wav_generater(data):
    try:
        data = data.astype(np.int16)
        current_time = datetime.now().strftime("%Y%m%d-%H%M")
        filename = f"vc_{current_time}.wav"
        wavfile.write(filename, 44100, data)
        print(f"File saved as {filename}")
    except Exception as e:
        print(f"An error occurred while generating WAV file: {str(e)}")

def remove_noise(data):
    try:
        normalized_data = data / np.max(np.abs(data))
        #Normalize the data
        
        sos_high = ss.butter(4, 300, btype='highpass', fs=44100, output='sos')
        filtered_data1 = ss.sosfilt(sos_high, normalized_data)
        #High pass filter to remove low-frequency noise
        
        sos_low = ss.butter(4, 3400, btype='lowpass', fs=44100, output='sos')
        filtered_data2 = ss.sosfilt(sos_low, filtered_data1)
        #Low pass filter to remove high-frequency noise
        
        restored_data = filtered_data2 * np.max(np.abs(data))
        return restored_data.astype(np.int16)
    
    except Exception as e:
        print(f"An error occurred while removing noise: {str(e)}")

def analyze_audio(data):

    try:
        data = data.astype(float)
        sr = 44100 
        f0, voiced_flag, voiced_probs = lr.pyin(data, fmin=80, fmax=400, sr=sr)
        #Get fundamental frequency from the data using pyin from librosa 

        pitches = f0[voiced_flag]
        avg_pitch = np.mean(pitches) if len(pitches) > 0 else 0

        #Filter for voiced frames and calculate average pitch
        spectral_centroids = lr.feature.spectral_centroid(y=data, sr=sr)
        avg_centroid = np.mean(spectral_centroids)
        #Calculate the average spectral centroid
        
        low_pitch_thres = 80
        high_pitch_thres = 250

        if avg_pitch < low_pitch_thres or avg_pitch > high_pitch_thres:
            print("\nDetected unusual pitch.")
            print("If you want the best voice changer effect, please use a normal speaking voice.")
            print("If you have already spoken normally and the system cannot determine your gender, please enter your gender ('Male' or 'Female').")
            print("If you did not speak normally, please say 'Retry' to delete the previous recording and start a new voice recording:")
            
            while True:
                user_input = input().capitalize()
                if user_input in ['Male', 'Female']:
                    return user_input, avg_pitch
                elif user_input == 'Retry':
                    print("Please start a new voice recording.")
                    return 'Retry', None
                else:
                    print("Invalid input. Please enter 'Male', 'Female', or 'Retry'.")

        elif avg_pitch > 165 and avg_centroid > 1500:
            gender = "Female"
        else:
            gender = "Male"

        return gender, avg_pitch
    except Exception as e:
        print(f"An error occurred while analyzing audio: {str(e)}")
        return None, None
    
def change_gender(data, sr=44100):
    try:
        low_pitch_thres=80
        high_pitch_thres=250
        male_target_pitch = 130
        female_target_pitch = 170
        gender, avg_pitch = analyze_audio(data)

        if gender is None or avg_pitch is 0:
            print("Audio analysis failed or returned None. Unable to change gender.")
            return data.astype(np.int16)
       
            
        if gender == 'Male':
            if avg_pitch < low_pitch_thres or avg_pitch > high_pitch_thres:
                n_steps = 8
            else: 
                n_steps = 12 * np.log2(female_target_pitch / avg_pitch)
            s_rate = 0.9
        elif gender == 'Female':
            if avg_pitch < low_pitch_thres or avg_pitch > high_pitch_thres:
                n_steps = -8
            else:
                n_steps = 12 * np.log2(male_target_pitch / avg_pitch)
            s_rate = 1.1

        # Perform pitch shifting
        data_shifted = lr.effects.pitch_shift(data.astype(float), sr=sr, n_steps=n_steps)
        #Shift pitch
        data_stretched = lr.effects.time_stretch(data_shifted, rate=s_rate)
        #Stretch time
        return data_stretched.astype(np.int16)

    except Exception as e:
        print(f"An error occurred while change_gender: {str(e)}")
        raise e


def play_audio(data, sr=44100):
    try:
        duration = len(data) / sr  # 计算音频播放的总时长（秒）
        sd.play(data, sr)  # 开始播放音频

        start_time = time.time()  # 记录开始播放的时间
        while True:
            current_time = time.time()
            elapsed_time = current_time - start_time

            # 计算播放进度
            progress = elapsed_time / duration
            if progress >= 1.0:
                break  # 当进度达到或超过100%时，退出循环

            # 绘制进度条
            progress_bar_length = 50  # 进度条的长度
            filled_length = int(progress_bar_length * progress)
            bar = '█' * filled_length + '-' * (progress_bar_length - filled_length)
            print(f'\rAudio Playback: |{bar}| {progress * 100:.2f}%', end='\r')

            time.sleep(0.1)  # 每0.1秒刷新一次进度条

        # 确保在退出循环时，进度条显示为 100%
        bar = '█' * progress_bar_length
        print(f'\rAudio Playback: |{bar}| 100.00%', end='\r')
        sd.wait()  # 等待音频播放完成
        print('\nAudio playback completed.')
    except Exception as e:
        print(f"An error occurred while playing audio: {str(e)}")

while True:
    data = record_voice()
    if data is not None:
        data = remove_noise(data)
        analysis_result = analyze_audio(data)
        if analysis_result[0] == 'Retry':
            continue
        elif analysis_result[0] is not None:
            print(analysis_result)
            data = change_gender(data)
            play_audio(data,44100)
            wav_generater(data)
            break