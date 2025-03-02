import mne

edf_file = "C:/Users/abith/PycharmProjects/SleepApnea_Vincents_data-only/data_modified/ucddb028_lifecard.edf"
raw = mne.io.read_raw_edf(edf_file, preload=True)
annotations = raw.annotations

# Print all annotations
print("Annotations in EDF file:")
for ann in annotations:
    print(f"Onset: {ann['onset']}, Duration: {ann['duration']}, Description: {ann['description']}")
