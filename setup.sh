git clone https://github.com/SkalskiP/yolov9.git 

mkdir -p ./weights

# Step 3: Download the pre-trained model weights into the 'weights' directory
wget -P ./weights -q https://github.com/WongKinYiu/yolov9/releases/download/v0.1/yolov9-c.pt
wget -P ./weights -q https://github.com/WongKinYiu/yolov9/releases/download/v0.1/yolov9-e.pt
wget -P ./weights -q https://github.com/WongKinYiu/yolov9/releases/download/v0.1/gelan-c.pt
wget -P ./weights -q https://github.com/WongKinYiu/yolov9/releases/download/v0.1/gelan-e.pt
