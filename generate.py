#!/usr/local/bin/python
import midiutil.MidiFile
import subprocess

midi = midiutil.MidiFile.MIDIFile(1)

midi.addTrackName(track=0, time=0, trackName='Track 0')
midi.addTempo(track=0, time=0, tempo=120)
midi.addNote(track=0, channel=0, pitch=60, time=0, duration=1, volume=100)

with open('output.mid', 'wb') as output:
    midi.writeFile(output)

subprocess.check_call(['timidity', 'output.mid', '-Ow', '-o', 'output.wav'])
subprocess.check_call(['lame', 'output.wav', '-b', '64', 'output.mp3'])
subprocess.check_call(['rm', 'output.mid', 'output.wav'])
