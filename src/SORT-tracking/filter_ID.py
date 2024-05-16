import os
from collections import defaultdict

def count_ids(folder_path):
    id_count = defaultdict(int)
    files_content = defaultdict(list)

    # Read each file and count ID frequencies
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split()
                if parts:
                    id_ = parts[-1]
                    id_count[id_] += 1
                    files_content[filename].append((line, id_))

    return id_count, files_content

def filter_and_write_files(folder_path, output_folder, id_count, files_content):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Write new files with filtered lines
    for filename, lines in files_content.items():
        lines_written = 0
        new_file_path = os.path.join(output_folder, filename)
        with open(new_file_path, 'w') as new_file:
            for line, id_ in lines:
                if id_count[id_] > 20:
                    new_file.write(line)
                    lines_written += 1
        
        # If no lines were written, delete the new file
        if lines_written == 0:
            os.remove(new_file_path)

def main(input_folder, output_folder):
    id_count, files_content = count_ids(input_folder)
    filter_and_write_files(input_folder, output_folder, id_count, files_content)

if __name__ == "__main__":
    input_folder = '../Data/labels_sort'  # Set the path to your input folder
    output_folder = '../Data/labels_sort_filtered'  # Set the path to your output folder
    main(input_folder, output_folder)
