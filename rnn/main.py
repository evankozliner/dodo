import numpy as np
import theano as theano
import theano.tensor as T
import time
import operator
from utils import load_data, load_model_parameters_theano, generate_sentences, train_with_sgd
from gru_theano import *
import sys

# Load data (this may take a few minutes)
VOCABULARY_SIZE = 2000
X_train, y_train, word_to_index, index_to_word = load_data("data/1900_tweets.csv", VOCABULARY_SIZE)

# Build your own model (not recommended unless you have a lot of time!)

LEARNING_RATE = 1e-3
NEPOCH = 20
HIDDEN_DIM = 128

model = GRUTheano(VOCABULARY_SIZE, HIDDEN_DIM)

t1 = time.time()
model.sgd_step(X_train[0], y_train[0], LEARNING_RATE)
t2 = time.time()
print "SGD Step time: ~%f milliseconds" % ((t2 - t1) * 1000.)

train_with_sgd(model, X_train, y_train, LEARNING_RATE, NEPOCH, decay=0.9)

generate_sentences(model, 100, index_to_word, word_to_index)
