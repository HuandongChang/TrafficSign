exp 5:

python train.py \
--batch 16 --epochs 300 --img 640 --device 0 --min-items 0 --close-mosaic 200 \
--data ../data33.yaml \
--weights ../weights/gelan-c.pt \
--cfg models/detect/gelan-c.yaml \
--hyp hyp.scratch-high.yaml \
--optimizer AdamW \
--patience 50

Data: 33 labels, no missing data, small bounding boxes removed. (dataset_clean)



exp4:

python train.py \
--batch 8 --epochs 300 --img 1280 --device 0 --min-items 0 --close-mosaic 280 \
--data ../data50.yaml \
--weights ../weights/gelan-c.pt \
--cfg models/detect/gelan-c.yaml \
--hyp hyp.scratch-high.yaml \
--optimizer AdamW \
--patience 50

Data: 50 labels, with missing data, all small bounding boxes are kept. (dataset_all)




exp3:
Training: 150 epochs, only use 5 mosaic, img still 640.
Data: 50 labels, with missing data, all small bounding boxes are kept. (dataset_all)