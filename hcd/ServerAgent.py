#!/usr/bin/python

"""
    ServerAgent.py -- example Server Agent for use with HealthCheck.
"""

import sys
import time
import socket
import getopt
import SocketServer

class MySocketServer(SocketServer.TCPServer):
    def __init__(self, server_address, RequestHandlerClass,
		 bind_and_activate=True, value=50, stimulus=False):
	self.value = value
	self.stimulus = stimulus
        SocketServer.TCPServer.__init__(self, server_address,
					RequestHandlerClass,
					bind_and_activate=True)
    def finish_request(self, request, client_address):
	self.RequestHandlerClass(request, client_address, self,
				 self.value, self.stimulus)
    def update(self, value):
	self.value = value

class MyTCPHandler(SocketServer.BaseRequestHandler):
    def __init__(self, request, client_address, server,
		 value=50, stimulus=False):
	self.value = value
	self.stimulus = stimulus
	SocketServer.BaseRequestHandler.__init__(self, request, client_address,
						 server)
    def handle(self):
	if self.stimulus:
	    self.data = self.request.recv(1024).strip()
	    print "RECEIVED: [", self.data, "]"
	self.request.send(str(self.value) + "\n");
	print "Handled a query with response [",self.value,"] at " + time.strftime("%H.%M.%S")

def usage():
    print "usage:", sys.argv[0], "[options]"
    print "    -h --help       display usage"
    print "    -H --host=      host name or IP (default: 127.0.0.1)"
    print "    -P --port=      port number     (default: 1510)"
    print "    -S --stimulus   expect stimulus (default: False)"
    print "    -D --datafile=  data filename   (default: None)"
    print "    -V --value=     initial value   (default: 50)"
    print "    -N --min=       minimum value   (default: 0)"
    print "    -X --max=       maximum value   (default: 100)"
    print "    -I --incr=      increment value (default: 0)"
    print ""
    print "By default, the reported value will slide from 'value',"
    print "between 'min' and 'max', in increments of 'incr'."
    print ""
    print "If a datafile name is supplied, the reported values will be read"
    print "from the file before handling each request. This supports"
    print "user-supplied values, without taking the Server Agent down."


def main():
    try:
	opts, args = getopt.getopt(sys.argv[1:], "hH:P:SD:V:N:X:I:",
	    ["help", "host=", "port=", "stimulus", "datafile=", "value=",
	    "min=", "max=", "incr="])
    except getopt.GetoptError, err:
	# print help information and exit:
	print str(err)
	usage()
	sys.exit(2)
    host = "127.0.0.1"
    port = 1510
    stimulus = False
    datafile = None
    value = 50
    min = 0
    max = 100
    incr = 0
    for o, a in opts:
	if o in ("-h", "--help"):
	    usage()
	    sys.exit()
	elif o in ("-H", "--host"):
	    host = a
	elif o in ("-P", "--port"):
	    port = int(a)
	    if port < 1 or port > 65535:
		print "Port must be from 1 to 65535"
	        sys.exit(2)
	elif o in ("-S", "--stimulus"):
	    stimulus = True
	elif o in ("-D", "--datafile"):
	    datafile = a
	elif o in ("-V", "--value"):
	    value = int(a)
	elif o in ("-N", "--min"):
	    min = int(a)
	elif o in ("-X", "--max"):
	    max = int(a)
	elif o in ("-I", "--incr"):
	    incr = int(a)
	else:
	    assert False, "unhandled option"
    server = MySocketServer((host, port), MyTCPHandler, True, value, stimulus)
    while True:
	if None != datafile:
	    try:
		v = open(datafile, 'r').read().strip()
	    except IOError:
		print " ".join(["Data file", "'" + datafile + "'",
		       "does not exist -- exiting"])
		sys.exit(2)
	    else:
		pass
	    try:
		value = float(v)
	    except ValueError, TypeError:
		print " ".join(["Data file", "'" + datafile + "'",
		       "contains non-numeric data", "'" + v + "'",
		       "-- exiting"])
		sys.exit(2)
	    else:
		pass
	server.update(value)
	server.handle_request()
	if None == datafile:
	    value += incr
	    if (value >= max):
		value = max
		incr = -incr
	    if (value <= min):
		value = min
		incr = -incr

if __name__ == "__main__":
    main()
