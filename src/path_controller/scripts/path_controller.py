#! /usr/bin/env python3
import rospy 
from geometry_msgs.msg import *
from sensor_msgs.msg import *
from nav_msgs.msg import *
import random
import math
from gazebo_msgs.msg import *
import numpy as np
import csv
import rospkg
import matplotlib.pyplot as plt
from matplotlib import cm
import time
from environment import Env
import math
from tf.transformations import euler_from_quaternion

LINEAR_VEL = 0.20
STOP_DISTANCE = 0.25
LIDAR_ERROR = 0.05
SAFE_STOP_DISTANCE = STOP_DISTANCE + LIDAR_ERROR

odometry = Odometry()

def odometry_callback(data):
	global odometry
	odometry = data

if __name__ == "__main__": 
    rospy.init_node("path_controller_node", anonymous=False)
    
    rospy.Subscriber('odom', Odometry, odometry_callback)
    
    env = Env()
    state_scan = env.reset()
    action = np.zeros(2)

    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)    
    r = rospy.Rate(5) # 10hz
    velocity = Twist()
    while not rospy.is_shutdown():
        # FACA SEU CODIGO AQUI
        heading, _ = env.move()
        if len(state_scan) > 100000:
            pass
        if len(state_scan) > 0:
            lidar_distances = env.get_scan()
            right_laser = min(lidar_distances[0:45])
            left_laser = min(lidar_distances[45:90])
            min_distance = min(lidar_distances)

            if min_distance < SAFE_STOP_DISTANCE:
                if turtlebot_moving:
                    action[0] = 0.0
                    if right_laser > left_laser:
                        action[1] = -.5
                    else:
                        action[1] = .5
                    state_scan = env.step(action)
                    turtlebot_moving = False
                    rospy.loginfo('Stop!')
            else:
                action[0] = LINEAR_VEL
                action[1] = heading * 0.60
                state_scan = env.step(action)
                turtlebot_moving = True
            
        state_scan = env.step(action)
                
        r.sleep()
