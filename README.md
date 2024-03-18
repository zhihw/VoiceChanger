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
   ```
### Running the Application
Navigate to the directory containing `main.py` and `voice_changer.py`.  
Execute the program by running:  
   ```bash
   python main.py
   ```
## Testing the Application

To ensure the Voice Changer Application works as expected, we have included a set of unit tests. These tests cover the core functionalities of the application, including audio processing and effect application. 

### Running Tests

Make sure you have all dependencies installed as mentioned in the [Building and Running the Project](#building-and-running-the-project) section. Once you have your environment set up, you can run the tests to verify the application's behavior.

To execute the tests, navigate to the project directory in your terminal and run:

   ```bash
   python -m unittest unittest.py
   ```

### Example of recording audio and applying a robot effect
   ```bash
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
   ```

### Reflections

Currently, the program faces two main issues: processing speed and accuracy of speech analysis. The app does not support real-time voice changing, but there is still room for improvement in processing speed. For example, using multi-threading technology to process audio data in parallel can significantly reduce the time required for audio processing. In terms of speech analysis, gender judgment mainly relies on average pitch and spectral centroid. Although this method is effective in most cases, it is difficult to explain the complex changes in different human voices based on only these two parameters.

In addition, the current sound effect processing method is to mechanically adjust the audio data. Although it can produce a certain voice changing effect, it is still far from the naturalness of the human voice. If possible, I would like to explore using deep learning model technology to create a more effective voice changer application.



