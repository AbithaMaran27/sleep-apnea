import os
import shutil

# Define directories
base_dir = "C:/Users/abith/PycharmProjects/SleepApnea_Vincents_data-only/data1"  # e.g., "C:/Users/abith/PycharmProjects/SleepApnea_Vincents_data-only/data1"
output_dir = os.path.join(base_dir, "organized_txt_files")
os.makedirs(output_dir, exist_ok=True)

# Subfolders for different types of `.txt` files
respevt_dir = os.path.join(output_dir, "respevt")
stage_dir = os.path.join(output_dir, "stage")
os.makedirs(respevt_dir, exist_ok=True)
os.makedirs(stage_dir, exist_ok=True)

# Organize `.txt` files
for filename in os.listdir(base_dir):
    if filename.endswith('_respevt.txt'):
        shutil.move(os.path.join(base_dir, filename), os.path.join(respevt_dir, filename))
    elif filename.endswith('_stage.txt'):
        shutil.move(os.path.join(base_dir, filename), os.path.join(stage_dir, filename))

print("Organized all .txt files into respective folders.")
