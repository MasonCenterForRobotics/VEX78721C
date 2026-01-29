# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       NolanParker                                                  #
# 	Created:      1/21/2026, 7:37:25 PM                                        #
# 	Description:  IQ2 project                                                  #
#                                                                              #
# ---------------------------------------------------------------------------- #

from vex import *

# Brain should be defined by default
brain = Brain()

# The internal EXP inertial sensor
brain_inertial = Inertial()

# The controller
controller = Controller()

# Drive motors
left_drive_1 = Motor(Ports.PORT1, False)
left_drive_2 = Motor(Ports.PORT7, False)
right_drive_1 = Motor(Ports.PORT6, True)
right_drive_2 = Motor(Ports.PORT12, True)

# Arm and claw motors will have brake mode set to hold
# Claw motor will have max torque limited
claw_motor = Motor(Ports.PORT4, True)
arm_motor = Motor(Ports.PORT10, True)

# Auxilary motors
motor_aux_1 = Motor(Ports.PORT11, False)
motor_aux_2 = Motor(Ports.PORT5, False)

# Max motor speed (percent) for motors controlled by buttons
MAX_SPEED = 50

#
# All motors are controlled from this function which is run as a separate thread
#
def drive_task():
    drive_left = 0
    drive_right = 0

    # setup the claw motor
    claw_motor.set_max_torque(25, PERCENT)
    claw_motor.set_stopping(HOLD)

    # setup the arm motor
    arm_motor.set_stopping(HOLD)

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
        drive_left = controller.axisA.position()
        drive_right = controller.axisD.position()

        # threshold the variable channels so the drive does not
        # move if the joystick axis does not return exactly to 0
        deadband = 15
        if abs(drive_left) < deadband:
            drive_left = 0
        if abs(drive_right) < deadband:
            drive_right = 0

        # Now send all drive values to motors

        # The drivetrain
        left_drive_1.spin(FORWARD, drive_left, PERCENT)
        left_drive_2.spin(FORWARD, drive_left, PERCENT)
        right_drive_1.spin(FORWARD, drive_right, PERCENT)
        right_drive_2.spin(FORWARD, drive_right, PERCENT)

        # Claw and Arm motors
        arm_motor.spin(FORWARD, control_l1, PERCENT)
        claw_motor.spin(FORWARD, control_r1, PERCENT)
 
        # and the auxilary motors
        motor_aux_1.spin(FORWARD, control_l2, PERCENT)
        motor_aux_2.spin(FORWARD, control_r2, PERCENT)

        # No need to run too fast
        sleep(10)

# Run the drive code
drive = Thread(drive_task)

# Python now drops into REPL
