
from pathlib import Path
from datetime import datetime

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel


app = FastAPI(
    title="Smart File Organizer & Duplicate Detector",
    description="API to retrieve organized file information.",
    version="1.0.0"
)


class FileInformation(BaseModel):
    file_name: str
    file_size: str
    extension: str
    modified_date: str
    file_path: str


class FileListResponse(BaseModel):
    total_files: int
    files: list[FileInformation]


@app.get("/")
def home():
    return {
        "message": "Smart File Organizer API is running",
        "documentation": "/docs"
    }


@app.get("/files", response_model=FileListResponse)
def get_organized_files(
    folder_path: str = Query(
        ...,
        description="Enter the folder path containing organized files"
    )
):

    # Get the folder path entered by the user
    organized_folder = Path(folder_path).expanduser()

    # Check whether folder exists
    if not organized_folder.exists():
        raise HTTPException(
            status_code=404,
            detail="Folder not found. Please enter a valid folder path."
        )

    # Check whether the path is a directory
    if not organized_folder.is_dir():
        raise HTTPException(
            status_code=400,
            detail="The given path is not a directory."
        )

    file_list = []

    try:
        # Read files from the selected folder and subfolders
        for file in organized_folder.rglob("*"):

            if file.is_file():

                try:
                    details = file.stat()

                    size = details.st_size

                    # Convert file size
                    if size < 1024:
                        readable_size = f"{size} Bytes"

                    elif size < 1024 ** 2:
                        readable_size = f"{size / 1024:.2f} KB"

                    elif size < 1024 ** 3:
                        readable_size = f"{size / (1024 ** 2):.2f} MB"

                    else:
                        readable_size = f"{size / (1024 ** 3):.2f} GB"

                    file_list.append(
                        FileInformation(
                            file_name=file.name,
                            file_size=readable_size,
                            extension=file.suffix.lower() or "No extension",
                            modified_date=datetime.fromtimestamp(
                                details.st_mtime
                            ).strftime("%d-%m-%Y %H:%M:%S"),
                            file_path=str(file)
                        )
                    )

                except (PermissionError, FileNotFoundError, OSError):
                    continue

    except PermissionError:
        raise HTTPException(
            status_code=403,
            detail="Permission denied while accessing the folder."
        )

    except OSError as error:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to read folder: {error}"
        )

    return FileListResponse(
        total_files=len(file_list),
        files=file_list
    )
