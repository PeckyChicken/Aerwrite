from imports import *
from constants import PURPOSE
pygame.mixer.init()


sounds: dict[str,mixer.Sound] = {}
sound_names = ["open","quit","save","typing1","typing2"]

def add_sound(sound_name):
    sounds[sound_name] = mixer.Sound(f"{__file__}/../sounds/{sound_name}.wav")

for sound in sound_names:
    add_sound(sound)

mixer.Sound.play(sounds["open"])

    
