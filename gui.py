from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from pathlib import Path


# GLOBALS #############################
filepath = Path()
output_folder = Path()
output_folder_suffix = "_OUT"           # create an output folder from file name and add this suffix
slider_val = 4                          # Skip next 4 frames and edit 5th frame
size_Val = 0                            # 0 = %50 | 1 = %100 | 2 = %200 | 3 = fullscreen
file_selected = False
delay = 3000                            # milliseconds before gui closes


# FUNCTIONS ###########################
def open_file():
    global filepath, file_selected
    filepath = filedialog.askopenfilename(initialdir=".", title="Select file",
                                          filetypes=(("video files", ".mp4 .avi .mov .flv .wmv .mpeg"), ("all files", ".*")))
    if filepath:
        file_selected = True
        write_to_log("File selected :")
        write_to_log(" " + str(filepath))
    else:
        write_to_log("No file selected!")


def edit():
    global file_selected
    if file_selected:
        global slider_val, size_Val
        slider_val = val_skip.get()
        size_Val = c3.current()

        create_output_folder()

        write_to_log("> Slider value set to : " + str(slider_val))
        write_to_log("> Window size set to : " + val_size.get())
        write_to_log("> Editing window opening...")

        window.after(delay, window.destroy)
    else:
        write_to_log("Warning : \n Please select a video file to edit!")


def create_output_folder():
    global filepath, output_folder
    output_folder = Path(filepath).parent
    name = Path(filepath).name.partition('.')[0].upper()
    output_folder = output_folder.joinpath(name + output_folder_suffix)

    if output_folder.exists():
        write_to_log("Output directory already exists:")
    else:
        output_folder.mkdir()
        write_to_log("Output directory created:")

    write_to_log(" " + str(output_folder))


def write_to_log(msg):
    num_lines = log.index('end - 1 line').split('.')[0]
    log['state'] = 'normal'
    if num_lines == 10:
        log.delete(1.0, 2.0)
    if log.index('end-1c') != '1.0':
        log.insert('end', '\n')
    log.insert('end', msg)
    log['state'] = 'disabled'
    log.yview_pickplace("end")


# GUI LAYOUT ##################################################################
window = Tk()
window.geometry('392x450')
window.resizable(width=False, height=False)
window.title("2D Manual Track [Beta]")
window.wm_iconbitmap('circle.ico')

nb = ttk.Notebook(window)

tab_menu = ttk.Frame(nb)
tab_help = ttk.Frame(nb)
tab_about = ttk.Frame(nb)

nb.add(tab_menu, text="   Setup   ")
nb.add(tab_help, text="   About   ")
nb.grid()

# SETUP TAB ###################################################################
l1 = Label(tab_menu, text="1)  Select a video file")
l1.grid(row=0, column=0, sticky=W, padx=20, pady=20)
b1 = Button(tab_menu, text='Open video file', width=25, command=lambda: open_file())
b1.grid(row=0, column=1, sticky=E, padx=20)

l2 = Label(tab_menu, text="2)  Set # frames to skip")
l2.grid(row=1, column=0, sticky=W, padx=20, pady=20)
val_skip = IntVar()
val_skip.set(4)
s2 = Scale(tab_menu, variable=val_skip, from_=0, to=29, orient=HORIZONTAL, length=180)
s2.grid(row=1, column=1, sticky=E, padx=20)

l3 = Label(tab_menu, text="3)  Set edit window size")
l3.grid(row=2, column=0, sticky=W, padx=20, pady=20)
val_size = StringVar()
c3 = ttk.Combobox(tab_menu, textvariable=val_size, width=25, state='readonly')
c3['values'] = (' %50 - Windowed', ' %100 - Windowed', ' %200 - Windowed', ' Fullscreen')
c3.current(0)
c3.grid(row=2, column=1, sticky=E, padx=20)

l4 = Label(tab_menu, text="4)  Start editing video")
l4.grid(row=3, column=0, sticky=W, padx=20, pady=20)
b4 = Button(tab_menu, text='Start editing...', width=25, command=edit)
b4.grid(row=3, column=1, sticky=E, padx=20)

console_frame = LabelFrame(tab_menu, text="Console")
console_frame.grid(row=4, columnspan=2, padx=20, pady=20)
log = Text(console_frame, width=40, height=6, state='disabled')
log.grid(padx=10, pady=10)

# ABOUT TAB ###################################################################
about_frame = LabelFrame(tab_help, text="About")
about_frame.grid(row=0, padx=20, pady=20)

about_text = Text(about_frame, width=40, height=6, spacing1=4, spacing2=2, spacing3=4)
about_text.insert('1.0', ' 2D Manual Track [Beta]\n')
about_text.insert('2.0', ' This software is designed for manually '
                         ' tracking four points through a footage '
                         ' to help positioning 2D-characters in a '
                         ' 2D animation.\n')
about_text.insert('3.0', ' Copyright ' + u'\u00A9' + ' 2020 Ali Osman Atik\n')
about_text.insert('4.0', ' This program is free software; you can '
                         ' redistribute it and/or modify it under '
                         ' the terms of the GNU GPLv3 or later.')

about_text['state'] = 'disabled'
about_text.grid(padx=10, pady=10)


controls_frame = LabelFrame(tab_help, text="Controls")
controls_frame.grid(row=1, padx=20)

controls_text = Text(controls_frame, width=40, height=6, spacing1=4, spacing2=2, spacing3=4)
controls_text.insert('1.0', ' Left-Click to select points on image\n')
controls_text.insert('2.0', ' Right-Click resets last selected point\n')
controls_text.insert('3.0', ' Press \'R\' to reset all selected points\n')
controls_text.insert('4.0', ' Press \'C\' to confirm selected 4 points\n')
controls_text.insert('5.0', ' Press \'S\' to skip current frame\n')
controls_text.insert('6.0', ' Press \'Q\' to quit program')

controls_text['state'] = 'disabled'
controls_text.grid(padx=10, pady=5)


window.mainloop()
