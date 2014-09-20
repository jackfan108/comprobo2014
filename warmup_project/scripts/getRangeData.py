#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import *
from geometry_msgs.msg import *
from math import *

distance = 0.8
dToWall = 0
diff = 0

def callback(data):
    for i in range(len(data.ranges)):
        print str(i) + str(data.ranges[i])

def main():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("scan", LaserScan, callback)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    r = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        rospy.spin
    r.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException: pass