

import os
import requests
import time

def count_files_in_subfolders(folder_path):
    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        print(f"Der angegebene Pfad '{folder_path}' existiert nicht oder ist kein Ordner.")
        return

    subfolders_info = {}  # Dictionary, um Informationen zu speichern

    for entry in os.scandir(folder_path):
        if entry.is_dir():
            subfolder_path = entry.path
            num_files = len(os.listdir(subfolder_path))
            subfolders_info[entry.name] = num_files

    return subfolders_info

def formulate_txion(path_new_yolo_folder):
    # Wartezeit von 15 Sekunden
    time.sleep(25)
    subfolders_info = count_files_in_subfolders(path_new_yolo_folder)

    print("Unterordner und die Anzahl der Elemente in jedem Unterordner:")
    for subfolder, num_elements in subfolders_info.items():
        print(f"Unterordner '{subfolder}' enthält {num_elements} Elemente.")

    # Erstellen Sie die data-Variable für die Transaktionen
    data = []
    for subfolder, num_elements in subfolders_info.items():
        # Extract the name of the subfolder from the full path
        subfolder_name = os.path.basename(subfolder)
        # Check if the subfolder name is in the allowed item list
        allowed_items = ["apple", "bottle", "cell phone", "fork", "cup"]
        if subfolder_name in allowed_items:
            transaction = {
                "from": "Inventar",
                "to": "Station A",
                "Object": subfolder_name,
                "amount": num_elements
            }
            data.append(transaction)

    # Rufen Sie die Funktion aus dem anderen Skript auf
    for transaction in data:
        response = requests.post("http://127.0.0.1:5000/transactions", json=transaction)
        print(response.text)



        #the folder_path so far: C:\Users\Area1\Desktop\virtual_env_forAI\yolov7\seg\runs\predict-seg\coco18\crops



def check_for_new_subfolders(yolo_runs_folder_path, interval=5):
    if not os.path.exists(yolo_runs_folder_path) or not os.path.isdir(yolo_runs_folder_path):
        print(f"The specified path '{yolo_runs_folder_path}' does not exist or is not a folder.")
        return

    subfolders = set(os.listdir(yolo_runs_folder_path))

    while True:
        time.sleep(interval)
        current_subfolders = set(os.listdir(yolo_runs_folder_path))
        new_subfolders = list(current_subfolders - subfolders)  # Convert the set to a list

        if new_subfolders:
            print("New subfolders detected")
            for new_subfolder in new_subfolders:
                full_path = os.path.join(yolo_runs_folder_path, new_subfolder)
                # Automatically add "/crops" to the full_path
                full_path_with_crops = os.path.join(full_path, "crops")
                formulate_txion(full_path_with_crops)
            subfolders = current_subfolders

if __name__ == "__main__":
    yolo_runs_folder_path = input("Enter the path of the folder to monitor: ")
    check_for_new_subfolders(yolo_runs_folder_path)