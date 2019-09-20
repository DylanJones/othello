#!/usr/bin/env python3
import keras
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout, Flatten
import numpy as np
from .helpers import *
import pickle
import tensorflow

print("Loading data...")
#boards, labels = pickle.load(open('boards.pkl', 'rb'))
boards, labels = pickle.load(open('type2.pkl', 'rb'))
#mx = max(labels)
#mn = min(labels)
#dl = abs(mn)+mx
#of = dl/2
# labels = np.array([x/64 for x in labels], dtype=np.float32)
# print(labels)
print("Loaded.")

with tensorflow.device('/gpu:1'):
    model = Sequential()
    # add layers
    model.add(Dense(units=64, activation='relu', input_dim=64))
    model.add(Dense(units=50, activation='sigmoid'))
    model.add(Dropout(0.05))
    model.add(Dense(units=32, activation='sigmoid'))
    model.add(Dense(units=1, activation='relu'))
    #model.add(Flatten())

    model.compile(optimizer='rmsprop',
            loss='mean_squared_error',
            metrics=['accuracy'])

    print("Training...")
    model.fit(boards, labels, epochs=4, batch_size=256)
    model.save('model.h5')
    #js = model.to_json()
    #with open('model.json', 'w') as f:
    #    f.write(js)

    model.evaluate(data, labels, batch_size=256)
