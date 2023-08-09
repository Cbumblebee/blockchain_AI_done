import os
import requests
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, DirCreatedEvent

def formulate_txion(obj_name):
    transaction = {
        "from": "Inventar",
        "to": "Station A",
        "Object": obj_name,
    }
    response = requests.post("http://127.0.0.1:5000/transactions", json=transaction)
    print(response.text)


class NewSub_SubfolderHandler(FileSystemEventHandler):
    def on_created(self, event):
        if isinstance(event, DirCreatedEvent):
            print(f"New Object detected: {event.src_path}")
            obj_name = os.path.basename(event.src_path)
            allowed_items = ["apple", "bottle", "cell phone", "fork", "cup"]
            if obj_name in allowed_items:
                formulate_txion(obj_name)
            else:
                no_obj = "Kein Objekt aus dem Inventar."
                return no_obj

def check_for_sub_subfolders(path_with_crops):
    print(f"subsub{path_with_crops}")
    scnd_event_handler = NewSub_SubfolderHandler()
    observer = Observer()
    observer.schedule(scnd_event_handler, path=path_with_crops, recursive=False)
    time.sleep(10)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()

def check_for_new_subfolders(yolo_runs_folder_path):
    if not os.path.exists(yolo_runs_folder_path) or not os.path.isdir(yolo_runs_folder_path):
        print(f"The specified path '{yolo_runs_folder_path}' does not exist or is not a folder.")
        return

    class NewSubfolderHandler(FileSystemEventHandler):
        def on_created(self, event):
            if event.is_directory: #überprüft, ob das Ereignis, das von Watchdog gemeldet wird, auf ein Verzeichnis (Ordner) bezogen ist
                print(f"New subfolder detected: {event.src_path}")
                path_with_crops = os.path.join(event.src_path, "crops")
                print(f"sob_one{path_with_crops}")
                check_for_sub_subfolders(path_with_crops)

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
    yolo_runs_folder_path = input("Enter the path of the folder to monitor: ")
    check_for_new_subfolders(yolo_runs_folder_path)