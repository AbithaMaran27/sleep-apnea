import os

txt_dir = "C:/Users/abith/PycharmProjects/SleepApnea_Vincents_data-only/data1"  # Replace with the folder containing .txt files
for filename in os.listdir(txt_dir):
    if filename.endswith(".txt"):
        print(f"Contents of {filename}:")
        with open(os.path.join(txt_dir, filename), "r") as file:
            print(file.read())
        print("-" * 50)
