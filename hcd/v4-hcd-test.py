#!/usr/bin/python
import SocketServer
import socket
import time
class MyTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
	if False:
	    self.data = self.request.recv(1024).strip()
	    print "RECEIVED: [", self.data, "]"
	if False:
	    time.sleep(0.5)
	if True:
	    self.request.send('60.1')
	if False:
	    time.sleep(0.5)
	if True:
	    self.request.send('234')
	if False:
	    time.sleep(0.5)
	if True:
	    self.request.send('\n')
	print "Handled a query at " + time.strftime("%H.%M.%S")
class V6Server(SocketServer.TCPServer):
    address_family = socket.AF_INET6
if __name__ == "__main__":
    print "IPv6 is NOT supported."
    server = SocketServer.TCPServer(("192.168.213.22", 1510), MyTCPHandler)
    server.serve_forever()
