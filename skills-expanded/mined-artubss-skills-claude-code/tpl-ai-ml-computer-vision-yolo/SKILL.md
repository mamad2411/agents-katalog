---
name: tpl-ai-ml-computer-vision-yolo
description: Template do pack (ai-ml/10-computer-vision-yolo.md). Orienta o agente em integracao de IA/ML, LLM e pipelines de dados alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: ai-ml/10-computer-vision-yolo.md
  generated_by: install_pack_templates_as_claude_skills
---

# PROJECT: Computer Vision with YOLOv8/v9 + FastAPI + ByteTrack

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `ai-ml/10-computer-vision-yolo.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## STACK
- **Detection:** Ultralytics YOLOv8/v9 (ultralytics >= 8.1)
- **Tracking:** ByteTrack (via ultralytics built-in)
- **Language:** Python 3.12
- **Video Processing:** OpenCV 4.9+
- **API:** FastAPI + WebSocket (real-time) + REST (batch)
- **GPU:** CUDA 12.1 + TensorRT 8.6 (inference optimization)
- **Export:** ONNX (CPU), TensorRT (NVIDIA GPU), CoreML (Apple)

---

## PROJECT STRUCTURE
```
yolo-api/
├── app/
│   ├── main.py               # FastAPI app
│   ├── detector.py           # YOLO detector singleton
│   ├── tracker.py            # ByteTrack wrapper
│   ├── routes/
│   │   ├── detect.py         # POST /v1/detect
│   │   ├── track.py          # POST /v1/track (video)
│   │   └── websocket.py      # WS /v1/stream
│   └── schemas.py            # Pydantic request/response
├── training/
│   ├── train.py              # Training script
│   ├── validate.py           # Evaluation metrics
│   └── datasets/             # YOLO format datasets
├── models/
│   ├── yolov8n.pt            # Nano (fastest)
│   ├── yolov8m.pt            # Medium (balanced)
│   └── yolov9c.pt            # YOLOv9 custom
├── export/
│   ├── export_onnx.py
│   └── export_tensorrt.py
├── tests/
│   └── test_detector.py
└── Dockerfile.gpu
```

---

## ARCHITECTURE RULES
1. **Model loads at startup** — YOLOv8 model loads once; never reload per request (warmup takes 2-5s).
2. **GPU inference exclusively** — CPU fallback only for dev/testing; production always GPU + CUDA.
3. **Confidence threshold ≥ 0.4** — never use default 0.25 in production; tune per class.
4. **NMS IOU threshold = 0.45** — default Ultralytics setting; only change with data evidence.
5. **TensorRT in production** — convert to `.engine` for 2-5x speedup; ONNX for portability.
6. **Batch size = 1 for REST API, 4-8 for video processing** — streaming APIs always batch_size=1.
7. **Dataset follows YOLO format strictly** — never convert mid-experiment; commit yaml + images together.
8. **Evaluation metrics before deploy** — mAP50 > 0.7 AND mAP50-95 > 0.5 minimum quality gate.

---

## DATASET STRUCTURE (YOLO FORMAT)

```
datasets/
└── my_dataset/
    ├── dataset.yaml         # Dataset config
    ├── images/
    │   ├── train/           # 70% of data
    │   │   ├── img001.jpg
    │   │   └── ...
    │   ├── val/             # 20% of data
    │   └── test/            # 10% of data
    └── labels/
        ├── train/
        │   ├── img001.txt   # One file per image
        │   └── ...
        ├── val/
        └── test/
```

```yaml
# datasets/my_dataset/dataset.yaml
path: /data/my_dataset    # Absolute path
train: images/train
val:   images/val
test:  images/test

nc: 3           # Number of classes
names:
  0: person
  1: car
  2: truck

# Label format (in each .txt file):
# class_id cx cy width height   (all normalized 0-1)
# 0 0.5 0.5 0.3 0.8
```

---

## TRAINING CONFIG + SCRIPT

```python
# training/train.py
from ultralytics import YOLO
import mlflow
import os

