import os
import numpy as np

# Path to the folder where your balanced label files are stored
folder_path = "data_balanced_labels"

# Initialize a dictionary to count labels
label_counts = {}

# Iterate through .npy files in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith(".npy"):  # Process only .npy files
        file_path = os.path.join(folder_path, file_name)
        try:
            # Load the dictionary from the file
            data = np.load(file_path, allow_pickle=True).item()  # Load as a dictionary
            labels = data.get("labels", [])  # Extract labels from the dictionary

            # Count occurrences of each label
            unique, counts = np.unique(labels, return_counts=True)
            for label, count in zip(unique, counts):
                label_counts[label] = label_counts.get(label, 0) + count
        except Exception as e:
            print(f"Error loading {file_name}: {e}")

# Print the label counts
print("Label Counts:")
for label, count in label_counts.items():
    print(f"Label {label}: {count}")
