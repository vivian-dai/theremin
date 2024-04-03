# theremin

## Background
I'm too poor to make a [pyrophone](https://en.wikipedia.org/wiki/Pyrophone) and too incompetent at physics to design an [ocarina](https://en.wikipedia.org/wiki/Ocarina) so here I am.... making a [theremin](https://en.wikipedia.org/wiki/Theremin).

## Setup
1. Run `pip install -r requirements.txt` to install all necessary libraries
2. Look through [`config.yml`](./config.yml) and set any variables you may want set

## Dependencies
Some weird nitpicky things about the libraries I'm using:
1. mediapipe above 0.10.9 doesn't work
2. Python above 3.11 doesn't work (and there's probably a lower bound too but I have yet to try)

## Usage/Instruction Manual
1. Run [`main.py`](./src/main.py) in the `/src/` folder
2. The way a theremin works: 
   1. left hand controls the volume and right hand controls pitch
   2. the volume is controlled based on the y position of the left hand
      1. higher up means louder
      2. lower down means quieter
   3. the pitch is controlled by the x position of the right hand
      1. closer to the right edge means higher pitch
      2. closer to the middle means lower pitch
      3. being on the left side of the screen will not produce sound
3. Enjoy! :)
