import os
try:
    os.system("timeout --k 8 8 aplay coolSong.wav")
except:
    print("Audio except")
print("Audio test end")
