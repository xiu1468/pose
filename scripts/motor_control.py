#!/usr/bin/env python
import rospy
from std_msgs.msg import Char
from std_msgs.msg import Int64
import sys
import tty


lv = 500
rv = 500
stop = 0
add_ve = 300
init = 1200
mv = 0
s1 = ""
s4 = ""
serial_part = "/dev/ttyUSB1"

GetAC1 = "1AC20\r"
GetAC4 = "4AC20\r"
GetDEC1 = "1DEC50\r"
GetDEC4 = "4DEC50\r"
GetRPM1 = "1GN\r"
GetRPM4 = "4GN\r"
start1 = "1EN\r"
start4 = "4EN\r"
stop1 = "1V0\r"
stop4 = "4V0\r"
go1 = "1V1200\r"
back1 = "1V-1200\r"
go4 = "4V-1200\r"
back4 = "4V1200\r"
right1 = "1V-700\r"
right4 = "4V-1600\r"
left1 = "1V1600\r"
left4 = "4V700\r"

def send_serial(com):
    global serial_part
    try:
        fd = open(serial_part, 'wb')
        fd.write(com.encode())
        fd.close()
    except Exception as e:
        rospy.logerr(f"Failed to send serial data: {e}")

def keyboard_number(msg):
    global lv, rv, stop, add_ve, mv, s1, s4
    rospy.loginfo("test")
    ch = msg.data
    if ch == 115:
        rv = 1000
        lv = 1000

    if ch == 119:  # W: go forward
        mv = min(lv, rv)
        lv = mv + add_ve
        rv = mv + add_ve
        send_serial(GetAC1)
        send_serial(GetAC4)
        s1 = f"1v{1500}\r"
        s4 = f"4v-{1510}\r"
        send_serial(s1)
        send_serial(s4)

    elif ch == 115:  # S: Stop
        send_serial(GetDEC1)
        send_serial(GetDEC4)
        s1 = f"1v{stop}\r"
        s4 = f"4v{stop}\r"
        send_serial(s1)
        send_serial(s4)

    elif ch == ord('x'):  # X: go backward
        mv = min(lv, rv)
        send_serial(GetAC1)
        send_serial(GetAC4)
        s1 = f"1v-{500}\r"
        s4 = f"4v{500}\r"
        send_serial(s1)
        send_serial(s4)

    elif ch == 100:  # D: turn right
        s1 = f"1v-{220}\r"
        s4 = f"4v-{220}\r"
        send_serial(s1)
        send_serial(s4)

    elif ch == 97:  # A: turn left
        s1 = f"1v{220}\r"
        s4 = f"4v{220}\r"
        send_serial(s1)
        send_serial(s4)


def main():
    global serial_part
    print(f"Opening the Serial Part {serial_part}")
    fd = None
    try:
        rospy.loginfo("go forward")
        fd = open(serial_part, 'wb')
        tty.setraw(sys.stdin.fileno())
        rospy.init_node("motor_serial")
        rospy.Subscriber("control_command", Char, keyboard_number)
        rospy.spin()
    except Exception as e:
        rospy.logerr(f"Failed to open the serial port: {e}")
    finally:
        if fd is not None:
            fd.close()

if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
