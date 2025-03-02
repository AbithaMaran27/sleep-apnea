import os
import numpy as np

# Directories for input and output
txt_dir = "data1/organized_txt_files"
output_dir = "output/parsed_labels"
os.makedirs(output_dir, exist_ok=True)


def parse_respevt(txt_file, output_path):
    """
    Parse the respevt.txt file to extract apnea event annotations.
    """
    try:
        events = []
        with open(txt_file, "r") as file:
            for line in file:
                if "OBSTRUCTIVE" in line.upper():
                    events.append({"onset": ..., "duration": ..., "description": "Obstructive Apnea"})
                elif "CENTRAL" in line.upper():
                    events.append({"onset": ..., "duration": ..., "description": "Central Apnea"})
                elif "MIXED" in line.upper():
                    events.append({"onset": ..., "duration": ..., "description": "Mixed Apnea"})
        np.save(output_path, events)
        print(f"Saved respevt labels to: {output_path}")
    except Exception as e:
        print(f"Error parsing {txt_file}: {e}")


def parse_stage(txt_file, output_path):
    """
    Parse the stage.txt file to extract sleep stage labels.
    """
    try:
        stages = []
        with open(txt_file, "r") as file:
            stages = [int(line.strip()) for line in file if line.strip().isdigit()]
        np.save(output_path, stages)
        print(f"Saved stage labels to: {output_path}")
    except Exception as e:
        print(f"Error parsing {txt_file}: {e}")


# Process all txt files and adjust naming convention
for subfolder in ["respevt", "stage"]:
    subfolder_path = os.path.join(txt_dir, subfolder)
    for file in os.listdir(subfolder_path):
        txt_file = os.path.join(subfolder_path, file)

        # Adjust naming to match the segmented files
        base_name = file.replace("_respevt.txt", "_lifecard").replace("_stage.txt", "_lifecard")

        # Save respevt and stage files with updated names
        if subfolder == "respevt":
            output_path = os.path.join(output_dir, f"{base_name}_respevt.npy")
            parse_respevt(txt_file, output_path)
        elif subfolder == "stage":
            output_path = os.path.join(output_dir, f"{base_name}_stage.npy")
            parse_stage(txt_file, output_path)
