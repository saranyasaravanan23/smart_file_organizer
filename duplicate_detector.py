import hashlib
from pathlib import Path


def calculate_md5(file_path: Path) -> str:
    """Calculate the MD5 hash of a file in small chunks."""
    md5_hash = hashlib.md5()
    with file_path.open("rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()


def find_duplicate_files(file_paths: list[Path]) -> list[list[Path]]:
    """Group files that have identical MD5 hashes."""
    hash_groups: dict[str, list[Path]] = {}

    for file_path in file_paths:
        try:
            file_hash = calculate_md5(file_path)
            hash_groups.setdefault(file_hash, []).append(file_path)
        except (PermissionError, FileNotFoundError, OSError) as error:
            print(f"Could not check {file_path.name}: {error}")

    return [group for group in hash_groups.values() if len(group) > 1]
