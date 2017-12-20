#!/usr/bin/env python
import rospy
from duckietown_msgs.msg import Twist2DStamped

def talker():
    pub = rospy.Publisher('duckiebot/joy_mapper_node/car_cmd', Twist2DStamped, queue_size=10)
    rospy.init_node('car_ctr', anonymous=True)
    rate = rospy.Rate(10)
    count = 0
    ctr = '';
    while not rospy.is_shutdown():
        msg = Twist2DStamped()
        msg.header.seq = count
        msg.header.stamp = rospy.Time.now()
        msg.header.frame_id = ""
        msg.v = 0.3
        msg.omega = 0
        pub.publish(msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
