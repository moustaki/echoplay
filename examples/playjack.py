from echoplay.player import *
import echonest.audio as audio
import sys

f = sys.argv[1]
p = Player() 
af = audio.AudioData(f)
p.play(af)
