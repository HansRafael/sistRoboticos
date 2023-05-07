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

	target_x = -2
	target_y = 5

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
			#rospy.loginfo("Where i am: X: %s, Y: %s, Angle_target: %s, Angle_diff %s", x, y,angle_to_target,angle_diff)
			
			if (len(laser.ranges) > 0):
				right_laser = max(laser.ranges[:300])
				left_laser = max(laser.ranges[780:1081])

				right_laser_movement = max(laser.ranges[300:540])
				left_laser_movemnt = max(laser.ranges[540:780])

				print(f'Laser left:{left_laser} ------ right{right_laser}')
				#print(f'Movemnt {right_laser_movement} ------ {left_laser_movemnt}')
				cabeca = max(right_laser, left_laser)
				
				if (min(laser.ranges[300:780]) > 0.25):
					if right_laser_movement > left_laser_movemnt:
						velocity.linear.x = 0.5 * distance
						velocity.angular.z = 0.5 * -angle_diff
					else:
						velocity.linear.x = 0.5 * distance
						velocity.angular.z = 0.5 * angle_diff
					
				else:
					velocity.linear.x = 0
					if right_laser+1 > left_laser:
						velocity.angular.z = -90
					if left_laser+1 > right_laser:
						velocity.angular.z = 90
				
				pub.publish(velocity)

		else:
			velocity.linear.x = 0.0
			velocity.angular.z = 0.0
			pub.publish(velocity)
			rospy.loginfo("Alvo Alcancado!!!!!")		 
		
		# r.sleep()
		




