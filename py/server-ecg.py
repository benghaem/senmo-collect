#
# Python server implimentation
# Binds a PUB socket to 5556
# Sends fake sensor data
#

import zmq
import random
from time import sleep

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5556")

sender = context.socket(zmq.PUSH)
sender.bind("tcp://*:5557")

sink = context.socket(zmq.PUSH)
sink.connect("tcp://localhost:5558")

sink.send(b'0')

max_buffer = 100
data_buffer = []
windows = (100,)

with open('senmo-collect/ecg_old.csv', 'r') as f:
	#get rid of garbage at top of file
	_ = f.readline()
	_ = f.readline()

	count = 0
	while True:
		# x_acc = random.randint(0,100)
		# y_acc = random.randint(0,100)
		# z_acc = random.randint(0,100)

		time, y_val = f.readline().split(',')
		# full_tuple = (x_acc, y_acc, z_acc)

		full_tuple = (count,float(y_val))

		data_buffer.append(full_tuple)
		if len(data_buffer) > max_buffer:
			_ = data_buffer.pop(0)

		print(data_buffer[-1:])
		for window_size in windows:
			if len(data_buffer) >= window_size:
				sender.send_pyobj(data_buffer[-window_size:])

		socket.send_string("%s %i %f" % ("update-ecg", count, float(y_val)))
		sleep(0.008)
		count = count + 1
