#!/usr/local/bin/python
import midiutil.MidiFile
import subprocess

midi = midiutil.MidiFile.MIDIFile(1)

midi.addTrackName(track=0, time=0, trackName='Track 0')

# `time` is measured in beats. `tempo` is measured in beats per minute.
midi.addTempo(track=0, time=0, tempo=120)

# 'program' == instrument. Change channel 1 to be something strange.
midi.addProgramChange(track=0, channel=1, time=0, program=64)

# `duration` is measured in beats.
midi.addNote(track=0, channel=0, pitch=60, time=0, duration=1, volume=100)
midi.addNote(track=0, channel=1, pitch=72, time=1, duration=1, volume=100)

with open('output.mid', 'wb') as output:
    midi.writeFile(output)

subprocess.check_call(['timidity', 'output.mid', '-Ow', '-o', 'output.wav'])
subprocess.check_call(['rm', 'output.mid'])
