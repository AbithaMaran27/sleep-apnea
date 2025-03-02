import os

# Define directories
label_dir = "output/parsed_labels"  # Folder with parsed labels
segmented_data_dir = "data1/data_preprocessed_segmented_vincent"  # Folder with segmented .npy files

# List all segmented files (to extract valid base names)
segmented_files = [os.path.basename(f).replace("_lifecard_segmented.npy", "")
                   for f in os.listdir(segmented_data_dir) if f.endswith("_segmented.npy")]

# Rename label files to match segmented file base names
for label_file in os.listdir(label_dir):
    label_path = os.path.join(label_dir, label_file)

    # Extract base name from label file (e.g., ucddb018)
    base_name = label_file.split("_")[0]

    # Check if the base name is in segmented files
    if base_name in segmented_files:
        # Determine the label type (_stage_labels or _respevt_labels)
        label_type = "_".join(label_file.split("_")[1:])
        new_name = f"{base_name}_{label_type}"
        new_path = os.path.join(label_dir, new_name)

        # Rename the file
        os.rename(label_path, new_path)
        print(f"Renamed: {label_file} --> {new_name}")
    else:
        print(f"Skipping: {label_file} (No matching segmented file found)")
