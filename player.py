# Modules by me
import carnatic_util
import mohanam



import sys
import optparse

_standard_length = 4


def GetOptions():
    usage = "usage: %prog [options]"
    parser = optparse.OptionParser(usage)

    parser.add_option("-f"
                     ,"--filename"
                     ,action="store"
                     ,type="str"
                     ,default=""
                     ,dest="filename"
                     ,help="filename to read music from (stdin by default)")

    parser.add_option("-q"
                     ,"--qpm"
                     ,action="store"
                     ,type="int"
                     ,default=180
                     ,dest="qpm"
                     ,help="Quarters per minute - an indicator of the beat (180 by default)")

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

    parser.add_option("-p"
                     ,"--pysnth_module"
                     ,action="store"
                     ,type="str"
                     ,default="n"
                     ,dest="pysynth_module"
                     ,help="s uses the string pysynth module (very slow), p the piano with caching (default is the plain piano with no caching), (s and p require numpy/scipy) ")

    (options, args) = parser.parse_args(args=None, values=None)

    # Open the file to be read
    if options.filename == "":
      f = sys.stdin
    else:
      f = open(options.filename, "r")

    return (f, options.qpm, options.output_filename, options.octave, options.pysynth_module)


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

  (read_file_handle, qpm, output_filename, octave, pysynth_module) = GetOptions()

  make_wav = ImportPysynthModule(pysynth_module)

  carnatic_notes = carnatic_util.ReadFromFile(read_file_handle)
  english_notes = []

  for (note, length) in carnatic_notes:
    english_note = mohanam.Translate(note, octave)
    english_notes.append((english_note, length))

  make_wav(english_notes, fn=output_filename, bpm = qpm)

  return

if __name__ == '__main__':
  main()





