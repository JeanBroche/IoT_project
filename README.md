# Les pieds
J'aime beaucoup les pieds (mes pieds sont connectés en ZigBee)

# Requirements
- Python 3.14+
- Redis 8.6+

# Computer vision model

Using openCV and a pre-trained model to detect people in images.

Used model : YoloV5s for object detection, because it's small and fast, adatpted for raspberry pi (2 Go).

### Install :

```bash
# Cloner YOLOv5
git clone https://github.com/ultralytics/yolov5.git
cd yolov5

# Installer dépendances
pip install -r requirements.txt

# Télécharger le modèle léger
python detect.py --weights yolov5s.pt --img 320 --save-txt --source data/images/

# Exporter en ONNX
python export.py --weights yolov5s.pt --img 320 --batch 1 --device cpu --include onnx --opset 11
```