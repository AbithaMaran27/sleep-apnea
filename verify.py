import numpy as np

def inspect_file(file_path):
    try:
        data = np.load(file_path, allow_pickle=True)
        print(f"File: {file_path}")
        print(f"Type: {type(data)}, Shape: {data.shape}")
        print("First few entries:", data[:5])
    except Exception as e:
        print(f"Error loading {file_path}: {e}")

files_to_check = [
    "C:/Users/abith/PycharmProjects/SleepApnea_Vincents_data-only/data_preprocessed_segmented_vincent/ucddb002_lifecard_segmented_segments.npy",
    "C:/Users/abith/PycharmProjects/SleepApnea_Vincents_data-only/data_preprocessed_segmented_vincent/ucddb002_lifecard_segmented_labels.npy",
    "C:/Users/abith/PycharmProjects/SleepApnea_Vincents_data-only/data_aligned_labels/ucddb003_lifecard_aligned_segments.npy",
    "C:/Users/abith/PycharmProjects/SleepApnea_Vincents_data-only/data_aligned_labels/ucddb003_lifecard_aligned_labels.npy",
]

for file_path in files_to_check:
    inspect_file(file_path)
