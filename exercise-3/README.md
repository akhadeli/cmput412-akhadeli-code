# CMPUT 412/503 Exercise 3

## Abdullah Khadeli and Ryan Rom

## Overview

This project implements various ROS nodes for controlling a Duckiebot:

- Image undistortion
- HSV Detection
- Color based navigation (behavioral execution)
- PID Controller implementation
- Lane following

## Package Structure

The main ROS package `my_package` contains the following key components:

- `src/undistort.py`: Implementation of the undistortion node
- `src/behavioral_execution.py`: Implementation of the behavioral execution node
- `src/color_detection.py`: Implementation of the color detection node
- `src/color_contours.py`: Implementation of the color contours node
- `src/pid_controller.py`: Implementation of the PID controller node, also used for the lane following demo

## Dependencies

The project requires:

- ROS 1/2
- Duckietown
- Python 3

## Usage

The project uses the standard Duckietown development container. To run:

1. Build the container:

```bash
dts devel build -f
```

2. Run the container:

```bash
dts devel run -R ROBOT_NAME -l LAUNCH_FILE [-X]
```

Launch files are located in the `/launchers` directory.

- `undistort.sh`: Launches the undistortion node
- `behavioral-execution.sh`: Launches the behavioral execution node
- `color-detection.sh`: Launches the color detection node
- `color-contours.sh`: Launches the color contours node
- `pid-controller.sh`: Launches the PID controller node
- `lane-following.sh`: Launches the lane following demo

## Maintainers

- Abdullah Khadeli (akhadeli@ualberta.ca)
- Ryan Rom (rom@ualberta.ca)
