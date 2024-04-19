from imports import *
from constants import PURPOSE
import guis
pygame.mixer.init()



last_text = guis.text_box.get("1.0","end")

sounds: dict[str,mixer.Sound] = {}
sound_names = ["open","quit","save","typing1","typing2"]

def add_sound(sound_name):
    sounds[sound_name] = mixer.Sound(f"{__file__}/../sounds/{sound_name}.wav")

for sound in sound_names:
    add_sound(sound)

mixer.Sound.play(sounds["open"])


def type_sound(_=None):
    global last_text
    cur_text = guis.text_box.get("1.0","end")
    if PURPOSE == "list":
        return
    if cur_text == last_text:
        return
    guis.window.title("*AerWrite*")
    last_text = cur_text
    mixer.Sound.play(sounds[f"typing{random.randint(1,2)}"])
    
