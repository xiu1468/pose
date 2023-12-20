#!/usr/bin/env python

import rospy
from std_msgs.msg import Char

def control_command_callback(msg):
    # 在这里处理接收到的控制命令消息
    ch = msg.data

    # 根据接收到的控制命令执行相应的操作
    if ch == 119:
        rospy.loginfo("Received 'w' command: Move forward")
    elif ch == 97:
        rospy.loginfo("Received 'a' command: Turn left")
    elif ch == 100:
        rospy.loginfo("Received 'd' command: Turn right")
    else:
        rospy.loginfo(f"Received unknown command: {ch}")

def main():
    rospy.init_node('control_command_subscriber', anonymous=True)
    rospy.Subscriber('control_command', Char, control_command_callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
