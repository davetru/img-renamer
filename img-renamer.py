import os
import datetime
import csv
import tkinter as tk
from tkinter import filedialog
import traceback
from PIL import Image
from PIL.ExifTags import TAGS

# 📂 Ask the user to select a folder
def prompt_folder():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askdirectory(title="Select a folder to rename images")

# 🧠 Extract DateTimeOriginal from EXIF (JPEG only)
def get_date_taken(file_path):
    try:
        image = Image.open(file_path)
        exif_data = image._getexif()
        if not exif_data:
            return None

        for tag_id, value in exif_data.items():
            if TAGS.get(tag_id, tag_id) == "DateTimeOriginal":
                return datetime.datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
    except Exception as e:
        print(f"⚠️ EXIF read failed for {file_path}: {e}")
    return None

# ✅ Main renaming logic
def rename_files_by_datetime(folder):
    log_path = os.path.join(folder, "rename_log.csv")
    log_rows = []

    print(f"📂 Scanning folder: {folder}")
    files = os.listdir(folder)
    print(f"📦 Found {len(files)} items")

    for filename in files:
        if filename == "rename_log.csv":
            print(f"⏭ Skipping log file: {filename}")
            continue

        file_path = os.path.join(folder, filename)
        if not os.path.isfile(file_path):
            continue

        name, ext = os.path.splitext(filename)
        ext = ext.lower()
        if ext not in [".jpg", ".jpeg", ".png"]:
            print(f"⏭ Skipping unsupported file type: {filename}")
            continue

        print(f"🧪 Found file: {filename}")
        try:
            if ext in [".jpg", ".jpeg"]:
                dt = get_date_taken(file_path)
                if dt:
                    source = "exif"
                else:
                    print("⚠️ No EXIF data found in JPEG, using file creation time.")
                    source = "ctime"
            else:
                print("ℹ️ PNG file — skipping EXIF, using file creation time.")
                dt = None
                source = "ctime"

            if not dt:
                dt = datetime.datetime.fromtimestamp(os.path.getctime(file_path))

            new_base = dt.strftime("%Y-%m-%d-%H%M")
            new_file_path = os.path.join(folder, new_base + ext)
            counter = 1
            while os.path.exists(new_file_path):
                new_file_path = os.path.join(folder, f"{new_base}_{counter}{ext}")
                counter += 1

            os.rename(file_path, new_file_path)
            print(f"✅ Renamed: {filename} → {os.path.basename(new_file_path)}")
            log_rows.append([filename, os.path.basename(new_file_path), source])

        except Exception as e:
            print(f"❌ Failed to rename {filename}: {e}")

    with open(log_path, mode='w', newline='', encoding='utf-8') as log_file:
        writer = csv.writer(log_file)
        writer.writerow(["original_filename", "new_filename", "timestamp_source"])
        writer.writerows(log_rows)

    print(f"\n📄 Rename log saved to: {log_path}")

# ▶️ Entry point
if __name__ == "__main__":
    try:
        folder = prompt_folder()
        if not folder or not os.path.isdir(folder):
            print("❌ No valid folder selected. Exiting.")
        else:
            rename_files_by_datetime(folder)
    except Exception as e:
        print(f"\n❌ Script failed: {e}")
        traceback.print_exc()

    input("\n🔚 Press Enter to exit...")
