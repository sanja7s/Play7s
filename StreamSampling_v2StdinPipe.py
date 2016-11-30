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

	printSample(sample)
	print len(sample)

	if len(sample) == k:
		for j in range(i, len(data)):
			el = data[j] 
			if el == '\n':
				print 'NEWLINE', data, sample, processedStreamSize
			if np.random.random() < 1.0/k:
				rndIndex = np.random.randint(0,k-1)
				print processedStreamSize, 1.0/processedStreamSize, el, sample[rndIndex], rndIndex
				sample[rndIndex] = el
			processedStreamSize += 1

	return sample, processedStreamSize


def internalTest(k=100):

	S7S = np.random.randint(1000000)
	print S7S

	np.random.seed(S7S)

	#print np.random.get_state()

	print "*** FIRST TEST CASE ***"
	print "*** given test string and k = 5 ***"
	k = 5
	testString = "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG"
	#print testString
	printSample(k, testString)
	print
	
	
	print "*** SECOND TEST CASE ***"
	print "*** randomly generated 1M integer string and k = 100 ***"
	largeSize = 10000000
	a = 0
	b = 10000
	k = 100
	testString2 = np.random.randint(0,largeSize,largeSize)
	#print testString2
	printSample(k, testString2)
	print

	print "*** THIRD TEST CASE ***"
	print "*** randomly generated 1M characters string and k = 1000 ***"
	largeSize = 10000000
	k = 1000
	#testString2 = np.random.randint(0,largeSize,largeSize)
	#lettersNumbers = np.array(string.ascii_letters + string.digits, dtype=char)
	#print lettersNumbers.size
	#testString3 = ''.join([np.random.choice(lettersNumbers) for n in xrange(largeSize)])
	testString3 = ''.join([str(unichr(el%26 + 65)) for el in testString2])
	#print testString3
	printSample(k, testString3)
	print


def printSample(sample):
	for el in sample:
		sys.stdout.write(str(el))
	print


"""
if __name__ == "__main__":
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
	print processedStreamSize
	print 'SAMPLE'
	printSample(sample)
	#print 'Total rounds ', cntRounds
"""

def promptUser():
	print 'Type in first line the number k of sample elements you want \
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
		line2 = raw_input('INPUT stream> ')
		processInput(k, line2)

if __name__ == "__main__":
	if '-' in sys.argv:
		internalTest()
	else:
		promptUser()
