#!/usr/local/bin/python
from pyknon.genmidi import Midi
from pyknon.music import NoteSeq

import sh

notes1 = NoteSeq('D4 F#8 A Bb4')
midi = Midi(1, instrument=40, tempo=90)
midi.seq_notes(notes1, track=0)
midi.write('output.mid')

sh.timidity('output.mid', '-Ow', '-o', 'output.wav')
sh.rm('output.mid')
