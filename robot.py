import RPi.GPIO as GPIO
import time

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


def Forward():# Forward
 GPIO.output(IN1, GPIO.HIGH)
 GPIO.output(IN2, GPIO.LOW)
 GPIO.output(IN3, GPIO.LOW)
 GPIO.output(IN4, GPIO.HIGH)




def backward(): # Backward
 GPIO.output(IN1, GPIO.LOW)
 GPIO.output(IN2, GPIO.HIGH)
 GPIO.output(IN3, GPIO.HIGH)
 GPIO.output(IN4, GPIO.LOW)


def Right(): # RIGHT 
 GPIO.output(IN1, GPIO.HIGH)
 GPIO.output(IN2, GPIO.LOW)
 GPIO.output(IN3, GPIO.HIGH)
 GPIO.output(IN4, GPIO.LOW)

def Left(): # Left 
 GPIO.output(IN1, GPIO.LOW)
 GPIO.output(IN2, GPIO.HIGH)
 GPIO.output(IN3, GPIO.LOW)
 GPIO.output(IN4, GPIO.HIGH)





GPIO.cleanup()


