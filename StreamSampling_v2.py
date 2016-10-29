#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
	author: sanja7s
	---------------
	write a stream sampler that picks a random (representative) 
	sample of size k from a stream of values with an unknown and
	possibly very large length.
"""
import numpy as np
import heapq
import sys

sys.stdout.flush()

lineCount = 0

def heapSampling(k, data, sampleHeap=[]):
	"""
	uses a heap to always keep k elements.
	randomess is achieved through assigning random numbers
	to the stream elements and then keeping always only
	the largest k elements.
	the memory used is the size of the sample k plus another
	k for the random numbers used in the process.
	"""

	i = 0
	while len(sampleHeap) < k and i < len(data):
		el = data[i]
		i += 1
		sampleHeap.append((np.random.random(), el))

	while i < len(data):
		el = data[i]
		i += 1
		heapq.heappushpop(sampleHeap,(np.random.random(), el))


def reservoirSampling(k, sample, data):
	"""
		uses probability calculation that after k, 
		each new element should be added with
		probability 1/k to the sample and in that case a
		random one from the current elements should be removed 
	"""

	i = 0
	while len(sample) < k and i < len(data):
		el = data[i]
		i += 1
		sample.append(el)

	if len(sample) == k:
		for j in range(i, len(data)):
			el = data[j] 
			if np.random.random() < 1.0/k:
				rndIndex = np.random.randint(0,k-1)
				sample[rndIndex] = el


def internalTest(k=100):
	"""
		First option for runing the internal tests
	"""
	# random seed
	S7S = np.random.randint(1000000)
	#print S7S
	np.random.seed(S7S)
	#print np.random.get_state()

	print "*** FIRST TEST CASE ***"
	print "*** given test string and k = 5 ***"
	k = 5
	testString = "THEQUICKBROWNFOXJUMPSOVERTHELAZYDOG"
	s1 = []
	print testString

	# reservoir sampling
	reservoirSampling(k, s1, testString)
	printSample(s1)

	"""
	# heap sampling
	heapSampling(k, testString, s1)
	sample = []
	for (r, el) in s1:
		sample.append(el)
	printSample(sample)
	"""

	print
	
	
	print "*** SECOND TEST CASE ***"
	print "*** randomly generated 1M integer string and k = 100 ***"
	largeSize = 1000000
	k = 100
	testString2 = np.random.randint(0,largeSize,largeSize)
	s2 = []

	# reservoir sampling
	reservoirSampling(k, s2, testString2)
	printSample(s2)

	"""
	# heap sampling
	heapSampling(k, testString2, s2)
	sample = []
	for (r, el) in s2:
		sample.append(el)
	printSample(sample)
	"""

	print

	print "*** THIRD TEST CASE ***"
	print "*** randomly generated 1M characters string and k = 1000 ***"
	k = 1000
	testString3 = ''.join([str(unichr(el%26 + 65)) for el in testString2])
	s3 = []

	# reservoir sampling
	reservoirSampling(k, s3, testString3)
	printSample(s3)

	"""
	# heap sampling
	heapSampling(k, testString3, s3)
	sample = []
	for (r, el) in s3:
		sample.append(el)
	printSample(sample)
	"""

	print

	print "*** FOURTH TEST CASE (edge case, sample size is smaller than the stream) ***"
	print "we allow such requirement, and then just output the whole stream"
	print "*** randomly generated 77 digits string and k = 100 ***"
	k = 100
	testString4 = np.random.randint(0,10,77)
	s4 = []
	printSample(testString4)

	# reservoir sampling
	reservoirSampling(k, s4, testString4)
	printSample(s4)

	"""
	# heap sampling
	heapSampling(k, testString4, s4)
	sample = []
	for (r, el) in s4:
		sample.append(el)
	printSample(sample)
	"""

	print


def printSample(sample):
	for el in sample:
		sys.stdout.write(unicode(el))
	print


def stdinInput(k=-1):
	"""
		Third option: stdin input
		And also the core fuction that splits the input in ~kBs and 
		sends them one by one to the sampler functions. 
	"""
	if k == -1:
		try:
			k = int(sys.stdin.readline().strip())
		except ValueError:
			print 'The input must contain the required sample size k in the first line. Exiting now.'
			return
	print 'SAMPLE SIZE ', k
	if k == 0:
		print 'Zero size sample is empty'
		return
	stream = sys.stdin
	cntRounds = 0

	# reservoir sample
	sample = []
	# say we wanna read around one kB per round
	data = stream.read(1024)#.strip()
	while (data):
		reservoirSampling(k, sample, data)
		cntRounds += 1
		data = stream.read(1024)#.strip()	
	print 'SAMPLE OUTPUT'
	printSample(sample)
	
	"""
	# heap sample
	heapSample = []
	# say we wanna read around one kB per round
	data = stream.read(1024).strip()
	while (data):
		heapSampling(k, data, heapSample)
		cntRounds += 1
		data = stream.read(1024).strip()

	sample = []
	for (r, el) in heapSample:
		sample.append(el)
	print 'SAMPLE'
	printSample(sample)
	"""

	#print cntRounds

def promptUser():
	"""
		Seond option: interactive user input
	"""

	print 'Enter k in one line and stream of values after that. '
	print 'Otherwise type "quit" to exit.'
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
				print 'Enter an integer value for the number of samples'
		# we seed a random int each time to increase the randomness 
		S7S = np.random.randint(1000000)
		np.random.seed(S7S)
		stdinInput(k)


if __name__ == "__main__":
	""" 
		First option: If you invoke this program with "1" as argument it runs several internal tests.
		Second option: If you invoke this program with "2" as argument, you are then prompted to interactively
					feed in to the program the number k of sample elements you want (in the first line)
					and in second line the stream of values from which to sample. 
		Third option: in any other case, you can pipe in arguments from stdin. Again the program expects
					k in the first line and treats the rest of the input until EOF as the stream.
			*In both, second and third case, the program will wait until EOF (Ctrl+D) for the end of stream.
			**Due to a python bug in 2.7 must press enter and twice Ctrl+D for the desired behavior.
	"""
	if '1' in sys.argv:
		internalTest()
	elif '2' in sys.argv:
		promptUser()
	else:
		stdinInput()
