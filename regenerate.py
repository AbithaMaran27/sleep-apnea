import numpy as np
import os

def load_and_resave(file_path, output_path):
    """
    Load an .npy file, check its structure, and resave it if necessary.
    """
    try:
        data = np.load(file_path, allow_pickle=True)
        print(f"Loaded {file_path} - Type: {type(data)}, Shape: {getattr(data, 'shape', 'N/A')}")

        # If data is a scalar, inspect its content and reshape or convert
        if isinstance(data, np.ndarray) and data.shape == ():
            # Extract content
            data = data.item()
            print(f"Data converted from scalar. New type: {type(data)}")

            # Handle dictionaries or other non-array data
            if isinstance(data, dict):
                print(f"Data is a dictionary with keys: {list(data.keys())}")
                if 'segments' in data and 'labels' in data:
                    segments = np.array(data['segments'])
                    labels = np.array(data['labels'])
                    np.save(output_path.replace('.npy', '_segments.npy'), segments)
                    np.save(output_path.replace('.npy', '_labels.npy'), labels)
                    print(f"Saved segments and labels separately: {output_path}")
            else:
                print(f"Unexpected data format: {type(data)}")
        else:
            print(f"File is already in proper format. No changes made.")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

# Files to check and resave
files_to_fix = [
    "C:/Users/abith/PycharmProjects/SleepApnea_Vincents_data-only/data_preprocessed_segmented_vincent/ucddb002_lifecard_segmented.npy",
    "C:/Users/abith/PycharmProjects/SleepApnea_Vincents_data-only/data_aligned_labels/ucddb003_lifecard_aligned.npy"
]

for file_path in files_to_fix:
    if os.path.exists(file_path):
        load_and_resave(file_path, file_path)
    else:
        print(f"File not found: {file_path}")
