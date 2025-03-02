import os

rec_dir = "C:/Users/abith/PycharmProjects/SleepApnea_Vincents_data-only/data1"  # Replace with the folder containing .rec files

for filename in os.listdir(rec_dir):
    if filename.endswith(".rec"):
        with open(os.path.join(rec_dir, filename), "r") as file:
            print(f"Contents of {filename}:")
            print(file.read())
            print("-" * 50)
