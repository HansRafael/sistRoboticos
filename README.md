# sistRoboticos

## How to
First, it's necessary run the roscore.
```
roscore
```
Then, jump into the directory and type:
```
catkin_make
```
It's necessary update your bash also
```
source devel/setup.zsh
```
In the end, just run:
```
roslaunch stage_controller launcher.launch
or
roslaunch path_controller launcher.launch
```


## any changes
```
catkin_make
source devel/setup.zsh
```
f -> stop camera

odom -> nav_msgs/Odometry

