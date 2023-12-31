# -*- coding: utf-8 -*-
"""COMP9414_Assn2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yOg-Ra1L1J1-8Rh62lkQvCwGbBfGfTmF
"""

## 23T2 UNSW COMP9414 Assn2
## Author: Bowen Zhao (z5446616)


import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ReduceLROnPlateau
from scipy.stats import zscore
from tensorflow.keras.layers import Activation
from tensorflow.keras import initializers


# Load Data
compoundA = np.loadtxt('compoundA.txt').reshape(-1, 1)
substrate = np.loadtxt('substrate.txt').reshape(-1, 1)
biomass = np.loadtxt('biomass.txt')

# Transform data and input data into one array
inputs = np.concatenate([compoundA, substrate], axis=1)

# Compute Z-score normalization for inputs
inputs = zscore(inputs, axis=0)

n_samples = len(inputs)

# Set number of training samples to 1200
n_train = 1200

# Split data
x_train, y_train = inputs[:n_train], biomass[:n_train]
x_test, y_test = inputs[n_train:], biomass[n_train:]

No=1
Ni=2

# Compute max parameters allowed
n_samples = x_train.shape[0]
max_params = n_samples // 10

# Determine number of neurons for hidden layer
Nh = min(16, max_params - No - Ni) # No=1, Ni=2

# Build Neural Network model
model = Sequential()

model.add(Dense(4*Nh, input_dim=Ni))
model.add(Activation('relu'))  # ReLU activation function

model.add(Dense(4*Nh))
model.add(Activation('tanh'))  # Tanh activation function

model.add(Dense(2*Nh))
model.add(Activation('sigmoid'))  # Sigmoid activation function

model.add(Dense(Nh))
model.add(Activation('tanh'))  # Tanh activation function

model.add(Dense(No, activation='linear'))  # Linear activation function for our output since it's a regression task



model.compile(loss='mean_squared_error', optimizer=Adam(learning_rate=0.01))

# Define learning rate adjustment strategy
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=5, min_lr=0.001)

# Train the model, and record the data during the training process
history = model.fit(x_train, y_train, validation_split=0.2, epochs=100, batch_size=10, verbose=1, callbacks=[reduce_lr])

# Evaluate the model on the test dataset
print(f"------The Loss of Test DataSet------")
mse = model.evaluate(x_test, y_test)
print(f"Mean Squared Error on test set: {mse}")

import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Train & Validation Loss / Epoch')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()
plt.show()

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error

# Predict the result use the model
predictions = model.predict(x_test)


# Calculate error metrics
N = len(y_test)

# Index of Agreement (IA)
oi_minus_pi = y_test - predictions.flatten()
oi_prime = y_test - np.mean(y_test)
pi_prime = predictions.flatten() - np.mean(y_test)
IA = 1 - np.sum(oi_minus_pi ** 2) / np.sum((np.abs(oi_prime) + np.abs(pi_prime)) ** 2)

# Root Mean Square Error (RMS)
RMS = np.sqrt(np.sum((predictions.flatten() - y_test) ** 2) / np.sum(y_test ** 2))

# Relative Standard Deviation (RSD)
RSD = np.sqrt(np.sum((predictions.flatten() - y_test) ** 2) / N)

# Print error metrics
print(f"Index of Agreement: {IA}")
print(f"Root Mean Square Error: {RMS}")
print(f"Relative Standard Deviation: {RSD}")


predictions = model.predict(x_test)

pred_count = np.arange(len(y_test))

# Plot
plt.figure(figsize=(10, 6))
plt.plot(pred_count, predictions, color='red', label='Predictions')
plt.plot(pred_count, y_test, color='black', label='True Values')
plt.xlabel('Number of Predictions')
plt.ylabel('Biomass')
plt.grid(True)
plt.legend()
plt.show()