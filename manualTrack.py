from tkinter import *
from tkinter import filedialog, ttk
from pathlib import Path


import sys
import cv2
from numpy import array
from math import atan2, degrees


# GLOBALS #############################
app_title = "2D Manual Track [Beta]"
icon_file = Path("circle.ico")
filepath = Path()
output_folder = Path()
output_folder_suffix = "_OUT"           # create an output folder from file name and add this suffix
slider_val = 4                          # initializing by default value : skip next 4 frames and edit 5th frame
size_Val = 0                            # initializing by default value : 0 = %50 | 1 = %100 | 2 = %200 | 3 = fullscreen
file_selected = False
delay = 2000                            # milliseconds before gui closes


#######################################################################################################################
#                                                                                                                     #
#                                                THIS IS THE GUI SECTION                                              #
#                                                                                                                     #
#######################################################################################################################


# FUNCTIONS ###########################
def open_file():
    global filepath, file_selected
    filepath = filedialog.askopenfilename(initialdir=Path().cwd(), title="Select file",
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


def window_closed():
    window.destroy()
    sys.exit(0)


# GUI LAYOUT ##################################################################
window = Tk()
window.geometry('392x450')
window.resizable(width=False, height=False)
window.title(app_title)
window.wm_iconbitmap(icon_file)
window.protocol("WM_DELETE_WINDOW", window_closed)

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


#######################################################################################################################
#                                                                                                                     #
#                                      THIS IS THE VIDEO EDITING SECTION                                              #
#                                                                                                                     #
#######################################################################################################################


# INFO BACKGROUND #####################
info_area = [(0, 0), (180, 0), (180, 300), (0, 300)]

# LINE TYPE OF LINE/CIRCLE/TEXT #######
lineType = 16                                   # default 8, anti-aliased 16

# COLORS ##############################
color_1 = (31, 31, 255)                         # corner 1 and line 1
color_2 = (31, 255, 255)                        # corner 2 and line 2
color_3 = (31, 255, 63)                         # corner 3 and line 3
color_4 = (255, 31, 31)                         # corner 4 and line 4
color_dark = (31, 31, 31)                       # blackish color
color_light = (223, 223, 223)                   # whitish color
color_count = (31, 127, 255)                    # frame count info
color_last = (31, 127, 255)                     # last frame warning
color_confirm = (31, 127, 255)                  # confirm points warning
color_quit = (31, 127, 255)                     # quit program warning
color_rectangle = (31, 31, 31)                  # rectangle color on output image
color_info_bg = (31, 31, 31)                    # background of output info
color_info = (223, 223, 223)                    # text color of output info

# GLOBALS #############################
refPts = []                                     # initialize the list of reference points
prevPts = [(0, 0), (1, 0), (1, 1), (0, 1), 0]   # initialize the list of previous points : 1px square
cc = 0                                          # click count
fc = 0                                          # frame count
fs = slider_val                                 # frames to skip
lb_down = False                                 # mouse left button status
exit_screen = False                             # 'Q' key enters to exit screen


# EDITING FUNCTIONS ###########################################################
# Resize frame to fit in screen
def rescale_frame(inFrame, percent=100):
    width = int(inFrame.shape[1] * percent / 100)
    height = int(inFrame.shape[0] * percent / 100)
    dim = (width, height)
    return cv2.resize(inFrame, dim, interpolation=cv2.INTER_AREA)


# Capture mouse events
def mouse_events(event, x, y, flags, param):
    # grab references to the global variables
    global lb_down, cc, refPts, overlaid_frame
    point = (x, y)
    local_frame = overlaid_frame.copy()

    # if the left mouse button was clicked, record (x, y) coordinates
    if event == cv2.EVENT_LBUTTONDOWN:
        lb_down = True

    elif not exit_screen and lb_down and event == cv2.EVENT_MOUSEMOVE:
        if 0 < cc < 4:
            cv2.line(local_frame, refPts[cc - 1], point, color_dark, 6, lineType)
            cv2.line(local_frame, refPts[cc - 1], point, color_light, 2, lineType)

        # draw a circle for current point
        if cc == 0:
            cv2.circle(local_frame, point, 15, color_dark, 2, lineType)
            cv2.circle(local_frame, point, 13, color_1, 2, lineType)
        if cc == 1:
            cv2.circle(local_frame, point, 15, color_dark, 2, lineType)
            cv2.circle(local_frame, point, 13, color_2, 2, lineType)
        if cc == 2:
            cv2.circle(local_frame, point, 15, color_dark, 2, lineType)
            cv2.circle(local_frame, point, 13, color_3, 2, lineType)
        if cc == 3:
            cv2.circle(local_frame, point, 15, color_dark, 2, lineType)
            cv2.circle(local_frame, point, 13, color_4, 2, lineType)

        # draw a circle for previously selected points
        draw_points(local_frame, refPts)

        if cc == 4:
            put_shaded_text(local_frame, "Press 'C' to confirm points", (int(dimX / 2) - 200, int(dimY / 2)), 5, 1.2,
                            color_confirm, 2, 2)

        cv2.imshow(app_title, local_frame)

    elif not exit_screen and cc < 4 and event == cv2.EVENT_LBUTTONUP:
        lb_down = False
        # increment counter and append the point
        cc = cc + 1
        print("\nPoint " + str(cc) + " added to list")
        refPts.append(point)
        print(refPts)
        # draw a circle for previously selected points
        draw_points(local_frame, refPts)
        cv2.imshow(app_title, local_frame)

    elif not exit_screen and cc > 0 and event == cv2.EVENT_RBUTTONDOWN:        
        print("\nPoint " + str(cc) + " removed from list")
        cc = cc - 1
        refPts.pop(cc)
        print(refPts)
        # draw a circle for previously selected points
        draw_points(local_frame, refPts)
        cv2.imshow(app_title, local_frame)


# draw circles on image at points in given list
def draw_points(image, point_list):
    for i, p in enumerate(point_list):
        if i == 0:
            cv2.circle(image, p, 15, color_dark, 2, lineType)
            cv2.circle(image, p, 11, color_1, 6, lineType)
        elif i == 1:
            cv2.circle(image, p, 15, color_dark, 2, lineType)
            cv2.circle(image, p, 11, color_2, 6, lineType)
        elif i == 2:
            cv2.circle(image, p, 15, color_dark, 2, lineType)
            cv2.circle(image, p, 11, color_3, 6, lineType)
        elif i == 3:
            cv2.circle(image, p, 15, color_dark, 2, lineType)
            cv2.circle(image, p, 11, color_4, 6, lineType)
    return image


# Skip some frames
def skip_frames(sf):
    global fc, refPts, cc
    print("\nSkipping frames...\n")
    for i in range(sf):
        cap.read()
        fc = fc + 1
        print("Skipped frame " + str(fc))
    refPts = []
    cc = 0
    pass


# Overlay a shaded text on image
def put_shaded_text(image, text, position, font, scale, color, thickness=1, border=1):
    cv2.putText(image, text, position, font, scale, (7, 7, 7), thickness + (2 * border), lineType)
    cv2.putText(image, text, position, font, scale, color, thickness, lineType)
    pass


# OUTPUT FUNCTIONS ############################################################
# calculate distance between points
def distance(p, q):
    return ((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2) ** 0.5


# calculate the change ratio of current distance over previous distance by %
def variance(dp, dc):
    # assuming there will be no tracking points with 1px distance;
    # I used 1px square for initial previous points,
    # so for the first frame I return "current distance" = length.
    if dp == 1:
        return round(dc, 2)
    else:
        return round((dc - dp) * 100 / dp, 2)


# calculate rotation of current line against previous line
#  clockwise rotations are positive by default
def rotation(lp, lc):
    return round(degrees(atan2(lc[1][1] - lc[0][1], lc[1][0] - lc[0][0])) -
                 degrees(atan2(lp[1][1] - lp[0][1], lp[1][0] - lp[0][0])), 2)


# overlay info and paint rectangle on output image and save to output folder
def save_output(points):
    global original_frame, prevPts

    # get frame info
    frame_no = points[4]
    prev_frame_no = prevPts[4]

    # get the corner points
    p1 = points[0]
    p2 = points[1]
    p3 = points[2]
    p4 = points[3]

    pp1 = prevPts[0]
    pp2 = prevPts[1]
    pp3 = prevPts[2]
    pp4 = prevPts[3]

    # set the lines for image coordinate system
    l1 = [p1, p2]
    l2 = [p2, p3]
    l3 = [p4, p3]
    l4 = [p1, p4]

    l13 = [p1, p3]
    l24 = [p4, p2]

    pl1 = [pp1, pp2]
    pl2 = [pp2, pp3]
    pl3 = [pp4, pp3]
    pl4 = [pp1, pp4]

    pl13 = [pp1, pp3]
    pl24 = [pp4, pp2]

    # fill the rectangle area
    cv2.fillPoly(original_frame, array([points[0:4]]), color_rectangle)

    # draw lines on sides
    cv2.line(original_frame, p1, p2, color_1, 1, lineType)
    cv2.line(original_frame, p2, p3, color_2, 1, lineType)
    cv2.line(original_frame, p3, p4, color_3, 1, lineType)
    cv2.line(original_frame, p4, p1, color_4, 1, lineType)

    # pin corner points
    cv2.circle(original_frame, p1, 1, color_1, 2, lineType)
    cv2.circle(original_frame, p2, 1, color_2, 2, lineType)
    cv2.circle(original_frame, p3, 1, color_3, 2, lineType)
    cv2.circle(original_frame, p4, 1, color_4, 2, lineType)

    # fill info background
    cv2.fillPoly(original_frame, array([info_area]), color_info_bg)

    # calculate distances
    d12 = distance(p1, p2)
    d23 = distance(p2, p3)
    d34 = distance(p3, p4)
    d41 = distance(p4, p1)

    d13 = distance(p1, p3)
    d24 = distance(p2, p4)

    pd12 = distance(pp1, pp2)
    pd23 = distance(pp2, pp3)
    pd34 = distance(pp3, pp4)
    pd41 = distance(pp4, pp1)

    pd13 = distance(pp1, pp3)
    pd24 = distance(pp2, pp4)

    # printing output info
    cv2.putText(original_frame, "Frame # :  " + str(frame_no), (10, 20), 5, 0.8, color_info)
    cv2.putText(original_frame, "Previous :  " + str(prev_frame_no), (10, 40), 5, 0.8, color_info)

    cv2.putText(original_frame, "V1  : % " + str(variance(pd12, d12)), (10, 70), 5, 0.8, color_1)
    cv2.putText(original_frame, "V2  : % " + str(variance(pd23, d23)), (10, 90), 5, 0.8, color_2)
    cv2.putText(original_frame, "V3  : % " + str(variance(pd34, d34)), (10, 110), 5, 0.8, color_3)
    cv2.putText(original_frame, "V4  : % " + str(variance(pd41, d41)), (10, 130), 5, 0.8, color_4)

    axv = round((variance(pd13, d13) + variance(pd24, d24)) / 2, 2)
    # for first frame avx = average cross distance
    if pd12 == pd23 == pd34 == pd41 == 1:
        axv = round((d13 + d24) / 2, 2)

    cv2.putText(original_frame, "AXV : % " + str(axv), (10, 160), 5, 0.8, color_light)

    if axv < 0:
        cv2.arrowedLine(original_frame, (168, 147), (168, 163), color_info, 1, tipLength=0.25)
    else:
        cv2.arrowedLine(original_frame, (168, 163), (168, 147), color_info, 1, tipLength=0.25)

    cv2.putText(original_frame, "R1  :  " + str(rotation(pl1, l1)), (10, 190), 5, 0.8, color_1)
    cv2.putText(original_frame, "R2  :  " + str(rotation(pl2, l2)), (10, 210), 5, 0.8, color_2)
    cv2.putText(original_frame, "R3  :  " + str(rotation(pl3, l3)), (10, 230), 5, 0.8, color_3)
    cv2.putText(original_frame, "R4  :  " + str(rotation(pl4, l4)), (10, 250), 5, 0.8, color_4)

    axr = round((rotation(pl13, l13) + rotation(pl24, l24)) / 2, 2)
    cv2.putText(original_frame, "AXR :  " + str(axr), (10, 280), 5, 0.8, color_light)
    if axr < 0:
        cv2.arrowedLine(original_frame, (168, 283), (168, 267), color_info, 1, tipLength=0.25)
    else:
        cv2.arrowedLine(original_frame, (168, 267), (168, 283), color_info, 1, tipLength=0.25)

    cv2.imwrite(str(output_folder.resolve().joinpath(Path('frame_' + str(frame_no) + '.jpg'))), original_frame)


# EDITING WINDOW ##############################################################
# Create a VideoCapture object and read from input file
cap = cv2.VideoCapture(filepath)

# Check if camera opened successfully
if not cap.isOpened():
    print("\nError opening video file")
    exit(-1)

print("\nVideo opened, reading file...")

# frame_rate = cap.get(5)
total_frames = cap.get(7)

# Read until video is completed
while cap.isOpened():

    # Capture frame-by-frame
    ret, frame = cap.read()

    if ret:
        # Resize frame - %100 default
        if size_Val == 0:
            frame = rescale_frame(frame, 50)
        if size_Val == 2:
            frame = rescale_frame(frame, 200)
        else:
            frame = rescale_frame(frame)

        # Backup original frame for output !!!
        original_frame = frame.copy()

        # Get dimensions of image
        dimY, dimX, ch = frame.shape

        # Corner numbers overlay
        put_shaded_text(frame, "[1]", (20, 30), 5, 1, color_1)
        put_shaded_text(frame, "[2]", (dimX - 60, 30), 5, 1, color_2)
        put_shaded_text(frame, "[3]", (dimX - 60, dimY - 20), 5, 1, color_3)
        put_shaded_text(frame, "[4]", (20, dimY - 20), 5, 1, color_4)

        # Frame count overlay
        fc = fc + 1
        if (total_frames - fc) <= fs:
            put_shaded_text(frame, "[ Frame = " + str(fc) + " / " + str(
                int(total_frames)) + " ]   *** LAST FRAME OF THE FILE ***", (60, 30), 5, 1, color_last)
        else:
            put_shaded_text(frame, "[ Frame = " + str(fc) + " / " + str(int(total_frames)) + " ]", (60, 30), 5, 1, color_count)

        # Clone the current frame for resetting !!!
        overlaid_frame = frame.copy()

        # Open window in selected size
        if size_Val == 3:
            cv2.namedWindow(app_title, cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty(app_title, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        else:
            cv2.namedWindow(app_title)

        # Select point for tracking from frame
        cv2.setMouseCallback(app_title, mouse_events)

        # keep looping until a key pressed ???
        while True:
            draw_points(frame, refPts)
            # display the image and wait for click
            cv2.imshow(app_title, frame)
            key = cv2.waitKey(0) & 0xFF

            # Press 'Q' key to Exit
            if key == ord('q'):
                exit_screen = True
                while True:
                    frame = overlaid_frame.copy()
                    put_shaded_text(frame, "Do you want to quit? (Y/N)", (int(dimX / 2) - 200, int(dimY / 2)), 5, 1.2, color_quit, 2, 2)
                    print("\nQ > Do you want to quit? (Y/N)")
                    cv2.imshow(app_title, frame)
                    key = cv2.waitKey(0) & 0xFF

                    if key == ord('y'):
                        print("Y > Exiting program...")
                        sys.exit()
                    if key == ord('n'):
                        print("N > Continuing program...")
                        exit_screen = False
                        frame = overlaid_frame.copy()
                        break

            # Press 'S' key to Skip next frame
            if key == ord('s'):
                print("\nS >  " + str(fs) + " frames will be skipped")
                skip_frames(fs)
                break

            # Press 'R' key to Reset points
            if key == ord("r"):
                frame = overlaid_frame.copy()
                refPts = []
                cc = 0
                print("\nR > Reset selected points")

            # Press 'C' key to Confirm points
            if cc == 4 and key == ord("c"):
                print("\nC > Confirmed selected points")
                # refPts need to be stored before calling skip_frames()
                refPts.append(fc)

                # prepare output overlay and save image
                save_output(refPts)

                # save current frame info for next frame output
                prevPts = refPts

                skip_frames(fs)
                break

        # Display the resulting frame
        cv2.imshow(app_title, frame)

    # Break the loop if not 'ret'
    else:
        print("Error reading video file")
        break

# When everything done, release the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()
