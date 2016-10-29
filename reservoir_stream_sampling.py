#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
	author: sanja7s
	---------------
	write a stream sampler that picks a random (representative) 
	sample of size k from a stream of values with an unknown and
	possibly very large length
"""
import sys
import numpy as np

def reservoir_sampling(k, sample, data, processedValues):
	"""
		uses probability calculation that after first k elements that we put in
		the sample or reservoir, each new element at a position j in the stream
		should be added with probability 1/j to the sample and, in that case,
		a random one from the elements currently saved should be removed. 
		*processedValues is an array of one int so to pass it by reference
	"""
	i = 0
	while len(sample) < k and i < len(data):
		el = data[i]
		i += 1
		sample.append(el)
		processedValues[0] += 1

	if len(sample) == k:
		for j in range(i, len(data)):
			el = data[j] 
			rnd_index = np.random.randint(0, processedValues[0])
			if rnd_index < k:
				sample[rnd_index] = el
			processedValues[0] += 1

	#print processedValues[0]

def print_sample(sample):
	for el in sample:
		sys.stdout.write(str(el))
	print


# this and function below adapt to stdin input type 
# adapted from (source https://gist.github.com/steakknife/8280661)
def read_from_stdin_text(fn, k, sample, buffer_size, processedValues):
	while True:
		buf = sys.stdin.readline(buffer_size)
		if not buf:
			break
		fn(k, buf, sample, processedValues)

# this and function above adapt to stdin input type 
# adapted from (source https://gist.github.com/steakknife/8280661)
def read_from_stdin_binary(fn, k, sample, buffer_size, processedValues):
	while True:
		buf = sys.stdin.read(buffer_size)
		if buf == None:
			continue
		if not buf:
			break
		fn(k, buf, sample, processedValues)

# depending on the platform and stdin input available, invoke the function
def read_from_stdin(fn, k, sample, buffer_size, processedValues):
	"""
		second option: stdin input
		splits the input in ~4kBs parts and 
		sends them one by one to the sampler  
	"""

	if sys.stdin.isatty():
		read_from_stdin_text(fn, k, sample, buffer_size, processedValues)
	else:
		read_from_stdin_binary(fn, k, sample, buffer_size, processedValues)

def internal_tests():
	"""
		first option: for runing the internal tests
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
	reservoir_sampling(k, s1, testString, [0])
	print_sample(s1)

	print
	
	
	print "*** SECOND TEST CASE ***"
	print "*** randomly generated 1M integer string and k = 100 ***"
	largeSize = 1000000
	k = 100
	testString2 = np.random.randint(0,largeSize,largeSize)
	s2 = []

	# reservoir sampling
	reservoir_sampling(k, s2, testString2, [0])
	print_sample(s2)

	print

	print "*** THIRD TEST CASE ***"
	print "*** randomly generated 1M characters string and k = 1000 ***"
	k = 1000
	testString3 = ''.join([str(unichr(el%26 + 65)) for el in testString2])
	s3 = []

	# reservoir sampling
	reservoir_sampling(k, s3, testString3, [0])
	print_sample(s3)


	print

	print "*** FOURTH TEST CASE (edge case, sample size is smaller than the stream) ***"
	print "we allow such requirement, and then just output the whole stream"
	print "*** randomly generated 77 digits string and k = 100 ***"
	k = 100
	testString4 = np.random.randint(0,10,77)
	s4 = []
	print_sample(testString4)

	# reservoir sampling
	reservoir_sampling(k, s4, testString4, [0])
	print_sample(s4)

	print


# make sure that the first line in the input is int = the sample size k
def get_sample_size():
	try:
		k = int(sys.stdin.readline().strip())
	except ValueError as e:
		print 'The input must contain the required sample size k in the first line. Exiting now.'
		return 0
	print 'SAMPLE SIZE ', k
	if k <= 0:
		print 'The sample is empty'
		return 0
	return k


if __name__ == "__main__":
	""" 
		First option: If you invoke this program with "-" as argument it runs several internal tests.

		Second option: in any other case, you can pipe in arguments from stdin. The program expects
					k in the first line and treats the rest of the input until EOF as the stream.
					*The program will wait until EOF (Ctrl+D) for the end of stream.
	"""

	if '-' in sys.argv:
		internal_tests()
	else:
		BUFFER_SIZE=4096
		k = get_sample_size()
		if k:
			sample = []
			processedValues = [0]
			read_from_stdin(lambda k, data, sample, processedValues: reservoir_sampling(k, sample, data, processedValues), \
				k, sample, BUFFER_SIZE, processedValues)
			print 'STREAM SAMPLE'
			print_sample(sample)


