# Rhythmic Forge
## Virtual Drum Machine
### Submitted By: Shrikrishna Bhat

## Description
This project is a fun project that is a simple drum machine application with a graphical user interface.
This application allows users to play different drum beats, including random beats and beats with reverb effect.
Initially you will get a screen where you can play 2 types of random drum sounds, and you can also play a reverb effect.
You can also open a mixer where you can play different types of drum beats in a GUI.

## How to Run
- First install all the dependencies in the requirements.txt using pip.
```pip install -r requirements.txt```
- To run the project, run the main file.
```python main.py```
- This project is fun if run on IDE. It does not mean it's runnable on command line. (Maybe in IDE it is just simpler to run)
- When you run the project, you will be presented with a window, choose any of the options to play or stop the drum sounds.
- If you want to be a mixer, click on the game option, and you can customize the beats, using ```mouse``` clicks. Both left and right clicks work.
- To close the project (pygame and main UI) close the window, there is no button to stop, it is the default ```x``` button.

## Methodology
### Sound generation
1. Waveform synthesis
   - Sine waves are used to generate tones with harmonic frequencies, mimicking the resonant characteristics of drum-heads and certain percussion instruments.
   - Square waves are employed to create sharp, percussive sounds typical of hi-hats, where the distinct "chick" sound is generated.
2. Noise generation
   - Random noise is utilized to replicate various aspects of percussion sounds.
   - White noise creates the metallic "sizzle" characteristic of hi-hats.
   - Pink noise can emulate the resonant buzz of snare wires or tambourines.
   - Smooth noise is used to generate ambiance, simulating the overall sound environment.
3. Filtering
   - Filters are applied to shape the frequency content of the generated sounds:
   - Low-pass filters emphasize bass frequencies, replicating the thud of kick drums.
   - High-pass or band-pass filters accentuate specific frequency ranges, such as the mid-range frequencies of snare drums or the high frequencies of hi-hats.
   - Filters may also be used to attenuate unwanted frequencies, ensuring a cleaner, more focused sound.
4. Envelope Shaping
   - Envelope functions, such as exponential decay or time-based modulation, are applied to modulate the amplitude of the sounds over time.
   - Decay functions simulate the natural decay of percussion sounds, ensuring a realistic fade-out.
   - Modulation functions add dynamic changes to the sound, creating variations in volume, pitch, or timbre.
5. Combination and Sequencing
   - These individual components are combined and sequenced to create cohesive percussion sounds.
   - Different waveforms, noise sources, and filtering techniques are combined in varying proportions to achieve the desired timbrel qualities of each instrument.
   - Sequencing involves arranging these sounds in time to create rhythmic patterns, with appropriate pauses and accents to simulate natural drumming patterns.
6. Panning
   - In the code, panning is achieved by adjusting the amplitude of the audio signal for each channel based on a specified angle. This angle determines the perceived position of the sound in the stereo field.
   - By applying different panning angles to each percussion instrument, the code simulates the spatial distribution of sound sources within a virtual environment.
7. Instrument Sequencing
   - Instrument sequencing is achieved by generating random patterns or sequences for each percussion instrument. These patterns dictate when each instrument should play (i.e., hit or make a sound) within the overall beat.
   - The generated sequences are then combined, resulting in a cohesive beat or rhythm that comprises multiple percussion instruments playing in synchrony.

### UI
- UI has 5 buttons, 2 to play random beat, 1 to play reverb beat, other to open a mixer that is pygame.
- First part of the UI was designed from tkinter where each button has specific tasks of playing the generated sounds it might be normal drum beat or a reverb.
- Second part of the UI is a mixer developed from pygame. User can select each bit and create a custom beat based on the generated wavfiles. User must use the mouse button to select each beat and can play with it.

## Testing
- Testing is done using the python's built-in unittest framework.
- First test is done using the ```generate_sound()``` function of the ```GenerateBeat``` class. It ensures that the function returns two numpy arrays (beat1 and beat2).
- It checks whether both beat1 and beat2 are instances of numpy arrays, and  verifies that both beat1 and beat2 have a minimum number of non-zero samples using np.count_nonzero and comparing it against a calculated minimum.
- Second test tests the sound generation functions of various drum instruments (e.g., Kick, Snare, HiHat).
- For each instrument, it checks whether the generated sound is a numpy array and whether it has the expected shape.
- 
## Challenges
- The challenges I faced in this were many. Main challenge was to generate diverse sounds.
- Even still there might be some ```grrr``` static noise in some of the beat, I tried various parameters, and it did not fix it.
- There is some bug in the pygame window, sometimes the left click does not work and only right click works. To solve this the classic solution must be employed. Just closing the IDE and opening the project again.
- I had challenges to implement Reverb effect, but had to go with professor's version.
- Second phase of UI that is mixer implementation was a difficult task.
- Some of the traditional sounds like tambourine and tabla still have static noise.

## Sources
- Sources is in a different md file ```sources.md```. [[sources.md]]
