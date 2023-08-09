import os
import time

def check_for_new_subfolders(folder_path, interval=5):
    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        print(f"The specified path '{folder_path}' does not exist or is not a folder.")
        return

    subfolders = set(os.listdir(folder_path))

    while True:
        time.sleep(interval)
        current_subfolders = set(os.listdir(folder_path))
        new_subfolders = current_subfolders - subfolders

        if new_subfolders:
            print("New subfolders detected:")
            for new_subfolder in new_subfolders:
                full_path = os.path.join(folder_path, new_subfolder)
                print(full_path)
            subfolders = current_subfolders

if __name__ == "__main__":
    folder_path = input("Enter the path of the folder to monitor: ")
    check_for_new_subfolders(folder_path)
