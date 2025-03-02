import numpy as np
from collections import Counter
import os
from sklearn.utils import resample

# Paths
aligned_data_folder = 'C:/Users/abith/PycharmProjects/SleepApnea_Vincents_data-only/data_aligned_labels'
balanced_data_folder = 'C:/Users/abith/PycharmProjects/SleepApnea_Vincents_data-only/data_balanced_labels'
os.makedirs(balanced_data_folder, exist_ok=True)


def balance_data(file_path):
    # Load aligned data
    data = np.load(file_path, allow_pickle=True).item()
    segments = data['segments']
    labels = data['labels']

    # Get class distribution
    label_counts = Counter(labels)
    print(f"Original Label Distribution: {label_counts}")

    # Find the max count for oversampling
    max_count = max(label_counts.values())

    # Balance data
    balanced_segments = []
    balanced_labels = []
    for label in label_counts:
        # Extract segments of this label
        label_indices = np.where(labels == label)[0]
        label_segments = segments[label_indices]

        # Oversample or replicate to balance
        balanced_label_segments = resample(
            label_segments,
            replace=True,  # Oversample with replacement
            n_samples=max_count,  # Match the max count
            random_state=42
        )
        balanced_segments.extend(balanced_label_segments)
        balanced_labels.extend([label] * max_count)

    # Shuffle balanced data
    balanced_segments = np.array(balanced_segments)
    balanced_labels = np.array(balanced_labels)
    indices = np.arange(len(balanced_segments))
    np.random.shuffle(indices)
    balanced_segments = balanced_segments[indices]
    balanced_labels = balanced_labels[indices]

    # Save balanced data
    balanced_file_path = os.path.join(balanced_data_folder, os.path.basename(file_path))
    np.save(balanced_file_path, {"segments": balanced_segments, "labels": balanced_labels})
    print(f"Balanced data saved to {balanced_file_path}")
    print(f"Balanced Label Distribution: {Counter(balanced_labels)}")


# Main function
def main():
    for file in os.listdir(aligned_data_folder):
        if file.endswith('_aligned.npy'):
            print(f"Processing {file}...")
            file_path = os.path.join(aligned_data_folder, file)
            balance_data(file_path)


if __name__ == "__main__":
    main()
