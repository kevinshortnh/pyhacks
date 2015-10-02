#!/usr/bin/python
import SocketServer
import socket
import time
class MyTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
	if True:
	    self.data = self.request.recv(1024).strip()
	    print "RECEIVED: [", self.data, "]"
	if True:
	    self.request.send('40.0')
	if True:
	    self.request.send('\n')
	print "Handled a query at " + time.strftime("%H.%M.%S")
if __name__ == "__main__":
    server = SocketServer.TCPServer(("192.168.213.22", 1511), MyTCPHandler)
    server.serve_forever()
