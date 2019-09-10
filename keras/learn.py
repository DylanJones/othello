import keras
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
import numpy as np
from helpers import *
import pickle

print("Loading data...")
boards, labels = pickle.load(open('boards.pkl', 'rb'))
print("Loaded.")

model = Sequential()
# add layers
model.add(Dense(units=64, activation='relu', input_dim=64))
model.add(Dense(units=256, activation='softmax'))
model.add(Dropout(0.05))
model.add(Dense(units=256, activation='relu'))
model.add(Dense(units=10, activation='softmax'))
model.add(Dense(units=1, activation='sigmoid'))

model.compile(optimizer='rmsprop',
        loss='mean_squared_error',
        metrics=['accuracy'])

print("Training...")
model.fit(boards, labels, epochs=20, batch_size=256)
js = model.to_json()
with open('model.json', 'w') as f:
    f.write(js)

model.evaluate(data, labels, batch_size=256)
