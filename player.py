# Modules by me
import carnatic_util
import mohanam
import markov_analyser


import sys
import optparse

_standard_length = 4


def GetOptions():
    usage = "usage: %prog [options] [music score(s)]"
    parser = optparse.OptionParser(usage)


    parser.add_option("-q"
                     ,"--qpm"
                     ,action="store"
                     ,type="int"
                     ,default=180
                     ,dest="qpm"
                     ,help="Quarters per minute - an indicator of the beat (180 by default)")
    
    parser.add_option("-n"
                     ,"--notes"
                     ,action="store"
                     ,type="int"
                     ,default=320
                     ,dest="num_notes"
                     ,help="number of notes to be generated (default 320)")

    parser.add_option("-w"
                     ,"--width"
                     ,action="store"
                     ,type="int"
                     ,default=4
                     ,dest="width"
                     ,help="memory width (in notes) of the state. (default 4 - stores the last 4 notes played)")

    parser.add_option("-t"
                     ,"--octave"
                     ,action="store"
                     ,type="int"
                     ,default=4
                     ,dest="octave"
                     ,help="The octave to generate music at (default 4)")

    parser.add_option("-o"
                     ,"--output_file"
                     ,action="store"
                     ,type="str"
                     ,default="output.wav"
                     ,dest="output_filename"
                     ,help="wav output filename ('output.wav' by default)")

    parser.add_option("-s"
                     ,"--output_score"
                     ,action="store"
                     ,type="str"
                     ,default="score_output.txt"
                     ,dest="output_score_file"
                     ,help="prints the output score ('score_output.txt' by default)")

    parser.add_option("-p"
                     ,"--pysnth_module"
                     ,action="store"
                     ,type="str"
                     ,default="n"
                     ,dest="pysynth_module"
                     ,help="s uses the string pysynth module (very slow), p the piano with caching (default is the plain piano with no caching), (s and p require numpy/scipy) ")

    (options, args) = parser.parse_args(args=None, values=None)

    # Open the file to be read
    
    if args is []:
      print "Reading Music from stdin since no files were given"
      file_handles = [sys.stdin]
    else:
      file_handles = [open(x, "r") for x in args]

    return (file_handles, options.qpm, options.output_filename, options.octave, options.num_notes, options.width, options.output_score_file, options.pysynth_module)



def ImportPysynthModule(c):
  try:
    if c == 'p':
      import pysynth_b as pysynth
    elif c == 's':
      import pysynth_s as pysynth
    else:
      import pysynth as pysynth
  except ImportError, e:
    print "Error Importing pysynth"
    print e

  make_wave = pysynth.make_wav

  return make_wave


def main():

  (read_file_handles, qpm, output_filename, octave, num_notes, width, output_score_file, pysynth_module) = GetOptions()

  make_wav = ImportPysynthModule(pysynth_module)

  carnatic_songs= []
  for f in read_file_handles:
    s = f.read()
    song = carnatic_util.CollectNotes(carnatic_util.PreProcessScore(s))
    carnatic_songs.append(song)
    f.close()

  markov_song_generator = markov_analyser.MarkovAnalyser(width)

  print "Reading Songs.."
  for song in carnatic_songs:
    markov_song_generator.AddSong(song)
  
  print "Analysing Songs.."
  markov_song_generator.MarkovAnalyse()
  print "Generating Song.."
  markov_song_generator.MarkovGenerate(num_notes)
  generated_song = markov_song_generator.GetGeneratedSong(output_score_file)
  generated_song = carnatic_util.ConvertLengthToTempo(generated_song)
  
  print "Converting to WAV.."
  english_notes = []

  for (note, length) in generated_song:
    english_note = mohanam.Translate(note, octave)
    english_notes.append((english_note, length))

  make_wav(english_notes, fn=output_filename, bpm = qpm)

  return

if __name__ == '__main__':
  main()





