#!/usr/bin/python

import SocketServer
import socket
import time
import ssl

class MyTCPHandler(SocketServer.BaseRequestHandler):
    def setup(self):
	self.request = ssl.wrap_socket(self.request,
				       certfile = 'server.crt.pem',
				       keyfile  = 'server.key.pem',
				       server_side = True,
				       cert_reqs = ssl.CERT_NONE,
				       ssl_version = ssl.PROTOCOL_SSLv23,
				       do_handshake_on_connect = False,
				       suppress_ragged_eofs = True)
    def handle(self):
	if False:
	    self.data = self.request.recv(1024).strip()
	    print "RECEIVED: [", self.data, "]"
	if True:
	    time.sleep(0.2)
	if True:
	    self.request.send('how')
	if True:
	    time.sleep(0.2)
	if True:
	    self.request.send('now')
	if True:
	    time.sleep(0.2)
	if True:
	    self.request.send('brown')
	if True:
	    time.sleep(0.2)
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
