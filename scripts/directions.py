#!/usr/bin/env python3
import pyttsx3
import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped, Point
from std_msgs.msg import String
import math
import tf

target_idx = 0

def chatterCallback(msg):
    global target_idx

    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y
    z = msg.pose.pose.position.z

    quat = (
        msg.pose.pose.orientation.x,
        msg.pose.pose.orientation.y,
        msg.pose.pose.orientation.z,
        msg.pose.pose.orientation.w)
    rpy = tf.transformations.euler_from_quaternion(quat)

    engine = pyttsx3.init()

    target_points = [Point(6.182, -2.3, 0.0), Point(14.81, -2.53, 0.0), Point(12.43, -13.32, 0.0)]
    dest_x, dest_y, dest_z = target_points[target_idx].x, target_points[target_idx].y, target_points[target_idx].z

    dist = math.sqrt(pow(x - dest_x, 2) + pow(y - dest_y, 2) + pow(z - dest_z, 2))

    current_yaw = rpy[2]

    dx = dest_x - x
    dy = dest_y - y
    theta = math.atan2(dx, dy) - current_yaw
    delta_theta = theta

    # Normalize the angle to be between -pi and pi
    if delta_theta > math.pi:
        delta_theta -= 2*math.pi
    if delta_theta <= -math.pi:
        delta_theta += 2*math.pi

    angle_degrees = int(delta_theta * 180.0 / math.pi)

    if dist > 1.5:
        if angle_degrees > 5:
            
            if delta_theta > 0:
                engine.say("turn left {} degrees.".format(angle_degrees))
            else:
                engine.say("turn right {} degrees .".format(angle_degrees))
        else :
            rospy.loginfo("Move forward")
            engine.say("Move forward")
    else:
        if target_idx < len(target_points) - 1:
            rospy.loginfo("Move to the next point")
            engine.say("Move to the next point")
            target_idx += 1
            dest_x, dest_y, dest_z = target_points[target_idx].x, target_points[target_idx].y, target_points[target_idx].z
        else:
            rospy.loginfo("Complete")
            engine.say("Complete")

    engine.runAndWait()

if __name__ == '__main__':
    rospy.init_node('amcl_pose_subscriber')

    sub = rospy.Subscriber('amcl_pose', PoseWithCovarianceStamped, chatterCallback)

    rospy.spin()