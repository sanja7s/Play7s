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

def rndSample(k, streamS):
	"""
	picks a random (representative) 
	sample of size k from the streamS
	"""
	rv = []

	for v in streamS:
		rv.append((v,np.random.random()))

	for v, r in heapq.nsmallest(k, rv, key=lambda x: x[1]):
		yield v


def printSample(k, streamS):
	for el in rndSample(k, streamS):
		sys.stdout.write(str(el) + ' ')
	print


def internalTest(k=100):

	print "*** first test case ***"
	print "*** given test string and k = 5 ***"
	k = 5
	testString = "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG"
	print testString
	printSample(k, testString)
	print
	

	print "*** second test case ***"
	print "*** randomly generated large test string and k = 1000 ***"
	largeSize = 1000000
	a = 0
	b = 10000
	k = 1000
	testString2 = np.random.randint(0,largeSize,largeSize)
	print testString2
	printSample(k, testString2)
	print



def processInput(k, line):
	global lineCount
	lineCount += 1
	print str(lineCount) + ': ',
	printSample(k, line.rstrip())
	

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
		internalTest()
	else:
		promptUser()