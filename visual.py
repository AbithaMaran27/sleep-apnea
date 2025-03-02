# Visualize the updated balanced dataset
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import os

balanced_data_folder = 'C:/Users/abith/PycharmProjects/SleepApnea_Vincents_data-only/data_balanced_labels'


def visualize_label_distribution(folder):
    label_counts = Counter()
    for file in os.listdir(folder):
        if file.endswith('_aligned.npy'):
            data = np.load(os.path.join(folder, file), allow_pickle=True).item()
            label_counts.update(data['labels'])

    labels, counts = zip(*label_counts.items())
    plt.bar(labels, counts, color='skyblue')
    plt.title("Balanced Label Distribution")
    plt.xlabel("Labels")
    plt.ylabel("Counts")
    plt.xticks(labels)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()


visualize_label_distribution(balanced_data_folder)
