from typing import Callable
import constants
import guis
import sounds
from constants import BACKGROUND_COLOR, CWD, SHINE_COLOR, STORAGE_DIR, TEXT_BACKGROUND_COLOR
from guis import window
from imports import *

modifiers = {
    0x0001: 'Shift',
    0x0002: 'Caps Lock',
    0x0004: 'Control',
    0x0008: 'Left-hand Alt',
    0x0010: 'Num Lock',
    0x0080: 'Right-hand Alt',
}

def create_file_name(text: str):
    for x in constants.SPLIT_CHARS:
        text = text.lstrip(x)
        text = text.split(x)[0]
    for x in constants.FORBIDDEN_CHARS:
        text = text.replace(x,"_")
    while os.path.exists(f"{CWD}/{STORAGE_DIR}/{text}"):
        text += "V1"
    return text

def save(file=None,e=None):
    try:
        if constants.PURPOSE == "list":
            return
        text = guis.text_box.get("1.0","end").strip()
        if text == "":
            return
        window.title("AerWrite")
        guis.text_box.config(background=constants.SHINE_COLOR)
        window.update()
        mixer.Sound.play(sounds.sounds["save"])
        if constants.PURPOSE == "new":
            name = create_file_name(text)
        else:
            name = constants.FILE_NAME
        with open(f"{CWD}/{STORAGE_DIR}/{name}.txt","w") as file:
            file.write(text)
    finally:
        window.after(500,lambda: guis.text_box.config(background=constants.TEXT_BACKGROUND_COLOR))


def close(_=None):
    mixer.Sound.play(sounds.sounds["quit"]) 
    window.after(500,window.destroy)

def confirm_close(_=None):
    if "*" in window.wm_title():
        confirm_dialog = tk.Toplevel(window,bg=constants.TEXT_BACKGROUND_COLOR)
        mixer.Sound.play(sounds.sounds["open"])
        confirm_dialog.title("Note not saved!⚠️")
        confirm_dialog.resizable(0,0)
        confirm_dialog.geometry("350x200")
        confirm_dialog.iconbitmap(f"{__file__}/../icon.ico")
        confirm_dialog.focus()

        destroy: Callable = lambda _=None:(mixer.Sound.play(sounds.sounds["quit"]),confirm_dialog.destroy())
        close_with_save: Callable = lambda _=None:(confirm_dialog.destroy(),save(),close())
        close_without_save: Callable = lambda _=None:(confirm_dialog.destroy(),close())

        warning = tk.Label(confirm_dialog,text="Your note is unsaved. Save?",font=(constants.FONT,constants.FONT_SIZE),bg=constants.TEXT_BACKGROUND_COLOR)
        buttons = tk.Frame(confirm_dialog,background=TEXT_BACKGROUND_COLOR)
        save_button=tk.Button(buttons,text="Save (Enter)",command=close_with_save,bg=BACKGROUND_COLOR,font=(constants.FONT,constants.FONT_SIZE-2),width=10,relief="sunken")
        quit_button=tk.Button(buttons,text="Don't save (X)",command=close_without_save,bg=BACKGROUND_COLOR,font=(constants.FONT,constants.FONT_SIZE-2),width=10)
        cancel_button=tk.Button(buttons,text="Cancel (C)",command=destroy,bg=BACKGROUND_COLOR,font=(constants.FONT,constants.FONT_SIZE-2),width=10)

        warning.pack()
        cancel_button.pack(side="right",padx=5)
        quit_button.pack(side="right",padx=5)
        save_button.pack(side="left",padx=5)
        buttons.pack(side="bottom",pady=50)
        confirm_dialog.bind("<Return>",close_with_save)

        confirm_dialog.bind("x",close_without_save)
        confirm_dialog.bind("X",close_without_save)

        confirm_dialog.bind("c",destroy)
        confirm_dialog.bind("C",destroy)
        confirm_dialog.bind("<Escape>",destroy)
        confirm_dialog.protocol("WM_DELETE_WINDOW",destroy)
    else:
        close()

        

window.bind("<Escape>", confirm_close)
window.protocol("WM_DELETE_WINDOW", confirm_close)
window.bind("<Control-Key-s>",lambda e: save(e=e))
window.bind("<Control-Key-S>",lambda e: save(e=e))
window.bind("<Control-Key-q>",lambda e: confirm_close(e))
window.bind("<Control-Key-Q>",lambda e: confirm_close(e))
window.bind("<Return>",lambda _: guis.check_indent())
guis.text_box.bind("<Key>", lambda _: window.after(1,sounds.type_sound))
