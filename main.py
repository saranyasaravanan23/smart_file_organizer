from organizer import FileOrganizer
def main():
    print("=" * 55)
    print(" SMART FILE ORGANIZER & DUPLICATE DETECTOR")
    print("=" * 55)
    folder_path = input(
        "\nEnter the folder path to organize: "
    ).strip().strip('"')
    try:
        organizer = FileOrganizer(folder_path)
        organizer.display_file_information()
        organizer.find_duplicates()
        print("\n===== FILE ORGANIZATION =====")
        organizer.organize_files()
        print("\nOrganization process completed.")
    except FileNotFoundError as error:
        print(f"Error: {error}")
    except NotADirectoryError as error:
        print(f"Error: {error}")
    except PermissionError as error:
        print(f"Permission denied: {error}")
    except OSError as error:
        print(f"File system error: {error}")
if __name__ == "__main__":
    main()
