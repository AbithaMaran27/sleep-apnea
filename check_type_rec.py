import os

rec_dir = "C:/Users/abith/PycharmProjects/SleepApnea_Vincents_data-only/data1"  # Replace with your .rec folder path

for filename in os.listdir(rec_dir):
    if filename.endswith(".rec"):
        file_path = os.path.join(rec_dir, filename)
        print(f"Inspecting {file_path}...")
        with open(file_path, "rb") as file:
            content = file.read(100)  # Read first 100 bytes
            print(f"First 100 bytes of {filename}: {content}")
        print("-" * 50)
