import os
import numpy as np
import matplotlib.pyplot as plt

# Path to your aligned `.npy` files
aligned_dir = "data_aligned_labels"

# Initialize counters for overall label distribution
overall_counts = {}

# Iterate through aligned files
for file in os.listdir(aligned_dir):
    if file.endswith("_aligned.npy"):
        filepath = os.path.join(aligned_dir, file)
        data = np.load(filepath, allow_pickle=True).item()

        labels = data['labels']
        unique, counts = np.unique(labels, return_counts=True)
        label_counts = dict(zip(unique, counts))

        # Update overall counts
        for label, count in label_counts.items():
            overall_counts[label] = overall_counts.get(label, 0) + count

        print(f"File: {file}")
        print(f"Label Distribution: {label_counts}")
        print("-------------------------------------")

# Plot overall distribution
labels = list(overall_counts.keys())
counts = list(overall_counts.values())

plt.figure(figsize=(8, 5))
plt.bar(labels, counts, color='skyblue')
plt.title("Overall Label Distribution")
plt.xlabel("Labels")
plt.ylabel("Count")
plt.xticks(labels, [f"Class {label}" for label in labels])
plt.show()
