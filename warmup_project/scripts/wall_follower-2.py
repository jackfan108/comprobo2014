#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import *
from geometry_msgs.msg import *
from math import *

distance = 0.8
dToWall = 1
range90 = 0
span = 20
diff = 0.0
lin = 0.1
ang = 0.0

def callback(data):
    global dToWall, range90, range1, range2, diff
    dToWall = data.ranges[0]
    range90 = data.ranges[90]
    range1 = data.ranges[90 - span]
    range2 = data.ranges[90 + span]
    diff = range1 - range2
    print 'distance to wall =' + str(dToWall)

def teleop(pub,lin,ang):
    pub.publish(Twist(linear = Vector3(x=lin),angular = Vector3(z=ang)))
def main():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("scan", LaserScan, callback)
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    r = rospy.Rate(5) # 10hz
    while not rospy.is_shutdown():
        print dToWall
        while distance <= dToWall:
            teleop(pub,0.15,ang)
            r.sleep()
        teleop(pub,0,0)
        while dToWall >= 0.3 or dToWall == 0:
            print 'range90 = ' + str(range90)
            print 'range1 = ' + str(range1)
            print 'range2 = ' + str(range2)
            print 'diff = ' + str(diff)
            if range90 == 0 or range1 == 0 or range2 == 0:
                teleop(pub,0,-0.5)
                r.sleep()
            elif diff >= 0.05:
                teleop(pub,0,0.5)
                r.sleep()
            elif diff <= -0.05:
                teleop(pub,0,-0.5)
                r.sleep()
                print 'spinning =D'
            else:
                teleop(pub,0.15,0)
                print 'running forward'
                r.sleep()
  
if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException: pass