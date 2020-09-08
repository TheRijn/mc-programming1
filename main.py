import operator
from argparse import ArgumentParser

MIN_LENGTH = 2
MAX_LENGTH = 13
P_I_ENGLISH = [0.082, 0.015, 0.028, 0.042, 0.127, 0.022, 0.020, 0.061, 0.070,
               0.001, 0.008, 0.040, 0.024, 0.067, 0.075, 0.019, 0.001, 0.060,
               0.063, 0.090, 0.028, 0.001, 0.024, 0.002, 0.001, 0.001]
P_I_2_ENGLISH = 0.065


def main(filename):
    cipher_array = []

    with open(filename, 'r') as ciphertext:
        char = ciphertext.read(2)
        while char:
            cipher_array.append(int(char, base=16))
            char = ciphertext.read(2)

    key_length = find_key_length(cipher_array)
    key = find_key(cipher_array, key_length)
    print(" ".join(['{0:02X}'.format(x) for x in key]))
    decrypt(cipher_array, key)


def find_key_length(cipher_array):
    # Difference between p_i^2 and q_i^2
    diff_pi2_qi2 = {}

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

        diff_pi2_qi2[n] = abs(P_I_2_ENGLISH - sum(q_i_2))

    # Return the keylength with the smallest difference between p_i^2 and q_i^2
    return min(diff_pi2_qi2.items(), key=operator.itemgetter(1))[0]


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
                letter = chr(cipher_array[char] ^ key_value)

                if letter.isascii() and letter.islower():
                    q_i[ord(letter.lower()) - ord("a")] += 1

            qipi = [P_I_ENGLISH[letter_pos] * q_i[letter_pos]
                    for letter_pos in range(26)]

            sum_qi_pi[key_value] = sum(qipi)

        # Select the value with the highest p_i * q_i
        key[i] = sum_qi_pi.index(max(sum_qi_pi))

    return key


def decrypt(cipher_array, key):
    for i, letter in enumerate(cipher_array):
        print(chr(letter ^ key[i % len(key)]), end="")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("file", nargs='?', default="ciphertext.txt")
    args = parser.parse_args()
    main(args.file)
