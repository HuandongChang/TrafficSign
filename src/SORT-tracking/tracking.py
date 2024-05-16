import numpy as np
import os
from sort.sort import Sort




import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Get Input & Output Files")
    parser.add_argument('--input_dir', type=str, required=True, help='Input directory path')
    parser.add_argument('--file_prefix', type=str, required=True, help='YOLO Predictions Txt File Prefix')
    parser.add_argument('--max_frames', type=int, required=True, help='Max Frames of the Video')
    # parser.add_argument('--output_dir', type=str, required=True, help='Output directory path')
    return parser.parse_args()

args = parse_args()
input_dir = args.input_dir
prefix = args.file_prefix
max_frames = args.max_frames
# output_dir = args.output_dir
output_dir = '../Data/labels_sort'    # Output directory to save modified detection files





# Initialize SORT tracker
tracker = Sort()

# Specify the directories
# input_dir = '/Users/Huandong/Desktop/CV-Project/STOP_labels'  # Input directory containing YOLO format detections
# output_dir = '/Users/Huandong/Desktop/CV-Project/STOP_labels_sort'    # Output directory to save modified detection files

def convert_yolo_to_sort(yolo_boxes):
    # YOLO format: [x_center, y_center, width, height]
    # SORT format: [x1, y1, x2, y2]
    sort_boxes = np.zeros_like(yolo_boxes)
    sort_boxes[:, 0] = yolo_boxes[:, 0] - (yolo_boxes[:, 2] / 2)  # x1 = x_center - width/2
    sort_boxes[:, 1] = yolo_boxes[:, 1] - (yolo_boxes[:, 3] / 2)  # y1 = y_center - height/2
    sort_boxes[:, 2] = yolo_boxes[:, 0] + (yolo_boxes[:, 2] / 2)  # x2 = x_center + width/2
    sort_boxes[:, 3] = yolo_boxes[:, 1] + (yolo_boxes[:, 3] / 2)  # y2 = y_center + height/2
    return sort_boxes

def convert_sort_to_yolo(sort_boxes):
    # SORT format: [x1, y1, x2, y2]
    # YOLO format: [x_center, y_center, width, height]
    yolo_boxes = np.zeros((sort_boxes.shape[0], 4))
    yolo_boxes[:, 0] = (sort_boxes[:, 0] + sort_boxes[:, 2]) / 2  # x_center
    yolo_boxes[:, 1] = (sort_boxes[:, 1] + sort_boxes[:, 3]) / 2  # y_center
    yolo_boxes[:, 2] = sort_boxes[:, 2] - sort_boxes[:, 0]  # width
    yolo_boxes[:, 3] = sort_boxes[:, 3] - sort_boxes[:, 1]  # height
    return yolo_boxes

if not os.path.exists(output_dir):
    os.makedirs(output_dir)




# # Process each detection file
# for filename in sorted(os.listdir(input_dir)):
#     filepath = os.path.join(input_dir, filename)
#     if filename.endswith('.txt'):
#         # Read detections from file
#         data = np.loadtxt(filepath, dtype=float, delimiter=' ')
        
#         # Check for empty detections
#         if data.size == 0:
#             continue
        
#         # Ensure data is two-dimensional
#         if data.ndim == 1:
#             data = np.expand_dims(data, axis=0)
        

#         converted_detections = convert_yolo_to_sort(data[:, 1:5], img_width=1920, img_height=1080)  
#         scores = data[:, 5:6]  # confidence scores
        
#         # Combine for SORT
#         detections = np.hstack((converted_detections, scores))


# max_frames = 900
# Process frames from 0 to max_frames
for frame_number in range(max_frames):
    filename = f"{prefix}_{frame_number}.txt"
    filepath = os.path.join(input_dir, filename)
    if os.path.exists(filepath):
        data = np.loadtxt(filepath, dtype=float, delimiter=' ')
        
        if data.size == 0:
            detections = np.empty((0, 5))
        else:
            if data.ndim == 1:
                data = np.expand_dims(data, axis=0)
            
            detections = convert_yolo_to_sort(data[:, 1:5])
            scores = data[:, 5:6]
            detections = np.hstack((detections, scores))
    else:
        detections = np.empty((0, 5))

        
        # Update SORT tracker with new detections
    tracked = tracker.update(detections)

    if tracked.size == 0:
        print(f"No objects tracked in {filename}, skipping.")
        continue
        
    if tracked.ndim == 1:
        tracked = np.expand_dims(tracked, axis=0)
        
    # Check that the number of detections matches the number of tracks
    if data.shape[0] != tracked.shape[0]:
        print(f"Mismatch in number of detections and tracks in {filename}, skipping.")
        continue
        
        # Prepare output with original class, tracked results, and object ID
        # Output format: [class, x, y, width, height, confidence, object_id]
    tracked_yolo_format = convert_sort_to_yolo(tracked[:, :4])
    output = np.hstack((data[:, 0:1], tracked_yolo_format, data[:, 5:6], tracked[:, 4:5]))

        # print("Output shape:", data[:, 0:1].shape, tracked[:, :4].shape, data[:, 5:6].shape, tracked[:, 4:5].shape)
        # print("Output sample:", output[0])
        
        # Save the new detections with object IDs
    np.savetxt(os.path.join(output_dir, f"{frame_number}.txt"), output, fmt='%d %f %f %f %f %f %d')

print("Tracking complete. Results saved to:", output_dir)