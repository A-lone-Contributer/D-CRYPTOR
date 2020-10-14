import random
import re
import string

import numpy as np


def DECRYPT(encoded_message):
    # for replacing non-alpha characters
    regex = re.compile('[^a-zA-Z]')

    letter_list = list(string.ascii_lowercase)

    # initialize Markov matrix
    M = np.ones((26, 26))

    # initial state distribution
    pi = np.zeros(26)

    # a function to update the Markov matrix
    def update_transition(ch1, ch2):
        i = ord(ch1) - 97
        j = ord(ch2) - 97
        M[i, j] += 1

    # a function to update the initial state distribution
    def update_pi(ch):
        i = ord(ch) - 97
        pi[i] += 1

    # get the log-probability of a word / token
    def get_word_prob(word):
        i = ord(word[0]) - 97
        logp = np.log(pi[i])

        for ch in word[1:]:
            j = ord(ch) - 97
            logp += np.log(M[i, j])  # update prob
            i = j  # update j

        return logp

    # get the probability of a sequence of words
    def get_sequence_prob(words):

        # if input is a string, split into an array of tokens
        if type(words) == str:
            words = words.split()

        logp = 0
        for word in words:
            logp += get_word_prob(word)
        return logp

    # a function to decode a message
    def decode_message(msg, word_map):
        decoded_msg = []
        for ch in msg:
            decoded_ch = ch  # could just be a space
            if ch in word_map:
                decoded_ch = word_map[ch]
            decoded_msg.append(decoded_ch)

        return ''.join(decoded_msg)

    def evolve_offspring(dna_pool, n_children):
        # make n_children per offspring
        offspring = []

        for dna in dna_pool:
            for _ in range(n_children):
                copy = dna.copy()
                j = np.random.randint(len(copy))
                k = np.random.randint(len(copy))

                # switch
                tmp = copy[j]
                copy[j] = copy[k]
                copy[k] = tmp
                offspring.append(copy)

        return offspring + dna_pool

    print("Decoding process started...")

    print("Calculating word probabilities...")

    # load in words
    for line in open("train.txt", encoding='utf-8'):
        line = line.rstrip()

        # there are blank lines in the file
        if line:
            line = regex.sub(' ', line)  # replace all non-alpha characters with space

            # split the tokens in the line and lowercase
            tokens = line.lower().split()

            for token in tokens:
                # update the model

                # first letter
                ch0 = token[0]
                update_pi(ch0)

                # other letters
                for ch1 in token[1:]:
                    update_transition(ch0, ch1)
                    ch0 = ch1

    print("Normalizing calculated probabilities...")
    pi /= pi.sum()
    M /= M.sum(axis=1, keepdims=True)

    print("Creating DNA Pool...")
    # this is our initialization point
    dna_pool = []
    for _ in range(525):
        dna = list(string.ascii_lowercase)
        random.shuffle(dna)
        dna_pool.append(dna)

    print("Starting mutation...")
    num_iters = 400
    scores = np.zeros(num_iters)
    best_dna = None
    best_map = None
    best_score = float('-inf')
    for i in range(num_iters):
        if i > 0:
            dna_pool = evolve_offspring(dna_pool, 20)

        # calculate score for each dna
        dna2score = {}
        for dna in dna_pool:
            # populate map
            current_map = {}
            for k, v in zip(letter_list, dna):
                current_map[k] = v

            decoded_message = decode_message(encoded_message, current_map)
            score = get_sequence_prob(decoded_message)

            # store it
            # needs to be a string to be a dict key
            dna2score[''.join(dna)] = score

            # record the best so far
            if score > best_score:
                best_map = current_map
                best_score = score

        # average score for this generation
        scores[i] = np.mean(list(dna2score.values()))

        # keep the best 25 dna
        # also turn them back into list of single chars
        sorted_dna = sorted(dna2score.items(), key=lambda x: x[1], reverse=True)
        dna_pool = [list(k) for k, v in sorted_dna[:25]]

        if i % 200 == 0:
            print("iter:", i, "score:", scores[i], "best so far:", best_score)

    print("Mutation complete!")

    # use best score
    decoded_message = decode_message(encoded_message, best_map)

    return decoded_message
