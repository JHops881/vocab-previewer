from tkinter import *
from tkinter import ttk, filedialog
from tkinter import scrolledtext
from typing import Callable

from prestudy_routine import prestudy_routine
# from functools import wraps

global input_file_path
global hsk_level_selector
global selected_input_option
global paste_text_box
global file_upload_button
global generate_button

UPLOAD = "upload"
PASTE  = "paste"

def log(func: Callable):
    def wrapper(*args, **kwargs):
        print(f"Calling `{func.__name__}` with arguments {args} and {kwargs}")
        value = func(*args, **kwargs)
        print("Success.")
        return value
    return wrapper
    

@log
def upload_file():
    global input_file_path
    input_file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("Text files", ".txt"), ("All files", ".*")])
    print("file path: " + input_file_path)
    if input_file_path:
        generate_button["state"] = NORMAL

@log
def toggle_input_options():
    if selected_input_option.get() == UPLOAD:
        file_upload_button["state"] = NORMAL
        paste_text_box["state"] = DISABLED

        paste_text_box.grid_forget()
        file_upload_button.grid(column=0, row=4, sticky=W)

    elif selected_input_option.get() == PASTE:
        file_upload_button["state"] = DISABLED
        paste_text_box["state"] = NORMAL

        file_upload_button.grid_forget()
        paste_text_box.grid(column=0, row=4, sticky=W)


@log
def generate_event():
    
    generate_button["state"] = DISABLED

    input_text: str = ""
    user_hsk_level: int = int(hsk_level_selector.get())

    if selected_input_option.get() == UPLOAD:
        with open(input_file_path, encoding="utf8") as input_file:
            input_text = input_file.read()

    elif selected_input_option.get() == PASTE:
        input_text = paste_text_box.get()

    prestudy_routine(input_text, user_hsk_level)

    generate_button["state"] = NORMAL
        

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
    "Paste Text" : PASTE,
    "Upload Text File" : UPLOAD,
}


file_upload_button = ttk.Button(
    frame_tab_prestudy,
    command=upload_file,
    text="Upload File"
)
file_upload_button.grid(column=0, row=5, sticky=W)
file_upload_button.config(padding=10)

paste_text_box = scrolledtext.ScrolledText(frame_tab_prestudy, wrap=WORD, width=40, height=10)
paste_text_box.grid(column=0, row=4, sticky=W)

selected_input_option = StringVar(root, radio_selection["Paste Text"])

toggle_input_options() # Gotta run once to disable upload on startup

row_counter = 2
for (k,v) in radio_selection.items():
    temp = ttk.Radiobutton(
        frame_tab_prestudy,
        text=k,
        value=v,
        variable=selected_input_option,
        command=toggle_input_options
    )
    temp.grid(column=0, row=row_counter, sticky=W)
    row_counter += 1

generate_button = ttk.Button(
    frame_tab_prestudy,
    command=generate_event,
    text="Generate Deck",
)
generate_button.grid(column=0, row=6)
generate_button.config(padding=10, state=DISABLED)




root.mainloop()

