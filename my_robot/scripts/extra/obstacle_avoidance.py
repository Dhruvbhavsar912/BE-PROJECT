#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion, quaternion_from_euler
import math
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import os
import sys




roll = pitch = yaw = 0.0
kp=0.5



pub = None


def get_rotation (msg):
    global roll, pitch, yaw
    orientation_q = msg.pose.pose.orientation
    orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
    (roll, pitch, yaw) = euler_from_quaternion (orientation_list)
    #print yaw



def clbk_laser(msg):
    print("om")
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

        if ((regions['front'] < 0.8 and regions['fleft'] < 0.8) or (regions['front'] < 0.8 and regions['fright'] < 0.8) or (regions['fleft'] < 0.51 ) or (regions['fright'] < 0.51 ) or (regions['fright'] < 0.8 and regions['fleft'] < 0.8)  or (regions['fleft']<0.8) or (regions['fright']<0.8)) and (regions['front']<1.0) :
            if (regions['fright']+regions['right'])>(regions['fleft']+regions['left']):
                target = -220
                sub1 = rospy.Subscriber ('/odom', Odometry, get_rotation)
                pub1= rospy.Publisher('/cmd_vel',Twist,queue_size=1)
                
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
                    pub1.publish(command)
                    print("Target={} current:{}".format(round(target_rad,2),round(yaw,2)))
                     
                    if b==region['front']:
                        break
                    else:
                        b=region['front'] 
                    if (region['front'] > 0.8 and region['fleft'] > 0.8) or (region['front'] > 0.8 and region['fright'] > 0.8) or (region['fright'] > 0.8 and region['fleft'] > 0.8) or (region['front'] > 2.5) :
                        print('---------------------------------------')
                        print(region['fleft'])
                        print(region['fright'])
                        print(region['front'])
                        print("---------------------------------------")  
                        break

                
            else:
                target = 220

                sub1 = rospy.Subscriber ('/odom', Odometry, get_rotation)
                pub1= rospy.Publisher('/cmd_vel',Twist,queue_size=1)
               
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
                    pub1.publish(command)
                    print("Target={} current:{}".format(round(target_rad,2),round(yaw,2)))
                     
                    if b==region['front']:
                        break
                    else:
                        b=region['front']
                
                    if (region['front'] > 0.8 and region['fleft'] > 0.8) or (region['front'] > 0.8 and region['fright'] > 0.8) or (region['fright'] > 0.8 and region['fleft'] > 0.8) or (region['front'] > 2.5) :
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



    '''
    
    if regions['front'] < 1 and regions['fleft'] > 1 and regions['fright'] > 1:
        state_description = 'case 2 - front'
        linear_x = 0
        angular_z = -0.3
    elif regions['front'] > 1 and regions['fleft'] > 1 and regions['fright'] < 1:
        state_description = 'case 3 - fright'
        linear_x = 0
        angular_z = -0.3
    elif regions['front'] > 1 and regions['fleft'] < 1 and regions['fright'] > 1:
        state_description = 'case 4 - fleft'
        linear_x = 0
        angular_z = 0.3
    elif regions['front'] < 1 and regions['fleft'] > 1 and regions['fright'] < 1:
        state_description = 'case 5 - front and fright'
        linear_x = 0
        angular_z = -0.3
    elif regions['front'] < 1 and regions['fleft'] < 1 and regions['fright'] > 1:
        state_description = 'case 6 - front and fleft'
        linear_x = 0
        angular_z = 0.3
    elif regions['front'] < 1 and regions['fleft'] < 1 and regions['fright'] < 1:
        state_description = 'case 7 - front and fleft and fright'
        linear_x = 0
        angular_z = -0.3
    elif regions['front'] > 1 and regions['fleft'] < 1 and regions['fright'] < 1:
        state_description = 'case 8 - fleft and fright'
        linear_x = 0
        angular_z = -0.3
    else:
        state_description = 'unknown case'
    '''

    


def main():
    global pub

    rospy.init_node('reading_laser')

    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

    sub = rospy.Subscriber('/scan', LaserScan, clbk_laser)

    rospy.spin()


if __name__ == '__main__':
    main()