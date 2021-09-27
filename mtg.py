import numpy as np
import nltk
import pandas as pd
from statistics import mode
import random


def prob_array(corpus, predictors):
    prob = {}
    n = len(predictors)
    for i in range(len(corpus)):
        if corpus[i : i + n] == predictors:
            prob[corpus[i + n]] = prob.get(corpus[i + n], 0) + 1
            pass
        pass
    array = pd.DataFrame(list(prob.items()))
    return array


def determine(array, corpus):
    max = array.iloc[:, 0][array.iloc[:, 1] == array.iloc[:, 1].max()].tolist()
    if len(max) == 1:
        return max[0]
    else:
        where = []
        for i in max:
            where.append(corpus.index(i))
            pass
        word = max[where.index(min(where))]
        return word
    pass


def not_determine(array):
    array["prob"] = array.iloc[:, 1] / sum(array.iloc[:, 1])
    seq = array.iloc[:, 0].tolist()
    weight = array.iloc[:, 2].tolist()
    return random.choices(seq, weight)[0]


def unigram(corpus, deterministic):
    if deterministic:
        word = mode(corpus)
        return word
    else:
        word = random.choice(corpus)
        return word


def finish_sentence(sentence, n, corpus, deterministic=False):
    next = "a"
    while len(sentence) < 15 and next not in [".", "?", "!"]:
        if n > 1:
            init = sentence[-n + 1 :]
            array = prob_array(corpus, init)
            pass
        else:
            init = []
            array = pd.DataFrame()
            pass
        while array.empty and init:
            init = init[1:]
            array = prob_array(corpus, init)
            pass
        if array.empty or n == 1:
            next = unigram(corpus, deterministic)
            sentence.append(next)
        elif deterministic:
            next = determine(array, corpus)
            sentence.append(next)
            pass
        else:
            next = not_determine(array)
            sentence.append(next)
    return sentence
