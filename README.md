# Smart File Organizer & Duplicate Detector

## Project objective
A Python application that displays file information, detects duplicate files using MD5 hashing, and organizes files into folders based on their extensions. The application asks for confirmation before moving each file and avoids overwriting existing files.

## Project structure

```text
Smart_File_Organizer/
├── main.py
├── organizer.py
├── file_info.py
├── duplicate_detector.py
├── api.py
├── requirements.txt
├── .gitignore
├── README.md
└── screenshots/
    └── README.txt
```

## Requirements
- Python 3.9 or later
- FastAPI and Uvicorn are needed only for the bonus API.

## Run the file organizer

Open a terminal in this project folder and run:

```bash
python main.py
```

Enter the full path of the folder you want to organize. The program displays file name, size, extension and modified date, checks for duplicate files, and asks before moving each file.

Example folder categories:
- `PDF` - PDF documents
- `Images` - JPG, JPEG, PNG, GIF, BMP and WEBP images
- `Excel` - XLS, XLSX and CSV files
- `Python` - Python files
- `Others` - other file extensions

The folders are created inside the selected folder only when needed. Files are not moved unless the user confirms.

## Duplicate detection
The `duplicate_detector.py` module reads files in binary mode and calculates an MD5 hash. Files with matching hashes are displayed as duplicates. The program does not automatically delete duplicate files.

## Preventing overwrite
Before moving a file, the program checks whether a file with the same name already exists in the destination. If it does, a numbered name such as `report_1.pdf` is used.

## Bonus: FastAPI endpoint

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

In `api.py`, change `ORGANIZED_FOLDER` to the folder you want the API to read. Then run:

```bash
python -m uvicorn api:app --reload
```

Open `http://127.0.0.1:8000/docs` and test `GET /files`.

## Modules explained
- `main.py`: Starts the command-line application and handles top-level errors.
- `organizer.py`: Contains the `FileOrganizer` class and file-moving logic.
- `file_info.py`: Reads file metadata and formats file sizes.
- `duplicate_detector.py`: Calculates MD5 hashes and groups duplicate files.
- `api.py`: Provides the optional FastAPI endpoint.

## Screenshots
Place your own terminal and API screenshots in the `screenshots` folder. Do not use sample or fabricated screenshots.

## Safety note
Test with a copy of a folder first. The organizer moves files after confirmation; it does not delete them. MD5 is used here for duplicate detection, not for security or password storage.
