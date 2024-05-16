import os
from collections import defaultdict
from statistics import mode

def read_predictions(folder_path):
    id_to_classes = defaultdict(list)
    files_content = defaultdict(list)

    # Aggregate class predictions by ID
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split()
                if parts:
                    class_prediction = parts[0]
                    id_ = parts[-1]
                    id_to_classes[id_].append(class_prediction)
                    files_content[filename].append(line)

    return id_to_classes, files_content

def get_modes(id_to_classes):
    id_to_mode = {}
    for id_, classes in id_to_classes.items():
        try:
            id_to_mode[id_] = mode(classes)
        except:
            id_to_mode[id_] = classes[0]  # Default to first class if no mode found
    return id_to_mode

def write_corrected_files(folder_path, output_folder, id_to_mode, files_content):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Write files with corrected class predictions
    for filename, lines in files_content.items():
        new_file_path = os.path.join(output_folder, filename)
        with open(new_file_path, 'w') as new_file:
            for line in lines:
                parts = line.strip().split()
                if parts:
                    parts[0] = id_to_mode[parts[-1]]  # Replace class prediction with mode
                    new_file.write(" ".join(parts) + "\n")

def main(input_folder, output_folder):
    id_to_classes, files_content = read_predictions(input_folder)
    id_to_mode = get_modes(id_to_classes)
    write_corrected_files(input_folder, output_folder, id_to_mode, files_content)

if __name__ == "__main__":
    input_folder = '/Users/Huandong/Desktop/CV-Project/STOP_labels_sort_filtered'  # Set the path to your input folder
    output_folder = '/Users/Huandong/Desktop/CV-Project/STOP_labels_sort_filtered_mode'  # Set the path to your output folder
    main(input_folder, output_folder)
