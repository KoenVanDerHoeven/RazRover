import RPi.GPIO as io
io.setmode(io.BCM)
import sys, tty, termios, time
import csv
import time
import math

# Define pins for motor 1
motor1_in1_pin = 22
motor1_in2_pin = 23
io.setup(motor1_in1_pin, io.OUT)
io.setup(motor1_in2_pin, io.OUT)

# Define pins for motor 2
motor2_in1_pin = 17
motor2_in2_pin = 18
io.setup(motor2_in1_pin, io.OUT)
io.setup(motor2_in2_pin, io.OUT)

# Define pins for the ultrasound sensor
TRIG = 12
ECHO = 6
io.setup(TRIG, io.OUT)
io.setup(ECHO, io.IN)
io.output(TRIG, False)

# Gets the key that has been pressed
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

# Moves motor 1 forward
def motor1_forward():
    io.output(motor1_in1_pin, True)
    io.output(motor1_in2_pin, False)
# Moves motor 1 backwards
def motor1_reverse():
    io.output(motor1_in1_pin, True)
    io.output(motor1_in2_pin, True)
# Moves motor 2 forward
def motor2_forward():
    io.output(motor2_in1_pin, True)
    io.output(motor2_in2_pin, False)
# Moves motor 2 backwards
def motor2_reverse():
    io.output(motor2_in1_pin, True)
    io.output(motor2_in2_pin, True)
#Stops the motors
def motor_stop():
    io.output(motor1_in1_pin, False)
    io.output(motor1_in2_pin, False)
    io.output(motor2_in1_pin, False)
    io.output(motor2_in2_pin, False)

# Instructions for when the user has an interface
print("w: acceleration")
print("a/d: steering")
print("r: get distance")
print("p: parse data")
print("c: clear data")
print("x: exit")

data = []

# Opens our CSV reader
with open('data.csv', 'wb') as csvfile:
    datawriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    # Infinitely run until the user types x
    while True:
        # Gets the keyboard character that is typed
        char = getch()
            
        # The car will drive forward when the "w" key is pressed
        if(char == "w"):
            print "RazRover moving forward"
            motor1_forward()
            motor2_forward()
            
        # The car will move left when the "a" key is pressed
        if(char == "a"):
            print "RazRover turning left"
            motor1_forward()
            motor2_reverse()

        # The car will move right when the "d" key is pressed
        if(char == "d"):
            print "RazRover turning right"
            motor1_reverse()
            motor2_forward()

        # The "q" key will  stop the car
        if(char == "q"):
            print "RazRover has stopped"
            motor_stop()

        # The "r" key will send a signal that will be used for reading data
        if(char == "r"):
            print "RazRover reading data please wait"
            time.sleep(0.5)
            io.output(TRIG, True)
            time.sleep(0.00001)
            io.output(TRIG, False)
            while io.input(ECHO)==0:
                pulse_start = time.time()
            while io.input(ECHO)==1:
                pulse_end = time.time()
            pulse_duration = pulse_end - pulse_start
            distance = pulse_duration * 17150
            distance = round(distance, 2)
            data.append(distance)
            datawriter.writerow([distance])
            print "Data read to RazRover and CSV file"

        # Parses the data to find the standard deviation and mean
        if(char == "p"):
            print "RazRover parsing its data"
            time.sleep(0.5)
            n = len(data)
            if n == 0:
                print "No data exists"
                n = 1
            sum_data = 0
            for i in data:
                sum_data = sum_data + i
            mean = sum_data / n
            print "Mean of data: ",mean
            x_mean = 0
            for i in data:
                middle = i - mean
                middle = middle * middle
                x_mean = x_mean + middle
            x_mean_n = x_mean / n
            s_d = x_mean_n**0.5
            print "Standard deviation of data: ",s_d
            
        # Clears our list data
        if(char == "c"):
            data = []
            print "RazRover data Cleared"
            
        # The "x" key will break the loop and exit the program
        if(char == "x"):
            print("RazRover terminated")
            motor_stop()
            break

        # Sets next character to default
        char = ""

# Program will cease all GPIO activity before terminating
io.cleanup()
