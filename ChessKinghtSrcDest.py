import numpy

# possible steps the knight can
# take from the src node
def step(src):
	# the row we are in
	i = int(src/8)
	# the column we are in
	j = src%8
	d = []

	# left moves
	if j >= 2:
		if i >= 2:
			# left moves up
			s = src - 8 - 2
			d.append(s)
			s = src - 16 - 1
			d.append(s)
		if i <= 5:
			# left moves down
			s = src + 8 - 2
			d.append(s)
			s = src + 16 - 1
			d.append(s)
	if j <= 5:
		if i >= 2:
			# right moves up
			s = src - 8 + 2
			d.append(s)
			s = src - 16 + 1
			d.append(s)
		if i <= 5:
			# right moves down
			s = src + 8 + 2
			d.append(s)
			s = src + 16 + 1
			d.append(s)
	return d

def answ(src, dest, m, visited):
	if m[src,dest]:
		return
	visited[src] = 1
	# possible step set
	d = step(src)
	print src, dest, d
	# if one of them is dest
	if dest in d:
		# assign distance 1
		m[src, dest] = 1
		m[dest, src] = 1
		return
	s = []
	for el in d:
		if visited[el]:
			s.append(m[el, dest])
			continue
		m[src,el] = 1
		m[el,src] = 1
		if m[el, dest] == 0:
			answ(el, dest, m, visited)
		s.append(m[el, dest])
	m[src, dest] = 1 + int(min(s)) 
	m[dest, src] = 1 + int(min(s)) 
	print s
	
def answ2(src, dest, visited):
	visited[src] = 1
	d = step(src)
	if dest in d:
		return 1
	s = []
	for el in d:
		if not visited[el]:
			n = answ2(el, dest, visited)
			s.append(n)
	
	if s == []:
		return 1000000
	return 1 + int(min(s)) 

def answer (src, dest):
    m = numpy.zeros(shape=(64,64))
    visited = numpy.zeros(shape=(64))
    answ(src, dest, m, visited)
    return int(m[src,dest])  

visited = numpy.zeros(shape=(64))
print answ2(19,44,visited)