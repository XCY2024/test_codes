"""
This is to watch the download folder and move the file to the corresponding folder
"""

import os
import time
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# 下载文件夹路径
USER = os.environ.get('USERNAME')
download_folder = f'C:\\Users\{USER}\\Downloads'

class DownloadHandler(FileSystemEventHandler):
    def on_created(self, event):
        time.sleep(1)
        if not event.is_directory:
            self.process_file(event.src_path)

    def on_moved(self, event):
        time.sleep(1)
        if not event.is_directory:
            self.process_file(event.dest_path)

    def process_file(self, file_path):
        skip_extensions = ['crdownload','tmp','ini']
        file_name = os.path.basename(file_path)
        extension = os.path.splitext(file_name)[1][1:]
        if extension in skip_extensions:
            return
        if extension:
            # 创建目标文件夹
            target_folder = os.path.join(download_folder, extension)
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)

            # 移动文件
            try:
                shutil.move(file_path, os.path.join(target_folder, file_name))
                print(f'Moved {file_name} to {target_folder}')
            except Exception as e:
                print(f'Failed to move {file_name}: {e}')

if __name__ == "__main__":
    event_handler = DownloadHandler()
    observer = Observer()
    observer.schedule(event_handler, download_folder, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()