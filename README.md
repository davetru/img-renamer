# 📸 Screenshot Renamer

A simple Python utility that scans a folder and renames `.jpg`, `.jpeg`, and `.png` files based on their original creation time — using embedded EXIF metadata when available.

Perfect for organizing screenshots, camera uploads, or exported media files into a clean, timestamped format like:

```
2024-08-09-1345.jpg
```

---

## ✨ Features

* 📂 Folder picker with GUI (no terminal input needed)
* 🧠 Renames JPEGs using `DateTimeOriginal` from EXIF metadata (if available)
* 📾 Falls back to file creation time (`ctime`) for:

  * PNGs (no EXIF)
  * JPEGs without metadata
* 🔁 Prevents name collisions by auto-appending `_1`, `_2`, etc.
* 📟 Creates a CSV log (`rename_log.csv`) for undo or audit purposes
* ⚙️ Supports `.jpg`, `.jpeg`, `.png`

---

## 📦 Requirements

Install the only required external library:

```bash
pip install pillow
```

Everything else uses built-in Python libraries (`os`, `datetime`, `tkinter`, etc.).

---

## 🚀 How to Use

1. Run the script:

```bash
python img-renamer.py
```

2. A folder selection dialog will appear. Choose the folder containing your screenshots or photos.

3. The script will rename each supported image using the format:

```
YYYY-MM-DD-HHMM
```

4. A `rename_log.csv` file will be created in the same folder.

---

## 💠 Undo Renames

Use the companion `undo_rename.py` script to restore all filenames from the log.

### How to Use `undo_rename.py`

1. Run the script:

```bash
python undo_rename.py
```

2. A folder selection dialog will appear. Choose the same folder where the original renaming was performed.

3. The script will read `rename_log.csv` in that folder and attempt to reverse all changes by renaming files back to their original names.

> ⚠️ The log must not be deleted or renamed for this to work.

---

## 🧩 Example Output

**Before:**

```
IMG_2023_1243.jpg
Screen Shot 2024-01-10 at 9.22.13 AM.png
```

**After:**

```
2023-07-12-1120.jpg
2024-01-10-0922.png
rename_log.csv
```

---

## 📌 License

MIT License — free for personal and commercial use.

---

## 💡 Notes

* PNG files do not contain EXIF metadata. Their timestamp will always default to the file creation time (`ctime`).
* Only `.jpg`, `.jpeg`, and `.png` are renamed. Other files are skipped safely.
* The script ignores its own `rename_log.csv` to avoid recursive renaming.

---

## 🧑‍💻 Author

Created by Dave Tran. Built for ease, simplicity, and clean photo folders.

## 🧠 Acknowledgments

Thanks to the Pillow library for making image processing fun and flexible!

