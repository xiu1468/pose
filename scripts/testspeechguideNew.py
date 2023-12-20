#!/usr/bin/env python

import rospy
import tf
import time
import math
import playsound
from std_msgs.msg import Char

import pyttsx3

def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def listener():
    rospy.init_node('listener', anonymous=True)

    engine = pyttsx3.init()

    listener = tf.TransformListener()

    goal_positions = [(7.19630, -0.147726, 0.0),(5.8945, -3.06678, 0.0), (15, -4, 0.0), (12.43, -13.32, 0.0)]
    goal_mp3_files = ['CNC.mp3','車床.mp3', '焊工.mp3', '飛機引擎.mp3']  
    goal_index = 0
    goal_tolerance = 0.5
    angle_tolerance_degrees = 15

    # 创建发布者
    pub = rospy.Publisher('control_command', Char, queue_size=10)

    rate = rospy.Rate(10)

    # 初始化当前播放的mp3文件为None
    current_mp3 = None

    while not rospy.is_shutdown() and goal_index < len(goal_positions):
        goal_name = f"goal_{goal_index}"
        try:
            (trans, rot) = listener.lookupTransform('base_link', goal_name, rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue

        dx, dy = trans[0], trans[1]
        angle = math.atan2(dy, dx)

        if angle > math.pi:
            angle -= 2*math.pi
        if angle <= -math.pi:
            angle += 2*math.pi

        angle_degrees = math.degrees(angle)

        distance_to_goal = distance(0, 0, dx, dy)
        if distance_to_goal <= goal_tolerance:
            rospy.loginfo("Goal %d reached", goal_index)
            playsound.playsound('抵達目的地.mp3')
            #engine.say("Goal %d reached" % goal_index)
            # 在目标点抵达时播放对应的mp3
            pub.publish(115)
            if goal_index < len(goal_mp3_files):
                current_mp3 = goal_mp3_files[goal_index]
                playsound.playsound(current_mp3)
            goal_index += 1
            if goal_index < len(goal_positions):
                rospy.loginfo("Move to the next goal")
                #engine.say("Move to the next goal")
        else:
            if abs(angle_degrees) <= angle_tolerance_degrees:
            	
                rospy.loginfo("move forward")
                
                new_mp3 = '請往前走.mp3'
                if new_mp3 != current_mp3:
                    current_mp3 = new_mp3
                    playsound.playsound(current_mp3)
                pub.publish(119)  # 发布字符 'w'，代表向前移动
                
            elif angle > 0:
            	
                rospy.loginfo("turn left: %.2f degrees", angle_degrees)
                pub.publish(115)
                new_mp3 = '請向左轉.mp3'
                if new_mp3 != current_mp3:
                    current_mp3 = new_mp3
                    playsound.playsound(current_mp3)
                pub.publish(97)  # 发布字符 'a'，代表向左转
                
            else:
            	
                rospy.loginfo("turn right: %.2f degrees", -angle_degrees)
                pub.publish(115)
                new_mp3 = '請向右轉.mp3'
                if new_mp3 != current_mp3:
                    current_mp3 = new_mp3
                    playsound.playsound(current_mp3)
                pub.publish(100)  # 发布字符 'd'，代表向右转

        engine.runAndWait()
        rate.sleep()

    rospy.loginfo("All goals have been reached")
    pub.publish(115)
    engine.say("All goals have been reached")

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
