from tkinter import scrolledtext
from typing import Callable
import classes
import constants
from imports import *
window = tk.Tk()
window.iconbitmap(f"{__file__}/../icon.ico")

note_background = tk.Frame(window,background=constants.BACKGROUND_COLOR,width=constants.SCREEN_WIDTH,height=constants.SCREEN_HEIGHT,bd=0)
text_box = tk.Text(note_background,background=constants.TEXT_BACKGROUND_COLOR,width=constants.SCREEN_WIDTH,height=constants.SCREEN_HEIGHT,bd=0,font=(constants.FONT,constants.FONT_SIZE),wrap="word")
text_box.pack(padx=constants.NOTE_PAD_MARGIN,pady=constants.NOTE_PAD_MARGIN)
text_box.focus()

if constants.PURPOSE == "open":
    with open(f"{constants.CWD}/{constants.STORAGE_DIR}/{constants.FILE_NAME}.txt") as f:
        text_box.insert("1.0",f.read())

def central_place(x):
    x.place(relx=0.5,rely=0.5,width=constants.SCREEN_WIDTH,height=constants.SCREEN_HEIGHT,anchor="center")

note_gui = classes.Gui({note_background:lambda: central_place(note_background)},size=(constants.SCREEN_WIDTH,constants.SCREEN_HEIGHT),title="AerWrite",load=False)

def open_note(name,note_type="--open"):
    cmd = [sys.executable] + [sys.argv[0]] + [note_type,name]
    subprocess.Popen(cmd)

def equalify(l:list,n:int,pad_item=""):
    '''Returns copy of list l with length n.
    If length of l is shorter than n, list will be padded with pad_item.
    if length of l is greater than n, list will be truncated.'''
    ls = l.copy()
    if len(ls) >= n:
        return ls[:n]
    ls += [pad_item] * (n-len(ls))
    return ls

def restart_window():
    command = list(reversed(equalify(sys.argv[1:],2,"this")) if len(sys.argv) > 1 else ["This","--list"])
    open_note(*command)
    window.destroy()

def import_text():
    filetypes = (
        ('Text files', '*.txt'),
        ('All files', '*.*')
    )
    file = filedialog.askopenfilename(filetypes=filetypes)
    if file == "":
        return
    name = ".".join(os.path.basename(file).split(".")[:-1])
    with open(file,"r") as old_file, open(f"{constants.CWD}/{constants.STORAGE_DIR}/{name}.txt","w") as new_file:
        new_file.write(old_file.read())
    restart_window()

def check_indent():
    if constants.PURPOSE == "list":
        return

    lines: list[str] = text_box.get("1.0","end").split("\n")
    cursor = list(map(int,text_box.index(tk.INSERT).split(".")))

    convert_cursor: Callable = lambda x,y: ".".join(map(str,(x,y)))

    last_line: str = lines[cursor[0]-2].strip()
    if lines[cursor[0]-1] == "": ... #If the current line is empty, check if indents need to be added

    if last_line.endswith(":") is not last_line.startswith("- "): # "is not" is the python version of xor
        text_box.insert(tk.INSERT,f"{lines[cursor[0]-2].split("-")[0]*last_line.startswith("- ")}- ")

    if last_line.endswith(":") and last_line.startswith("- "):
        text_box.insert(tk.INSERT,f"{lines[cursor[0]-2].split("-")[0]}  - ") #Finds indent of the last line and adds 2 spaces to it.
    
    if last_line == "-": #That is, the last line is empty except for the indent
        text_box.delete(convert_cursor(cursor[0]-1,0),convert_cursor(cursor[0]-1,2))
        text_box.delete(convert_cursor(cursor[0]-1,len(lines[cursor[0]-2])-2),convert_cursor(cursor[0],0))
        text_box.mark_set(tk.INSERT, convert_cursor(cursor[0]-1,len(lines[cursor[0]-2])-2))
    
    strip_lines(convert_cursor)

def strip_lines(convert_cursor):
    lines: list[str] = text_box.get("1.0","end").split("\n")
    cursor = list(map(int,text_box.index(tk.INSERT).split(".")))

    for line_num,line in enumerate(lines,start=1):
        line_data = line.split("- ")
        if line_num == cursor[0]:
            continue
        text_box.delete(convert_cursor(line_num,0),convert_cursor(line_num,len(line)))
        text_box.insert(convert_cursor(line_num,0),f"{"- ".join(line_data[:-1]+[line_data[-1].strip(" ")])}")
    text_box.mark_set(tk.INSERT,convert_cursor(*cursor))

def load_guis():
    note_gui.unload()
    list_gui.unload()
    if constants.PURPOSE in("open","new"):
        note_gui.load()
    elif constants.PURPOSE == "list":
        list_gui.load()

def delete_note(note):
    os.remove(f"{constants.STORAGE_DIR}/{note}.txt")
    restart_window()


selection_background = tk.Frame(window,background=constants.TEXT_BACKGROUND_COLOR,width=constants.SCREEN_WIDTH,height=constants.SCREEN_HEIGHT,bd=0)

note_buttons: dict[str,tk.Button] = {}

import_button = tk.Button(selection_background,text="Import",background=constants.BACKGROUND_COLOR,command=import_text)

for note in constants.NOTE_LIST.items():
    frame = tk.Frame(selection_background,background=constants.BACKGROUND_COLOR,bd=10)
    note_buttons[note[0]] = frame
    tk.Button(frame,text=note[0],background=constants.BACKGROUND_COLOR,font=(constants.FONT,constants.FONT_SIZE),command=lambda n=note: open_note(n[0],note_type="--open")).pack(side="left")
    tk.Button(frame,text="🗑️"[0],background=constants.DANGER_RED_COLOR,font=(constants.FONT,constants.FONT_SIZE),foreground="#FFFFFF",command=lambda n=note: delete_note(n[0])).pack(side="right")

list_gui = classes.Gui({selection_background:lambda: central_place(selection_background),
                        import_button:lambda: import_button.pack(anchor="ne",side="right")}|
                            {button:lambda button=button: button.pack(anchor="nw",fill="x") for i,button in enumerate(note_buttons.values())},
                        title="AerWrite",load=constants.PURPOSE=="list")
load_guis()