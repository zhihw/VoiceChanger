import pyaudio
import numpy as np
import keyboard
import sounddevice as sd
import scipy.signal as ss
import librosa as lr
import time
from datetime import datetime
from scipy.io import wavfile


def wav_generater(data):
    #Generate wav file using data
    try:
        data = data.astype(np.int16)
        current_time = datetime.now().strftime("%Y%m%d-%H%M")
        filename = f"vc_{current_time}.wav"
        wavfile.write(filename, 44100, data)
        print(f"File saved as {filename}")
    except Exception as e:
        print(f"An error occurred while generating WAV file: {str(e)}")


def read_wav_file(filename):
    #Read wav file
    try:
        sr, data = wavfile.read(filename)
        data = data.astype(np.int16)
        return data
    except Exception as e:
        print(f"An error occurred while reading WAV file: {str(e)}")
        return None


def low_pass_filter(data, sr, cutoff):
    #Low pass filter
    try:
        sos = ss.butter(10, cutoff, fs=sr, btype='low', output='sos')
        filtered_data = ss.sosfilt(sos, data)
        return filtered_data
    except Exception as e:
        print(f"An error occurred in low_pass_filter: {str(e)}")

def high_pass_filter(data, sr, cutoff):
    #High pass filter
    try:
        sos = ss.butter(10, cutoff, fs=sr, btype='high', output='sos')
        filtered_data = ss.sosfilt(sos, data)
        return filtered_data
    except Exception as e:
        print(f"An error occurred in high_pass_filter: {str(e)}")
    

def record_voice():
    #This function records the input sound data in mono and at a sampling rate of 44100. 
    #It reads 1024 frames of data from the audio stream each time until the user presses the Esc key to stop recording.
    #Then, it merges the data into a NumPy array and returns this array.
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


def play_audio(data, sr=44100):
    #Use sounddevice play and wait to play sounds and simulate the effect of the progress bar.
    try:
        duration = len(data) / sr  
        sd.play(data, sr)  

        start_time = time.time()  
        while True:
            current_time = time.time()
            elapsed_time = current_time - start_time
            progress = elapsed_time / duration
            if progress >= 1.0:
                break  
            
            progress_bar_length = 50  
            filled_length = int(progress_bar_length * progress)
            bar = '█' * filled_length + '-' * (progress_bar_length - filled_length)
            print(f'\rPlay Audio: |{bar}| {progress * 100:.2f}%', end='\r')
            time.sleep(0.1)  
        bar = '█' * progress_bar_length
        print(f'\rPlay Audio: |{bar}| 100.00%', end='\r')
        sd.wait()  
        print('\ncompleted.')
    except Exception as e:
        print(f"An error occurred while playing audio: {str(e)}")


def remove_noise(data):
    #The frequency range from 300 Hz to 3400 Hz is the standard frequency bandwidth for human voice communication. This function will filter out irrelevant sounds based on this range.
    try:
        normalized_data = data / np.max(np.abs(data))
        #Normalize the data
        
        filtered_data1 = high_pass_filter(normalized_data, 44100, cutoff=300)
        #High pass filter to remove low-frequency noise
        
        filtered_data2 = low_pass_filter(filtered_data1, 44100, cutoff=3400)
        #Low pass filter to remove high-frequency noise
        
        clear_data = filtered_data2 * np.max(np.abs(data))
        #denormalization

        return clear_data.astype(np.int16)
    
    except Exception as e:
        print(f"An error occurred while removing noise: {str(e)}")


