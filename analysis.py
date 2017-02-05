

import csv
import numpy as np
from sklearn import tree
from sklearn.preprocessing import OneHotEncoder
from collections import Counter

import random

import tensorflow as tf
import keras
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Flatten, Dropout




with open('train_2008.csv', 'r') as dest_f:

    data_iter = csv.reader(dest_f, delimiter = ",", quotechar = '"')
    data = [data for data in data_iter]

    # print data[0]
    # print data[1]
    # print data[2]

    lables = data[0]
    data = data[1:]

    random.shuffle(data)

    X_train = np.array([map(int, datum[:-1]) for datum in data])
    y_train = np.array([int(datum[-1]) for datum in data])

    categorical_indices = []

    for i in range(len(X_train[0])):

        cnt = {}
        for X in X_train:
            if X[i] not in cnt:
                cnt[X[i]] = len(cnt)

        print lables[i], cnt

        if len(cnt) < 150:
            categorical_indices.append(i)
            for X in X_train:
                X[i] = cnt[X[i]]




    enc = OneHotEncoder(categorical_features=categorical_indices)
    enc.fit(X_train)



    print X_train[0]
    X_train = enc.transform(X_train).toarray()
    for foo in X_train[0]:
        print ">", foo






# Normalize data
row_means = X_train.mean(axis=1)
row_stds = X_train.std(axis=1)
X_train = X_train - row_means[:, np.newaxis]
X_train = X_train / row_stds[:, np.newaxis]


# Split into a training set and a test set for validation
X_test = X_train[:6400]
y_test = y_train[:6400] - 1

X_train = X_train[6400:]
y_train = y_train[6400:] - 1

print float(sum(y_test))/len(y_test)

## Transforms output to one-hot encoding
y_train = keras.utils.np_utils.to_categorical(y_train, 2)
y_test = keras.utils.np_utils.to_categorical(y_test, 2)

print X_train.shape






## Create your own model here given the constraints in the problem
model = Sequential()
model.add(Dense(1000, input_shape=(len(X_train[0]),)))
model.add(Activation('sigmoid'))
# model.add(Dense(20))
# model.add(Activation('relu'))
## We use one-hot encoding, we now put 10 on our output layer
model.add(Dense(2))
model.add(Activation('softmax'))

## Printing a summary of the layers and weights in your model
model.summary()


## Since we are one-hot encoding the labels, we use 'categorical_crossentropy' as your loss.
model.compile(loss='categorical_crossentropy',optimizer='rmsprop', metrics=['accuracy'])

fit = model.fit(X_train, y_train, batch_size=128, nb_epoch=10,
    verbose=1)

## Printing the accuracy of our model, according to the loss function specified in model.compile above
score = model.evaluate(X_test, y_test, verbose=1)
print('Test score:', score[0])
print('Test accuracy:', score[1])

print model.predict_on_batch(X_test)







#
# for i in range(1, len(X_lables) - 1):
#
#     cnt = Counter()
#
#     for X in X_train:
#         cnt[X[i]] += 1
#
#     if len(cnt) > 20:
#         print X_lables[i], len(cnt)