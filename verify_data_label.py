import numpy as np

def verify_labels(segments_path, labels_path, num_samples=5):
    """
    Verifies that the segments and labels are correctly aligned.
    Prints a few samples to verify.

    Parameters:
        - segments_path: Path to the segmented data.
        - labels_path: Path to the labels data.
        - num_samples: Number of samples to print for verification.
    """
    # Load the segmented data and labels
    segments_data = np.load(segments_path, allow_pickle=True).item()
    labels_data = np.load(labels_path, allow_pickle=True)

    segments = segments_data['segments']
    labels = labels_data['labels']

    # Print first few segments and their corresponding labels
    print("First few samples of the segmented data with labels:")
    for i in range(min(num_samples, len(segments))):
        print(f"Segment {i+1} Label: {labels[i]}")

# Example Usage
segments_path = 'C:/Users/abith/PycharmProjects/SleepApnea_Vincents_data-only/data_preprocessed_segmented_vincent/ucddb003_lifecard_segmented.npy'
labels_path = 'C:/Users/abith\PycharmProjects\SleepApnea_Vincents_data-only\output\parsed_labels'
verify_labels(segments_path, labels_path)
