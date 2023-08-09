import os, re
import requests
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, DirCreatedEvent

box_count = 0
old_box_count = 0
light_incrementor = 0
traffic_light = False
old_traffic_light_bool = False
traffic_light_path = ""
path_with_crops = ""

def formulate_txion(obj_name):
    global box_count
    if box_count > 0:
        station_name = "Station " + str(box_count)
        if obj_name.lower() in ["apple", "cup", "bottle", "cell phone", "fork", "banana"]:
            print(f"{obj_name} part of allowed items")
            transaction = {
                "from": "Inventar",
                "to": station_name,
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
        added_subfolders = [subfolder_name for subfolder_name in new_subfolders if subfolder_name not in existing_subfolders or subfolder_name == "traffic light"]
        return added_subfolders
    except FileNotFoundError:
        # If the folder_path is not found, print an error message and return an empty list
        print(f"Folder not found: {path_with_crops}")
        return []
    
def choose_next_step(subfolder_arr):
    global traffic_light, box_count, old_traffic_light_bool, box_count
    if traffic_light == True and old_traffic_light_bool == False:
        old_traffic_light_bool = True
        print(f"Work surface is free. Please place the box on the loading area!")
    elif traffic_light == False and old_traffic_light_bool == True:
        box_count += 1
        print(f"New object(s) found in box {box_count}: {subfolder_arr}")
        old_traffic_light_bool = False
        for subfolder in subfolder_arr:
            formulate_txion(subfolder)
    elif traffic_light == False and old_traffic_light_bool == False:
        print(f"New object(s) found in box {box_count}: {subfolder_arr}")
        for subfolder in subfolder_arr:
            formulate_txion(subfolder)

def rename_file(path_with_crops):
    global traffic_light_path, light_incrementor
    light_incrementor += 1
    new_name = f"{light_incrementor} traffic light"
    new_traffic_light_path = os.path.join(path_with_crops, new_name).replace("/", "\\")
    os.rename(traffic_light_path, new_traffic_light_path)

def check_traffic_light_subfolder(added_subfolders):
    x = True
    pattern = r"\d+ traffic light"
    for subfolder in added_subfolders:
        if re.match(pattern, subfolder) is not None: #aka if a match is found
            x = False
    return x

def monitor_sub_subfolders(path_with_crops):
    global traffic_light, traffic_light_path, old_box_count
    time.sleep(10)
    # Get the initial subfolder names in the specified folder_path
    subfolders = get_initial_subfolder_names(path_with_crops)
    if "traffic light" in subfolders:
        traffic_light = True
        rename_file(path_with_crops)
        choose_next_step(subfolders)
    else:
        print(f"Please clear the work surface before starting your work!")

    while True:
        time.sleep(7)  # Wait for 2 seconds before checking for new subfolders
        # Get any newly added subfolders since the last check

        # Check if box_count is not equal to old_box_count
        if box_count != old_box_count:
            old_box_count = box_count
            # Create a list to store items that should be kept
            items_to_keep = []

            # Loop through each item in the subfolders list
            for item in subfolders:
                # Check if the item name contains "traffic light" or is a number
                if item == "traffic light" or (item[:-14].isdigit() and item.endswith("traffic light")):
                    items_to_keep.append(item)
            # Update the subfolders list to only include items_to_keep
            subfolders[:] = items_to_keep
            
        added_subfolders = get_new_subfolders(path_with_crops, subfolders)

        if added_subfolders:
            subfolders.extend(added_subfolders)
            if "traffic light" in added_subfolders:
                traffic_light = True
                rename_file(path_with_crops)
            elif check_traffic_light_subfolder(added_subfolders):
                # If there are newly added subfolders, extend the subfolders list and print the names
                traffic_light = False
        else:
            traffic_light = False
        choose_next_step(added_subfolders)

def check_for_new_subfolders(yolo_runs_folder_path):
    global traffic_light_path
    if not os.path.exists(yolo_runs_folder_path) or not os.path.isdir(yolo_runs_folder_path):
        print(f"The specified path '{yolo_runs_folder_path}' does not exist or is not a folder.")
        return

    class NewSubfolderHandler(FileSystemEventHandler):
        def on_created(self, event):
            global traffic_light_path
            if event.is_directory:
                print(f"New subfolder detected: {event.src_path}")
                path_with_crops = os.path.join(event.src_path, "crops").replace("/", "\\")
                traffic_light_path = os.path.join(path_with_crops, "traffic light").replace("/", "\\")
                #func
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