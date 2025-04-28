from tkinter import *
from tkinter import ttk, filedialog
# from functools import wraps


# Pull values from config here...
# ///

def log(func):
    def wrapper(*args, **kwargs):
        print(f"Calling: {func.__name__}")
        func(*args, **kwargs)
    return wrapper

def print_level():
    print(hsk_level_selector.get())
    print(string_var.get())
    
@log
def upload_file():
    print("Upload File")
    file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("Text files", ".txt"), ("All files", ".*")])
    print(file_path)

# Initializes Tk and creates its associated Tcl interpreter.
# It also creates a toplevel window, known as the root window,
# which serves as the main window of the application.
root = Tk()

tab_control = ttk.Notebook(root)

frame_tab_prestudy = ttk.Frame(tab_control, padding=10)
frame_tab_prestudy.grid()

frame_tab_quick_add = ttk.Frame(tab_control, padding=10)
frame_tab_quick_add.grid()

frame_tab_dictionary = ttk.Frame(tab_control, padding=10)
frame_tab_dictionary.grid()

tab_control.add(frame_tab_prestudy, text='Pre-study')
tab_control.add(frame_tab_quick_add, text='Quick Add')
tab_control.add(frame_tab_dictionary, text='My Words Dictionary')

tab_control.pack(expand=1, fill="both")


# TAB 1 : TEXT ANALYZER PRESTUDY TOOL

ttk.Label(frame_tab_prestudy, text="Highest HSK Level Completed:").grid(column=0, row=0) 

hsk_levels = [0, 1, 2, 3, 4, 5, 6]
hsk_level_selector = ttk.Combobox(
    frame_tab_prestudy,
    values=hsk_levels,
    state="readonly",
    width=2,
)
hsk_level_selector.grid(column=1, row=0)
hsk_level_selector.current(1)
    
radio_selection = {
    "Paste Text" : "paste",
    "Upload Text File" : "file",
}

string_var = StringVar(root, radio_selection["Paste Text"])

row = 2
for (k,v) in radio_selection.items():
    temp = ttk.Radiobutton(frame_tab_prestudy, text=k, value=v, variable=string_var)
    temp.grid(column=0, row=row, sticky=W)
    row += 1

file_upload_button = ttk.Button(
    frame_tab_prestudy,
    command=upload_file,
    text="Upload File"
)
file_upload_button.grid(column=0, row=5, sticky=W)
file_upload_button.config(padding=10)

generate_button = ttk.Button(
    frame_tab_prestudy,
    command=print_level,
    text="Generate",
)
generate_button.grid(column=0, row=6)
generate_button.config(padding=10)

root.mainloop()

# Writing to config here...
# ///