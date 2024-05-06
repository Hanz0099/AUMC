import os
import shutil
import chardet

def move_study_files(source_folder, destination_folder):
    # Create the destination folder if it does not exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Traverse all files in the source folder
    for root, dirs, files in os.walk(source_folder):
        for file in files:
            if file.endswith('.txt'):
                # Construct the full file path
                source_file = os.path.join(root, file)
                destination_file = os.path.join(destination_folder, file)
                # Move the file
                shutil.move(source_file, destination_file)
                print(f"Moved: {source_file} to {destination_file}")

source_folder = '/Users/hnfd/Desktop/zhanghan/UvA/Thesis/AUMC/idr-metadata'  # Source folder path
destination_folder = '/Users/hnfd/Desktop/zhanghan/UvA/Thesis/AUMC/All-txt'  # Destination folder path
# move_study_files(source_folder, destination_folder)


# Detect and convert all files to utf-8 format
def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
    return result['encoding']

def convert_to_utf8(file_path):
    encoding = detect_encoding(file_path)
    print(f"Detected encoding for {file_path}: {encoding}")
    if encoding != 'utf-8':
        with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
            text = f.read()
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Converted {file_path} to UTF-8")
    else:
        print(f"{file_path} is already UTF-8")

def process_directory(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.txt'):
                file_path = os.path.join(root, file)
                convert_to_utf8(file_path)

directory_path = '/Users/hnfd/Desktop/zhanghan/UvA/Thesis/AUMC/All-txt'  
# process_directory(directory_path)


