---
name: computer-vision-warehouse
description: When the user wants to apply computer vision in warehouses, detect defects, track packages, count inventory, or automate visual inspection. Also use when the user mentions "computer vision," "image recognition," "object detection," "barcode reading," "package tracking," "quality inspection," "YOLO," "RCNN," "image classification," or "warehouse automation with vision." For general ML, see ml-supply-chain.
---

# Computer Vision for Warehouse Operations

You are an expert in applying computer vision to warehouse and supply chain operations. Your goal is to implement object detection, classification, tracking, and inspection systems using CNNs, YOLO, and other vision models.

## Applications

1. **Package Detection & Tracking**: YOLO, tracking algorithms
2. **Quality Inspection**: CNN classification, defect detection
3. **Inventory Counting**: Object counting, OCR
4. **Barcode/QR Reading**: Traditional + ML methods
5. **Safety Monitoring**: Person detection, PPE detection

---

## YOLO for Package Detection

```python
import cv2
from ultralytics import YOLO

class PackageDetector:
    """
    Real-time package detection using YOLO
    """
    
    def __init__(self, model_path='yolov8n.pt'):
        self.model = YOLO(model_path)
    
    def detect_packages(self, image_path):
        """Detect packages in warehouse image"""
        
        results = self.model(image_path)
        
        detections = []
        for result in results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                confidence = box.conf[0]
                class_id = box.cls[0]
                
                detections.append({
                    'bbox': (x1, y1, x2, y2),
                    'confidence': confidence,
                    'class': class_id
                })
        
        return detections
```

---

## CNN for Quality Inspection

```python
from tensorflow import keras
from tensorflow.keras import layers

class QualityInspector:
    """
    CNN for defect detection
    """
    
    def build_model(self, image_size=(224, 224), num_classes=2):
        model = keras.Sequential([
            layers.Conv2D(32, 3, activation='relu',
                         input_shape=(*image_size, 3)),
            layers.MaxPooling2D(2),
            layers.Conv2D(64, 3, activation='relu'),
            layers.MaxPooling2D(2),
            layers.Conv2D(128, 3, activation='relu'),
            layers.MaxPooling2D(2),
            layers.Flatten(),
            layers.Dense(256, activation='relu'),
            layers.Dropout(0.5),
            layers.Dense(num_classes, activation='softmax')
        ])
        
        model.compile(optimizer='adam',
                     loss='categorical_crossentropy',
                     metrics=['accuracy'])
        
        return model
```

---

## Object Tracking

```python
from sort import Sort

class PackageTracker:
    """
    Multi-object tracking for packages
    """
    
    def __init__(self):
        self.tracker = Sort()
        self.package_trajectories = {}
    
    def track(self, detections, frame_id):
        """
        Track packages across frames
        """
        
        # Convert detections to format for tracker
        dets = np.array([[d['bbox'][0], d['bbox'][1],
                         d['bbox'][2], d['bbox'][3],
                         d['confidence']] for d in detections])
        
        # Update tracker
        tracked_objects = self.tracker.update(dets)
        
        # Store trajectories
        for obj in tracked_objects:
            obj_id = int(obj[4])
            bbox = obj[:4]
            
            if obj_id not in self.package_trajectories:
                self.package_trajectories[obj_id] = []
            
            self.package_trajectories[obj_id].append({
                'frame': frame_id,
                'bbox': bbox
            })
```

---

## Tools & Libraries

- `OpenCV`: image processing
- `YOLOv8`: object detection
- `TensorFlow/PyTorch`: deep learning
- `Roboflow`: dataset management
- `Detectron2`: Facebook detection

---

## Related Skills

- **ml-supply-chain**: general ML
- **warehouse-automation**: automation systems
- **quality-management**: inspection processes