def train(
    model_size: str = "n",    # n, s, m, l, x
    epochs: int = 100,
    imgsz: int = 640,
    batch: int = 16,
    dataset_yaml: str = "datasets/my_dataset/dataset.yaml",
):
    mlflow.set_experiment("yolo-detection")
    run_name = f"yolov8{model_size}_{epochs}ep_{imgsz}px"

    model = YOLO(f"yolov8{model_size}.pt")   # Load pretrained weights

    results = model.train(
        data=dataset_yaml,
        epochs=epochs,
        imgsz=imgsz,
        batch=batch,
        device=0,              # GPU 0; multi-GPU: [0, 1]
        patience=20,           # Early stopping

        # Optimizer
        optimizer="AdamW",
        lr0=0.001,
        lrf=0.01,              # Final LR = lr0 * lrf
        momentum=0.937,
        weight_decay=0.0005,

        # Augmentation (tune per dataset)
        hsv_h=0.015,           # Hue variation
        hsv_s=0.7,
        hsv_v=0.4,
        flipud=0.0,
        fliplr=0.5,
        mosaic=1.0,            # Mosaic augmentation (crucial for small objects)
        mixup=0.0,             # Disable for simple datasets
        copy_paste=0.0,        # For instance segmentation

        # Logging
        project="runs/train",
        name=run_name,
        save=True,
        save_period=10,        # Save checkpoint every 10 epochs
        plots=True,
    )

    # Log to MLflow
    with mlflow.start_run(run_name=run_name):
        mlflow.log_params({
            "model": f"yolov8{model_size}",
            "epochs": epochs, "imgsz": imgsz, "batch": batch,
        })
        mlflow.log_metrics({
            "mAP50":    results.results_dict["metrics/mAP50(B)"],
            "mAP50-95": results.results_dict["metrics/mAP50-95(B)"],
            "precision": results.results_dict["metrics/precision(B)"],
            "recall":   results.results_dict["metrics/recall(B)"],
        })
        mlflow.log_artifact(str(results.save_dir / "weights/best.pt"))

    return results

# DATA AUGMENTATION RULES:
# Small objects (< 32px): increase mosaic=1.0, imgsz=1280
# Dense scenes: copy_paste=0.5 helps
# Medical/satellite: reduce augmentation (flipud=0.5, less color)
# Night/thermal: hsv_h=0, hsv_s=0 (no color aug)
```

---

## VALIDATION + METRICS

```python
# training/validate.py
from ultralytics import YOLO

QUALITY_GATES = {
    "mAP50":    0.70,    # Mean Average Precision at IoU=0.5
    "mAP50-95": 0.50,    # Strict metric (COCO standard)
    "precision": 0.75,
    "recall":   0.65,
}

# IoU thresholds:
# 0.5  = "good enough" — standard for most applications
# 0.75 = "strict" — precise localization required
# 0.5-0.95 (COCO) = gold standard for benchmarking

def validate_model(weights_path: str, dataset_yaml: str) -> dict:
    model = YOLO(weights_path)
    metrics = model.val(data=dataset_yaml, imgsz=640, conf=0.001, iou=0.7)

    results = {
        "mAP50":     metrics.box.map50,
        "mAP50-95":  metrics.box.map,
        "precision": metrics.box.mp,
        "recall":    metrics.box.mr,
        "per_class": {
            model.names[i]: {"ap50": ap}
            for i, ap in enumerate(metrics.box.ap50)
        }
    }

    # Quality gate check
    failures = [
        f"{k}: {v:.3f} < {QUALITY_GATES[k]}"
        for k, v in results.items()
        if k in QUALITY_GATES and v < QUALITY_GATES[k]
    ]
    if failures:
        raise ValueError(f"Quality gates failed:\n" + "\n".join(failures))

    return results
```

---

## MODEL LOADING SINGLETON

```python
# app/detector.py
from ultralytics import YOLO
from ultralytics.engine.results import Results
import torch
import numpy as np
from pathlib import Path

class YOLODetector:
    _instance: "YOLODetector | None" = None
    _model: YOLO | None = None

    @classmethod
    def get_instance(cls) -> "YOLODetector":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def load(
        self,
        weights: str = "models/best.pt",
        device: str = "0",   # "0" = GPU 0, "cpu" = CPU
        half: bool = True,   # FP16 on GPU for 2x throughput
    ) -> None:
        self._model = YOLO(weights)
        self._model.to(device)
        if half and torch.cuda.is_available():
            self._model.model.half()

        # Warmup: run dummy inference to JIT-compile
        dummy = np.zeros((640, 640, 3), dtype=np.uint8)
        self._model(dummy, verbose=False)
        print(f"Model loaded and warmed up. Device: {device}")

    def detect(
        self,
        image: np.ndarray,
        conf: float = 0.4,
        iou: float = 0.45,
        classes: list[int] | None = None,
        max_det: int = 300,
    ) -> Results:
        if self._model is None:
            raise RuntimeError("Model not loaded. Call load() first.")

        with torch.inference_mode():
            results = self._model(
                image,
                conf=conf,
                iou=iou,
                classes=classes,
                max_det=max_det,
                verbose=False,
            )
        return results[0]
