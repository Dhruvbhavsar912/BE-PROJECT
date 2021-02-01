#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rospy
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, Point, Quaternion
import speech_recognition as sr
import pyttsx3
from gtts import gTTS
import os
import gazebo_msgs.msg
import geometry_msgs.msg
import time
from gazebo_msgs.srv import GetModelState
import pdb



class Block:
    def __init__(self, name, relative_entity_name):
        self._name = name
        self._relative_entity_name = relative_entity_name


class GoToPose():
    def __init__(self):

        self.goal_sent = False

        # What to do if shut down (e.g. Ctrl-C or failure)
        rospy.on_shutdown(self.shutdown)

        # Tell the action client that we want to spin a thread by default
        self.move_base = actionlib.SimpleActionClient(
            "move_base", MoveBaseAction)
        rospy.loginfo("Wait for the action server to come up")

        # Allow up to 5 seconds for the action server to come up
        self.move_base.wait_for_server(rospy.Duration(5))

    def goto(self, pos, quat):

        # Send a goal
        self.goal_sent = True
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = 'map'
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose = Pose(Point(pos['x'], pos['y'], 0.000),
                                     Quaternion(quat['r1'], quat['r2'], quat['r3'], quat['r4']))

        # Start moving
        self.move_base.send_goal(goal)

        # Allow TurtleBot up to 60 seconds to complete task
        success = self.move_base.wait_for_result(rospy.Duration(60))

        state = self.move_base.get_state()
        result = False

        if success and state == GoalStatus.SUCCEEDED:
            # We made it!
            result = True
        else:
            self.move_base.cancel_goal()

        self.goal_sent = False
        return result

    def shutdown(self):
        if self.goal_sent:
            self.move_base.cancel_goal()
        rospy.loginfo("Stop")
        rospy.sleep(1)


    _blockListDict = {
        'block_a': Block('person_standing', 'link'),

    }

    def show_gazebo_models(self):
        try:
            model_coordinates = rospy.ServiceProxy('/gazebo/get_model_state', GetModelState)
            for block in self._blockListDict.values():
                blockName = str(block._name)
                resp_coordinates = model_coordinates(blockName, block._relative_entity_name)
                print('\n')
                print(" X : " + str(resp_coordinates.pose.position.x))
                print(" Y : " + str(resp_coordinates.pose.position.y))
                x1=resp_coordinates.pose.position.x 
                y1=resp_coordinates.pose.position.y - 0.25
            return x1,y1

        except rospy.ServiceException as e:
            rospy.loginfo("Get Model State service call failed:  {0}".format(e))
    


if __name__ == '__main__':

    try:

        rospy.init_node('nav_test', anonymous=False)

        
        navigator = GoToPose()
        r = sr.Recognizer()

        # Loop infinitely for user to
        # speak
        n = 0
        while(n == 0):

            # Exception handling to handle
            # exceptions at the runtime
            try:

                # use the microphone as source for input.
                with sr.Microphone() as source2:

                    # wait for a second to let the recognizer
                    # adjust the energy threshold based on
                    # the surrounding noise level
                    r.adjust_for_ambient_noise(source2, duration=0.2)

                    # listens for the user's input
                    audio2 = r.listen(source2)

                    # Using ggogle to recognize audio
                    MyText = r.recognize_google(audio2)
                    MyText = MyText.lower()

                    print("Did you say "+MyText)
                    print("OK")
                    n = int(input())

                    if MyText == "origin":
                        x1 = 0.0
                        y1 = 0.0
                    elif MyText == "room 1":
                        x1 = -5.88
                        y1 = 5.65
                    elif MyText == "room 2":
                        x1 = -7.12
                        y1 = -6.3
                    elif MyText == "room 3":
                        x1 = 2.15
                        y1 = 5.65
                    elif MyText == "room 4":
                        x1 = 2.5
                        y1 = -6.3
                    elif MyText == "room 5":
                        x1 = 15.87
                        y1 = 6.69
                    elif MyText == "room 6":
                        x1 = 16.29
                        y1 = -5.58
                    elif MyText=="yogesh":
                        tuto =GoToPose()
                        x1,y1=tuto.show_gazebo_models()
                    else:
                        x1 = 0.0
                        y1 = 0.0
            except sr.RequestError as e:
                print("Could not request results; {0}".format(e))

            except sr.UnknownValueError:
                print("unknown error occured")

        # Customize the following values so they are appropriate for your location
        position = {'x': x1, 'y': y1}
        quaternion = {'r1': 0.000, 'r2': 0.000, 'r3': 0.000, 'r4': 1.000}

        rospy.loginfo("Going to (%s) pose", MyText)
        
        success = navigator.goto(position, quaternion)

        if success:
            rospy.loginfo("Hooray, reached the desired pose")
            mytext = 'नमस्ते, HOD सर आपको बुला रहे है'

            # Language in which you want to convert
            language = 'hi'

            myobj = gTTS(text=mytext, lang=language, slow=False)

            # Saving the converted audio in a mp3 file named
            # welcome
            myobj.save("welcome.mp3")

            # Playing the converted file
            os.system("mpg321 welcome.mp3")

        else:
            rospy.loginfo("The base failed to reach the desired pose")

        # Sleep to give the last log messages time to be sent
        rospy.sleep(1)

    except rospy.ROSInterruptException:
        rospy.loginfo("Ctrl-C caught. Quitting")

