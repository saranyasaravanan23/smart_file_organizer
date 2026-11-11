from pathlib import Path
import shutil

from duplicate_detector import find_duplicate_files
from file_info import format_file_size, get_file_information


class FileOrganizer:
    """Organize files into extension-based folders and detect duplicates."""

    CATEGORIES = {
        ".pdf": "PDF",
        ".jpg": "Images", ".jpeg": "Images", ".png": "Images",
        ".gif": "Images", ".bmp": "Images", ".webp": "Images",
        ".xls": "Excel", ".xlsx": "Excel", ".csv": "Excel",
        ".py": "Python",
    }

    def __init__(self, folder_path: str):
        self.folder = Path(folder_path).expanduser()
        if not self.folder.exists():
            raise FileNotFoundError(f"Folder does not exist: {self.folder}")
        if not self.folder.is_dir():
            raise NotADirectoryError(f"Path is not a folder: {self.folder}")

    def get_files(self) -> list[Path]:
        """Return files directly inside the selected folder."""
        return [path for path in self.folder.iterdir() if path.is_file()]

    def display_file_information(self) -> None:
        print("\n===== FILE INFORMATION =====")
        for file_path in self.get_files():
            try:
                info = get_file_information(file_path)
                print(f"\nFile Name: {info['name']}")
                print(f"File Size: {format_file_size(info['size'])}")
                print(f"Extension: {info['extension']}")
                print(f"Modified Date: {info['modified_date']}")
            except (PermissionError, FileNotFoundError, OSError) as error:
                print(f"Could not read {file_path.name}: {error}")

    def find_duplicates(self) -> None:
        print("\n===== DUPLICATE FILES (MD5) =====")
        duplicates = find_duplicate_files(self.get_files())
        if not duplicates:
            print("No duplicate files found.")
            return

        for number, group in enumerate(duplicates, start=1):
            print(f"\nDuplicate Group {number}:")
            for file_path in group:
                print(f" - {file_path.name}")

    def _destination_without_overwrite(self, destination: Path) -> Path:
        """Choose a free destination name; never overwrite an existing file."""
        if not destination.exists():
            return destination

        counter = 1
        while True:
            candidate = destination.with_name(
                f"{destination.stem}_{counter}{destination.suffix}"
            )
            if not candidate.exists():
                return candidate
            counter += 1

    def organize_files(self) -> None:
        for file_path in self.get_files():
            extension = file_path.suffix.lower()
            folder_name = self.CATEGORIES.get(extension, "Others")
            target_folder = self.folder / folder_name
            destination = target_folder / file_path.name

            answer = input(f"Do you want to move {file_path.name} to {folder_name}? (yes/no): ")
            if answer.strip().lower() not in {"yes", "y"}:
                print("File movement cancelled.")
                continue

            try:
                target_folder.mkdir(parents=True, exist_ok=True)
                destination = self._destination_without_overwrite(destination)
                shutil.move(str(file_path), str(destination))
                print(f"File moved successfully: {destination.name}")
            except (PermissionError, FileNotFoundError, shutil.Error, OSError) as error:
                print(f"Could not move {file_path.name}: {error}")
