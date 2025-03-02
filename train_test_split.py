import os
import numpy as np
from sklearn.model_selection import train_test_split

# Load the balanced aligned data
def load_balanced_aligned_data(data_folder):
    files = [f for f in os.listdir(data_folder) if f.endswith("_aligned.npy")]
    data_list = []
    label_list = []

    for file in files:
        file_path = os.path.join(data_folder, file)
        print(f"Processing {file}...")
        aligned_data = np.load(file_path, allow_pickle=True).item()
        data_list.append(aligned_data['segments'])
        label_list.append(aligned_data['labels'])

    # Combine all data
    data = np.concatenate(data_list, axis=0)
    labels = np.concatenate(label_list, axis=0)
    return data, labels

# Split and save the data
def split_and_save(data_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    # Load the data
    data, labels = load_balanced_aligned_data(data_folder)
    print("Combined data shape:", data.shape)
    print("Combined labels shape:", labels.shape)

    # Split into train, validation, and test
    train_data, temp_data, train_labels, temp_labels = train_test_split(
        data, labels, test_size=0.3, random_state=42, stratify=labels
    )
    val_data, test_data, val_labels, test_labels = train_test_split(
        temp_data, temp_labels, test_size=0.5, random_state=42, stratify=temp_labels
    )

    print("Training data shape:", train_data.shape, "Training labels shape:", train_labels.shape)
    print("Validation data shape:", val_data.shape, "Validation labels shape:", val_labels.shape)
    print("Test data shape:", test_data.shape, "Test labels shape:", test_labels.shape)

    # Save the splits
    np.save(os.path.join(output_folder, "train_data.npy"), train_data)
    np.save(os.path.join(output_folder, "train_labels.npy"), train_labels)
    np.save(os.path.join(output_folder, "val_data.npy"), val_data)
    np.save(os.path.join(output_folder, "val_labels.npy"), val_labels)
    np.save(os.path.join(output_folder, "test_data.npy"), test_data)
    np.save(os.path.join(output_folder, "test_labels.npy"), test_labels)

    print("Data splitting and saving completed!")

# Main function
def main():
    data_balanced_folder = "C:/Users/abith/PycharmProjects/SleepApnea_Vincents_data-only/data_balanced_labels"
    output_folder = "C:/Users/abith/PycharmProjects/SleepApnea_Vincents_data-only/data_balanced_split"
    split_and_save(data_balanced_folder, output_folder)

if __name__ == "__main__":
    main()
