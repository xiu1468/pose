#!/usr/bin/env python

import rospy
import tf
import math

import pyttsx3

def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def listener():
    rospy.init_node('listener', anonymous=True)

    engine = pyttsx3.init()

    listener = tf.TransformListener()

    goal_positions = [(6.182, -2.3, 0.0), (14.81, -2.53, 0.0), (12.43, -13.32, 0.0)]
    goal_index = 0
    goal_tolerance = 0.5
    angle_tolerance_degrees = 15

    rate = rospy.Rate(10)
    while not rospy.is_shutdown() and goal_index < len(goal_positions):
        goal_name = f"goal_{goal_index}"
        try:
            (trans, rot) = listener.lookupTransform('base_link', goal_name, rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue

        

        dx, dy = trans[0], trans[1]
        angle = math.atan2(dy, dx)

        # Normalize the angle to be between -pi and pi
        if angle > math.pi:
            angle -= 2*math.pi
        if angle <= -math.pi:
            angle += 2*math.pi

        # Convert angle to degrees
        angle_degrees = math.degrees(angle)



        # Check if the goal is reached
        distance_to_goal = distance(0, 0, dx, dy)
        if distance_to_goal <= goal_tolerance:
            rospy.loginfo("Goal %d reached", goal_index)
            engine.say("Goal %d reached", goal_index)
            goal_index += 1
            if goal_index < len(goal_positions):
                rospy.loginfo("Move to the next goal")
                engine.say("Move to the next goal")
        else:
            #rospy.loginfo("Distance to goal %d: %.2f meters", goal_index, distance_to_goal)

            if abs(angle_degrees) <= angle_tolerance_degrees:
                rospy.loginfo("move forward")
                engine.say("move forward")
            elif angle > 0:
                rospy.loginfo("turn left: %.2f degrees", angle_degrees)
                engine.say("turn left: %.2f degrees", angle_degrees)
            else:
                rospy.loginfo("turn right: %.2f degrees", -angle_degrees)
                engine.say("turn right: %.2f degrees", -angle_degrees)

        engine.runAndWait()

        rate.sleep()

    rospy.loginfo("All goals have been reached")
    engine.say("All goals have been reached")

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
