# AUDIO VISUALIZER [AUDIO.PY]
# written by KiwiKodes

import pyaudio
import wave
import numpy as np
import sys
import math
import os
from pathlib import Path
from time import time

#CAUTION: [W] is BROKEN
#Ascii-ify [W] Next Week

version = 'WIP 0.10'

settings = input(f"Welcome to AUDIO.py by KiwiKodes - Current Version: {version}"
                 "\nWould you like to run the [H]istogram or [W]aveform Spectrogram?"
                 "\nPress [Control-C] (or Control-Z on MacOS Only) to Exit at any time. "
                 "\nEnter Input:")



num = 1

CHUNK = 1024

FORMAT = pyaudio.paInt32
CHANNELS = 1

RATE = 44100 # Hz
RECORD_SECONDS = 3

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* Opening microphone...")

frames = []

minimum = np.inf
maximum = -np.inf

vis = np.empty((70, 75), dtype=np.dtype('<U3'))

vis[:, :] = ' '  # set every element to ' ' (spaces)

def histogram(data, arr, minimum, maximum, copy=True):
    thesum = (np.sum(np.abs(data)))

    if thesum < minimum:
        minimum = thesum
    elif thesum > maximum:
        maximum = thesum

    linear_mapping = lambda x: (x - minimum) * (100 - 0) / (maximum - minimum) + 0


    frac = linear_mapping(thesum)
    frac = math.floor(frac/2)
    #print(frac)

    if copy:
        for col in range(0, arr.shape[1]-1):
            arr[:, col] = arr[:, col+1]

    arr[:, -1] = ' '  # set every element to ' ' (spaces)
    arr[len(arr)-int(frac):, -1] = '█'
    #print(len(vis)-int(frac))
    return arr, minimum, maximum

def waveform(data, arr, minimum, maximum):
    #arr[:,:] = ' '  # set every element to ' ' (spaces)

    #fdata = np.fft.fft(data)

    #return waveform(fdata, arr, minimum, maximum, copy=True)

    start = time()
    left, right = np.split(np.abs(np.fft.fft(data)), 2)
    y = np.add(left,right[::-1])
    x = np.arange(len(data)/2, dtype = float)

    if (y < minimum).any():
        minimum = y.min()
    elif (y > maximum).any():
        maximum = y.max()

    linear_mapping = lambda x: (x - minimum) * (100 - 0) / (maximum - minimum) + 0


    frac2 = linear_mapping(y)

    avg_tub = []
    list_of_numberos = np.linspace(0, x.max(), arr.shape[1])
    for n, tub in enumerate(list_of_numberos):
        if n == 0:
            continue
        treadmill = 0
        count_drac = 0
        for m, xsample in enumerate(x):
            if xsample < tub:
                treadmill += frac2[m]
                count_drac += 1
            if xsample >= tub:
                avg_tub.append(treadmill/count_drac)
                break

    print (f'{time()-start} seconds')
    for j in range(arr.shape[1]):
        arr[:, j] = ' '  # set every j to ' ' (spaces)
        arr[len(arr)-int(frac2[j]):, j] = '█'
    return vis, minimum, maximum
#for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
while True:
    data = stream.read(CHUNK)
#    frames.append(data)

    data = np.frombuffer(data, np.int32)

    data = np.array(data,np.int32)

    if settings.lower() == 'w':
        vis, minimum, maximum = waveform(data, vis, minimum, maximum)

    elif settings.lower() == 'h':
        vis, minimum, maximum = histogram(data, vis, minimum, maximum)

    #os.system('clear')

    for row in vis:
        print("".join([(char) for char in row]))

print("* Recording Complete.")

stream.stop_stream()
stream.close()
p.terminate()

outpoot = 'thefifthweek.wav'
outpoot = Path(outpoot)

while outpoot.exists():
    outpoot = str(outpoot)[:-len(outpoot.suffix)]
    outpoot = outpoot + f"_{num}.wav"
    outpoot = Path(outpoot)

    num += 1


wf = wave.open(str(outpoot), 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

#Spare Notes:
#b l o c k █
#75 is god for the WS
#\nVersion {version}"
# minimum = np.inf
#maximum = -np.inf
