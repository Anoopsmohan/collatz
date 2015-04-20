#! /usr/bin/python

import time
import gevent

from gevent.server import StreamServer

CACHE = {1: 1}
def collatz(n):
    global CACHE
    if n not in CACHE:
        if n % 2 == 0:
            CACHE[n] = 1 + collatz(n/2)[0]
        else:
            CACHE[n] = 2 + collatz((3*n + 1)/2)[0]
    return CACHE[n], n


def handle(socket, address):
    gevent.sleep(0)
    try:
        socket.send("Range from :\n")
        _from = int(socket.recv(10))
        socket.send("Range till :\n")
        to = int(socket.recv(10))
	if _from > 1000000 or to > 1000000 or _from > to:
            socket.send('Please enter the range between 1 - 1000000 \n')
	else:
    	    start_time = time.time()
    	    time_diff = lambda: '{}'.format(time.time() - start_time)
    	    result = max(collatz(i) for i in xrange(_from, to + 1))
    	    socket.send('Number: {}, Sequence: {}, Execution Time: {}'.format(result[1], result[0], time_diff()) + '\n')
    except Exception, e:
	socket.send('Exception : {} \n'.format(e))
    socket.close()

server = StreamServer(('127.0.0.1', 5000), handle)
server.serve_forever()
