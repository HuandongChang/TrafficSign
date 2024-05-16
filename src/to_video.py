import cv2
import os

def load_labels(label_path):
    """Charger les labels à partir d'un fichier texte où chaque ligne contient 'id nom_label'."""
    labels = {}
    with open(label_path, 'r') as file:
        for line in file:
            parts = line.strip().split(' ', 1)  # Split seulement sur le premier espace
            if len(parts) == 2:
                label_id, label_name = parts
                labels[int(label_id)] = label_name  # Convertir label_id en entier
    return labels

def yolo_to_corners(x, y, w, h, img_width, img_height):
    """Convertir les coordonnées YOLO relatives aux coins absolus de la bounding box."""
    x_center = x * img_width
    y_center = y * img_height
    width = w * img_width
    height = h * img_height

    x_min = int(x_center - width / 2)
    y_min = int(y_center - height / 2)
    x_max = int(x_center + width / 2)
    y_max = int(y_center + height / 2)

    return x_min, y_min, x_max, y_max

def annotate_video(video_path, annotations_dir, labels_path, output_path):
    """Annoter la vidéo avec des bounding boxes basées sur les fichiers YOLO."""
    # Charger la vidéo
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Erreur : Impossible d'ouvrir la vidéo.")
        return

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    labels = load_labels(labels_path)

    # Préparer le writer de la vidéo de sortie
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, 60.0, (frame_width, frame_height))

    frame_id = 1
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # annotation_file = os.path.join(annotations_dir, f"Cambridge_{frame_id}.txt")
        annotation_file = os.path.join(annotations_dir, f"{frame_id}.txt")
        if os.path.exists(annotation_file):
            with open(annotation_file, 'r') as file:
                for line in file:
                    parts = line.strip().split()
                    if len(parts) == 6:
                        label_id, x, y, w, h, conf = map(float, parts)
                        x_min, y_min, x_max, y_max = yolo_to_corners(x, y, w, h, frame_width, frame_height)
                        label_name = labels.get(int(label_id), 'Unknown')
                        cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
                        cv2.putText(frame, label_name, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    elif len(parts) == 7:
                        label_id, x, y, w, h, conf, tracking_id = map(float, parts)
                        x_min, y_min, x_max, y_max = yolo_to_corners(x, y, w, h, frame_width, frame_height)
                        label_name = labels.get(int(label_id), 'Unknown') + " id:" + str(tracking_id)
                        cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
                        cv2.putText(frame, label_name, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        out.write(frame)
        frame_id += 1

    # Libérer les ressources
    cap.release()
    out.release()
    print("Vidéo annotée sauvegardée à :", output_path)

# Chemins des fichiers
video_path = '/Users/Huandong/Desktop/CV-Project/STOP.mp4'
annotations_dir = '/Users/Huandong/Desktop/CV-Project/STOP_labels_sort_filtered_mode'
labels_path = '/Users/Huandong/Desktop/CV-Project/dataset_clean/labels_list.txt'
output_path = '/Users/Huandong/Desktop/STOP_0.5_Sort_Filtered_Mode.mp4'

# Exécuter la fonction
annotate_video(video_path, annotations_dir, labels_path, output_path)