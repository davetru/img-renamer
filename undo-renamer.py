import os
import csv
import tkinter as tk
from tkinter import filedialog
import traceback

# 📂 Ask the user to select a folder
def prompt_folder():
    root = tk.Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory(title="Select the folder with rename_log.csv")
    return folder_selected

# 🔁 Undo renaming from the log
def undo_rename(folder):
    log_path = os.path.join(folder, "rename_log.csv")
    if not os.path.exists(log_path):
        print("⚠️ Rename log not found in selected folder!")
        return

    with open(log_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)

    for row in reversed(rows):
        old = os.path.join(folder, row['original_filename'])
        new = os.path.join(folder, row['new_filename'])

        if os.path.exists(new):
            try:
                os.rename(new, old)
                print(f"🔁 Restored: {row['new_filename']} → {row['original_filename']}")
            except Exception as e:
                print(f"⚠️ Failed to rename {new} → {old}: {e}")
        else:
            print(f"❌ File not found: {new}")

    print("\n✅ Undo complete.")

# ▶️ Entry point
if __name__ == "__main__":
    try:
        folder = prompt_folder()
        if not folder or not os.path.isdir(folder):
            print("❌ No valid folder selected. Exiting.")
        else:
            undo_rename(folder)
    except Exception as e:
        print(f"\n❌ Script failed: {e}")
        traceback.print_exc()

    input("\n🔚 Press Enter to exit...")
