# -*- coding: utf-8 -*-
"""Covid19 prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1l89YxT3YUxxZE3PX7a59-Mw4XlgXb6E2
"""

!git clone https://github.com/ana-lan/CovidDetetcion

import numpy as np
import matplotlib.pyplot as plt
import keras
from keras.layers import *
from keras.models import * 
from keras_preprocessing import image
import os

DATASET_PATH = "CovidDetetcion/Dataset"
TRAINING_DATASET_PATH=DATASET_PATH + "/Train"
VALIDATION_DATASET_PATH=DATASET_PATH + "/Val"
UPLOAD_CONTENT_PATH="CovidPrediction/Content/"

# CNN Based Model in Keras

model = Sequential()
model.add(Conv2D(32,kernel_size=(3,3),activation='relu',input_shape=(224,224,3)))
model.add(Conv2D(64,(3,3),activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.25))

model.add(Conv2D(64,(3,3),activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.25))

model.add(Conv2D(128,(3,3),activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(64,activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(1,activation='sigmoid'))

model.compile(loss=keras.losses.binary_crossentropy,optimizer='adam',metrics=['accuracy'])

model.summary()

# Train from scratch
train_datagen = image.ImageDataGenerator(
    rescale = 1./255,
    shear_range = 0.2,
    zoom_range = 0.2,
    horizontal_flip = True,
)

test_dataset = image.ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(TRAINING_DATASET_PATH,
    target_size = (224,224),
    batch_size = 32,
    class_mode = 'binary')

CLASSES = train_generator.class_indices
print(CLASSES)

validation_generator = test_dataset.flow_from_directory(VALIDATION_DATASET_PATH,
    target_size = (224,224),
    batch_size = 32,
    class_mode = 'binary')

hist = model.fit(
    train_generator,
    steps_per_epoch=7,
    epochs = 15,
    validation_data = validation_generator,
    validation_steps=2
)

fig, ax = plt.subplots(1, 2, figsize=(10, 3))
ax = ax.ravel()

for i, met in enumerate(['accuracy', 'loss']):
    ax[i].plot(hist.history[met])
    ax[i].plot(hist.history['val_' + met])
    ax[i].set_title('Model {}'.format(met))
    ax[i].set_xlabel('epochs')
    ax[i].set_ylabel(met)
    ax[i].legend(['train', 'val'])

from google.colab import files
from matplotlib import pyplot as plt
import cv2

uploaded = files.upload()
f = plt.figure(figsize=(50,50)) # specifying the overall grid size
i=1

for fn in uploaded.keys():
  # predict images
  path = "/content/" + fn
  img = image.load_img(path, target_size=(224,224))
  x = image.img_to_array(img)
  x = np.expand_dims(x, axis =0)
  images = np.vstack([x])
  prediction = model.predict(images, batch_size = 10)
  predicted_class_indices= int(prediction[0][0])
  predicted_type = list(CLASSES.keys())[list(CLASSES.values()).index(predicted_class_indices)]
  f.add_subplot(5,5,i);
  i=i+1;
  print("Originally -" + fn + ", Predicted  - "+predicted_type)
  plt.title(predicted_type)
  plt.imshow(img)


plt.show(block=True)

print("training_accuracy", hist.history['accuracy'][-1])
print("validation_accuracy", hist.history['val_accuracy'][-1])

label = validation_generator.classes

pred= model.predict(validation_generator)
predicted_class_indices=np.argmax(pred,axis=1)
labels = (validation_generator.class_indices)
labels2 = dict((v,k) for k,v in labels.items())
predictions = [labels2[k] for k in predicted_class_indices]
print(predicted_class_indices)
print (labels)
print (predictions)

from sklearn.metrics import confusion_matrix

cf = confusion_matrix(predicted_class_indices,label)
cf

import pandas as pd
exp_series = pd.Series(label)
pred_series = pd.Series(predicted_class_indices)
pd.crosstab(exp_series, pred_series, rownames=['Actual'], colnames=['Predicted'],margins=True)

plt.matshow(cf)
plt.title('Confusion Matrix Plot')
plt.colorbar()
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.show();