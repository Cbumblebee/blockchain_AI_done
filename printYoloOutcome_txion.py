import os
import requests

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

if __name__ == "__main__":
    folder_path = input("Geben Sie den Pfad des Ordners ein: ")
    subfolders_info = count_files_in_subfolders(folder_path)

    print("Unterordner und die Anzahl der Elemente in jedem Unterordner:")
    for subfolder, num_elements in subfolders_info.items():
        print(f"Unterordner '{subfolder}' enthält {num_elements} Elemente.")

    # Erstellen Sie die data-Variable für die Transaktionen
    data = []
    for subfolder, num_elements in subfolders_info.items():
        transaction = {
            "from": "Inventar",
            "to": "Station A",
            "Object": subfolder,
            "amount": num_elements
        }
        data.append(transaction)

        # Rufen Sie die Funktion aus dem anderen Skript auf
        response = requests.post("http://127.0.0.1:5000/transactions", json=transaction)
        print(response.text)



        #the folder_path so far: C:\Users\Area1\Desktop\virtual_env_forAI\yolov7\seg\runs\predict-seg\coco18\crops