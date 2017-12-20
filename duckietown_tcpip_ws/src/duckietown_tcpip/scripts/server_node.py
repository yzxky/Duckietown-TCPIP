#!/usr/bin/env python
import rospy
from duckietown_msgs.msg import Twist2DStamped
import asyncore
import socket

class EchoHandler(asyncore.dispatcher_with_send):
    def __init__(self, sock, pub):
        asyncore.dispatcher_with_send.__init__(self, sock=sock)
        self.pub = pub

    def handle_read(self):
        data = self.recv(1024)
        if data:
            self.send(data)
            self.process_cmd(data)

    def process_cmd(self, command):
        cmds = command.split('&')
        if cmds[0] is 's':
            mode = 1 # receive remote control
            print(mode)
            self.remote_control(cmds[1])
        elif cmds[0] is 'r':
            if cmds[1] is 'compressed':
                mode = 2 # send compressed image
            elif cmds[1] is 'raw':
                mode = 3 # send raw image

    def remote_control(self, cmd):
        (v, omega) = eval(cmd)
        msg = Twist2DStamped()
        msg.header.seq = 0
        msg.header.stamp = rospy.Time.now()
        msg.header.frame_id = ""
        msg.v = v
        msg.omega = omega
        self.pub.publish(msg)        

    def send_image(self):
        pass


class EchoServer(asyncore.dispatcher):
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.pub = rospy.Publisher('duckiebot1/joy_mapper_node/car_cmd', Twist2DStamped, queue_size = 10)

        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print 'Incoming connection from %s' % repr(addr)
            handler = EchoHandler(sock, self.pub)

try:
    rospy.init_node('tcp_server', anonymous = True)
    server = EchoServer('localhost', 5005)

    asyncore.loop()
except rospy.ROSInterruptException:
    pass
