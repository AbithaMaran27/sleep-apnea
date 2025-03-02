import numpy as np
import os


def parse_stage_file(stage_file):
    """
    Parses the stage file to extract event data.
    This file contains information about stages (Normal, REM, etc.).
    """
    labels = []
    with open(stage_file, 'r') as f:
        for line in f:
            # Assuming a certain structure for the stage file, e.g., [start_time, end_time, stage_label]
            parts = line.strip().split()
            if len(parts) < 3:
                continue  # Skip invalid lines

            start_time, end_time, label = float(parts[0]), float(parts[1]), parts[2]
            labels.append((start_time, end_time, label))  # (start, end, label)

    return labels


def parse_respevt_file(respevt_file):
    """
    Parses the respiratory event file to extract event data like apneas, hypopneas, etc.
    """
    events = []
    with open(respevt_file, 'r') as f:
        for line in f:
            # Assuming a certain structure for the resp event file
            parts = line.strip().split()
            if len(parts) < 3:
                continue  # Skip invalid lines

            start_time, event_type = float(parts[0]), parts[1]
            events.append((start_time, event_type))  # (time, event_type)

    return events


def map_labels_to_segments(segments, stage_labels, resp_events, sfreq):
    """
    Maps labels from stage and respiratory events to the corresponding segments of the EDF data.
    """
    segment_labels = np.zeros(len(segments), dtype=int)  # Initialize all as Normal (0)

    # Iterate over each segment and assign the appropriate label
    for i, segment in enumerate(segments):
        segment_start = i * (len(segment) / sfreq)
        segment_end = (i + 1) * (len(segment) / sfreq)

        # Check if the segment falls within any stage event (e.g., apnea, hypopnea, etc.)
        for start_time, end_time, stage_label in stage_labels:
            if segment_start >= start_time and segment_end <= end_time:
                if stage_label.lower() == 'obstructive_apnea':
                    segment_labels[i] = 1  # Assign label for Obstructive Apnea
                elif stage_label.lower() == 'central_apnea':
                    segment_labels[i] = 2  # Assign label for Central Apnea
                elif stage_label.lower() == 'mixed_apnea':
                    segment_labels[i] = 3  # Assign label for Mixed Apnea
                else:
                    segment_labels[i] = 0  # Assign label for Normal

        # Additional logic to map respiratory events to the segments (if needed)
        for start_time, event_type in resp_events:
            if segment_start >= start_time and segment_end <= start_time + 10:  # Adjust window as needed
                if 'apnea' in event_type.lower():
                    segment_labels[i] = 1  # Assign for Obstructive Apnea, modify if needed

    return segment_labels


def process_data_for_labels(segmented_data_folder, stage_folder, resp_evt_folder):
    """
    Iterates through the segmented data and assigns labels based on stage and resp events.
    """
    # Iterate through segmented files
    for file in os.listdir(segmented_data_folder):
        if file.endswith(".npy"):
            segmented_file_path = os.path.join(segmented_data_folder, file)
            stage_file_path = os.path.join(stage_folder,
                                           file.replace('.npy', '_stage.txt'))  # Assuming naming convention
            resp_evt_file_path = os.path.join(resp_evt_folder,
                                              file.replace('.npy', '_respevt.txt'))  # Assuming naming convention

            print(f"Processing {file}...")

            try:
                # Load segmented data
                segmented_data = np.load(segmented_file_path, allow_pickle=True)
                segments = segmented_data['segments']
                sfreq = 250  # Replace with the actual sample frequency of your dataset if different

                # Parse the stage and respiratory event files
                stage_labels = parse_stage_file(stage_file_path)
                resp_events = parse_respevt_file(resp_evt_file_path)

                # Map labels to segments
                segment_labels = map_labels_to_segments(segments, stage_labels, resp_events, sfreq)

                # Save the new file with labels
                labels_file_path = os.path.join(segmented_data_folder, file.replace('.npy', '_labeled.npy'))
                np.save(labels_file_path, {'segments': segments, 'labels': segment_labels})
                print(f"Labeled data saved: {labels_file_path}")

            except Exception as e:
                print(f"Error processing {file}: {e}")


# Paths to your folders
segmented_data_folder = "C:/Users/abith\PycharmProjects\SleepApnea_Vincents_data-only\data_preprocessed_segmented_vincent"
stage_folder = "C:/Users/abith\PycharmProjects\SleepApnea_Vincents_data-only\data1\organized_txt_files/stage"
resp_evt_folder = "C:/Users/abith\PycharmProjects\SleepApnea_Vincents_data-only\data1\organized_txt_files/respevt"

process_data_for_labels(segmented_data_folder, stage_folder, resp_evt_folder)
