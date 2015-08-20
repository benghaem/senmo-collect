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

while True:
	x_acc = random.randint(0,100)
	y_acc = random.randint(0,100)
	z_acc = random.randint(0,100)

	full_tuple = (x_acc, y_acc, z_acc)
	
	data_buffer.append(full_tuple)
	if len(data_buffer) > max_buffer:
		_ = data_buffer.pop(0)

	print(data_buffer[-1:])
	for window_size in windows:
		if len(data_buffer) >= window_size:
			sender.send_pyobj(data_buffer[-window_size:])

	socket.send_string("%s %i %i %i" % ("update", x_acc, y_acc, z_acc))
	sleep(0.08)
