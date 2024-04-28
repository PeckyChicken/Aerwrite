import os
import glob
from imports import *

#Colors
BACKGROUND_COLOR = "#EDB26F"
TEXT_BACKGROUND_COLOR = "#AD8351"
SHINE_COLOR = "#EBC7B2"
DANGER_RED_COLOR = "#F32013"


#Text Styling
FONT = "Malgun Gothic"
FONT_SIZE = 15

#Measurements
SCREEN_WIDTH = 750
SCREEN_HEIGHT = 600
NOTE_PAD_MARGIN = 7

#File system
FORBIDDEN_CHARS = r'\/:*?"<>|'
SPLIT_CHARS = (".","!","?","\n",",",":",";")
LINE_ENDS = (".",",","!","?",":",";","(","{","[")

STORAGE_DIR = "notes"
CWD = os.getcwd()

NOTES = glob.glob(f"*.txt",root_dir=f"{CWD}/{STORAGE_DIR}")

NOTE_LIST: dict[str,str] = {}
NOTE_TIMESAVE: dict[str,int] = {}
for note in NOTES:
    note_filepath = f"{CWD}/{STORAGE_DIR}/{note}"
    note_title = "".join(os.path.basename(note).split(".")[:-1])
    with open(note_filepath) as f:
        NOTE_LIST[note_title] = f.read()
        NOTE_TIMESAVE[note_title] = os.stat(note_filepath).st_mtime

params = sys.argv

#sys.argv[1] is the mode inputted by the user.
#Convert this to simple format, and store it in PURPOSE to be used later.
if len(sys.argv) > 1:
    if sys.argv[1] == "--open":
        if len(sys.argv) > 2:
            PURPOSE = "open"
            FILE_NAME = sys.argv[2]
        else:
            PURPOSE = "new"
    elif sys.argv[1] == "--new":
        PURPOSE = "new"
    elif sys.argv[1] == "--list":
        PURPOSE = "list"
    else:
        print(f"Unrecognised option {sys.argv[1]}.")
else:
    PURPOSE = "list"