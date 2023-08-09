import os
import requests
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, DirCreatedEvent

def formulate_txion(obj_name):
    print(f"Object found:{obj_name}")
    if obj_name.lower() in ["apple", "cup", "bottle", "cell phone", "fork", "banana"]:
        print(f"part of allowed items")
        transaction = {
            "from": "Inventar",
            "to": "Station A",
            "Object": obj_name,
        }
        response = requests.post("http://127.0.0.1:5000/transactions", json=transaction)
        print(response.text)
    else:
        print(f"Transaction skipped for '{obj_name}'.")


def get_initial_subfolder_names(path_with_crops):
    try:
        # Get a list of subfolders' names in the given folder_path
        subfolders = [subfolder_name for subfolder_name in os.listdir(path_with_crops) if os.path.isdir(os.path.join(path_with_crops, subfolder_name))]
        return subfolders
    except FileNotFoundError:
        # If the folder_path is not found, print an error message and return an empty list
        print(f"Folder not found: {path_with_crops}")
        return []

def get_new_subfolders(path_with_crops, existing_subfolders):
    try:
        # Get a list of subfolders' names in the given folder_path
        new_subfolders = [subfolder_name for subfolder_name in os.listdir(path_with_crops) if os.path.isdir(os.path.join(path_with_crops, subfolder_name))]
        
        # Find subfolders that are in new_subfolders but not in existing_subfolders
        added_subfolders = [subfolder_name for subfolder_name in new_subfolders if subfolder_name not in existing_subfolders]
        return added_subfolders
    except FileNotFoundError:
        # If the folder_path is not found, print an error message and return an empty list
        print(f"Folder not found: {path_with_crops}")
        return []

def monitor_sub_subfolders(path_with_crops):
    time.sleep(10)
    # Get the initial subfolder names in the specified folder_path
    subfolders = get_initial_subfolder_names(path_with_crops)
    print(f"Initial subfolders: {subfolders}")
    for subfolder in subfolders:
        formulate_txion(subfolder)

    while True:
        time.sleep(2)  # Wait for 2 seconds before checking for new subfolders
        # Get any newly added subfolders since the last check
        added_subfolders = get_new_subfolders(path_with_crops, subfolders)

        if added_subfolders:
            # If there are newly added subfolders, extend the subfolders list and print the names
            subfolders.extend(added_subfolders)
            print(f"Added subfolders: {added_subfolders}")
            for added_subfolder in added_subfolders:
                formulate_txion(added_subfolder)


def check_for_new_subfolders(yolo_runs_folder_path):
    if not os.path.exists(yolo_runs_folder_path) or not os.path.isdir(yolo_runs_folder_path):
        print(f"The specified path '{yolo_runs_folder_path}' does not exist or is not a folder.")
        return

    class NewSubfolderHandler(FileSystemEventHandler):
        def on_created(self, event):
            if event.is_directory:
                print(f"New subfolder detected: {event.src_path}")
                path_with_crops = os.path.join(event.src_path, "crops").replace("/", "\\")
                monitor_sub_subfolders(path_with_crops)


    event_handler = NewSubfolderHandler()
    observer = Observer()
    observer.schedule(event_handler, path=yolo_runs_folder_path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join() #wartet, dass der Observer seine Arbeit abschließt und alle Hintergrundprozesse beendet werden, bevor das Programm beendet wird

if __name__ == "__main__":
    yolo_runs_folder_path = r"C:\Users\Area1\Desktop\cloned_blockchain_AI\blockchain_AI\yolo\runs\detect"
    check_for_new_subfolders(yolo_runs_folder_path)