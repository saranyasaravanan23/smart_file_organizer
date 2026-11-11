from datetime import datetime
from pathlib import Path


def get_file_information(file_path: Path) -> dict:
    """Return basic information about one file."""
    details = file_path.stat()
    return {
        "name": file_path.name,
        "size": details.st_size,
        "extension": file_path.suffix.lower() or "No extension",
        "modified_date": datetime.fromtimestamp(details.st_mtime).strftime(
            "%d-%m-%Y %H:%M:%S"
        ),
    }


def format_file_size(size_in_bytes: int) -> str:
    """Convert bytes into a readable size."""
    if size_in_bytes < 1024:
        return f"{size_in_bytes} Bytes"
    if size_in_bytes < 1024 ** 2:
        return f"{size_in_bytes / 1024:.2f} KB"
    if size_in_bytes < 1024 ** 3:
        return f"{size_in_bytes / (1024 ** 2):.2f} MB"
    return f"{size_in_bytes / (1024 ** 3):.2f} GB"
