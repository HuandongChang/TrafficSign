cd yolov9
python train.py \
--batch 8 --epochs 20 --img 1280 --device 0 --min-items 0 --close-mosaic 15 \
--data ../data50.yaml \
--weights ../weights/gelan-c.pt \
--cfg models/detect/gelan-c.yaml \
--hyp hyp.scratch-high.yaml \
--optimizer Adam

cd ..