#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import *
from geometry_msgs.msg import *
from math import *

span = 40
LeftScan = 0
RightScan = 0
FrontScan = 0

def callback(data):
    global LeftScan, RightScan, FrontScan, count
    LeftScan = 0
    RightScan = 0
    FrontScan = 0
    countLeft = 0
    countRight = 0
    countFront = 0
    for i in data.ranges[0:span]:
        if i != 0:
            LeftScan += i
            countLeft += 1
    for i in data.ranges[360-span/2:360]:
        if i != 0:
            FrontScan += i
            countFront += 1
    for i in data.ranges[0:span/2]:
        if i != 0:
            FrontScan += i
            countFront += 1
    LeftScan /= countLeft
    RightScan /= countRight


def teleop(pub,lin,ang):
    print'beforepub'
    pub.publish(Twist(linear = Vector3(x=lin),angular = Vector3(z=ang)))
    print'afterpub'


def main():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("scan", LaserScan, callback)
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    r = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        if FrontScan <= 0.2:
            teleop(pub,-0.5,0.2)
        elif LeftScan >= 0.2:
            if LeftScan >= RightScan:
                teleop(pub,0.2,0.8)
            else:
                teleop(pub,0.2,-0.8)
        elif RightScan >= 0.2:
            if RightScan >= LeftScan:
                teleop(pub,0.2,-0.8)
            else:
                teleop(pub,0.2,0.8)
        else:
            teleop(pub,0.8,0)


        print 'Front Left Average is ' + str(LeftScan)
        print 'Front Right Average is ' + str(RightScan)
  
if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException: pass