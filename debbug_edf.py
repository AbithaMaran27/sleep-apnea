import numpy as np

segmented_file = "C:/Users/abith/PycharmProjects/SleepApnea_Vincents_data-only/data_preprocessed_segmented_vincent/ucddb028_lifecard_segmented.npy"
data = np.load(segmented_file, allow_pickle=True).item()

print("Segments shape:", data['segments'].shape)
print("Labels shape:", data['labels'].shape)
print("Unique labels:", set(data['labels']))
