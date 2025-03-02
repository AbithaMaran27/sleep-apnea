import numpy as np
import matplotlib.pyplot as plt
from collections import Counter


def load_labels(file_path):
    try:
        labels = np.load(file_path, allow_pickle=True)
        print(f"Loaded labels file: {file_path}")
        print(f"Original Data Type: {type(labels)}, Shape: {labels.shape}")

        # Handle improperly formatted labels
        if labels.shape == ():  # Scalar case
            labels = labels.item()  # Extract the contained object
            if isinstance(labels, dict) and 'labels' in labels:
                labels = labels['labels']  # Extract 'labels' if stored in a dictionary
            else:
                raise ValueError("Unexpected data format in the loaded file.")

        # Ensure it's a 1D array
        if len(labels.shape) != 1:
            raise ValueError("Loaded labels are not a 1D array. Please check the file.")

        print(f"Processed Labels Shape: {labels.shape}")
        return labels
    except Exception as e:
        print(f"Error loading labels file: {e}")
        return None


def plot_label_distribution(labels):
    label_counts = Counter(labels)
    labels, counts = zip(*label_counts.items())
    plt.bar(labels, counts, color='skyblue')
    plt.title("Balanced Label Distribution")
    plt.xlabel("Labels")
    plt.ylabel("Counts")
    plt.xticks(labels)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()


def simulate_segments(labels, num_samples=5, segment_length=1280):
    unique_labels = list(set(labels))
    simulated_data = {}

    for label in unique_labels:
        simulated_data[label] = [np.sin(np.linspace(0, 10, segment_length) + label) for _ in range(num_samples)]

    return simulated_data


def plot_simulated_segments(simulated_data):
    plt.figure(figsize=(15, 10))
    for idx, (label, segments) in enumerate(simulated_data.items()):
        for segment_idx, segment in enumerate(segments):
            plt.subplot(len(simulated_data), 1, idx + 1)
            plt.plot(segment, label=f"Sample {segment_idx + 1}")
            plt.title(f"Simulated Signal for Label {label}")
            plt.xlabel("Time")
            plt.ylabel("Amplitude")
        plt.legend()
    plt.tight_layout()
    plt.show()


def main():
    # Path to your balanced labels file
    balanced_labels_path = "C:/Users/abith/PycharmProjects/SleepApnea_Vincents_data-only/data_balanced_labels/ucddb003_lifecard_aligned.npy"

    # Load balanced labels
    balanced_labels = load_labels(balanced_labels_path)

    # Visualize label distribution
    if balanced_labels is not None:
        print("\n### Visualizing Balanced Labels ###")
        print(f"Label Distribution: {Counter(balanced_labels)}")
        plot_label_distribution(balanced_labels)

        # Simulate and visualize segments
        print("\n### Simulating and Plotting Sample Segments ###")
        simulated_data = simulate_segments(balanced_labels)
        plot_simulated_segments(simulated_data)


if __name__ == "__main__":
    main()