```

---

## FASTAPI DETECT ENDPOINT

```python
# app/routes/detect.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.detector import YOLODetector
from app.schemas import DetectionResponse, Detection
import numpy as np
import cv2

router = APIRouter(prefix="/v1")

@router.post("/detect", response_model=DetectionResponse)
async def detect_objects(
    file: UploadFile = File(...),
    conf: float = 0.4,
    classes: str | None = None,    # "0,1,2" CSV of class IDs
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=422, detail="File must be an image")

    content = await file.read()
    nparr = np.frombuffer(content, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if image is None:
        raise HTTPException(status_code=422, detail="Could not decode image")

    class_filter = [int(c) for c in classes.split(",")] if classes else None
    detector = YOLODetector.get_instance()
    results = detector.detect(image, conf=conf, classes=class_filter)

    detections = []
    for box in results.boxes:
        detections.append(Detection(
            class_id=int(box.cls),
            class_name=results.names[int(box.cls)],
            confidence=float(box.conf),
            bbox_xyxy=[float(x) for x in box.xyxy[0].tolist()],
        ))

    return DetectionResponse(
        image_shape={"width": image.shape[1], "height": image.shape[0]},
        detections=detections,
        inference_time_ms=results.speed["inference"],
    )
```

---

## TENSORRT EXPORT + BENCHMARK

```python
# export/export_tensorrt.py
from ultralytics import YOLO
import time
import numpy as np

def export_tensorrt(weights: str = "models/best.pt"):
    model = YOLO(weights)

    # Export to TensorRT engine
    model.export(
        format="engine",
        device=0,
        half=True,          # FP16
        imgsz=640,
        workspace=4,        # GB for TRT workspace
        simplify=True,
        dynamic=False,      # Static shape: faster; True: variable input size
    )
    print("Exported to models/best.engine")

def benchmark():
    """Compare PyTorch vs ONNX vs TensorRT speed."""
    dummy = np.random.randint(0, 255, (640, 640, 3), dtype=np.uint8)
    N = 100

    for fmt, path in [("pytorch", "models/best.pt"),
                       ("onnx",    "models/best.onnx"),
                       ("tensorrt","models/best.engine")]:
        model = YOLO(path)
        model(dummy, verbose=False)   # Warmup

        t0 = time.perf_counter()
        for _ in range(N):
            model(dummy, verbose=False)
        elapsed = (time.perf_counter() - t0) / N * 1000

        print(f"{fmt:10}: {elapsed:.1f} ms/image | {1000/elapsed:.0f} FPS")

# Typical on RTX 3090 (640px, FP16):
# pytorch:   8.5 ms  → 117 FPS
# onnx:      6.2 ms  → 161 FPS
# tensorrt:  3.1 ms  → 322 FPS
```

---

## BYTETRACK OBJECT TRACKING

```python
# app/tracker.py
from ultralytics import YOLO
import cv2

def track_video(video_path: str, output_path: str, weights: str = "models/best.pt"):
    model = YOLO(weights)

    results = model.track(
        source=video_path,
        save=True,
        project="runs/track",
        tracker="bytetrack.yaml",  # Built into ultralytics
        conf=0.4,
        iou=0.5,
        persist=True,          # Persist tracking state between frames
        stream=True,           # Memory-efficient for long videos
    )

    for frame_result in results:
        if frame_result.boxes.id is None:
            continue  # No tracked objects in this frame

        for i, box in enumerate(frame_result.boxes):
            track_id   = int(box.id)
            class_id   = int(box.cls)
            confidence = float(box.conf)
            x1, y1, x2, y2 = [int(v) for v in box.xyxy[0].tolist()]

            # Process: log, count unique IDs, trigger events
            print(f"Frame: track_id={track_id}, class={class_id}, conf={confidence:.2f}")
```

---

## DOCKERFILE (GPU)

```dockerfile
FROM nvcr.io/nvidia/pytorch:24.01-py3 AS base
WORKDIR /app

# OpenCV dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Pre-download model weights (baked into image for fast cold start)
RUN python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"

ENV PYTHONUNBUFFERED=1 PORT=8000
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]

# Note: Use --workers=1 with GPU. Multiple workers fight over GPU memory.
# Scale horizontally (multiple containers) instead of multiple workers.
```
