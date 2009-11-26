#!/usr/bin/env python

""" A module to translate notes in mohanam, to the ABC notation"""


# We write s  r  g  p  d  s  for the notes in the current octave
# We write S  R  G  P  D  S  in the higher octave
# We write s. r. g. p. d. s. in the lower octave

notes = [s for s in "srgpd"]
mapping = { 's' : 'c'
          , 'r' : 'd'
          , 'g' : 'e'
          , 'p' : 'g'
          , 'd' : 'a'}

def Translate(note, octave=4):
  if len(note) == 2 and note[1] == ".":
    octave = octave - 1
  if note.isupper():
    note = note.lower()
    octave += 1
  
  try:
    return mapping[note[0]] + str(octave)
  except KeyError:
    print "The note %s could not be converted. Is it in mohanam? Error?"%(note)
    return

