#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import *
from geometry_msgs.msg import *
from math import *

span = 50
LeftScan = 0
RightScan = 0
FrontScan = 0


def callback(data):
    global LeftScan, RightScan, FrontScan, count
    LeftScan = 0
    RightScan = 0
    FrontScan = 0
    countLeft = 1
    countRight = 1
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
    pub.publish(Twist(linear = Vector3(x=lin),angular = Vector3(z=ang)))


def main():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("scan", LaserScan, callback)
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    r = rospy.Rate(5) # 10hz
    while not rospy.is_shutdown():
        if FrontScan <= 0.2:
            teleop(pub,-0.5,0.2)
            print 'backup xD'
            r.sleep()
        elif LeftScan >= 0.2 and LeftScan <= 0.8:
            if RightScan == 0 or LeftScan <= LeftScan:
                teleop(pub,0.2,-0.8)
                print 'spinning'
                r.sleep()
            else:
                teleop(pub,0.2,0.8)
                print 'spinning'
                r.sleep()
        elif RightScan >= 0.2 and RightScan <= 0.8:
            if LeftScan == 0 or RightScan <= LeftScan:
                teleop(pub,0.2,0.8)
                print 'spinning'
                r.sleep()
            else:
                teleop(pub,0.2,-0.8)
                print 'spinning'
                r.sleep()
        else:
            teleop(pub,1,0)
            print 'forward '
            r.sleep()

        #print 'Front Average is ' + str(FrontScan)
        #print 'Left Average is ' + str(LeftScan)
        #print 'Right Average is ' + str(RightScan)
  
if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException: pass