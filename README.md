# sistRoboticos

## Rosmaster
```
roscore
```

## start
```
roslaunch stage_controller launcher.launch
```


## any changing
```
catkin_make
source devel/setup.zsh
```
f -> stop camera


odom -> nav_msgs/Odometry


pose: 
  pose: 
    position: 
      x: 0.45000014603139094
      y: 2.6333335453851503
      z: 0.0
    orientation: 
      x: 0.0
      y: 0.0
      z: 0.6997160753466033
      w: 0.7144210340559316



rosmsg show sensor_msgs/LaserScan 
std_msgs/Header header
  uint32 seq
  time stamp
  string frame_id
float32 angle_min
float32 angle_max
float32 angle_increment
float32 time_increment
float32 scan_time
float32 range_min
float32 range_max
float32[] ranges
float32[] intensities
