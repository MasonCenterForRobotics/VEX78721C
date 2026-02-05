# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       VexTeamSquared                                          #
# 	Created:      1/4/2026, 2:19:54 PM                                         #
# 	Description:  IQ2 project                                                  #
#                                                                              #
# ---------------------------------------------------------------------------- #

from vex import *

# Brain should be defined by default
brain = Brain()

drivetrain = DriveTrain();

# The internal EXP inertial sensor
brain_inertial = Inertial()

# The controller
controller = Controller()

# Drive motors
left_drive_2 = Motor(Ports.PORT7, True)
right_drive_2 = Motor(Ports.PORT12,  False)

# Arm and claw motors will have brake mode set to hold
# Claw motor will have max torque limited
claw_motor = Motor(Ports.PORT4, False)
lift_motor = Motor(Ports.PORT11, True)

# Max motor speed (percent) for motors controlled by buttons
MAX_SPEED = 50

#
# All motors are controlled from this function which is run as a separate thread
#
def drive_task():
    drive_axis = 0
    turn_axis = 0

    # setup the claw motor
    claw_motor.set_max_torque(25, PERCENT)
    claw_motor.set_stopping(HOLD)

    # setup the arm motor
    lift_motor.set_stopping(HOLD)

    # loop forever
    while True:
        # buttons
        # Three values, max, 0 and -max.
        #
        control_l1  = (controller.buttonLUp.pressing() - controller.buttonLDown.pressing()) * MAX_SPEED
        control_r1  = (controller.buttonRUp.pressing() - controller.buttonRDown.pressing()) * MAX_SPEED
        control_l2  = (controller.buttonEUp.pressing() - controller.buttonEDown.pressing()) * MAX_SPEED
        control_r2  = (controller.buttonFUp.pressing() - controller.buttonFDown.pressing()) * MAX_SPEED

        # joystick tank control
        drive_axis = controller.axisD.position()
        turn_axis = controller.axisB.position()

        # threshold the variable channels so the drive does not
        # move if the joystick axis does not return exactly to 0
        deadband = 15
        if abs(drive_axis) + abs(turn_axis) > deadband:
            left_drive_2.set_velocity((drive_axis + turn_axis), PERCENT)
            right_drive_2.set_velocity((drive_axis - turn_axis), PERCENT)
        else:
            left_drive_2.set_velocity(0, PERCENT)
            right_drive_2.set_velocity(0, PERCENT)
        left_drive_2.spin(FORWARD)
        right_drive_2.spin(FORWARD)

        wait(20, MSEC)

        #if abs(drive_axis) < deadband:
            #drive_axis = 0
        #if abs(turn_axis) < deadband:
            #turn_axis = 0

       # # Now send all drive values to motors

       # # The drivetrain
        #left_drive_2.spin(FORWARD, drive_axis, PERCENT)
        #right_drive_2.spin(FORWARD, turn_axis, PERCENT)

        # Claw and Arm motors
        claw_motor.spin(FORWARD, control_r1, PERCENT)
 
        # and the auxilary motors
        lift_motor.spin(FORWARD, control_l2, PERCENT)
        # No need to run too fast
        sleep(10)

# Run the drive code
drive = Thread(drive_task)

# Python now drops into REPL
