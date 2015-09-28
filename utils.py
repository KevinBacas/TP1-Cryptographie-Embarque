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
		res = res + ((f >> i) & 1)
	return res == ((1 << n) / 2)
