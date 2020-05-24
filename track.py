import sys
import cv2


################################################################################
# THIS VALUES SHOULD BE SUPPLIED BY GUI IN UNITED CODE !!!
from pathlib import Path
output_folder = Path('VIDEO_OUT')
output_folder.mkdir(exist_ok=True)
print(output_folder.resolve())
filepath = 'video.mp4'
slider_val = 4                  # Skip next 4 frames and edit 5th frame
size_Val = 0                    # 0 = %50 | 1 = %100 | 2 = %200 | 3 = fullscreen
################################################################################


# Create a VideoCapture object and read from input file
cap = cv2.VideoCapture(filepath)

# Check if camera opened successfully
if not cap.isOpened():
    print("Error opening video stream or file")

# frame_rate = cap.get(5)
total_frames = cap.get(7)


# GLOBALS #############################
refPt = []                                      # initialize the list of reference points
refPtList = []                                  # initialize the list of reference points lists
cc = 0                                          # click count
fc = 0                                          # frame count
fs = slider_val                                 # frames to skip
lb_down = False                                 # mouse left button status
exit_screen = False                             # 'Q' key enters to exit screen


# Resize frame to fit in screen
def rescale_frame(inFrame, percent=100):
    width = int(inFrame.shape[1] * percent / 100)
    height = int(inFrame.shape[0] * percent / 100)
    dim = (width, height)
    return cv2.resize(inFrame, dim, interpolation=cv2.INTER_AREA)


# Capture mouse events
def mouse_events(event, x, y, flags, param):
    # grab references to the global variables
    global lb_down, cc, refPt, overlaid_frame
    point = (x, y)
    local_frame = overlaid_frame.copy()

    # if the left mouse button was clicked, record (x, y) coordinates
    if event == cv2.EVENT_LBUTTONDOWN:
        lb_down = True

    elif not exit_screen and lb_down and event == cv2.EVENT_MOUSEMOVE:
        if 0 < cc < 4:
            cv2.line(local_frame, refPt[cc - 1], point, (0, 0, 0), 6)
            cv2.line(local_frame, refPt[cc - 1], point, (255, 255, 255), 2)

        if cc == 4:
            put_shaded_text(local_frame, "Press 'C' to confirm points", (int(dimX / 2) - 200, int(dimY / 2)), 5, 1.2,
                            (0, 127, 255), 2, 2)
            # cv2.circle(local_frame, point, 13, (0, 0, 255), 3)
        else:
            # draw a circle for current point
            if cc == 0:
                cv2.circle(local_frame, point, 15, (0, 0, 0), 2)
                cv2.circle(local_frame, point, 13, (0, 0, 255), 2)
            if cc == 1:
                cv2.circle(local_frame, point, 15, (0, 0, 0), 2)
                cv2.circle(local_frame, point, 13, (0, 255, 255), 2)
            if cc == 2:
                cv2.circle(local_frame, point, 15, (0, 0, 0), 2)
                cv2.circle(local_frame, point, 13, (0, 255, 0), 2)
            if cc == 3:
                cv2.circle(local_frame, point, 15, (0, 0, 0), 2)
                cv2.circle(local_frame, point, 13, (255, 0, 0), 2)

        # draw a circle for previously selected points
        draw_points(local_frame, refPt)
        cv2.imshow("Frame", local_frame)

    elif not exit_screen and cc < 4 and event == cv2.EVENT_LBUTTONUP:
        lb_down = False
        # increment counter and append the point
        cc = cc + 1
        print("Point " + str(cc) + " appended to 'refPt' list")
        refPt.append(point)
        print(refPt)
        # draw a circle for previously selected points
        draw_points(local_frame, refPt)
        cv2.imshow("Frame", local_frame)

    elif not exit_screen and cc > 0 and event == cv2.EVENT_RBUTTONDOWN:
        cc = cc - 1
        print(str(cc))
        refPt.pop(cc)
        print(refPt)
        # draw a circle for previously selected points
        draw_points(local_frame, refPt)
        cv2.imshow("Frame", local_frame)


