# MAUVe

Code for controlling the MAUVe motors and logging data and readings on BeagleBone Blue.
To run everything, run logger.py and sendimu.py in the background while running rotate.py or step.py in the foreground. If running both rotate.py and step.py, rotate.py should be in the background while step.py is in the foreground.

___

### Main program files

#### logger.py
Program that logs the variables sent by the other three main programs to their respective LCM channels. The log is output to a csv file named log.csv

#### rotate.py
Test program that sweeps the servo motor back and forth at a certain angle specified in the file

#### sendimu.py
Program that continuously runs the IMU and sends the variables to its LCM channel at 10 Hz

#### step.py
Test program that rotates the stepper motor at RPM specified in the file in the direction specified in the file
___

### Class files

#### Servo.py
Class for controlling the servo. 
See file for commented functions

#### Stepper2.py
Class for controlling the stepper. 
See file for commented functions

#### Switch.py
Class for controlling the switch. 
See file for commented functions
___

### Test program files

#### imu.py
Test program that runs the imu and prints the output

#### test_switch.py
Test program the continuously checks the switch state and prints a message every time a change has been detected.
___

### LCM backend files

#### gen_types.sh
The exlcm directory is necessary for the lcm code to run properly. If it gets deleted, run this script to regenerate these files. 

#### battery.lcm, imu.lcm, servo.lcm
The .lcm files contain the type information to generate the exlcm files.
