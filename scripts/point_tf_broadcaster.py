#!/usr/bin/env python

import rospy
import tf
from geometry_msgs.msg import PoseWithCovarianceStamped

car_pose = None

def amcl_pose_callback(msg):
    global car_pose
    car_pose = msg.pose.pose

def broadcaster():
    rospy.init_node('broadcaster', anonymous=True)
    rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, amcl_pose_callback)

    br = tf.TransformBroadcaster()
    rate = rospy.Rate(10)

    goal_positions = [(7.19630, -0.147726, 0.0),(5.8945, -3.06678, 0.0), (15, -4, 0.0), (12.43, -13.32, 0.0)]
    while not rospy.is_shutdown():
        if car_pose is None:
            continue

        # 發布自走車位置
        br.sendTransform((car_pose.position.x, car_pose.position.y, car_pose.position.z),
                         (car_pose.orientation.x, car_pose.orientation.y, car_pose.orientation.z, car_pose.orientation.w),
                         rospy.Time.now(),
                         "base_link",
                         "map")

        # 發布目標點位置
        for i, (x, y, z) in enumerate(goal_positions):
            goal_name = f"goal_{i}"
            br.sendTransform((x, y, z),
                             tf.transformations.quaternion_from_euler(0, 0, 0),
                             rospy.Time.now(),
                             goal_name,
                             "map")

        rate.sleep()

if __name__ == '__main__':
    try:
        broadcaster()
    except rospy.ROSInterruptException:
        pass
