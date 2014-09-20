#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import *
from geometry_msgs.msg import *
from math import *

distance = 0.8
dToWall = 1
range90 = 0
diff = 0.0
lin = 0.1
ang = 0.0

def callback(data):
    global dToWall, diff, range90
    dToWall = data.ranges[0]
    range90 = data.ranges[90]
    diff = data.ranges[45] - data.ranges[135]
    print 'distance to wall =' + str(dToWall)

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
        print distance
        print dToWall
        while distance <= dToWall:
            print 'in loop 1'
            teleop(pub,0.08,ang)
            r.sleep()
        teleop(pub,0,0)
        while range90 == 0 or diff >= 0.01:
            #print 'diff = ' + str(diff)
            print 'in loop 2'
            teleop(pub,0,-0.2)
            r.sleep()
        while dToWall >= 0.3 or dToWall == 0:
            print 'in loop 3'
            teleop(pub,1.0,0)
            r.sleep()
  
if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException: pass