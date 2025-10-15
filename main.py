import cv2
import time

# define the video capture parameters
videoCaptureProject = None
main_window_closed_checker = False
camera_closed = False
grayscale_background = False
drone_control_active = False

# fps parameters
ptime = 0
ctime = 0


while True:
    if not camera_closed and videoCaptureProject is None:
        videoCaptureProject = cv2.VideoCapture(0)

    if not camera_closed:
        ret, frame = videoCaptureProject.read()

        if not ret:
            print('Failure to read video from the camera.')
            break

        # Flip the frame horizontally
        frame = cv2.flip(frame, 1)

        # Change the background color based on the grayscale_background flag
        if grayscale_background:
            # Convert the video frame to grayscale
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Convert the grayscale frame back to BGR format
            frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2BGR)

        # Add the text message "Camera Test" on the upper middle of the frame
        text_size = cv2.getTextSize("Camera Test", cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
        text_x = (frame.shape[1] - text_size[0]) // 2
        cv2.putText(frame, "Camera Test", (text_x, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Update and display FPS
        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime
        cv2.putText(frame, "FPS: " + str(int(fps)), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

        # Display the resulting frame
        if not main_window_closed_checker:
            cv2.imshow('video', frame)

    key = cv2.waitKey(1) & 0xFF

    # Press 'q' to close and quit the program
    if key == ord('q'):
        break
        
    # Press 'c' to close the camera lens without quitting the program (for camera lens test)
    elif key == ord('c'):
        if not camera_closed:
            videoCaptureProject.release()
            cv2.destroyWindow('video')
            main_window_closed_checker = True
            camera_closed = True

    # Press 'o' to open the camera lens window (for camera lens test)
    elif key == ord('o'):
        if main_window_closed_checker:
            videoCaptureProject = cv2.VideoCapture(0)
            cv2.namedWindow('video')
            main_window_closed_checker = False
            camera_closed = False

    # Press 'g' to start/stop grayscale (for camera lens test)
    elif key == ord('g'):
        grayscale_background = not grayscale_background

    # Press 'd' to start drone control panel
    elif key == ord('d'):
        if not camera_closed:
            videoCaptureProject.release()
            cv2.destroyWindow('video')
            main_window_closed_checker = True
            camera_closed = True

        # Run drone connection (Wi-Fi) test
        if not drone_control_active:
            from DroneConnectionTest import test_drone_connection

            if test_drone_connection():
                drone_control_active = True

            else:
                print("Tello is not connected!")
        else:
            drone_control_active = False

    if drone_control_active:
        from DroneControlModule import run_drone

        run_drone()

if videoCaptureProject is not None:
    videoCaptureProject.release()
cv2.destroyAllWindows()