import string
import math
import pickle
import nltk
import re
from nltk import sent_tokenize

"""
This file contains the functions to truecase a sentence.
"""


def getScore(prevToken, possibleToken, nextToken, wordCasingLookup, uniDist, backwardBiDist, forwardBiDist,
             trigramDist):
    pseudoCount = 5.0

    # Get Unigram Score
    nominator = uniDist[possibleToken] + pseudoCount
    denominator = 0
    for alternativeToken in wordCasingLookup[possibleToken.lower()]:
        denominator += uniDist[alternativeToken] + pseudoCount

    unigramScore = nominator / denominator

    # Get Backward Score
    bigramBackwardScore = 1
    if prevToken != None:
        nominator = backwardBiDist[prevToken + '_' + possibleToken] + pseudoCount
        denominator = 0
        for alternativeToken in wordCasingLookup[possibleToken.lower()]:
            denominator += backwardBiDist[prevToken + '_' + alternativeToken] + pseudoCount

        bigramBackwardScore = nominator / denominator

    # Get Forward Score
    bigramForwardScore = 1
    if nextToken != None:
        nextToken = nextToken.lower()  # Ensure it is lower case
        nominator = forwardBiDist[possibleToken + "_" + nextToken] + pseudoCount
        denominator = 0
        for alternativeToken in wordCasingLookup[possibleToken.lower()]:
            denominator += forwardBiDist[alternativeToken + "_" + nextToken] + pseudoCount

        bigramForwardScore = nominator / denominator

    # Get Trigram Score
    trigramScore = 1
    if prevToken != None and nextToken != None:
        nextToken = nextToken.lower()  # Ensure it is lower case
        nominator = trigramDist[prevToken + "_" + possibleToken + "_" + nextToken] + pseudoCount
        denominator = 0
        for alternativeToken in wordCasingLookup[possibleToken.lower()]:
            denominator += trigramDist[prevToken + "_" + alternativeToken + "_" + nextToken] + pseudoCount

        trigramScore = nominator / denominator

    result = math.log(unigramScore) + math.log(bigramBackwardScore) + math.log(bigramForwardScore) + math.log(
        trigramScore)

    return result


def getTrueCase(tokens, outOfVocabularyTokenOption, wordCasingLookup, uniDist, backwardBiDist, forwardBiDist,
                trigramDist):
    """
    Returns the true case for the passed tokens.
    @param tokens: Tokens in a single sentence
    @param outOfVocabulariyTokenOption:
        title: Returns out of vocabulary (OOV) tokens in 'title' format
        lower: Returns OOV tokens in lower case
        as-is: Returns OOV tokens as is
    """
    tokensTrueCase = []
    for tokenIdx in range(len(tokens)):
        token = tokens[tokenIdx]
        if token in string.punctuation or token.isdigit():
            tokensTrueCase.append(token)
        else:
            if token in wordCasingLookup:
                if len(wordCasingLookup[token]) == 1:
                    tokensTrueCase.append(list(wordCasingLookup[token])[0])
                else:
                    prevToken = tokensTrueCase[tokenIdx - 1] if tokenIdx > 0 else None
                    nextToken = tokens[tokenIdx + 1] if tokenIdx < len(tokens) - 1 else None

                    bestToken = None
                    highestScore = float("-inf")

                    for possibleToken in wordCasingLookup[token]:
                        score = getScore(prevToken, possibleToken, nextToken, wordCasingLookup, uniDist, backwardBiDist,
                                         forwardBiDist, trigramDist)

                        if score > highestScore:
                            bestToken = possibleToken
                            highestScore = score

                    tokensTrueCase.append(bestToken)

                if tokenIdx == 0:
                    tokensTrueCase[0] = tokensTrueCase[0].title()

            else:  # Token out of vocabulary
                if outOfVocabularyTokenOption == 'title':
                    tokensTrueCase.append(token.title())
                elif outOfVocabularyTokenOption == 'lower':
                    tokensTrueCase.append(token.lower())
                else:
                    tokensTrueCase.append(token)

    return tokensTrueCase


f = open('distributions.obj', 'rb')
uniDist = pickle.load(f)
backwardBiDist = pickle.load(f)
forwardBiDist = pickle.load(f)
trigramDist = pickle.load(f)
wordCasingLookup = pickle.load(f)
f.close()


def truecasing_by_stats(input_text):
    truecase_text = ''
    sentences = sent_tokenize(input_text, language='english')
    for s in sentences:
        tokens = [token.lower() for token in nltk.word_tokenize(s)]
        tokensTrueCase = getTrueCase(tokens, 'lower', wordCasingLookup, uniDist, backwardBiDist, forwardBiDist,
                                     trigramDist)
        sTrueCase = re.sub(" (?=[\.,'!?:;])", "", ' '.join(tokensTrueCase))
        truecase_text = truecase_text + sTrueCase + ' '
    return truecase_text.strip()
