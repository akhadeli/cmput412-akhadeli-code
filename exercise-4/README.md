# CMPUT 412/503 Exercise 4

## Abdullah Khadeli and Ryan Rom

### Source Repo

[Here](https://github.com/ryankennethrom/cmput412-dtros)

NOTE: Some commits in the source repo are pushed under another student's name since that student put their name in the git global config in the lab machines. Unfortunately, we were not aware that they set their name in the global config. All code in the source repo is our own, and commited by ourselves through the lab machines.

## Overview

This project implements various ROS nodes for controlling a Duckiebot:

- Apriltag detection
- PID Controller implementation
- Crosswalk detection
- Safe navigation

## Package Structure

The main ROS package `my_package` contains the following key components:

- `src/apriltag_behavior.py`: Implementation of the apriltag behavior node
- `src/apriltag_detection.py`: Implementation of the apriltag detection node
- `src/apriltags.py`: Apriltag enum definition
- `src/image_publisher.py`: Implementation of the image publisher node
- `src/led_control.py`: Implementation of the LED control node
- `src/pid_controller.py`: Implementation of the PID controller node
- `src/pd_crosswalk.py`: Implementation of the crosswalk detection node
- `src/vehicle_avoidance.py`: Implementation of the safe navigation node

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

- `apriltag-behavior.sh`: Launches the AprilTag behavior node
- `apriltag-detection.sh`: Launches the AprilTag detection node
- `image-publishers.sh`: Launches the image publishers node
- `led-control.sh`: Launches the LED control node
- `pd-crosswalk.sh`: Launches the crosswalk detection node
- `pid-controller.sh`: Launches the PID controller node
- `vehicle-avoidance.sh`: Launches the vehicle avoidance node

## Maintainers

- Abdullah Khadeli (akhadeli@ualberta.ca)
- Ryan Rom (rom@ualberta.ca)
