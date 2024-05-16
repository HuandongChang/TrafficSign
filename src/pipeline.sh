## SORT
INPUT_DIR="/Users/Huandong/Desktop/CV-Project/repo/Data/labels"
FILE_PREFIX="Cambridge"
FOLDER_PREFIX="Cambridge_Testing"
MAX_FRAMES=6000


python SORT-tracking/tracking.py \
--input_dir "$INPUT_DIR" \
--file_prefix "$FILE_PREFIX" \
--max_frames $MAX_FRAMES && \
python SORT-tracking/filter_ID.py && \
python SORT-tracking/prediction_mode.py  \
--folder_prefix "$FOLDER_PREFIX" && \

rm -r '../Data/labels_sort' && \
rm -r '../Data/labels_sort_filtered'

# Check if the last command was successful
if [ $? -eq 0 ]; then
    echo "All scripts executed successfully."
else
    echo "An error occurred in one of the scripts."
    exit 1
fi
