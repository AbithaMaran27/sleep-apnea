import numpy as np
import os
from keras.models import Sequential
from keras.layers import Conv1D, MaxPooling1D, LSTM, Dense, Flatten, Dropout, BatchNormalization, Input, Attention
from keras.utils import to_categorical
from keras.callbacks import EarlyStopping, ReduceLROnPlateau
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import pickle
from sklearn.utils.class_weight import compute_class_weight

# Load the data
def load_split_data(data_folder):
    train_data = np.load(os.path.join(data_folder, "train_data.npy"), allow_pickle=True)
    train_labels = np.load(os.path.join(data_folder, "train_labels.npy"), allow_pickle=True)
    val_data = np.load(os.path.join(data_folder, "val_data.npy"), allow_pickle=True)
    val_labels = np.load(os.path.join(data_folder, "val_labels.npy"), allow_pickle=True)
    test_data = np.load(os.path.join(data_folder, "test_data.npy"), allow_pickle=True)
    test_labels = np.load(os.path.join(data_folder, "test_labels.npy"), allow_pickle=True)
    return train_data, train_labels, val_data, val_labels, test_data, test_labels

# Build the CNN-LSTM with Attention model
def build_cnn_lstm_attention_model(input_shape, num_classes):
    model = Sequential([
        Input(shape=input_shape),
        Conv1D(64, kernel_size=3, activation='relu'),
        BatchNormalization(),
        MaxPooling1D(pool_size=2),
        Conv1D(128, kernel_size=3, activation='relu'),
        BatchNormalization(),
        MaxPooling1D(pool_size=2),
        LSTM(64, return_sequences=True),
        Attention(),
        Dropout(0.3),
        Flatten(),
        Dense(64, activation='relu'),
        Dropout(0.3),
        Dense(num_classes, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

# Train and evaluate the model
def train_hybrid_model(data_folder):
    # Load data
    train_data, train_labels, val_data, val_labels, test_data, test_labels = load_split_data(data_folder)

    # Transpose data for CNN-LSTM compatibility
    train_data = np.transpose(train_data, (0, 2, 1))
    val_data = np.transpose(val_data, (0, 2, 1))
    test_data = np.transpose(test_data, (0, 2, 1))

    # Get class weights
    unique_classes = np.unique(train_labels)
    class_weights = compute_class_weight('balanced', classes=unique_classes, y=train_labels)
    class_weights_dict = {i: weight for i, weight in zip(unique_classes, class_weights)}

    # Convert labels to one-hot encoding
    num_classes = len(unique_classes)
    train_labels_onehot = to_categorical(train_labels, num_classes)
    val_labels_onehot = to_categorical(val_labels, num_classes)

    # Build CNN-LSTM with Attention model
    input_shape = (train_data.shape[1], train_data.shape[2])
    cnn_lstm_model = build_cnn_lstm_attention_model(input_shape, num_classes)

    # Callbacks for early stopping and learning rate reduction
    early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
    lr_scheduler = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3)

    # Train the model
    cnn_lstm_model.fit(
        train_data, train_labels_onehot,
        validation_data=(val_data, val_labels_onehot),
        epochs=30,
        batch_size=64,
        class_weight=class_weights_dict,
        callbacks=[early_stopping, lr_scheduler]
    )

    # Extract features for Random Forest
    feature_extractor = Sequential(cnn_lstm_model.layers[:-2])
    feature_extractor.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    X_train_features = feature_extractor.predict(train_data)
    X_val_features = feature_extractor.predict(val_data)
    X_test_features = feature_extractor.predict(test_data)

    # Train Random Forest
    rf_model = RandomForestClassifier(n_estimators=200, random_state=42, class_weight='balanced')
    rf_model.fit(X_train_features, train_labels)

    # Evaluate Random Forest
    test_predictions = rf_model.predict(X_test_features)
    print("Classification Report:")
    print(classification_report(test_labels, test_predictions))
    print("Confusion Matrix:")
    print(confusion_matrix(test_labels, test_predictions))

    # Save models
    rf_model_path = os.path.join(data_folder, "random_forest_model.pkl")
    cnn_lstm_model_path = os.path.join(data_folder, "cnn_lstm_attention_model.h5")
    with open(rf_model_path, "wb") as f:
        pickle.dump(rf_model, f)
    cnn_lstm_model.save(cnn_lstm_model_path)
    print(f"Random Forest model saved to {rf_model_path}")
    print(f"CNN-LSTM Attention model saved to {cnn_lstm_model_path}")

# Main function
def main():
    data_split_folder = 'C:/Users/abith/PycharmProjects/SleepApnea_Vincents_data-only/data_split'
    train_hybrid_model(data_split_folder)

if __name__ == "__main__":
    main()