# draw circles on image at points in given list
def draw_points(image, point_list):
    for i, p in enumerate(point_list):
        if i == 0:
            cv2.circle(image, p, 15, (0, 0, 0), 2)
            cv2.circle(image, p, 11, (0, 0, 255), 6)
        elif i == 1:
            cv2.circle(image, p, 15, (0, 0, 0), 2)
            cv2.circle(image, p, 11, (0, 255, 255), 6)
        elif i == 2:
            cv2.circle(image, p, 15, (0, 0, 0), 2)
            cv2.circle(image, p, 11, (0, 255, 0), 6)
        elif i == 3:
            cv2.circle(image, p, 15, (0, 0, 0), 2)
            cv2.circle(image, p, 11, (255, 0, 0), 6)
    return image


# Skip some frames
def skip_frames(sf):
    global fc, refPt, cc
    for i in range(sf):
        cap.read()
        fc = fc + 1
        print("Skipped frame " + str(fc))
    refPt = []
    cc = 0
    pass


# Overlay a shaded text on image
def put_shaded_text(image, text, position, font, scale, color, thickness=1, border=1):
    cv2.putText(image, text, position, font, scale, (7, 7, 7), thickness+(2*border))
    cv2.putText(image, text, position, font, scale, color, thickness)
    pass


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
        put_shaded_text(frame, "[1]", (20, 30), 5, 1, (0, 0, 255))
        put_shaded_text(frame, "[2]", (dimX - 60, 30), 5, 1, (0, 255, 255))
        put_shaded_text(frame, "[3]", (dimX - 60, dimY - 20), 5, 1, (0, 255, 0))
        put_shaded_text(frame, "[4]", (20, dimY - 20), 5, 1, (255, 0, 0))

        # Frame count overlay
        fc = fc + 1
        if (total_frames - fc) <= fs:
            put_shaded_text(frame, "[ Frame = " + str(fc) + " / " + str(int(total_frames)) + " ]   *** LAST FRAME OF THE FILE ***", (60, 30), 5,  1, (0, 127, 255))
        else:
            put_shaded_text(frame, "[ Frame = " + str(fc) + " / " + str(int(total_frames)) + " ]", (60, 30), 5, 1, (0, 127, 255))

        # Clone the current frame for resetting !!!
        overlaid_frame = frame.copy()

        # Open window in selected size
        if size_Val == 3:
            cv2.namedWindow("Frame", cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty("Frame", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        else:
            cv2.namedWindow("Frame")

        # Select point for tracking from frame
        cv2.setMouseCallback("Frame", mouse_events)

        # keep looping until a key pressed ???
        while True:
            draw_points(frame, refPt)
            # display the image and wait for click
            cv2.imshow("Frame", frame)
            key = cv2.waitKey(0) & 0xFF

            # Press 'Q' key to Exit
            if key == ord('q'):
                exit_screen = True
                while True:
                    frame = overlaid_frame.copy()
                    put_shaded_text(frame, "Do you want to quit? (Y/N)", (int(dimX / 2) - 200, int(dimY / 2)), 5,  1.2, (0, 127, 255), 2, 2)
                    cv2.imshow("Frame", frame)
                    key = cv2.waitKey(0) & 0xFF

                    if key == ord('y'):
                        print("\nQ > Exiting program")
                        sys.exit()
                    if key == ord('n'):
                        exit_screen = False
                        frame = overlaid_frame.copy()
                        break

            # Press 'S' key to Skip next frame
            if key == ord('s'):
                skip_frames(fs)
                print("\nS > " + str(fs) + " frames skipped and point selection reset\n")
                break

            # Press 'R' key to Reset points
            if key == ord("r"):
                frame = overlaid_frame.copy()
                refPt = []
                cc = 0
                print("\nR > Point selection reset\n")

            # Press 'C' key to Reset points
            if cc == 4 and key == ord("c"):
                print("\nC > Selected points confirmed\n")
                # refPt need to be stored before calling skip_frames()
                refPt.append(fc)
                refPtList.append(refPt)
                print(refPtList)
                skip_frames(fs)
                break

        # Display the resulting frame
        cv2.imshow('Frame', frame)

    # Break the loop
    else:
        break

# When everything done, release the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()
