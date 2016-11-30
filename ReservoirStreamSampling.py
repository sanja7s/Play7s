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
import sys

#sys.stdout.flush()

lineCount = 0

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
				rndIndex = np.random.randint(0,k)
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

	print

	print "*** THIRD TEST CASE ***"
	print "*** randomly generated 1M characters string and k = 1000 ***"
	k = 1000
	testString3 = ''.join([str(unichr(el%26 + 65)) for el in testString2])
	s3 = []

	# reservoir sampling
	reservoirSampling(k, s3, testString3)
	printSample(s3)


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

	print


def printSample(sample):
	for el in sample:
		el = el.encode('utf-8')
		sys.stdout.write(el)
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

	
	BUFFER_SIZE=4096
	sample = []

	def read_from_stdin_text(fn, buffer_size=BUFFER_SIZE):
		while True:
			buf = sys.stdin.readline(buffer_size)
			if not buf:
				break
			fn(buf)

	def read_from_stdin_binary(fn, buffer_size=BUFFER_SIZE):
		while True:
			buf = sys.stdin.read(buffer_size)
			if buf == None:
				continue
			if not buf:
				break
			fn(buf)

	# fn is a lambda buf: ...., buf is either a string or byte array
	def read_from_stdin(fn, buffer_size=BUFFER_SIZE):
		if sys.stdin.isatty():
			read_from_stdin_text(fn, buffer_size)
		else:
			read_from_stdin_binary(fn, buffer_size)

	

	while (True):
		read_from_stdin(lambda data: reservoirSampling(k, sample, data))

	print 'SAMPLE OUTPUT'
	printSample(sample)


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
