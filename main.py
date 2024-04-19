from imports import *
import guis
import shortcuts
from constants import CWD, STORAGE_DIR

if not os.path.isdir(CWD+f"/{STORAGE_DIR}"):
    os.makedirs(CWD+f"/{STORAGE_DIR}")

if __name__ == "__main__":
    guis.window.mainloop()