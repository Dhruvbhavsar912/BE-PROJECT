#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion, quaternion_from_euler
from math import atan2
from geometry_msgs.msg import Twist,Point



x=0.0
y=0.0
theta=0.0

def newOdom(msg):
	global x
	global y
	global theta

	x=msg.pose.pose.position.x
	y=msg.pose.pose.position.y
	rot_q=msg.pose.pose.orientation


	(roll,pitch,theta)=euler_from_quaternion([rot_q.x,rot_q.y,rot_q.z, rot_q.w ])

rospy.init_node("angle")

sub= rospy.Subscriber("/odom",Odometry,newOdom)
pub = rospy.Publisher("/cmd_vel",Twist,queue_size=1)

speed= Twist()
r=rospy.Rate(4)
goal=Point()
goal.x=0
goal.y=7

while not rospy.is_shutdown():
	inc_x=goal.x-x
	inc_y=goal.y-y

	print('om')
	angle_to_goal=atan2(inc_y,inc_x)
	print(angle_to_goal)

	print(angle_to_goal*180/3.14)



	pub.publish(speed)


	r.sleep()