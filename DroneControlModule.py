from djitellopy import tello
import time
import cv2
from HandLandmarkModule import handLandmarkDetector, in_circle

# Function to generate a unique filename for each photo
def generate_photo_filename():
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    photo_folder = "C:/Users/chenr/Documents/GitHub/HandGestureDJITello/TelloPhoto"
    return f"{photo_folder}/photo_{timestamp}.jpg"


def run_drone():
    # activate control center view (default=True)
    controlCenter = True

    speed = 40

    # set up Flight Control mode from start (default=False)
    fControl = False

    # set up Tello
    myTello = tello.Tello()
    myTello.connect()
    battery_level = myTello.get_battery()
    print("Current Battery Level:", battery_level)
    myTello.streamon()

    # set up cam and other settings
    width = 1200
    height = 700
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    WhiteColor = (255, 255, 255)

    ptime = 0
    ctime = 0
    counter = 0
    counterLandTakeoff = 0

    detector = handLandmarkDetector()

    while True:

        _, img = cap.read()


        if controlCenter:
            # create new background for joystick image (control center mode)
            background_image = cv2.imread('C:/Users/chenr/Documents/GitHub/HandGestureDJITello/BackGround/Galaxy.jpg')
            background_image = cv2.resize(background_image, (width, height))
            img2 = background_image.copy()

            img = detector.findHands(img, draw=False)
            fingerLs = detector.drawFingerPoint(img2)
            if fingerLs is not None:
                # Access image_trigger using detector.image_trigger
                image_trigger = detector.image_trigger

                if image_trigger:
                    # Display camera trigger in control panel
                    cv2.putText(img2, 'Camera', (width - 140, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255), 1)
                    photo_path = generate_photo_filename()
                    cv2.imwrite(photo_path, frame)
                    # Display saved photo path on terminal
                    print(f"Photo captured and saved as: {photo_path}")
                    detector.image_trigger = False
                    # Put program on hold and wait for the next hand gesture sign
                    time.sleep(0.8)
                    detector.image_trigger = False

        # if control center mode is set to false
        else:
            img2 = img
            img2 = detector.findHands(img, draw=False)
            fingerLs = detector.drawFingerPoint(img2)
            if fingerLs is not None:
                # Access image_trigger using detector.image_trigger
                image_trigger = detector.image_trigger

                if image_trigger:
                    # Display camera trigger in control panel
                    cv2.putText(img2, 'Camera', (width - 140, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255), 1)
                    photo_path = generate_photo_filename()
                    cv2.imwrite(photo_path, frame)
                    # Display saved photo path on terminal
                    print(f"Photo captured and saved as: {photo_path}")
                    detector.image_trigger = False
                    # Put program on hold and wait for the next hand gesture sign
                    time.sleep(0.8)
                    detector.image_trigger = False



        # get tello stream
        frame = myTello.get_frame_read().frame
        frame = cv2.resize(frame, (360, 240))
        # print(counter)

        # fps display on control panel
        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime
        cv2.putText(img2, "FPS: " + str(int(fps)), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, WhiteColor, 1)


        # draw control activation circles
        cv2.circle(img2, (int(width * 0.4), int(height * 0.1)), 25, WhiteColor, 2)
        cv2.circle(img2, (int(width * 0.6), int(height * 0.1)), 25, WhiteColor, 2)

        # tello battery status display on control panel
        battery = myTello.get_battery()
        cv2.putText(img2, f"Battery: {battery}%", (width - 140, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, WhiteColor, 1)

        # check if control mode is activated (if both index fingers in circles: activates control mode)
        try:
            if in_circle(int(width * 0.4), int(height * 0.1), 25, fingerLs[0]) and in_circle(int(width * 0.6), int(height * 0.1), 25, fingerLs[1]):
                counter += 1
                if counter == 30:
                    fControl = not fControl
                    print('Control activated:', fControl)
            else:
                counter = 0
        except:
            pass

        # Control mode panel set up display
        if fControl:
            cv2.putText(img2, 'CONTROL ACTIVATED', (446, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)
            # left joystick
            cv2.circle(img2, (int(width * 0.3), int(height * 0.45)), 125, WhiteColor, 3)
            # Add 'up' sign to the upper middle of the left joystick circle
            cv2.putText(img2, 'up', (int(width * 0.3) - 15, int(height * 0.45) - 70), cv2.FONT_HERSHEY_SIMPLEX, 1, WhiteColor, 2)
            # Add 'down' sign to the lower middle of the left joystick circle
            cv2.putText(img2, 'down', (int(width * 0.3) - 40, int(height * 0.45) + 90), cv2.FONT_HERSHEY_SIMPLEX, 1, WhiteColor, 2)
            # Add 'turnL' sign to the left middle of the left joystick circle
            cv2.putText(img2, 'TnL', (int(width * 0.3) - 110, int(height * 0.45)), cv2.FONT_HERSHEY_SIMPLEX, 1, WhiteColor,2)
            # Add 'turnR' sign to the right middle of the left joystick circle
            cv2.putText(img2, 'TnR', (int(width * 0.3) + 60, int(height * 0.45)), cv2.FONT_HERSHEY_SIMPLEX, 1, WhiteColor,2)


            # right joystick
            cv2.circle(img2, (int(width * 0.7), int(height * 0.45)), 125, WhiteColor, 3)
            # Add 'Fwd' sign to the upper middle of the right joystick circle
            cv2.putText(img2, 'Fwd', (int(width * 0.7) - 25, int(height * 0.45) - 70), cv2.FONT_HERSHEY_SIMPLEX, 1,WhiteColor, 2)
            # Add 'Bwd' sign to the lower middle of the right joystick circle
            cv2.putText(img2, 'Bwd', (int(width * 0.7) - 30, int(height * 0.45) + 90), cv2.FONT_HERSHEY_SIMPLEX, 1,WhiteColor, 2)
            # Add 'left' sign to the left middle of the right joystick circle
            cv2.putText(img2, 'L', (int(width * 0.7) - 110, int(height * 0.45)), cv2.FONT_HERSHEY_SIMPLEX, 1, WhiteColor,2)
            # Add 'right' sign to the right middle of the right joystick circle
            cv2.putText(img2, 'R', (int(width * 0.7) + 85, int(height * 0.45)), cv2.FONT_HERSHEY_SIMPLEX, 1, WhiteColor,2)

            # land drone circle
            cv2.circle(img2, (int(width * 0.4), int(height * 0.25)), 25, WhiteColor, 2)
            cv2.putText(img2, str('Land'), (int(width * 0.395) - 30, int(height * 0.25) - 40), cv2.FONT_HERSHEY_SIMPLEX,1, WhiteColor, 2)
            # takeoff drone circle
            cv2.circle(img2, (int(width * 0.6), int(height * 0.25)), 25, WhiteColor, 2)
            cv2.putText(img2, str('Takeoff'), (int(width * 0.59) - 40, int(height * 0.25) - 40), cv2.FONT_HERSHEY_SIMPLEX, 1, WhiteColor, 2)

            # Drone state (landing/take off)
            try:
                # Drone Landing
                if in_circle(int(width * 0.4), int(height * 0.25), 25, fingerLs[0]) or in_circle(int(width * 0.4),
                                                                                                 int(height * 0.25), 25,
                                                                                                 fingerLs[1]):
                    counterLandTakeoff += 1
                    if counterLandTakeoff == 20: myTello.land()
                    # print('Tello Landing!!!!' )

                # Drone takeoff
                elif in_circle(int(width * 0.6), int(height * 0.25), 25, fingerLs[0]) or in_circle(int(width * 0.6),
                                                                                                   int(height * 0.25),
                                                                                                   25, fingerLs[1]):
                    counterLandTakeoff += 1
                    if counterLandTakeoff == 20: myTello.takeoff()
                    # print('Tello Takeoff!!!!' )
                else:
                    counterLandTakeoff = 0
            except:
                pass

            # direction/velocity commands
            try:
                if in_circle(int(width * 0.3), int(height * 0.45), 125, fingerLs[0]) and in_circle(int(width * 0.7),int(height * 0.45),125, fingerLs[1]):
                    # left joystick
                    # up down
                    if fingerLs[0][1] > int(height * 0.45):
                        ud = (int(height * 0.45 - fingerLs[0][1])) / 125
                    else:
                        ud = (int(height * 0.45 - fingerLs[0][1])) / 125
                    # yaw velocity
                    if fingerLs[0][0] > int(width * 0.3):
                        yv = -((int(width * 0.3 - fingerLs[0][0])) / 125)
                    else:
                        yv = -(int(width * 0.3 - fingerLs[0][0])) / 125

                    # right joystick
                    # left right
                    if fingerLs[1][0] > int(width * 0.7):
                        lr = -((int(width * 0.7 - fingerLs[1][0])) / 125)
                    else:
                        lr = -(int(width * 0.7 - fingerLs[1][0])) / 125
                    # forward backward
                    if fingerLs[1][1] > int(height * 0.45):
                        fb = (int(height * 0.45 - fingerLs[1][1])) / 125
                    else:
                        fb = (int(height * 0.45 - fingerLs[1][1])) / 125

                    # send rc to tello
                    myTello.send_rc_control(int(lr * speed), int(fb * speed), int(ud * speed), int(yv * speed))
                    # print('left idx F: ', (int(lr*speed),int(fb*speed)), 'right idx F: ', (int(ud*speed),int(yv*speed)))

                # for safety check if one finger is outside of the joystick circles set velocity to 0
                else:
                    myTello.send_rc_control(0, 0, 0, 0)
                    cv2.circle(img2, (int(width * 0.3), int(height * 0.45)), 25, WhiteColor, cv2.FILLED)
                    cv2.circle(img2, (int(width * 0.7), int(height * 0.45)), 25, WhiteColor, cv2.FILLED)

            except:
                cv2.circle(img2, (int(width * 0.3), int(height * 0.45)), 25, WhiteColor, cv2.FILLED)
                cv2.circle(img2, (int(width * 0.7), int(height * 0.45)), 25, WhiteColor, cv2.FILLED)
                pass

                # Tello live stream into control center image
            try:
                img2[460:700, 420:780] = frame
            except:
                pass

        # Deactivation mode when drone out of control
        else:
            cv2.putText(img2, 'CONTROL DEACTIVATED', (426, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)
            cv2.putText(img2, 'To activate Tello hand controller', (340, 300), cv2.FONT_HERSHEY_SIMPLEX, 1, WhiteColor, 2)
            cv2.putText(img2, 'move both index fingers', (400, 340), cv2.FONT_HERSHEY_SIMPLEX, 1, WhiteColor, 2)
            cv2.putText(img2, 'into the boxes above', (430, 380), cv2.FONT_HERSHEY_SIMPLEX, 1, WhiteColor, 2)

            # Insert Tello videostream into control center
            try:
                img2[460:700, 420:780] = frame

            except:
                pass

        if controlCenter:
            cv2.imshow('Control Center', img2)
        else:
            cv2.imshow('Control Center', img2)
            cv2.imshow('WebcamImage', img)
            cv2.imshow('Tello', frame)


        key = cv2.waitKey(5) & 0xFF

        # Press 'q' to close and quit the program
        if key == 27 or key == ord('q'):
            break


    myTello.streamoff()
    myTello.land()

    cap.release()