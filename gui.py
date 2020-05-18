from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox


# GLOBALS #############################
filepath = None
slider = 4
file_selected = False


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
        global slider
        slider = v.get()
        write_to_log("Slider value is : " + str(slider))
        write_to_log("Editing window opened...")
    else:
        messagebox.showinfo("Warning", "Please select a video file to edit!")


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
root = Tk()
root.geometry('392x450')
root.resizable(width=False, height=False)
root.title("2D Manual Track [Beta]")

nb = ttk.Notebook(root)

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
v = IntVar()
v.set(4)
s1 = Scale(tab_menu, variable=v, from_=0, to=29, orient=HORIZONTAL, length=180)
s1.grid(row=1, column=1, sticky=E, padx=20)

l3 = Label(tab_menu, text="3)  Start editing video")
l3.grid(row=2, column=0, sticky=W, padx=20, pady=20)
b3 = Button(tab_menu, text='Start editing...', width=25, command=edit)
b3.grid(row=2, column=1, sticky=E, padx=20)

console_frame = LabelFrame(tab_menu, text="Console")
console_frame.grid(row=3, columnspan=2, padx=20, pady=20)
log = Text(console_frame, width=40, height=10, state='disabled')
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


root.mainloop()


