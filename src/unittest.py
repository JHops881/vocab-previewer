from tkinter import *
from tkinter import ttk

# Pull values from config here...
# ///

# Initializes Tk and creates its associated Tcl interpreter.
# It also creates a toplevel window, known as the root window,
# which serves as the main window of the application.
root = Tk()

# The following line creates a frame widget.
# The frame is fit inside the root window.
frame = ttk.Frame(root, padding=10)
frame.grid()

ttk.Label(frame, text="Highest HSK Level Completed:").grid(column=0, row=0) 

hsk_levels: list[int] = [0, 1, 2, 3, 4, 5, 6]
HSK_LEVEL_SELECTOR: ttk.Combobox = ttk.Combobox(
    frame,
    values=hsk_levels,
    state="readonly",
    width=2,
)
HSK_LEVEL_SELECTOR.grid(column=1, row=0)
HSK_LEVEL_SELECTOR.current(1)



def print_level():
    print(HSK_LEVEL_SELECTOR.get())

button: ttk.Button = ttk.Button(
    frame,
    command=print_level,
    text="hola",
)
button.grid(column=0, row=3)

root.mainloop()

# Writing to config here...
# ///