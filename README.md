ackermann_vehicle
=================

ROS packages for simulating a vehicle with Ackermann steering

This fork contains a vehicle with camera and IMU. It also loads a simple track.

## Dependencies
`ros-kinetic-ackermann-msgs`, `ros-kinetic-ackermann-controller`, 
`ros-kinetic-ros-control`, `ros-kinetic-ros-controllers`, 
`ros-kinetic-controller-interface`, `ros-kinetic-controller-manager`, 
`ros-kinetic-controller-manager-msgs`,
`ros-kinetic-gazebo-ros`, `ros-kinetic-gazebo-ros-control`, 
`ros-kinetic-gazebo-msgs`, `ros-kinetic-gazebo-ros-pkgs`,
`ros-kinetic-gazebo-plugins`    

## Usage
`roslaunch ackermann_vehicle_gazebo ackermann_vehicle.launch`

## Controlling the vehicle using ros topics
Highlevel control of the vehicle can be implemented by subscribing to the sensor topics and publishing to the `ackermann_cmd`topic. See [ackermann_controller](https://github.com/alfkjartan/ackermann_controller) for an example. 
