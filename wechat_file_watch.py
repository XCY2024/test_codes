"""
watch the wechat file folder, if there is a new file, copy it to the dst folder
"""
import time
import shutil
import os
import time
import threading
# this is where your wechat files are stored, change it to your own path
windows_username = os.environ['USERNAME']
src_folder = "C:\\Users\\windows_username\\Documents\\WeChat Files"
ext_list = ['jpg','png','gif','bmp','jpeg','webp','ico','pdf','doc','docx','xls','xlsx','ppt','pptx','txt','zip','rar','7z','exe','apk','ipa','dmg','mp4','mkv','avi','rmvb','rm','wmv','mov','mp3','wav','aac','flac','ogg','wma','ape','flac','ape','aac','ogg','wma','ape']
skip_extensions = ['crdownload','tmp','ini']
dst_folder = "C:\\Users\\windows_username\\Downloads\\"
# history file path in user directory
history_file_path = "C:\\Users\\windows_username\\history_record.txt"

# function to watch src folder, with os.walk function, if there is a new file, copy it to dst folder,there is a history record, so it will not copy the same file again
def watch_folder(src_folder, dst_folder, ext_list, skip_extensions):
    # get the history record
    history_record = []
    with open(history_file_path, "r") as f:
        for line in f.readlines():
            history_record.append(line.strip())
    # get the file list in src folder
    while True:
        for root, dirs, files in os.walk(src_folder):
            for file in files:
                # get the file path
                file_path = os.path.join(root, file)
                # if the file_path is in the history record, skip it
                if file_path in history_record:
                    continue
                # get the file extension
                file_extension = file_path.split(".")[-1]
                # if the file extension is in the ext_list and not in the skip_extensions, copy it to dst folder
                if file_extension in ext_list and file_extension not in skip_extensions:
                    shutil.copy(file_path, dst_folder)
                    history_record.append(file_path)
                    print("copy file: %s to %s" % (file_path, dst_folder))
                # save the history record
                with open(history_file_path, "a") as f:
                    f.write(file_path + "\n")
        time.sleep(1)

if __name__ == "__main__":
    # check if there's a history file, if not, creat one
    if not os.path.exists(history_file_path):
        with open(history_file_path, "w") as f:
            f.write('')
    # start a thread to watch the folder
    t = threading.Thread(target=watch_folder, args=(src_folder, dst_folder, ext_list, skip_extensions))
    t.start()
    # keep the main thread alive
    while True:
        time.sleep(1)
    
    
    

    