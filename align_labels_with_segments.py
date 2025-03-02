import os
import numpy as np

# Directories
segmented_dir = "data_preprocessed_segmented_vincent"
parsed_labels_dir = "output/parsed_labels"
aligned_output_dir = "data_aligned_labels"
os.makedirs(aligned_output_dir, exist_ok=True)

def align_labels(segmented_file, respevt_labels, stage_labels):
    """
    Align parsed labels (respevt and stage) with segmented data.
    """
    data = np.load(segmented_file, allow_pickle=True).item()
    segments = data["segments"]
    sfreq = 128  # Adjust based on your dataset's sampling frequency
    segment_duration = 10
    segment_samples = sfreq * segment_duration

    aligned_labels = []
    for i in range(segments.shape[0]):
        segment_start = i * segment_samples / sfreq
        segment_end = (i + 1) * segment_samples / sfreq

        # Align apnea event labels
        apnea_label = 0
        for event in respevt_labels:
            if event["onset"] <= segment_start <= (event["onset"] + event["duration"]):
                if "OBSTRUCTIVE" in event["description"].upper():
                    apnea_label = 1
                elif "CENTRAL" in event["description"].upper():
                    apnea_label = 2
                elif "MIXED" in event["description"].upper():
                    apnea_label = 3
                break

        # Align sleep stage labels
        stage_index = int(segment_start / segment_duration)
        stage_label = stage_labels[stage_index] if stage_index < len(stage_labels) else 0

        # Combine labels (priority to apnea events)
        aligned_labels.append(apnea_label if apnea_label != 0 else stage_label)

    return segments, np.array(aligned_labels)

# Align each segmented file


for file in os.listdir(segmented_dir):
    if file.endswith("_segmented.npy"):
        base_name = file.replace("_segmented.npy", "")
        respevt_file = os.path.join(parsed_labels_dir, f"{base_name}_respevt.npy")
        stage_file = os.path.join(parsed_labels_dir, f"{base_name}_stage.npy")

        print(f"Processing {file}...")
        if not os.path.exists(respevt_file) or not os.path.exists(stage_file):
            print(f"  Missing label files for {base_name}, skipping...")
            continue

        try:
            # Load data
            segmented_data = np.load(os.path.join(segmented_dir, file), allow_pickle=True).item()
            respevt_labels = np.load(respevt_file, allow_pickle=True)
            stage_labels = np.load(stage_file, allow_pickle=True)

            # Align labels
            segments = segmented_data["segments"]
            aligned_labels = []
            for i, segment in enumerate(segments):
                respevt_label = respevt_labels[i] if i < len(respevt_labels) else 0
                stage_label = stage_labels[i] if i < len(stage_labels) else 0
                combined_label = max(respevt_label, stage_label)  # Adjust logic as needed
                aligned_labels.append(combined_label)

            # Save aligned data
            aligned_data = {
                "segments": segments,
                "labels": np.array(aligned_labels)
            }
            aligned_file = os.path.join(aligned_output_dir, f"{base_name}_aligned.npy")
            np.save(aligned_file, aligned_data)
            print(f"  Aligned data saved to {aligned_file}")
        except Exception as e:
            print(f"  Error processing {file}: {e}")
