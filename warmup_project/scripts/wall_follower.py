#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import *
from geometry_msgs.msg import *
from math import *

distance = 0.8
dToWall_old = 1.0
dToWall_new = 1.0
delta = 0.0
error = 0.0
error_old = 0.0
error_delta = 0.0
angle = 0.0
ang = 0.0

def callback(data):
    rospy.loginfo(rospy.get_caller_id()+"I heard %s",data.ranges[90])
    global dToWall_old, dToWall_new, angle, error, delta, error_delta
    dToWall_old = dToWall_new
    dToWall_new = 5
    for i in data.ranges:
        if i != 0:
            dToWall_new = min(dToWall_new,i)
    delta = dToWall_new - dToWall_old
    error_old = error
    error = distance - dToWall_new
    error_delta = abs(error) - abs(error_old)
    angle = data.ranges.index(dToWall_new)

    print 'dToWall = ' + str(dToWall_new)
    print 'spinning angle = ' + str(ang)
    print 'delta  = ' + str(delta)
    print 'error =' + str(error)
    print 'error_delta =' + str(error_delta)
       
#def callback2(data):
#    rospy.loginfo(rospy.get_caller_id()+"I heard %s",data.range[91])
#    global d2
#    print data
#    d2 = data.range[91]

def teleop(pub,ang):
    pub.publish(Twist(linear = Vector3(x=0.08),angular = Vector3(z=ang)))

def adjust(delta, error):
    global ang
    if error > 0 and error_delta > 0 and abs(ang)<=0.1:
        ang -= 0.01
        print('1')
    elif error > 0 and error_delta < 0:
        print('2')
        ang += 0.01
    elif error < 0 and error_delta > 0 and abs(ang)<=0.1:
        print('3')
        ang += 0.01
    elif error < 0 and error_delta < 0:
        print('4')
        ang -= 0.01



def main():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("scan", LaserScan, callback)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    r = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        r.sleep()
        adjust(delta, error)
        #print 'ang is now =' + str(ang)
        teleop(pub,ang)

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException: pass