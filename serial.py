import serial
import time
from multiprocessing import Process, Value, Array

def gothrusteps(quit):
	t = 0
	while not quit.value:
		a = get_moves(t)
		for i in range(4):
			serial[i].write(a[i])
		t+=1
		time.sleep(1)

def get_moves(t):
	for i in range

def douwantquit(quit):
	quit.value = True
	print "changed to true"

if __name__ == "__main__":
	quit = Value('i', 0)
	p1 = Process(target=gothrusteps, args=(quit,))
	p2 = Process(target=douwantquit, args=(quit,))
	p1.start()
	time.sleep(2)
	p2.start()
	p1.join()
	p2.join()