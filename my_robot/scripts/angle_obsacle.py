#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion, quaternion_from_euler
import math
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist,Point
from move_base_msgs.msg import MoveBaseActionGoal
import os
import sys
from math import atan2



roll = pitch = yaw = 0.0
kp=0.5




pub = None


x=0.0
y=0.0
theta=0.0

goal_x=0.0
goal_y=0.0

def get_goal(msg):
    global goal_x,goal_y
    goal_x=msg.goal.target_pose.pose.position.x
    goal_y=msg.goal.target_pose.pose.position.y

    




def get_rotation (msg):
    global roll, pitch, yaw
    orientation_q = msg.pose.pose.orientation
    orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
    (roll, pitch, yaw) = euler_from_quaternion (orientation_list)
    global x
    global y
    global theta

    x=msg.pose.pose.position.x
    y=msg.pose.pose.position.y
    rot_q=msg.pose.pose.orientation
    




    #print yaw



def clbk_laser(msg):
    print("go")
    regions = {
        'right':  min(min(msg.ranges[0:143]), 10),
        'fright': min(min(msg.ranges[144:287]), 10),
        'front':  min(min(msg.ranges[288:431]), 10),
        'fleft':  min(min(msg.ranges[432:575]), 10),
        'left':   min(min(msg.ranges[576:713]), 10),
    }


    take_action(regions,msg)


def take_action(regions,msg):



    try:
        #msg = Twist()

       
        b=1.22368957412
        
        goal=Point()
        goal.x=goal_x
        goal.y=goal_y
        inc_x=goal.x-x
        inc_y=goal.y-y
        


        angle_to_rad=atan2(inc_y,inc_x)
        print('go1')
        print(x)
        print(y)
        angle_to_goal=angle_to_rad*180/3.14
        print(angle_to_goal)
        if ((regions['front'] < 1.0 and regions['fleft'] < 1.0) or (regions['front'] < 1.0 and regions['fright'] < 1.0) or (regions['fleft'] < 0.51 ) or (regions['fright'] < 0.51 ) or (regions['left'] < 0.51 ) or (regions['right'] < 0.51 ) or (regions['fright'] < 1.0 and regions['fleft'] < 1.0)  or (regions['fleft']<0.51) or (regions['fright']<1.0)) and (regions['front']<1.0) :

            if (-90.0<angle_to_goal<0.0) or (90.0<angle_to_goal<180.0):
                #(regions['fright']+regions['right'])>(regions['fleft']+regions['left'])
                print(angle_to_goal)
                print('right')

                print('**********************')
                print(regions['fright'])
                print(regions['right'])
                print('*********************')
                if regions['fright']<1.1:
                    target = 220 
                    print('left')
                else:
                    target = -220
                    print('right')

                command = Twist()
                r = rospy.Rate(10)

                while not rospy.is_shutdown():    
                  
                    region = {
                        'right':  min(min(msg.ranges[0:143]), 10),
                        'fright': min(min(msg.ranges[144:287]), 10),
                        'front':  min(min(msg.ranges[288:431]), 10),
                        'fleft':  min(min(msg.ranges[432:575]), 10),
                        'left':   min(min(msg.ranges[576:713]), 10),
                    }

                    
                    print(region)
                    target_rad=target*math.pi/180 
                    command.angular.z =kp*(target_rad-yaw)
                    pub.publish(command)
                    print("Target={} current:{}".format(round(target_rad,2),round(yaw,2)))
                     
                    if b==region['front']:
                        break
                    else:
                        b=region['front'] 
                    if (region['front'] > 1.0 and region['fleft'] > 1.0) or (region['right'] > 0.77) or (region['left'] > 0.77) or (region['front'] > 1.0 and region['fright'] > 1.0) or (region['front'] > 2.5) :
                        print('---------------------------------------')
                        print(region['fleft'])
                        print(region['fright'])
                        print(region['front'])
                        print("---------------------------------------")  
                        break

                
            else:
                print(angle_to_goal)
                print('left')
                print('**********************')
                print(regions['fleft'])
                print(regions['left'])
                print('*********************')
                if regions['fleft']<1.1:
                    target = -220 
                    print('right')
                else:
                    target = 220
                    print('left')
            
                command = Twist()
                r = rospy.Rate(10)

                while not rospy.is_shutdown():    
                    region = {
                        'right':  min(min(msg.ranges[0:143]), 10),
                        'fright': min(min(msg.ranges[144:287]), 10),
                        'front':  min(min(msg.ranges[288:431]), 10),
                        'fleft':  min(min(msg.ranges[432:575]), 10),
                        'left':   min(min(msg.ranges[576:713]), 10),
                    }
                    
                    target_rad=target*math.pi/180 
                    command.angular.z =kp*(target_rad-yaw)
                    pub.publish(command)
                    print("Target={} current:{}".format(round(target_rad,2),round(yaw,2)))
                     
                    if b==region['front']:
                        break
                    else:
                        b=region['front']
                
                    if (region['front'] > 1.0 and region['fleft'] > 1.0) or (region['front'] > 1.0 and region['fright'] > 1.0) or (region['right'] > 0.77) or (region['left'] > 0.77) or (region['front'] > 2.5) :
                        print('---------------------------------------')
                        print(region['fleft'])
                        print(region['fright'])
                        print(region['front'])
                        print(regions)
                        print("---------------------------------------")   
                        break

            #r.sleep()



            '''
            linear_x = 0.0
            angular_z = 0.0
            linear_y=0.0
            print("hi")

            mytext = 'पेहली फुर्सत गो निकल'
            print('hi')

            # Language in which you want to convert
            language = 'hi'

            myobj = gTTS(text=mytext, lang=language, slow=False)

            # Saving the converted audio in a mp3 file named
            # welcome1
            myobj.save("welcome1.mp3")

            # Playing the converted file
            os.system("mpg321 welcome1.mp3")
            '''

            





    except rospy.ROSInterruptException:
        rospy.loginfo("Ctrl-C caught. Quitting")



    


def main():
    global pub

    rospy.init_node('reading_laser')

    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

    sub1 = rospy.Subscriber ('/odom', Odometry, get_rotation)
    sub2 = rospy.Subscriber ('/move_base/goal', MoveBaseActionGoal , get_goal)

    sub = rospy.Subscriber('/scan', LaserScan, clbk_laser)


    rospy.spin()


if __name__ == '__main__':
    main()