# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       kevin                                                        #
# 	Created:      1/17/2026, 7:24:34 AM                                        #
# 	Description:  IQ2 project                                                  #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *
import sys

# Brain should be defined by default
brain=Brain()

# DriveTrain setup
left_motor = Motor(Ports.PORT7, 1.0, True)
right_motor = Motor(Ports.PORT12, 1.0, False)

drivetrain = DriveTrain(lm=left_motor,rm=right_motor)

# Claw/Lift Motors
claw_motor = Motor(Ports.PORT4)
lift_motor = Motor(Ports.PORT11)

# Sensors
optical_sensor = Optical(Ports.PORT1)
touch_led_sensor = Touchled(Ports.PORT2)
distance_sensor = Distance(Ports.PORT9)
LUpRelease = Event()
LDownPress = Event()
LUpPress = Event()
LDownRelease = Event()
RDownPress = Event()
RDownRelease = Event()
RUpPress = Event()
RUpRelease = Event()

def clr_prnt(message):
    brain.screen.clear_screen()
    brain.screen.set_cursor(1,1)
    brain.screen.print(message)

def setup_motors():
    clr_prnt("Initializing...")
    lift_motor.set_velocity(100, PERCENT)
    claw_motor.set_velocity(100, PERCENT)


def autonomous_code():
    # autonomous code
    RDownPress.broadcast()
    wait(1000, MSEC)
    lift_motor.spin_for(REVERSE, 1000, DEGREES)
    drivetrain.drive_for(FORWARD, 310, MM)
    drivetrain.turn_for(RIGHT, 14, DEGREES)
    drivetrain.drive_for(FORWARD, 51, MM)
    wait(500, MSEC)
    claw_motor.spin(FORWARD)
    lift_motor.spin_for(FORWARD, 1000, DEGREES)
    drivetrain.drive_for(FORWARD, 10, MM)
    claw_motor.spin(REVERSE)
    drivetrain.turn_for(LEFT, 20, DEGREES)
    lift_motor.spin_for(REVERSE, 1000, DEGREES)
    drivetrain.drive_for(FORWARD, 75, MM)

    #drivetrain.drive_for(REVERSE, 20, MM)
    #lift_motor.spin_for(FORWARD, 500, DEGREES)
    #claw_motor.spin(REVERSE)
    sys.exit()

def vrcode():
    #drivetrain.drive_for(FORWARD, 390, MM)
    #drivetrain.turn_for(RIGHT, 45, DEGREES)
    #drivetrain.drive_for(FORWARD, 90, MM)
    #drivetrain.turn_for(RIGHT, 10, DEGREES)
    #lift_motor.spin_for(FORWARD, 60, DEGREES)
    #claw_motor.spin(FORWARD)
    lift_motor.spin_for(FORWARD, 400, DEGREES)
    claw_motor.spin(REVERSE)
    drivetrain.turn_for(LEFT, 75, DEGREES)
    lift_motor.spin_for(REVERSE, 450, DEGREES)
    drivetrain.turn_for(RIGHT, 10, DEGREES)
    drivetrain.drive_for(FORWARD, 135, MM)
    lift_motor.spin_for(FORWARD, 90, DEGREES)
    claw_motor.spin(FORWARD)
    lift_motor.spin_for(FORWARD, 400, DEGREES)
    claw_motor.spin(REVERSE)
    lift_motor.spin_for(REVERSE, 1000, DEGREES)
    lift_motor.spin_for(REVERSE, 500, DEGREES)
    drivetrain.drive_for(FORWARD, 300, MM)
    drivetrain.turn_for(RIGHT, 45, DEGREES)
    drivetrain.drive_for(FORWARD, 200, MM)
    drivetrain.turn_for(LEFT, 2.5, DEGREES)
    lift_motor.spin_for(FORWARD, 480, DEGREES)
    claw_motor.spin(FORWARD)
    wait(1, SECONDS)
    drivetrain.drive_for(REVERSE, 200, MM)
    drivetrain.turn_for(LEFT, 87, DEGREES)
    lift_motor.spin_for(FORWARD, 1350, DEGREES)
    drivetrain.drive_for(FORWARD, 50, MM)
    claw_motor.spin(REVERSE)
    lift_motor.spin_for(REVERSE, 500, DEGREES)
    drivetrain.drive_for(FORWARD, 300, MM)
    drivetrain.turn_for(RIGHT, 8, DEGREES)
    claw_motor.spin(FORWARD)
    lift_motor.spin_for(FORWARD, 1100, DEGREES)
    claw_motor.spin(REVERSE)
    wait(1.5, SECONDS)
    drivetrain.drive_for(FORWARD, 200, MM)
    lift_motor.spin_for(REVERSE, 450, DEGREES)
    drivetrain.turn_for(LEFT, 43, DEGREES)
    drivetrain.drive_for(FORWARD, 220, MM)
    claw_motor.spin(FORWARD)
    wait(0.5, SECONDS)
    lift_motor.spin_for(FORWARD, 1150, DEGREES)
    claw_motor.spin(REVERSE)
    wait(0.5, SECONDS)
    drivetrain.turn_for(LEFT, 45, DEGREES)
    drivetrain.drive_for(FORWARD, 300, MM)
    drivetrain.turn_for(RIGHT, 45, DEGREES)
    drivetrain.drive_for(FORWARD, 165, MM)
    claw_motor.spin(FORWARD)
    wait(1, SECONDS)
    drivetrain.drive_for(REVERSE, 600, MM)


#### LIFT MOTOR UP CALLBACK ####
def cbLDownPress():
    lift_motor.spin(REVERSE)

def cbLDownRelease():
    lift_motor.stop()

#### LIFT MOTOR DOWN CALLBACK ####
def cbLUpPress():
    lift_motor.spin(FORWARD)

def cbLUpRelease():
    lift_motor.stop()

#### CLAW MOTOR CLOSE CALLBACK ####
def cbRDownPress():
    claw_motor.spin(REVERSE)

def cbRDownRelease():
    claw_motor.stop()

#### CLAW MOTOR OPEN CALLBACK ####
def cbRUpPress():
    claw_motor.spin(FORWARD)

def cbRUpRelease():
    claw_motor.stop()

# system event handlers
LDownPress(cbLDownPress)
LUpPress(cbLUpPress)
LDownRelease(cbLDownRelease)
LUpRelease(cbLUpRelease)
RDownPress(cbRDownPress)
RUpPress(cbRUpPress)
RDownRelease(cbRDownRelease)
RUpRelease(cbRUpRelease)
# add 15ms delay to make sure events are registered correctly.
wait(15, MSEC)

ws2 = Thread( autonomous_code )
setup_motors()
