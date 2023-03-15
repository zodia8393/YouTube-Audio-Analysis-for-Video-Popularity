import numpy as np
from tensorflow.keras.applications import VGG16
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split

def load_pretrained_model(input_shape, num_classes):
    base_model = VGG16(weights='imagenet', include_top=False, input_shape=input_shape)
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(512, activation='relu')(x)
    x = Dropout(0.5)(x)
    predictions = Dense(num_classes, activation='softmax')(x)

    model = Model(inputs=base_model.input, outputs=predictions)
    return model

def prepare_dataset(data, num_classes, test_size=0.2):
    X = np.stack(data['audio_features'].to_numpy())
    y = to_categorical(data['class_label'].to_numpy(), num_classes=num_classes)

    # If necessary, reshape the features to match the model's input shape
    X = np.expand_dims(X, axis=-1)

    # Repeat the single channel 3 times to match the VGG16 input shape
    X = np.repeat(X, 3, axis=-1)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
    return X_train, X_test, y_train, y_test

def train_model(model, X_train, y_train, X_val, y_val, epochs=10, batch_size=32):
    # Freeze the layers of the base model
    for layer in model.layers[:-4]:
        layer.trainable = False

    optimizer = Adam(lr=0.0001)
    model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

    history = model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=epochs, batch_size=batch_size)
    return model, history

def evaluate_model(model, X_test, y_test):
    test_loss, test_accuracy = model.evaluate(X_test, y_test)
    print(f"Test loss: {test_loss:.4f}")
    print(f"Test accuracy: {test_accuracy:.4f}")

    return test_loss, test_accuracy
