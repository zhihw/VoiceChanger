import pyaudio
import numpy as np
import keyboard
import sounddevice as sd
import scipy.signal as ss
from datetime import datetime
from scipy.io import wavfile
import librosa as lr

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
        f0, voiced_flag, voiced_probs = lr.pyin(data, fmin=80, fmax=400, sr=44100)
        #Get fundamental frequency from the data using pyin from librosa 
        pitches = f0[voiced_flag]
        avg_pitch = np.mean(pitches) if len(pitches) > 0 else 0
        #Filter for voiced frames and calculate average pitch
        spectral_centroids = lr.feature.spectral_centroid(y=data, sr=44100)
        avg_centroid = np.mean(spectral_centroids)
        #Calculate the average spectral centroid
        
        if avg_pitch > 165 and avg_centroid > 1500:
            gender = "Female"
        else:
            gender = "Male"
        return gender
    except Exception as e:
        print(f"An error occurred while analyzing audio: {str(e)}")
        
def change_gender(data):
    gender = analyze_audio(data)
    if gender == 'Male':
         # Change a male voice to a female, increase pitch
        n_steps = 8 
        s_rate=0.9
    elif gender == 'Female':
        # Change a female voice to a male, decrease pitch
        n_steps = -8  
        s_rate=1.1
    # Perform pitch shifting
    data_shifted = lr.effects.pitch_shift(data.astype(float), sr=44100, n_steps=n_steps) 
    #Shift pitch
    data_stretched=lr.effects.time_stretch(data_shifted, rate=s_rate)
    #Stretch time
    return data_stretched.astype(np.int16)


def play_audio(data):
    try:
        pass 
    except Exception as e:
        print(f"An error occurred while playing audio: {str(e)}")

data = record_voice()
if data is not None:
    data = remove_noise(data)
    if data is not None:
        print(analyze_audio(data))
        data=change_gender(data)
        sd.play(data)
        sd.wait()
        wav_generater(data)