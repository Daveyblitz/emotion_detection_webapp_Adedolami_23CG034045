import os
import numpy as np
import cv2
from deepface import DeepFace
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten, Dropout
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ModelCheckpoint

def create_model(input_shape):
    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation='relu', input_shape=input_shape))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(7, activation='softmax'))  # Assuming 7 emotion classes
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

def preprocess_data(data_directory):
    datagen = ImageDataGenerator(rescale=1./255)
    train_generator = datagen.flow_from_directory(
        data_directory,
        target_size=(48, 48),
        batch_size=32,
        class_mode='categorical',
        color_mode='grayscale'
    )
    return train_generator

def train_model(data_directory, model_save_path):
    input_shape = (48, 48, 1)  # Adjust based on your input image size
    model = create_model(input_shape)
    train_generator = preprocess_data(data_directory)

    checkpoint = ModelCheckpoint(model_save_path, save_best_only=True, monitor='val_loss')
    
    model.fit(train_generator, epochs=50, callbacks=[checkpoint])

def load_model(model_path):
    from keras.models import load_model
    return load_model(model_path)

def detect_emotion(frame):
    result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
    return result[0]['dominant_emotion']

if __name__ == "__main__":
    data_directory = 'path_to_your_training_data'  # Update this path
    model_save_path = os.path.join('models', 'emotion_detection_model.h5')
    train_model(data_directory, model_save_path)