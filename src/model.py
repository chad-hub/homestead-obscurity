# %%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import timeit
import matplotlib

import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
from keras import activations
from skimage.color import rgb2gray

%load_ext tensorboard
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from sklearn.metrics import classification_report, confusion_matrix
from tensorflow.keras.callbacks import ModelCheckpoint,LearningRateScheduler
from tensorflow.keras import backend as K
from keras.models import Model
keras = tf.keras
AUTOTUNE = tf.data.experimental.AUTOTUNE ## tf.data transformation parameters

matplotlib.style.use('ggplot')

import image_pipeline
import tf_explain
# %%
def image_process(data_dir, batch_size, img_height, img_width, num_classes):
  train_ds = tf.keras.preprocessing.image_dataset_from_directory(
                          data_dir,
                          color_mode = 'rgb',
                          validation_split=0.2,
                          subset="training",
                          seed=42,
                          image_size=(img_height, img_width),
                          batch_size=batch_size)
  val_ds = tf.keras.preprocessing.image_dataset_from_directory(
                          data_dir,
                          color_mode = 'rgb',
                          validation_split=0.2,
                          subset="validation",
                          seed=42,
                          image_size=(img_height, img_width),
                          batch_size=batch_size)

  class_names = train_ds.class_names

  plt.figure(figsize=(10, 10))
  for images, labels in train_ds.take(1):
    for i in range(num_classes):
      ax = plt.subplot(3, 3, i + 1)
      plt.imshow(images[i].numpy().astype("uint8"))
      plt.title(class_names[labels[i]])
      plt.axis("off")
    plt.tight_layout()
    plt.show()


  return train_ds, val_ds, class_names

# %%
def create_model(num_classes, data_augmentation, img_height, img_width, train_ds):

  # plt.figure(figsize=(10, 10))

  # for images, _ in train_ds.take(2):
  #   for i in range(6):
  #     augmented_images = data_augmentation(images)
  #     ax = plt.subplot(3, 2, i + 1)
  #     plt.imshow(augmented_images[0].numpy().astype("uint8"))
  #     plt.axis("off")
  #   plt.tight_layout()
  #   plt.show()

  model = Sequential([
	    # data_augmentation,
	    layers.experimental.preprocessing.Rescaling(1./255, input_shape=(img_height, img_width, 3)),
	    layers.Conv2D(32, 3, strides=2, padding='valid', activation='relu', name='target_layer'),
	    layers.MaxPooling2D(pool_size=(2, 2), strides=2),
	    layers.Dropout(0.2),

	    # layers.Conv2D(32, 5, padding='same', activation='relu'),
	    # # layers.MaxPooling2D(strides=2),
	    # layers.Dropout(0.1),

	    layers.Conv2D(64, 3, padding='valid', activation='relu'),
	    layers.MaxPooling2D(pool_size=(2, 2), strides=2),
	    layers.Dropout(0.2),

	    layers.Flatten(),
	    layers.Dense(128, activation='relu'),
	    layers.Dense(num_classes, activation='softmax', name='visualized_layer')])

  model.compile(optimizer='adam',
	                loss='categorical_crossentropy',
	                metrics=['accuracy'])

  print(model.summary())



  return model

def train_model(model, n_epochs, train_gen, val_gen):
  model = model.fit(train_gen,
                      validation_data = val_gen,
                      validation_steps=val_gen.n // val_gen.batch_size,
                      epochs=n_epochs,
                      steps_per_epoch=train_gen.n//train_gen.batch_size)
                      # callbacks=[callbacks])
                      # use_multiprocessing=True,
                      # workers = -1)
  %tensorboard --logdir logs

  return model


# %%

def plot_training_results(history, n_epochs):
  acc = history.history['accuracy']
  val_acc = history.history['val_accuracy']

  loss=history.history['loss']
  val_loss=history.history['val_loss']

  epochs_range = range(n_epochs)

  plt.figure(figsize=(8, 8))
  plt.subplot(1, 2, 1)
  plt.plot(epochs_range, acc, label='Training Accuracy')
  plt.plot(epochs_range, val_acc, label='Validation Accuracy')
  plt.legend(loc='lower right')
  plt.title('Training and Validation Accuracy')

  plt.subplot(1, 2, 2)
  plt.plot(epochs_range, loss, label='Training Loss')
  plt.plot(epochs_range, val_loss, label='Validation Loss')
  plt.legend(loc='upper right')
  plt.title('Training and Validation Loss')
  plt.show()



# %%
if __name__ == '__main__':
  batch_size = 32
  img_height = 299
  img_width = 299
  num_classes = 7
  n_epochs = 2
  data_dir = '../data'
  output_dir = '../callbacks'

  train_generator, validation_generator = image_pipeline.main()

  data_augmentation = keras.Sequential([
    layers.experimental.preprocessing.RandomFlip("horizontal",
                                                 input_shape=(img_height,
                                                              img_width,
                                                              3)),
    layers.experimental.preprocessing.RandomZoom(0.2),
    layers.experimental.preprocessing.RandomWidth(0.2),
    layers.experimental.preprocessing.RandomHeight(0.2),
  ])

  model = create_model(num_classes, data_augmentation, img_height,
                          img_width, train_generator)

  history = train_model(model, n_epochs, train_generator, validation_generator)

  filename = '../models/cnn_sequential/train_model'
  tf.saved_model.save(model, filename)

  plot_training_results(history, n_epochs)

# %%
