#!/usr/bin/env python
import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion, quaternion_from_euler
from geometry_msgs.msg import Twist
import math


roll = pitch = yaw = 0.0
target=180
kp=0.5


def get_rotation (msg):
    global roll, pitch, yaw
    orientation_q = msg.pose.pose.orientation
    orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
    (roll, pitch, yaw) = euler_from_quaternion (orientation_list)
    #print yaw

rospy.init_node('my_robot')

sub = rospy.Subscriber ('/odom', Odometry, get_rotation)
pub= rospy.Publisher('/cmd_vel',Twist,queue_size=1)

r = rospy.Rate(10)
command = Twist()

while not rospy.is_shutdown():    
    #quat = quaternion_from_euler (roll, pitch,yaw)
    #print quat
    target_rad=target*math.pi/180
    command.angular.z =kp*(target_rad-yaw)
    pub.publish(command)
    print("Target={} current:{}".format(round(target_rad,2),round(yaw,2)))
    if round(target_rad,1)==round(yaw,1):
    	break
    r.sleep()