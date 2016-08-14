#!/usr/local/bin/python
import matplotlib.pyplot as plot

import numpy as np

from pyknon.genmidi import Midi
from pyknon.music import Note, NoteSeq

from scipy.fftpack import fft
from scipy.io import wavfile

import random
import sh

# Notes in a midi file are in the range [0, 120).
kMaxNote = 120

'''
Creates a wav file of a piano playing `note` and writes it to `wav_filename`.
'''
def generateWavFile(note, wav_filename):
    midi = Midi(1, instrument=0, tempo=90)
    midi.seq_notes(NoteSeq([Note(note - 60)]), track=0)
    midi_filename = 'temp.mid'
    midi.write(midi_filename)
    sh.timidity(midi_filename, '-Ow', '-o', wav_filename)
    sh.rm(midi_filename)

'''
Plots the given sequence with matplotlib.
'''
def plotSequence(sequence):
    plot.plot(sequence)
    plot.show(block=True)

'''
Reads a wav file and returns the spectrum of a 0.1-second interval that is
`progress` of the way through the file (e.g., if `progress` were 0.5, halfway
through the file.)
'''
def readSpectrum(wav_filename, progress):
    (sample_rate, data) = wavfile.read(wav_filename)
    samples = data.T[0]
    window = sample_rate / 10
    # Sample from between the first 0.1s and 0.9s of the note.
    start = (0.1 + 0.8 * progress) * min(len(samples), sample_rate) - window/2
    start = min(max(start, 0), len(samples) - window)
    fragment = samples[start:start + window]
    return map(abs, fft(fragment)[:window/2])

'''
Generates a single training sample for our note-classifying network.
The result is a pair (frequencies, note), where frequencies is a
4410-dimensional feature vector (the frequencies of 0.1 seconds of a wav file,
because the default sample rate for wavs is 44100), and the output is a
120-dimensional one-hot encoding of the note.
'''
def sampleLabeledData(note=None, progress=None):
    # The distribution we're sampling from is parametrized by a note to play
    # and by progress, the time into the duration of the note from which we
    # sample the frequencies.
    if note is None:
        note = random.randint(0, kMaxNote - 1)
    if progress is None:
        progress = random.random()
    # Generate the actual training sample.
    wav_filename = 'temp.wav'
    generateWavFile(note, wav_filename)
    features = readSpectrum(wav_filename, progress)
    sh.rm(wav_filename)
    return (
        np.reshape(features, (1, -1)),
        np.reshape([int(x == note) for x in xrange(kMaxNote)], (1, -1))
    )
