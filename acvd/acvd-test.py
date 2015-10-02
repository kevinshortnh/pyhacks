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
	    self.request.send('how')
	if False:
	    time.sleep(0.5)
	if True:
	    self.request.send('now')
	if True:
	    self.request.send('brown')
	if True:
	    self.request.send('cow')
	if True:
	    self.request.send('\n')
	print "Handled a query at " + time.strftime("%H.%M.%S")
class V6Server(SocketServer.TCPServer):
    address_family = socket.AF_INET6
if __name__ == "__main__":
    if socket.has_ipv6:
	print "IPv6 is supported."
	server = V6Server(("::ffff:10.0.0.29", 9999), MyTCPHandler)
    else:
	print "IPv6 is NOT supported."
	server = SocketServer.TCPServer(("10.0.0.29", 9999), MyTCPHandler)
    server.serve_forever()
