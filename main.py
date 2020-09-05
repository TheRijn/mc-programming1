from pprint import PrettyPrinter
import operator

MIN_LENGTH = 2
MAX_LENGTH = 13
P_i = [0.082, 0.015, 0.028, 0.043, 0.13, 0.022, 0.020, 0.061, 0.070, 0.0015,
       0.0077, 0.04, 0.024, 0.067, 0.075, 0.019, 0.00095, 0.06, 0.063, 0.091,
       0.028, 0.0098, 0.024, 0.0015, 0.02, 0.00074]

pprint = PrettyPrinter().pprint


def main():
    cipher_array = []

    with open('ciphertext.txt', 'r') as ciphertext:
        while char := ciphertext.read(2):
            cipher_array.append(int(char, base=16))

    key_length = find_key_length(cipher_array)

    # key = find_key(cipher_array, key_length)

    # decrypt(cipher_array, key)


def find_key_length(cipher_array):
    sum_q_i_2 = {}

    # Iterate over all possible keylengths
    for n in range(MIN_LENGTH, MAX_LENGTH + 1):
        # List for q_0 ... q_255
        hist = [0 for _ in range(256)]

        # Count all occurrences into hist
        for i in range(0, len(cipher_array), n):
            hist[cipher_array[i]] += 1

        total = sum(hist)

        q_i = [(i / total) for i in hist]

        q_i_2 = [i ** 2 for i in q_i]

        sum_q_i_2[n] = sum(q_i_2)

    pprint(sum_q_i_2)

    maximum = max(sum_q_i_2.items(), key=operator.itemgetter(1))[0]
    return maximum


def find_key(cipher_array, key_length):
    key = [0 for _ in range(key_length)]

    # For every byte in key
    for i in range(key_length):
        sum_qi_pi = [0 for _ in range(256)]

        # Try all possible key values
        for key_value in range(256):
            q_i = [0 for _ in range(26)]

            # Count al letters within the i-th byte of the key
            for char in range(i, len(cipher_array), key_length):
                letter = chr(char ^ key_value)

                if letter.isascii() and letter.isalpha():
                    q_i[ord(letter.lower()) - ord("a")] += 1

            qipi = [P_i[letter_pos] * q_i[letter_pos] for letter_pos in range(26)]

            sum_qi_pi[key_value] = sum(qipi)

        key[i] = sum_qi_pi.index(max(sum_qi_pi))

    print(key)
    return key


def decrypt(ciper_array, key):
    for i, letter in enumerate(ciper_array):
        print(chr(letter ^ key[i % len(key)]), end="")


if __name__ == "__main__":
    main()
