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
import string
sys.stdout.flush()

lineCount = 0

def heapSample(k, data, sampleHeap=[], currentSampleSize = 0):
	"""
	uses a heap to always keep k elements.
	randomess is achieved through assigning random numbers
	to the stream elements and then keeping always only
	the largest k elements.
	The memory used is the size of the sample k plus another
	k for the random numbers used in the process.
	"""
	
	i = sampleSize
	for v in data:
		if i < k:
			sampleHeap.append((np.random.random(), v))
			i += 1
		elif i == k:
			heapq.heapify(sample)
			heapq.heappushpop(sampleHeap,(np.random.random(), v))
			i += 1
		else:
			heapq.heappushpop(sampleHeap,(np.random.random(), v))

	#print currentSampleSize
	#print len(sample)
	sample = []
	for (r, v) in sampleHeap:
		sample.append(v)

	return sample, i

def reservoirSample(k, sample, data, processedStreamSize):

	i = 0
	while len(sample) < k and i < len(data):
		el = data[i]
		i += 1
		sample.append(el)
		processedStreamSize += 1

	#printSample(sample)
	#print len(sample)

	if len(sample) == k:
		for j in range(i, len(data)):
			el = data[j] 
			if np.random.random() < 1.0/k:
				rndIndex = np.random.randint(0,k-1)
				#print processedStreamSize, 1.0/processedStreamSize, el, sample[rndIndex], rndIndex
				sample[rndIndex] = el
			processedStreamSize += 1

	return sample, processedStreamSize


def internalTest(k=100):

	S7S = np.random.randint(1000000)
	#print S7S
	np.random.seed(S7S)
	#print np.random.get_state()

	print "*** FIRST TEST CASE ***"
	print "*** given test string and k = 5 ***"
	k = 5
	testString = "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG"
	sample = []
	s1, s1Size = reservoirSample(k, sample, testString, 0)
	print testString
	printSample(s1)
	print
	
	
	print "*** SECOND TEST CASE ***"
	print "*** randomly generated 1M integer string and k = 100 ***"
	largeSize = 1000000
	a = 0
	b = 10000
	k = 100
	testString2 = np.random.randint(0,largeSize,largeSize)
	sample = []
	s2, s2Size = reservoirSample(k, sample, testString2, 0)
	printSample(s2)
	print

	print "*** THIRD TEST CASE ***"
	print "*** randomly generated 1M characters string and k = 1000 ***"
	largeSize = 1000000
	k = 1000
	testString3 = ''.join([str(unichr(el%26 + 65)) for el in testString2])
	sample = []
	s3, s3Size = reservoirSample(k, sample, testString3, 0)
	printSample(s3)
	print

	print "*** FOURTH TEST CASE (edge case, sample size is smaller than the stream) ***"
	print "we allow such requirement, and then just output the whole stream"
	print "*** randomly generated 77 digits string and k = 100 ***"
	k = 100
	testString4 = np.random.randint(0,9,77)
	sample = []
	s4, s4Size = reservoirSample(k, sample, testString4, 0)
	printSample(testString4)
	printSample(s4)
	print


def printSample(sample):
	for el in sample:
		sys.stdout.write(str(el))
	print


def stdinInput(k=0):
	"""
		core fuction that splits the input in ~kBs and sends them one by one
		to the sampler functions. 
	"""
	if k == 0:
		k = int(sys.stdin.readline().strip())
	print 'SAMPLE SIZE ', k
	stream = sys.stdin
	sample = []
	cntRounds = 0
	# say we wanna read around one kB per round
	data = stream.read(1024).strip()
	processedStreamSize = 0
	while (data):
		#sample, sampleSize = processInputPart(k, data, sample, sampleSize)
		sample, processedStreamSize = reservoirSample(k, sample, data, processedStreamSize)
		cntRounds += 1
		data = stream.read(1024).strip()
		#print data
	#print processedStreamSize
	print 'SAMPLE'
	printSample(sample)
	#print 'Total rounds ', cntRounds

def promptUser():
	print 'First option: If you invoke this program with "-"" argument \
	 it runs several internal tests. Second option: '
	print 'Feed in to the program \
	in the first line the number k of sample elements you want \
	and in second line the stream of values to from which to sample'
	print'Otherwise type "quit" to exit.'
	while (True):
		kRead = False
		while not kRead:
			line = raw_input('INPUT k or quit> ')
			if line.strip() == 'quit':
				sys.exit()
			try:
				k = int(line)
				kRead = True
			except ValueError as e:
				print "Enter an integer value for the number of samples"
		# we seed a random int each time to increase the randomness 
		S7S = np.random.randint(1000000)
		np.random.seed(S7S)
		stdinInput(k)


if __name__ == "__main__":
	"""
		this program can be tested in several ways:
		"-" - it can be asked to run internal tests that are coded (3 such tests)
		"1" - it can prompt the user to enter the sample size and stream, interactively 
		"" - allows as another option that a stream is piped in to stdin, for instance from a file
			in this case it requires that k is in the first line, and the rest of the stdin input 
			will be treated as the stream 
	"""
	if '-' in sys.argv:
		internalTest()
	elif '1' in sys.argv:
		promptUser()
	else:
		stdinInput()
