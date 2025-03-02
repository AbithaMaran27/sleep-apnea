import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

def plot_label_distribution(labels, title="Label Distribution"):
    """
    Plots the distribution of labels in a dataset.
    """
    label_counts = Counter(labels)
    labels, counts = zip(*label_counts.items())
    plt.bar(labels, counts, color='skyblue')
    plt.title(title)
    plt.xlabel("Labels")
    plt.ylabel("Counts")
    plt.xticks(labels)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

def plot_data_splits(train_size, val_size, test_size):
    """
    Plots a pie chart of the data splits.
    """
    sizes = [train_size, val_size, test_size]
    labels = ["Training", "Validation", "Testing"]
    colors = ["skyblue", "lightgreen", "salmon"]
    plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140, colors=colors)
    plt.title("Data Splits")
    plt.axis("equal")
    plt.show()

def load_labels(file_path, file_type="labels"):
    """
    Load label data from a given file path.
    """
    try:
        labels = np.load(file_path)
        print(f"Loaded {file_type} shape: {labels.shape}")
        return labels
    except Exception as e:
        print(f"Error loading {file_type}: {e}")
        return None

def main():
    # File paths
    preprocessed_segments_path = "C:/Users/abith/PycharmProjects/SleepApnea_Vincents_data-only/data_preprocessed_segmented_vincent/ucddb002_lifecard_segmented_segments.npy"
    preprocessed_labels_path = "C:/Users/abith/PycharmProjects/SleepApnea_Vincents_data-only/data_preprocessed_segmented_vincent/ucddb002_lifecard_segmented_labels.npy"
    aligned_labels_path = "C:/Users/abith/PycharmProjects/SleepApnea_Vincents_data-only/data_aligned_labels/ucddb003_lifecard_aligned_labels.npy"
    balanced_labels_path = "C:/Users/abith/PycharmProjects/SleepApnea_Vincents_data-only/data_balanced_labels/ucddb003_lifecard_aligned.npy"
    split_paths = {
        "train_labels": "C:/Users/abith/PycharmProjects/SleepApnea_Vincents_data-only/data_split/train_labels.npy",
        "val_labels": "C:/Users/abith/PycharmProjects/SleepApnea_Vincents_data-only/data_split/val_labels.npy",
        "test_labels": "C:/Users/abith/PycharmProjects/SleepApnea_Vincents_data-only/data_split/test_labels.npy",
    }

    # Visualize Preprocessed Data
    print("### Preprocessed Data ###")
    preprocessed_labels = load_labels(preprocessed_labels_path, "Preprocessed Labels")
    if preprocessed_labels is not None:
        plot_label_distribution(preprocessed_labels, title="Preprocessed Label Distribution")

    # Visualize Aligned Data
    print("\n### Aligned Data ###")
    aligned_labels = load_labels(aligned_labels_path, "Aligned Labels")
    if aligned_labels is not None:
        plot_label_distribution(aligned_labels, title="Aligned Label Distribution")

    # Visualize Balanced Data
    print("\n### Balanced Data ###")
    balanced_labels = load_labels(balanced_labels_path, "Balanced Labels")
    if balanced_labels is not None:
        plot_label_distribution(balanced_labels, title="Balanced Label Distribution")

    # Visualize Data Splits
    print("\n### Data Splits ###")
    train_labels = load_labels(split_paths["train_labels"], "Training Labels")
    val_labels = load_labels(split_paths["val_labels"], "Validation Labels")
    test_labels = load_labels(split_paths["test_labels"], "Testing Labels")
    if train_labels is not None and val_labels is not None and test_labels is not None:
        plot_data_splits(len(train_labels), len(val_labels), len(test_labels))

if __name__ == "__main__":
    main()
