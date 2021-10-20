import RPi.GPIO as GPIO
import numpy as np
import time
import cv2

# for 1st Motor on ENA
ENA = 33
IN1 = 35
IN2 = 36

# for 2nd Motor on BNA
ENB = 32
IN3 = 37
IN4 = 38

# set pin numbers to the board's
GPIO.setmode(GPIO.BOARD)

# initialize EnA, In1 and In2
GPIO.setup(ENA, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN2, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ENB, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN3, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(IN4, GPIO.OUT, initial=GPIO.LOW)

# Stop
GPIO.output(ENA, GPIO.HIGH)
GPIO.output(IN1, GPIO.LOW)
GPIO.output(IN2, GPIO.LOW)
GPIO.output(ENB, GPIO.HIGH)
GPIO.output(IN3, GPIO.LOW)
GPIO.output(IN4, GPIO.LOW)


def Stop():
    GPIO.output(ENA, GPIO.HIGH)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(ENB, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)


def Forward():  # Forward
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)


def backward():  # Backward
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)


def Right():  # RIGHT
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)


def Left():  # Left
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)


def gstreamer_pipeline(
        capture_width=160,
        capture_height=120,
        display_width=160,
        display_height=120,
        framerate=30,
        flip_method=0,
):
    return (
            "nvarguscamerasrc ! "
            "video/x-raw(memory:NVMM), "
            "width=(int)%d, height=(int)%d, "
            "format=(string)NV12, framerate=(fraction)%d/1 ! "
            "nvvidconv flip-method=%d ! "
            "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
            "videoconvert ! "
            "video/x-raw, format=(string)BGR ! appsink"
            % (
                capture_width,
                capture_height,
                framerate,
                flip_method,
                display_width,
                display_height,
            )
    )


while True:

    # Capture the frames

    ret, frame = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)

    # Crop the image

    crop_img = frame[60:120, 0:160]

    # Convert to grayscale

    gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

    # Gaussian blur

    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Color thresholding

    ret, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY_INV)

    # Find the contours of the frame

    contours, hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)

    # Find the biggest contour (if detected)

    if len(contours) > 0:

        c = max(contours, key=cv2.contourArea)

        M = cv2.moments(c)

        cx = int(M['m10'] / M['m00'])

        cy = int(M['m01'] / M['m00'])

        cv2.line(crop_img, (cx, 0), (cx, 720), (255, 0, 0), 1)

        cv2.line(crop_img, (0, cy), (1280, cy), (255, 0, 0), 1)

        cv2.drawContours(crop_img, contours, -1, (0, 255, 0), 1)

        if cx >= 120:
            print("Turn Left!")

        if 120 > cx > 50:
            print("On Track!")

        if cx <= 50:
            print("Turn Right")



    else:

        print("I don't see the line")

    # Display the resulting frame

    cv2.imshow('frame', crop_img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

GPIO.cleanup()
