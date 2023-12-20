#!/usr/bin/env python
import rospy
from std_msgs.msg import Int64
import sys
import tty
import termios

def main():
    rospy.init_node("keyboard_input")

    pub = rospy.Publisher("keyboard", Int64, queue_size=1000)
    rate = rospy.Rate(100)

    while not rospy.is_shutdown():
        ch = getch()
        print(ch)

        msg = Int64()
        msg.data = ord(ch)
        pub.publish(msg)
        rate.sleep()

        if ch == '\x1b':  # Check for ESC key (ASCII value 27)
            break

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass

