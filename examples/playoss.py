from echoplay.player import *
import echonest.audio as audio
import sys

f = sys.argv[1]
p = Player(output='oss') 
af = audio.AudioData(f)
p.play(af)
