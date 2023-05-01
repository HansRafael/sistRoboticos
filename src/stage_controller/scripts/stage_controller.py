#! /usr/bin/env python3
import rospy 
from geometry_msgs.msg import *
from sensor_msgs.msg import *
from nav_msgs.msg import *
import random
import math
from tf.transformations import euler_from_quaternion

laser = LaserScan()
odometry = Odometry()

def odometry_callback(data):
	global odometry
	odometry = data
	
def laser_callback(data):
	global laser
	laser = data

if __name__ == "__main__": 
	rospy.init_node("stage_controller_node", anonymous=False)  

	rospy.Subscriber("/base_pose_ground_truth", Odometry, odometry_callback)

	rospy.Subscriber("/base_scan", LaserScan, laser_callback)

	target_x = 0.0
	target_y = 8.0

	min_distance = 0.1

	pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)    
	r = rospy.Rate(5) # 10hz
	velocity = Twist()
	while not rospy.is_shutdown():
		#print(laser.ranges)
		x = odometry.pose.pose.position.x
		y = odometry.pose.pose.position.y
		
		# Verifica se chegou ao alvo
		distance = math.sqrt((x-target_x)**2 + (y-target_y)**2)
		if (distance > min_distance):

			# FACA O SEU CODIGO AQUI
			orientation_q = odometry.pose.pose.orientation
			orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
			(roll, pitch, yaw) = euler_from_quaternion(orientation_list)
			angle_to_target = math.atan2(target_y-y, target_x-x)
			angle_diff = angle_to_target - yaw
			rospy.loginfo("Where i am: X: %s, Y: %s, Angle_target: %s, Angle_diff %s", x, y,angle_to_target,angle_diff)
			
			if (len(laser.ranges) > 0):
				if (min(laser.ranges[45*4:225*4]) > 0.25):
					velocity.linear.x = 0.5 * distance
					velocity.angular.z = 0.5 * angle_diff
					
				else:
					velocity.linear.x = 0.0
					velocity.angular.z = 0.5 * (angle_diff/angle_diff)
				
				pub.publish(velocity)


			
		else:
			velocity.linear.x = 0.0
			velocity.angular.z = 0.0
			pub.publish(velocity)
			rospy.loginfo("Alvo Alcancado!!!!!")		 
		
		# r.sleep()
		




