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
        right_laser = max(state_scan[300:360])
        left_laser = max(state_scan[60:120])
        heading, current_distance = env.move()
        count = 0
        if len(state_scan) > 100000:
            print("nao entrei ne")
            if min(state_scan[0:30] > 0.25):
                action[0] = LINEAR_VEL
                action[1] = heading * 0.5

            else:
                action[0] = 0
                if right_laser > left_laser:
                    while min(state_scan[0:30] <= 0.25):  
                        action[1] = 1.5
                        state_scan = env.step(action)
                else:
                    while min(state_scan[0:30] <= 0.25):  
                        action[1] = -1.5
                        state_scan = env.step(action)
            action[1] = heading

        else:
            lidar_distances = env.get_scan()
            print(len(lidar_distances))
            right_laser = max(lidar_distances[0:1])
            left_laser = max(lidar_distances[50:60])
            min_distance = min(lidar_distances)
            print(f'Movemnt {right_laser} ------ {left_laser}')

            if min_distance < SAFE_STOP_DISTANCE:
                if turtlebot_moving:
                    
                    action[0] = 0.0
                    action[1] = -.5
                    state_scan = env.step(action)
                    turtlebot_moving = False
                    rospy.loginfo('Stop!')
            else:
                action[0] = LINEAR_VEL
                action[1] = heading * 0.5
                state_scan = env.step(action)
                turtlebot_moving = True
                rospy.loginfo('Distance of the obstacle : %f', min_distance)
            
        state_scan = env.step(action)
                
        r.sleep()
