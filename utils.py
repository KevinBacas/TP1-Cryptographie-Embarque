import random


def boolean_function(x1, x2, x3):
    x = x3 ^ (x2 << 1) ^ (x1 << 2)
    return (226 >> x) & 1


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
        res += (1 if ((f >> i) & 1) else -1)
    return res == 0


def update_lfsr(state, poly, n):
    sn = 0
    for i in xrange(n-1):
        sn ^= ((poly >> (i+1)) & 1) & ((state >> (n-1-i)) & 1)
    return ((state >> 1) ^ (sn << n-1)), (state & 1)


def generate_keystream_with_lfsr(state, poly, n, l):
    res = 0
    tmp_state = state
    for i in xrange(l):
        tmp_state, lower_bit = update_lfsr(tmp_state, poly, n)
        res = (lower_bit << i) ^ res
    return res


def generator(cle, l):
    cle1 = cle & 0b1111111111  			# 10 bits
    cle2 = (cle >> 10) & 0b11111111111  # 11 bits
    cle3 = (cle >> 21)  				# 12 bits
    poly1 = (1 << 10) ^ (1 << 3) ^ 1
    poly2 = (1 << 11) ^ (1 << 2) ^ 1
    poly3 = (1 << 12) ^ (1 << 6) ^ (1 << 4) ^ (1 << 1) ^ 1
    x1 = generate_keystream_with_lfsr(cle1, poly1, 10, l)
    x2 = generate_keystream_with_lfsr(cle2, poly2, 11, l)
    x3 = generate_keystream_with_lfsr(cle3, poly3, 12, l)
    res = 0
    for i in xrange(l):
        res = (res << 1) ^ boolean_function((x1 >> i) & 1, (x2 >> i) & 1, (x3 >> i) & 1)
    return res


def statistical_test(s1, s2, l):
    count = 0
    for i in xrange(l):
        if ((s1 >> i) & 1) == ((s2 >> i) & 1):
            count += 1
    return count > (l * 3 / 4)


def attaque_par_correlation():
    cle_random = random.randint(0, 1 << 33)
    cle1 = cle_random & 0b1111111111
    cle2 = (cle_random >> 10) & 0b11111111111
    cle3 = (cle_random >> 21)
    print "cle1 :", cle1
    print "cle2 :", cle2
    print "cle3 :", cle3
    cle_300 = generator(cle_random, 300)
    poly1 = (1 << 10) ^ (1 << 3) ^ 1
    poly2 = (1 << 11) ^ (1 << 2) ^ 1
    poly3 = (1 << 12) ^ (1 << 6) ^ (1 << 4) ^ (1 << 1) ^ 1

    # Recherche LFSR 1
    LFSR1 = 0
    foundLFSR1 = False
    while not foundLFSR1 and LFSR1 < (1 << 11):
        if statistical_test(cle_300, generate_keystream_with_lfsr(LFSR1, poly1, 10, 300), 300):
            foundLFSR1 = True
        else:
            LFSR1 += 1
    print statistical_test(cle_300, generate_keystream_with_lfsr(LFSR1, poly1, 10, 300), 300), LFSR1

    # Recherche LFSR 3
    LFSR3 = 0
    foundLFSR3 = False
    while not foundLFSR3 and LFSR3 < (1 << 13):
        if statistical_test(cle_300, generate_keystream_with_lfsr(LFSR3, poly3, 10, 300), 300):
            foundLFSR3 = True
        else:
            foundLFSR3 += 1
    print statistical_test(cle_300, generate_keystream_with_lfsr(LFSR3, poly3, 10, 300), 300), LFSR3
