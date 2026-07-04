import os
import shutil

# AUTO-DETECT DOWNLOADS PATH
DOWNLOADS_PATH = os.path.join(os.path.expanduser("~"), "Downloads")

DESTINATIONS = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "Documents": [".pdf", ".docx", ".txt"],
    "Software": [".exe", ".msi", ".zip", ".rar"],
    "Videos": [".mp4", ".mkv", ".mov"],
    "Music": [".mp3", ".wav", ".aac"]
}

JUNK_EXTENSIONS = [".tmp", ".crdownload", ".ds_store"]

# Create folders if not exist
for folder in DESTINATIONS.keys():
    os.makedirs(os.path.join(DOWNLOADS_PATH, folder), exist_ok=True)

def get_new_filename(path):
    base, ext = os.path.splittext(path)
    counter = 1
    new_path = path
    
    while os.path.exists(new_path):
        new_path = f"{base}({counter}){ext}"
        counter += 1
        
    return new_path

for file in os.listdir(DOWNLOADS_PATH):
    file_path = os.path.join(DOWNLOADS_PATH, file)
    
    if os.path.isdir(file_path):
        continue
        
    _, ext = os.path.splittext(file)
    
    # Delete junk
    if ext.lower() in JUNK_EXTENSIONS:
        os.remove(file_path)
        continue
        
    # Move files
    for folder, extensions in DESTINATIONS.items():
        if ext.lower() in extensions:
            new_path = get_new_filename(os.path.join(DOWNLOADS_PATH, folder, file))
            shutil.move(file_path, new_path)
            break