from tkinter import scrolledtext
from typing import Callable, Literal

import classes
import constants
import sounds
from imports import *
import autocorrection

window = tk.Tk()
window.iconbitmap(f"{__file__}/../icon.ico")

note_background = tk.Frame(window,background=constants.BACKGROUND_COLOR,width=constants.SCREEN_WIDTH,height=constants.SCREEN_HEIGHT,bd=0)
text_box = tk.Text(note_background,background=constants.TEXT_BACKGROUND_COLOR,width=constants.SCREEN_WIDTH,height=constants.SCREEN_HEIGHT,bd=0,font=(constants.FONT,constants.FONT_SIZE),wrap="word")

text_box.pack(padx=constants.NOTE_PAD_MARGIN,pady=constants.NOTE_PAD_MARGIN)
text_box.focus()


MENU_SETTINGS = {"master":window,"tearoff":0,"background":constants.TEXT_BACKGROUND_COLOR,"type":"normal","selectcolor":constants.BACKGROUND_COLOR,"font":(constants.FONT,int(constants.FONT_SIZE//1.25))}

if constants.PURPOSE == "open":
    with open(f"{constants.CWD}/{constants.STORAGE_DIR}/{constants.FILE_NAME}.txt") as f:
        text_box.insert("1.0",f.read())

last_text = text_box.get("1.0","end")


def central_place(x):
    x.place(relx=0.5,rely=0.5,width=constants.SCREEN_WIDTH,height=constants.SCREEN_HEIGHT,anchor="center")

note_gui = classes.Gui({note_background:lambda: central_place(note_background)},size=(constants.SCREEN_WIDTH,constants.SCREEN_HEIGHT),title=constants.FILE_NAME if constants.PURPOSE == "open" else "Untitled",load=False)

def open_note(name,note_type="--open"):
    cmd = [sys.executable] + [sys.argv[0]] + [note_type,name]
    subprocess.Popen(cmd)

def find_frame_from_note(note):
    for f in selection_background.children.values():
        if f.children["!label"].cget("text") == note[0]:
            return f
    return None

def copy_text(note):
    window.clipboard_clear()
    window.clipboard_append(note[1])
    f = find_frame_from_note(note)
    for item in list(f.children.values()) + [f]:
        item.config(background=constants.SHINE_COLOR)
    window.after(500,lambda frame=f:(i.config(background=constants.TEXT_BACKGROUND_COLOR) for i in list(frame.children.values()) + [frame]))
            
    window.update()
    mixer.Sound.play(sounds.sounds["save"])

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

    if last_line.endswith(":") is not last_line.startswith("- "): # "is not" is the python version of xor
        text_box.insert(tk.INSERT,f"{lines[cursor[0]-2].split("-")[0]*last_line.startswith("- ")}- ")

    if last_line.endswith(":") and last_line.startswith("- "):
        text_box.insert(tk.INSERT,f"{lines[cursor[0]-2].split("-")[0]}  - ") #Finds indent of the last line and adds 2 spaces to it.
    
    if last_line == "-": #That is, the last line is empty except for the indent
        #Unindent 1 space
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

def type_sound(_=None):
    global last_text
    cur_text = text_box.get("1.0","end")
    if constants.PURPOSE == "list":
        return
    if cur_text == last_text:
        return
    window.title(f"*{window.title().strip("*")}*")
    last_text = cur_text
    mixer.Sound.play(sounds.sounds[f"typing{random.randint(1,2)}"])

def load_guis():
    note_gui.unload()
    list_gui.unload()
    if constants.PURPOSE in("open","new"):
        note_gui.load()
    elif constants.PURPOSE == "list":
        text_box.pack_forget()
        list_gui.load()

def delete_note(note):
    os.remove(f"{constants.STORAGE_DIR}/{note[0]}.txt")
    mixer.Sound.play(sounds.sounds["quit"])
    find_frame_from_note(note).destroy()

def highlight(self:tk.Widget,highlight=True):
    for child in list(self.children.values())+[self]:
        child.config(background=constants.BACKGROUND_COLOR if highlight else constants.TEXT_BACKGROUND_COLOR)

def open_menu(event:tk.Event,note):
    note_options_menu.entryconfig(0,command=lambda n=note:open_note(n[0],note_type="--open"))
    note_options_menu.entryconfig(1,command=lambda n=note:copy_text(note))
    note_options_menu.entryconfig(2,command=lambda n=note:...)
    note_options_menu.entryconfig(3,command=lambda n=note:...)
    note_options_menu.entryconfig(4,command=lambda n=note:delete_note(note))
    note_options_menu.post(event.x_root,event.y_root)

def sort_notes(order:Literal["name","time","expiry"],silent=False):
    order = order.lower()
    if order == "name":
        key = None
    elif order == "time":
        key = lambda x: -constants.NOTE_TIMESAVE[x]
    elif order == "expiry":
        key = None
    else:
        raise NameError(f"Bad name {order}: Must be \"name\", \"time\" or \"expiry\"")
    if not silent:
        mixer.Sound.play(sounds.sounds["save"])
    list_gui.widgets = {note_background:lambda: central_place(note_background)}|{frame:lambda f=frame: f.pack(anchor="nw",fill="x") for i,frame in enumerate(note_frames[j] for j in sorted(note_frames.keys(),key=key))}
    list_gui.reload()

note_options_menu = tk.Menu(**MENU_SETTINGS)
note_options_menu.add_command(label="Open")
note_options_menu.add_command(label="Copy text")
note_options_menu.add_command(label="Rename")
note_options_menu.add_command(label="Duplicate")
note_options_menu.add_command(label="Delete")

sort_by_menu = tk.Menu(**MENU_SETTINGS)

options_menu = tk.Menu(**MENU_SETTINGS)
options_menu.add_command(label="New note",command=lambda: open_note("","--new"))
options_menu.add_command(label="Options",command=lambda:...)
options_menu.add_command(label="Import",command=import_text)
options_menu.add_command(label="Reload",command=restart_window)

#The sort by option is more complicated, as there are multiple ways you can sort.
sort_by_menu.add_command(label="Last modified",command=lambda: sort_notes("time"))
sort_by_menu.add_command(label="Name",command=lambda: sort_notes("name"))
sort_by_menu.add_command(label="Expiry",command=lambda: sort_notes("expiry"))
options_menu.add_cascade(label="Sort by...",menu=sort_by_menu)

completion_menu = tk.Menu(**MENU_SETTINGS)


selection_background = tk.Frame(note_background,background=constants.TEXT_BACKGROUND_COLOR,width=constants.SCREEN_WIDTH,height=constants.SCREEN_HEIGHT,bd=0)
selection_background.pack(padx=constants.NOTE_PAD_MARGIN,pady=constants.NOTE_PAD_MARGIN,expand=True,fill="both")

note_frames: dict[str,tk.Frame] = {}

#import_button = tk.Button(selection_background,text="Import",background=constants.BACKGROUND_COLOR,command=import_text)
def draw_notes(notes=constants.NOTE_LIST.items()):
    for note in notes:
        frame = tk.Frame(selection_background,background=constants.TEXT_BACKGROUND_COLOR,relief="raised",bd=2)
        note_frames[note[0]] = frame
        note_time = datetime.datetime.fromtimestamp(constants.NOTE_TIMESAVE[note[0]]).strftime('%D\n%H:%M:%S')
        note_text = note[0]
        if len(note_text) > 60:
            note_text = note_text[:61]+"..."
        l = tk.Label(frame,text=note_text,background=constants.TEXT_BACKGROUND_COLOR,relief="flat",font=(constants.FONT,constants.FONT_SIZE))
        l.pack(side="left",pady=10)
        time_label = tk.Label(frame,text=note_time,background=constants.TEXT_BACKGROUND_COLOR,relief="flat",font=(constants.FONT,int(constants.FONT_SIZE//1.5)))
        time_label.pack(side="right",pady=10)

        frame.bind("<Enter>",lambda _,f=frame: highlight(f))
        frame.bind("<Leave>",lambda _,f=frame: highlight(f,False))
        for item in [frame,l,time_label]:
            item.bind("<Button-1>",lambda _,f=frame,n=note: (f.config(relief="sunken"),open_note(n[0],note_type="--open")))
            item.bind("<ButtonRelease-1>",lambda _,f=frame,n=note: (f.config(relief="raised")))
            item.bind("<Button-3>",lambda e,n=note: open_menu(e,n))

draw_notes()


list_gui = classes.Gui({note_background:lambda: central_place(note_background)}|
                            {button:lambda button=button: button.pack(anchor="nw",fill="x") for i,button in enumerate(note_frames.values())},
                        title="Aerwrite",load=constants.PURPOSE=="list")

sort_notes("time",silent=True)

selection_background.bind("<Button-3>",lambda e: options_menu.post(e.x_root,e.y_root))

load_guis()