# CMPUT 412/503 Exercise 2

## Abdullah Khadeli and Ryan Rom

## Overview

This project implements various ROS nodes for controlling a Duckiebot:

- Straight line driving
- Rotation
- Curved path following
- "D"-shaped path driving task with LED status indicators
- Wheel encoder reading and control
- Camera feed processing and annotation
- Basic publisher/subscriber nodes

## Package Structure

The main ROS package `my_package` contains the following key components:

- `src/d_path.py`: Implementation of the control the "D"-shaped path task
- `src/d_path_service.py`: Implementation of LED service for the "D"-shaped path task
- `src/straight.py`: Implementation of straight line task
- `src/rotate.py`: Implementation of rotation task
- `src/curve.py`: Implementation of curved path following task
- `src/wheel_encoder_reader_node.py`: Implementation of wheel encoder reader node (from docs)
- `src/wheel_control_node.py`: Implementation of wheel control node (from docs)
- `src/camera_node.py`: Implementation of camera subscriber node and annotation task
- `src/my_publisher_node.py`: Implementation of first publisher node (from docs)
- `src/my_subscriber_node.py`: Implementation of first subscriber node (from docs)

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

## Maintainers

- Abdullah Khadeli (akhadeli@ualberta.ca)
- Ryan Rom (rom@ualberta.ca)
