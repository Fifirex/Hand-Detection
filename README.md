# Hand-Detection
This Repository contains all the code we plan to use for implementing a Hand Detection system, which powers a mechanical crane on wheels.

## Overview
We used the functions provided by mediapipe for [Hand Detection](https://google.github.io/mediapipe/solutions/hands.html) as the core of the program. We also used [cv2](https://opencv.org) libraries to enable camera live feed and to display the results.

Then we turn this .py file into an executable and using the [ROS](https://www.ros.org) software, we turn the matrix output by the program to movement coordinates, which are then passed to the Arduino file `Arduino_code.ino` (brilliant name, yes) which powers a bot equipped with the required components.

## The Code
Computing the landmarks for the different IDs issued by mediapipe, we first run a configuration cycle (`CONFIG_CYCLE`) to measre the extremes of the hand in the frame.

The cycle re runs everytime there is a `NULL` detection on the screen, making the code "switchable" between different people during the same run.

We then put all the detected gestures into a matrix for transmission. 

```
A = [TRNSL, CLAWED]
    [ROTAT, SWITCH]
```
* `TRNSL` is the value that tells the translation state for the bot. It is denoted the by `[-1, 0, 1]` for `[BWD, STOP, FWD]`. This is detected by the realtive position of the hand on the screen.

* `CLAWED` is the value that tells the crane of the bot to relese or pick up objects. It is denoted by `[0, 1]` for `[NOT_CLAWED, CLAWED]`. This is detected by the relative position of the middle finger tip to the palm.

* `ROTAT` is the value that tells the rotation state for the bot. It is denoted the by `[-1, 0, 1]` for `[ROT_R, NO_ROT, ROT_L]`. This is detected by the orientation of the hand on the screen, the bot rotates in the direction the thumb is pointing to.

* `SWITCH` is the value that tells the current state of the bot. It is denoted the by `[0, 1]` for `[OFF, ON]`. The bot is turned `ON` when it detectes  states `NO_ROT` and `STOP` for the first time.

> Note: The bot never rotates in the state of translation, to manage the perfect rotation of the bot. Hence, it is always under `NO_ROT` if the `TRNSL` is set to anything other than `STOP`, no matter the orientation of the hand on the screen.

## Get the code!
If you just want to test out the code without the ROS integrations, u can get the `nROSmaster.py` and run it with the above dependencies.

To get the entire Repo just run the following line on your command line to clone the Repo:

```
git clone https://github.com/Fifirex/Hand-Detection.git
```

Once you have the code, make sure to install all the required basic Python libraries using:

```
pip install numpy
pip install opencv-python
pip install mediapipe
```

Replace `pip` by `pip3` if you have both installed on your system.

## The Team
This project is created for the DIY Assignment this semester, and this is our team:

### Software
@Fifirex
@Aeroscythe

### Mechatronics
@Viswesh-N
@SM200602
