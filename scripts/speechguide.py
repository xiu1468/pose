#!/usr/bin/env python
import pyttsx3

import rospy
from geometry_msgs.msg import PoseStamped

def chatterCallback(msg):
    x = msg.pose.position.x
    y = msg.pose.position.y
    z = msg.pose.position.z
    engine = pyttsx3.init()
    if x > 10:
        rospy.loginfo("turn left")
        engine.say("turn left")
    elif x < -10:
        rospy.loginfo("turn right")
        engine.say("turn right")
    elif y > 60:
        rospy.loginfo("move backward")
        engine.say("move backward")
    elif y < 40:
        rospy.loginfo("move forward")
        engine.say("move forward")
    else:
        rospy.loginfo("stop")
        engine.say("stop")
    print("\n \n") 
"""
def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("chatter", PoseStamped, chatterCallback)
    rospy.spin()
"""
def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("chatter", PoseStamped, chatterCallback)
    rate = rospy.Rate(1)  # 1 Hz
    while not rospy.is_shutdown():
        rate.sleep()




if __name__ == '__main__':
    listener()
