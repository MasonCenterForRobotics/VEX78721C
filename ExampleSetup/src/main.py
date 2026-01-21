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
    wait(1, SECONDS)
    clr_prnt("Autonomous Code...")
    drivetrain.drive_for(FORWARD, 200, MM)
    drivetrain.drive_for(REVERSE, 200, MM)
    # open claw
    clr_prnt("Open claw...")
    RUpPress.broadcast()
    drivetrain.turn_for(LEFT, 45, DEGREES)
    drivetrain.drive_for(FORWARD, 200, MM)
    RUpRelease.broadcast()
    wait(0.5, SECONDS)
    # close claw
    clr_prnt("Close claw...")
    RDownPress.broadcast()
    wait(1, SECONDS)
    # lift motor up
    clr_prnt("Lift...")
    LDownPress.broadcast()
    wait(2, SECONDS)
    LDownRelease.broadcast()
    drivetrain.turn_for(RIGHT, 45, DEGREES)
    # lift motoro down
    clr_prnt("Lower...")
    LUpPress.broadcast()
    wait(1.5, SECONDS)
    LUpRelease.broadcast()

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
