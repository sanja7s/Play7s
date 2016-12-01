#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
	author: sanja7s
	---------------
	write answer(src,dest) function that returns minimum
	number of steps between two positions on a chess board
	that a knight can take. Knights move in L shape moves.


"""

# possible steps the knight can
# take from the src node
def step(src):
	# the row we are in
	i = int(src/8)
	# the column we are in
	j = src%8
	d = []

	# left moves
	if j >= 1:
		if i >= 2:
			# left moves up
			s = src - 16 - 1
			d.append(s)
		if i <= 5:
			s = src + 16 - 1
			d.append(s)
		if j >= 2:
			if i >= 1:
				s = src - 8 - 2
				d.append(s)	
			if i <= 6:
			# left moves down
				s = src + 8 - 2
				d.append(s)	


	if j <= 6:
		if i >= 2:
			# right moves up
			s = src - 16 + 1
			d.append(s)
		if i <= 5:
			# right moves down
			s = src + 16 + 1
			d.append(s)
		if j <= 5:
			if i >= 1:
				s = src - 8 + 2
				d.append(s)
			if i <= 6:
				s = src + 8 + 2
				d.append(s)


	return d

# BFS algorithm. It searches in levels
# all the steps from the source node;
# marking the nodes that are already visited.
# the algorithm stops when it reaches dest,
# this will be the minimum number of steps
# so the search is not exhaustive, as I first
# tried with recurisve algorithms ;)	
def answer(src, dest):
	visited = [0]*64
	if src == dest:
		return 0
	visited[src] = 1
	d = step(src)
	print d
	i = 0
	while True:
		i += 1
		d1 = []
		for node in d:
			if not visited[node]:
				#print node
				visited[node] = 1
				if node == dest:
					return i
				for el in step(node):
					d1.append(el)
		if set(d) == set(d1):
			return -1
		d = set(d1)
		print d


# this is a check for all possible pairs
# of positions. Moreover, it is a test of
# speed as eariler versions of my code did
# not finish for some combination of src, dest
def test():		
	for i in range (64):
		for j in range(64):
			print i, j, answer(i, j)

