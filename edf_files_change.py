import os
import mne

def fix_edf(input_path, output_path):
    """
    Fixes EDF files using MNE and saves the corrected file.
    """
    try:
        # Read the EDF file
        raw = mne.io.read_raw_edf(input_path, preload=True)
        raw.info['bads'] = []  # Clear any bad channels

        # Save the file as an EDF using export()
        raw.export(output_path, fmt='edf', overwrite=True)
        print(f"Fixed and saved: {output_path}")
    except Exception as e:
        print(f"Error fixing {input_path}: {e}")

def process_folder(input_folder, output_folder):
    """
    Processes all EDF files in the input folder, fixes them,
    and saves the corrected versions to the output folder.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file in os.listdir(input_folder):
        if file.endswith('.edf'):
            input_path = os.path.join(input_folder, file)
            output_path = os.path.join(output_folder, file)
            print(f"Processing {file}...")
            fix_edf(input_path, output_path)

# Paths to input and output folders
input_folder = 'data1'  # Update with your folder containing original EDF files
output_folder = 'data_modified'  # Folder to save fixed EDF files
process_folder(input_folder, output_folder)



