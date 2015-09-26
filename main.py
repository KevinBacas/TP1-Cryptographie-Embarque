from utils import boolean_function, display_truth_table, is_balanced, statistical_test, generate_keystream_with_lfsr, attaque_par_correlation

if __name__ == '__main__':
    print boolean_function(1, 0, 0)

    display_truth_table(226, 3)

    print is_balanced(226, 3)

    print generate_keystream_with_lfsr(57, 105, 7, 20)

    val1 = 0b111
    val2 = 0b111
    print statistical_test(val1, val2, 3)

    attaque_par_correlation()
