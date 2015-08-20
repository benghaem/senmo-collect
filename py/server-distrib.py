#
# Python server implimentation
# Binds a PUB socket to 5556
# Sends fake sensor data
#

import zmq
import random
from time import sleep

context = zmq.Context()
socket = context.socket(zmq.PUSH)
socket.connect("tcp://localhost:5000")

with open('ecg_old.csv', 'r') as f:
	#get rid of garbage at top of file
	_ = f.readline()
	_ = f.readline()

	count = 0
	while True:

		time, y_val = f.readline().split(',')
		
		socket.send_string("%s %i %f" % ("ecg", count, float(y_val)))
		sleep(0.008)
		count = count + 1
