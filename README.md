# Voice Changer Application

## Author: zhihao wang

### Description
The Voice Changer Application is a sound processing tool designed to allow users to record voices, import existing sound files, and apply a variety of sound effects such as gender transformation, robot effects, and child voices.

### How It Works
The application operates by capturing audio input through a microphone or importing audio files in WAV format. Users can select the desired audio effect to apply. The application processes the audio data using various filtering and transformation techniques to achieve effects like noise reduction, pitch alteration, and more. The processed audio can then be previewed by the user and saved for future use.

### Building and Running the Project
1. **Prerequisites**: Ensure Python 3.x is installed on your system.
2. **Dependencies**: Install the necessary Python libraries by running:
   ```bash
   pip install pyaudio numpy keyboard sounddevice scipy librosa datetime

### Running the Application
Navigate to the directory containing `main.py` and `voice_changer.py`.  
Execute the program by running:  
```bash
python main.py

### Example of Operation

```bash
# Example of recording audio and applying a robot effect
> python main.py
[1] Record Voice
[2] Import WAV File
> 1
"Recording... Press 'Esc' to stop."
"Recording stopped."
[1] Original
[2] Gender Transformation
[3] Robot Effect
[4] Child Voice
> 3
"Applying Robot Effect... Done."

