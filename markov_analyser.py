#!/usr/bin/env python

import carnatic_util
import mohanam
import random


class MarkovAnalyser:
  def __init__(self, width=4):
    self.width = width
    self.ascend_descend_probability = 0.3
    self.songs = []
    self.markov_state_space = {}

    self.NumberNotes(mohanam.notes)
    return
  
  def SetAscendDescendProbability(self, prob):
    self.ascend_descend_probability = prob
    return

  def SetAscendProbability(self, des):
    self.descend_probability = des
    return

  def NumberNotes(self, notes):
    numberings = []
    l = len(notes)
    for i in range(l):
      numberings.append((notes[i]+"."     , i))       # Lower Octave
      numberings.append((notes[i]         , i+l))   # Current Octave
      numberings.append((notes[i].upper() , i+2*l)) # Higher Octave

    self.notes_to_numbers = dict([(a, b) for (a,b) in numberings])
    self.numbers_to_notes = dict([(b, a) for (a,b) in numberings])
    return

  def IncrementNote(self, note):
    note, l = note.split()
    n = self.notes_to_numbers[note]
    n += 1
    if n == self.notes_to_numbers["D"]:
      n -= 1
    return self.HashNote((self.numbers_to_notes[n], 1))

  def DecrementNote(self, note):
    note, l = note.split()
    n = self.notes_to_numbers[note]
    n -= 1
    if n == self.notes_to_numbers["s."]:
      n += 1
    return self.HashNote((self.numbers_to_notes[n], 1))

  def HashNote(self, (a, b)):
    return a + " " + str(b)
  
  def UnHashNote(self, s):
    (a, b) = s.split()
    b = int(b)
    return (a, b)

  def AddSong(self, notes):
    song = []
    for (note, length) in notes:
      song.append(self.HashNote((note, length)))

    self.songs.append(song)
    return
  
  def MakeKeyFromNotes(self, notes):
    """ Makes an immutable string from the given notes played 
    that can be used as a hash key"""
    return '|'.join(notes)


  def MarkovAnalyse(self):
    """ Analyse the songs given, so that we have 
        a dictionary from last `width` notes played
        to the next possible note """
    for song in self.songs:
      for i in range(len(song) - self.width-1):
        key = self.MakeKeyFromNotes(song[i:i+self.width])
        try:
          self.markov_state_space[key].append(song[i+1])
        except KeyError:
          self.markov_state_space[key] = [song[i+1]]

    return

  def GenerateStartingNotes(self):
    song = random.choice(self.songs)
    random_start_index = random.randint(0, len(song) - self.width - 2)
    # print random_start_index
    return song[random_start_index:random_start_index+self.width]

  def ChooseFirstWithProbability(self, a, b, p):
    roll = random.uniform(0, 1)
    if roll <= p:
      return a
    else:
      return b

  def PerturbNote(self, notes):
    last_note = notes[-1]
    (up_note, down_note) = (self.IncrementNote(notes[-1]) ,self.DecrementNote(notes[-1]))

    if notes[-2] == up_note:
      perturbed_note = self.ChooseFirstWithProbability(down_note, up_note, 0.75)
    elif notes[-2] == down_note:
      perturbed_note = self.ChooseFirstWithProbability(up_note, down_note, 0.75)
    else:
      perturbed_note = self.ChooseFirstWithProbability(up_note, down_note, 0.5)

    perturbed_note = self.ChooseFirstWithProbability(notes[-1], perturbed_note, 0.2)
    (s, l) = self.UnHashNote(perturbed_note)
    # Choose length according to the following distribution
    l = random.choice([1,1,1,1,2,2,3,4])
    # print "perturbed_note is", perturbed_note
    perturbed_note = self.HashNote((s, l))

    return perturbed_note


  def MarkovGenerate(self, song_length=100):
    notes = self.GenerateStartingNotes()

    i = 0
    while i+self.width < song_length:
      key = self.MakeKeyFromNotes(notes[-self.width:])

      perturbed_note = self.PerturbNote(notes[-self.width:])

      if self.markov_state_space.has_key(key):
        next_note = random.choice(self.markov_state_space[key])
        next_note = self.ChooseFirstWithProbability(perturbed_note, next_note, self.ascend_descend_probability)
      else:
        next_note = perturbed_note
        
      notes.append(next_note)
      (n, l) = self.UnHashNote(next_note)
      i+=l

    # print notes 
    self.generated_song = notes
    return

  def WriteToFile(self, song, filename="temp.song.swp"):
    print "Writing a copy to %s"%filename
    f = open(filename, "w")
    l = 0
    for (s, r) in song:
      f.write(s.ljust(3))
      l += 1
      if l%16 == 0:
        f.write("\n")

      for i in range(r-1):
        f.write(",".ljust(3))
        l += 1
        if l%16 == 0:
          f.write("\n")

    f.close()
    return

  def GetGeneratedSong(self, filename):
    song = [self.UnHashNote(n) for n in self.generated_song]
    # print song
    print filename
    self.WriteToFile(song, filename)
    return song




