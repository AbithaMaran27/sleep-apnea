import numpy as np
from collections import Counter
from sklearn.utils import resample
import os

# Input paths
aligned_folder = "data_aligned_labels"  # Replace with the folder where aligned `.npy` files are stored
output_folder = "data_resampled"  # Replace with the folder to save resampled data

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

def resample_dataset(segments, labels):
    """
    Resample dataset to balance class distribution.
    """
    # Find the unique labels and their counts
    label_counts = Counter(labels)
    print(f"Original Label Distribution: {label_counts}")

    # Get the maximum number of samples in any class
    max_samples = max(label_counts.values())

    # Separate data by class
    resampled_segments = []
    resampled_labels = []
    for label in label_counts.keys():
        class_indices = np.where(labels == label)[0]
        class_segments = segments[class_indices]

        # Oversample the minority classes to match the majority class
        resampled_class_segments = resample(
            class_segments,
            replace=True,  # Allow duplication
            n_samples=max_samples,
            random_state=42
        )
        resampled_class_labels = np.full(max_samples, label)

        resampled_segments.append(resampled_class_segments)
        resampled_labels.append(resampled_class_labels)

    # Combine all classes
    resampled_segments = np.vstack(resampled_segments)
    resampled_labels = np.concatenate(resampled_labels)
    print(f"Resampled Label Distribution: {Counter(resampled_labels)}")

    return resampled_segments, resampled_labels

# Process all aligned files
for file in os.listdir(aligned_folder):
    if file.endswith("_aligned.npy"):
        file_path = os.path.join(aligned_folder, file)

        # Load data
        data = np.load(file_path, allow_pickle=True).item()
        segments = data["segments"]
        labels = data["labels"]

        # Resample dataset
        resampled_segments, resampled_labels = resample_dataset(segments, labels)

        # Save the resampled dataset
        output_path = os.path.join(output_folder, file)
        np.save(output_path, {"segments": resampled_segments, "labels": resampled_labels})
        print(f"Resampled data saved to {output_path}")
