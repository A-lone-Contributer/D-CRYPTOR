import random
import re
import string


def ENCRYPT(message):

    # a function to encode a message
    def encode_message(msg, true_mapping):
        msg = msg.lower()

        regex = re.compile('[^a-zA-Z]')

        # replace non-alpha characters
        msg = regex.sub(' ', msg)

        # make the encoded message
        coded_msg = []
        for ch in msg:
            coded_ch = ch  # could just be a space
            if ch in true_mapping:
                coded_ch = true_mapping[ch]
            coded_msg.append(coded_ch)

        return ''.join(coded_msg)

    # create substitution cipher
    def substitution_cipher():

        letters1 = list(string.ascii_lowercase)
        letters2 = list(string.ascii_lowercase)

        true_mapping = {}

        # shuffle second set of letters
        random.shuffle(letters2)

        # populate map
        for k, v in zip(letters1, letters2):
            true_mapping[k] = v

        return true_mapping

    print("Generating random alphabet mapping...")

    mapping = substitution_cipher()

    encoded = encode_message(message, true_mapping=mapping)

    print("Encoding complete!")

    return encoded
