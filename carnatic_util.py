#!/usr/bin/evn python

import util

"""A module to help read and carnatic notation"""

def ConvertString(s):
  """ Converts a string of the form
      g , g, r , , , 
      [(g, 8), (g, 8), (r, 16)]
      (assuming tempo = 4) """
  standard_length = 1

  li = s.split()
  notes = []
  previous_note = ''
  previous_length = 0

  for c in li:
    if c != ',':
      notes.append((c, standard_length))
    if c == ',':
      try:
        (previous_note, previous_length) = notes[-1]
      except IndexError:
        print "Does the piece start with a , ? Error."
        return
      notes[-1] = (previous_note, previous_length+standard_length)

  # find the least common multiple of all the lengths
  note_lengths = [b for (a, b) in notes]
  lcm = util.lcm_many(*note_lengths)

  tempo_notes = []
  for (a, b) in notes:
    tempo_notes.append((a, lcm/b))

  return tempo_notes



def PreProcessScore(s):
  """ Remove all the | and the || """
  s = s.replace("|", " ")
  s = s.replace("  ", " ")
  return s

def ReadFromFile(f):
  """ Reads music from a file handle, preprocesses, 
      converts the notes into tempo format and returns"""
  
  s = f.read()
  s = PreProcessScore(s)
  l = ConvertString(s)
  return l