def analyze_audio(data):
 #The function determines the gender of the voice by analyzing the pitch and spectral centroid, calculating the average pitch of the voiced frames and the average spectral centroid of the audio.
 #The threshold of 165 for the pitch was established through multiple tests, under the premise of normal speech. 
 #Pitches lower than 80 or higher than 300 typically occur when speaking intentionally loud or soft. 
 #In this case，to accurately determine the gender, manual confirmation from the user is required.
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
        high_pitch_thres = 300

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
    #This function uses pitch shifting and time stretching techniques to simulate the voice characteristics of another gender, in addition to using filters to enhance the effect. 
    #The number of steps for pitch shifting has a base value, which is then fine-tuned dynamically based on the target pitch and the current pitch. 
    #The time stretch ratio, however, is fixed.
    #In special cases where the pitch falls below 80 or above 300, to prevent excessive pitch correction, the number of steps is adjusted to a fixed value.
    try:
        low_pitch_thres=80
        high_pitch_thres=300
        male_target_pitch = 130
        female_target_pitch = 240
        gender, avg_pitch = analyze_audio(data)

        if gender is None or avg_pitch == 0:
            print("Audio analysis failed or returned None. Unable to change gender.")
            return data.astype(np.int16)
       
            
        if gender == 'Male':
            if avg_pitch < low_pitch_thres or avg_pitch > high_pitch_thres:
                n_steps = 8 #special cases for male is 8
            else: 
                base_n_steps = 5 #base value for male is 5
                pitch_diff = female_target_pitch - avg_pitch
                n_steps_adjustment = pitch_diff / 50 
                n_steps = base_n_steps + n_steps_adjustment
            s_rate = 0.9
        elif gender == 'Female':
            if avg_pitch < low_pitch_thres or avg_pitch > high_pitch_thres:
                n_steps = -8 #special cases for female is -8
            else:
                base_n_steps = -3  #base value for female is -3
                pitch_diff = avg_pitch - male_target_pitch  
                n_steps_adjustment = pitch_diff / 50
                n_steps = base_n_steps - n_steps_adjustment
            s_rate = 1.1

        # Perform pitch shifting
        data_shifted = lr.effects.pitch_shift(data.astype(float), sr=sr, n_steps=n_steps)
        #Shift pitch
        data_stretched = lr.effects.time_stretch(data_shifted, rate=s_rate)
        #Stretch time
        if gender == 'Male':
            data_stretched = high_pass_filter(data_stretched, sr, cutoff=500)
        #Use a high-pass filter to filter low-frequency sounds and further emphasize high-frequency sounds
        elif gender == 'Female':
            data_stretched = low_pass_filter(data_stretched, sr, cutoff=2000) 
        return data_stretched.astype(np.int16),n_steps
        #Use a low-pass filter to filter high-frequency sounds and further emphasize low-frequency sounds
    except Exception as e:
        print(f"An error occurred while changing voice gender: {str(e)}")
        raise e
    


def robot_effect(data, mod_freq=270):
    #Simulate the effect of electronic or mechanical sounds by adding modulated sine waves to the original sound.

    gender, avg_pitch = analyze_audio(data)
    if gender is None or avg_pitch == 0:
        print("Audio analysis failed or returned None. Unable to add robot effect.")
        return data.astype(np.int16)
    
    target_pitch = (130 + 240) / 2  
    pitch_diff = target_pitch - avg_pitch
    n_steps = pitch_diff / 30
    neutral_voice = lr.effects.pitch_shift(data.astype(float), sr=44100, n_steps=n_steps)
    #Dynamically defining n_steps values makes the audio sound relatively neutral

    t = np.arange(len(neutral_voice)) / 44100
    robot_mod = 0.8 * np.sin(2 * np.pi * mod_freq * t) + 0.2#Ensure that the amplitude range is between 0 and 1
    robot_voice = np.multiply(neutral_voice, robot_mod)
    #Generates a sine wave that modulates the signal with slight fluctuations and applies it point by point to the data to simulate a mechanical feel.
    
    return robot_voice.astype(np.int16)


def child_effect(data):
    #Make your sound younger with pitch adjustment and high-pass filter
    
    child_voice = lr.effects.pitch_shift(data.astype(np.float32), sr=44100, n_steps=4)
    #Adjust the pitch upward to achieve a younger-sounding effect

    filtered_data = high_pass_filter(child_voice, sr=44100, cutoff=800)
    #Make the sound brighter with a high-pass filter

    return filtered_data.astype(np.int16)


while True:
    data=read_wav_file("llow.wav")
    #play_audio(data)
    #data=record_voice()
    #wav_generater(data)
    if data is not None:
        data = remove_noise(data)
        analysis_result = analyze_audio(data)
        if analysis_result[0] == 'Retry':
            continue
        elif analysis_result[0] is not None:
            print(analysis_result)
            data =  child_effect(data)
            
           
            while(1):
                play_audio(data)
                #wav_generater(data)
            break