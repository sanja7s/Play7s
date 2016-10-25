#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
	Write a stream sampler that picks a random (representative) 
	sample of size k from a stream of values with unknown and
	possibly very large length.
"""
import numpy as np
import heapq
import sys
sys.stdout.flush()

lineCount = 0

def rndSample(streamS, k):
	"""
	picks a random (representative) 
	sample of size k from the streamS
	"""
	rv = []

	for v in streamS:
		rv.append((v,np.random.random()))

	for v, r in heapq.nsmallest(k, rv, key=lambda x: x[1]):
		yield v


def internalTest(k=5):
	print [el for el in rndSample(testString, k)]

	largeSize = 1000000
	a = 0
	b = 10000
	testString2 = (b - a) * np.random.random(largeSize) + a 

	print [el for el in rndSample(testString2, k)]

	testString3 = np.random.randint(0,largeSize,largeSize)
	print testString3
	print [el for el in rndSample(testString3, k)]
	k = 5

	testString = "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG"

	rndIndices = np.random.random_integers(0,20,k)


	rndValues = [testString[i] for i in rndIndices]


	print rndValues



def processInput(k, line):
	global lineCount
	lineCount += 1
	print str(lineCount) + ': ',
	for el in rndSample(line.rstrip(), k):
		sys.stdout.write(str(el))
	print

def readStdin():
	global lineCount
	for line in sys.stdin:
		processInput(7, line)

def promptUser():
	print 'Type in first line the number k of sample elements you want \
	and in second line the stream of values to from which to sample'
	print'Otherwise type "quit" to exit.'
	while (True):
		kRead = False
		while not kRead:
			line = raw_input('INPUT k or quit> ')
			if line == 'quit':
				sys.exit()
			try:
				k = int(line)
				kRead = True
			except ValueError as e:
				print "Enter an integer value for the number of samples"
		line2 = raw_input('INPUT stream> ')
		processInput(k, line2)

if __name__ == "__main__":
	if '-' in sys.argv:
		readStdin()
	else:
		promptUser()