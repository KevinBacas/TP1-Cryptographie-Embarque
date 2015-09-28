def Boolean_function(x1, x2, x3) :
	x = x3 ^ (x2 << 1) ^ (x1 << 2)
	return ((226 >> x) & 1)

def binary_string(x, n):
	s = ''
	for i in range(n):
		if ((x >> i) & 1) == 1:
			s = "1" + s
		else:
			s = "0" + s
	return s

def display_truth_table(f, n):
	for i in range(1 << n):
		print binary_string(i, n), (f >> i) & 1

def is_balanced(f, n):
	res = 0
	for i in range(1 << n):
		res = res + (1 if ((f >> i) & 1) else -1)
	return res == 0

def update_LFSR(state, poly, n):
	sn = 0
	for i in xrange(n-1):
		sn = sn ^ ((poly >> (i+1))&1) & ((state >> (n-1-i))&1)
	return ((state >> 1) ^ (sn << (n-1))), (state & 1)

def generate_keystream_with_LFSR(state, poly, n, l):
	res = 0
	tmp_state = state
	for i in xrange(l):
		tmp_state, lower_bit = update_LFSR(tmp_state, poly, n)
		res = (lower_bit << i) ^ (res)
	return res
