#!/bin/sh
catkin_make
export TURTLEBOT3_MODEL=burger
source devel/setup.zsh
roslaunch path_controller launcher.launch
