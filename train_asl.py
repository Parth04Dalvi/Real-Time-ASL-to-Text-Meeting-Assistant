import tensorflow as tf
from tensorflow.keras import layers, models

# Input: 21 Hand Landmarks (x, y, z) = 63 features
model = models.Sequential([
    layers.Input(shape=(63,)),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.2),
    layers.Dense(64, activation='relu'),
    layers.Dense(26, activation='softmax') # 26 Letters of Alphabet
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Export for Browser use
import tensorflowjs as tfjs
tfjs.converters.save_keras_model(model, 'asl_model_js')
