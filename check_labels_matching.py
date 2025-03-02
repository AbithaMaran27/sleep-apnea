import os

segmented_dir = "data_preprocessed_segmented_vincent"
parsed_labels_dir = "output/parsed_labels"

for file in os.listdir(segmented_dir):
    if file.endswith("_segmented.npy"):
        base_name = file.replace("_segmented.npy", "")
        respevt_file = os.path.join(parsed_labels_dir, f"{base_name}_respevt.npy")
        stage_file = os.path.join(parsed_labels_dir, f"{base_name}_stage.npy")

        print(f"Checking for {file}:")
        if not os.path.exists(respevt_file):
            print(f"  Missing: {base_name}_respevt.npy")
        if not os.path.exists(stage_file):
            print(f"  Missing: {base_name}_stage.npy")
        if os.path.exists(respevt_file) and os.path.exists(stage_file):
            print("  Both label files found.")
