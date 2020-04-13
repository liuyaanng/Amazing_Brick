from DQN import *
import tensorflow as tf

image_size = (80,80)
channels = 4
num_actions = 3
model = Build_Q_network(image_size, 4, 3)
model.compile(optimizer='adam',
              loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
              metrics=['accuracy'])

model.summary()
