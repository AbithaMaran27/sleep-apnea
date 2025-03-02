import os
import mne
import numpy as np

# Directories
input_dir = "data_modified"  # Fixed EDF files
output_dir = "data_preprocessed_segmented_vincent"  # Directory to save preprocessed files
os.makedirs(output_dir, exist_ok=True)

def preprocess_and_segment(edf_file, output_file):
    """
    Preprocess and segment an EDF file into 10-second chunks.
    Saves the segmented data and default labels (Normal: 0).
    """
    try:
        raw = mne.io.read_raw_edf(edf_file, preload=True)
        raw.filter(0.5, 40, fir_design='firwin')

        # Sampling frequency and segment duration
        sfreq = int(raw.info['sfreq'])
        segment_samples = sfreq * 10  # 10-second chunks
        n_segments = len(raw.times) // segment_samples

        segments = np.empty((n_segments, len(raw.ch_names), segment_samples))
        labels = np.zeros(n_segments, dtype=int)  # Default labels (all 0)

        for i in range(n_segments):
            start = i * segment_samples
            stop = start + segment_samples
            segments[i], _ = raw[:, start:stop]

        # Save segments and default labels
        np.save(output_file, {"segments": segments, "labels": labels})
        print(f"Processed and saved: {output_file}")
    except Exception as e:
        print(f"Error processing {edf_file}: {e}")

# Preprocess and segment each EDF file
for file in os.listdir(input_dir):
    if file.endswith(".edf"):
        input_file = os.path.join(input_dir, file)
        output_file = os.path.join(output_dir, file.replace(".edf", "_segmented.npy"))
        preprocess_and_segment(input_file, output_file)
