import asyncore
import socket

class EchoHandler(asyncore.dispatcher_with_send):
    def handle_read(self):
        data = self.recv(1024)
        if data:
            self.send(data)

    def process_cmd(self, command):
        cmds = command.split('&')
        if cmds[0] is 's':
            mode = 1 # receive remote control
        elif cmds[0] is 'r':
            if cmds[1] is 'compressed':
                mode = 2 # send compressed image
            elif cmds[1] is 'raw':
                mode = 3 # send raw image

    def remote_control(self, cmd):
        pass

    def send_image(self):
        pass


class EchoServer(asyncore.dispatcher):
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print 'Incoming connection from %s' % repr(addr)
            handler = EchoHandler(sock)

server = EchoServer('localhost', 5005)
asyncore.loop()
