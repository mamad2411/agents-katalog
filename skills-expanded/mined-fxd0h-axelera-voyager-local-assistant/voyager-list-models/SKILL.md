---
name: voyager-list-models
description: List and search models in the Voyager SDK model zoo for Axelera AI hardware. Use when the user wants to find available models by task, framework, or dataset.
argument-hint: "[search criteria]"
allowed-tools: Read, Bash, Glob, Grep, mcp__voyager__*
---

# List Available Models

List and search models in the Voyager SDK model zoo for Axelera AI hardware

## Important Context

Do not call a model deployable or validated until SDK evidence and runtime
artifacts show that status.

## Instructions

List models based on the specified criteria: **$ARGUMENTS**

### Step 0: Data Source & Environment Selection

{{INCLUDE common/voyager-sdk-setup.md}}

### Step 0.5: Axelera Voyager Project & Task Integration

{{INCLUDE common/voyager-task-integration.md}}

### Step 1: List All Models

```bash
# Show all available models
./deploy.py --help

# Or use make (help is the default target; prints per-model help)
make help
```

Classify each result as:

- `listed`: YAML or deploy help entry exists
- `payload-present`: compiled payload exists under `build/<model>/`
- `downloadable`: `axdownloadmodel <model>` succeeds and payload exists
- `metis-validated`: `inference.py` ran on visible Metis hardware and produced output

### Step 2: Search by Task Type

Search models by their primary task:

**Object Detection:**

```bash
# YOLO models
ls ax_models/zoo/yolo/object_detection/

# Oriented bounding boxes (OBB)
ls ax_models/zoo/yolo/obb_detection/

# SSD models
ls ax_models/zoo/tensorflow/object_detection/

# RetinaFace (face detection)
ls ax_models/zoo/torch/ | grep -i retinaface
```

**Classification:**

```bash
# TorchVision classifiers
ls ax_models/zoo/torchvision/classification/

# Timm models
ls ax_models/zoo/timm/
```

**Segmentation:**

```bash
# Instance segmentation (YOLO-based)
ls ax_models/zoo/yolo/instance_segmentation/

# Semantic segmentation
ls ax_models/zoo/mmlab/mmseg/
ls ax_models/zoo/yolo/semantic_segmentation/
```

**Pose Estimation:**

```bash
# Pose models (YOLO-based keypoint detection)
ls ax_models/zoo/yolo/keypoint_detection/
```

**Depth Estimation:**

```bash
ls ax_models/zoo/torch/ | grep -i depth
```

**LLM/Language Models:**

```bash
ls ax_models/zoo/llm/
ls ax_models/llm/
```

### Step 3: Search by Framework

The zoo YAMLs declare their framework via the `class:` key (there is no
`source:` key). Search by model class:

```bash
# ONNX models
find ax_models/zoo -name "*-onnx.yaml"

# Timm models
find ax_models/zoo -name "*.yaml" | xargs grep -l "class: AxTimmModel"

# Ultralytics models
find ax_models/zoo -name "*.yaml" | xargs grep -l "class: AxUltralyticsYOLO"

# Darknet YOLO models (v1.7.0 adds yolov4 variants)
find ax_models/zoo -name "*.yaml" | xargs grep -l "class: AxYoloDarknet"

# TorchVision models
ls ax_models/zoo/torchvision/
```

### Step 4: Search by Dataset

```bash
# COCO trained models
find ax_models -name "*coco*.yaml"

# ImageNet trained models
find ax_models -name "*imagenet*.yaml"

# Custom/other datasets
find ax_models -name "*widerface*.yaml"
find ax_models -name "*lfw*.yaml"
```

### Step 5: Reference Pipelines

```bash
# Cascade pipelines (multi-model)
ls ax_models/reference/cascade/

# Parallel pipelines
ls ax_models/reference/parallel/

# With tracker
ls ax_models/reference/cascade/with_tracker/

# Image preprocessing pipelines
ls ax_models/reference/image_preprocess/
```

### Step 6: Model Information

Get details about a specific model:

```bash
# View the model YAML directly
cat ax_models/zoo/yolo/object_detection/yolov8n-coco.yaml

# Print per-model help for the whole zoo (default make target)
make help
```

### Step 7: List by Model Size/Speed

YOLO model variants (speed vs accuracy), using the YOLO11 family as an
example; zoo YOLOv5/YOLOv8 builds stop at the `l` size:

```
| Model    | Size  | Speed | Accuracy |
|----------|-------|-------|----------|
| yolo11n  | nano  | fast  | lower    |
| yolo11s  | small | fast  | good     |
| yolo11m  | medium| med   | better   |
| yolo11l  | large | slow  | high     |
| yolo11x  | xlarge| slow  | highest  |
```

### Step 8: Tutorial Models

```bash
# General tutorials
ls ax_models/tutorials/general/

# YOLO tutorials
ls ax_models/tutorials/yolo/

# Custom training tutorials
ls ax_models/tutorials/torch/
ls ax_models/tutorials/onnx/
```

### Step 9: Custom Search

```bash
# Find all detection models
find ax_models -name "*.yaml" -exec grep -l "decodeyolo\\|ssd\\|retinaface" {} \;

# Find models with specific input size
find ax_models -name "*.yaml" -exec grep -l "640, 640" {} \;

# Find models with tracker support
find ax_models -name "*tracker*.yaml"
```

### Step 10: Model Categories Summary

```
Detection (COCO unless noted):
- yolov5n/s/m/l-v7-coco          YOLOv5 v7 (also yolov5s-v5, yolov5s-relu)
- yolov7-coco, yolov7-tiny-coco, yolov7-640x480-coco
- yolov8n/s/m/l-coco             YOLOv8 variants
- yolov9t/s/m/c-coco-onnx        YOLOv9 (plus gelan-s/m/c-coco-onnx)
- yolov10n/s/b-coco-onnx         YOLOv10 variants
- yolo11n/s/m/l/x-coco-onnx      YOLO11 family
- yolo26n/s/m/l/x-coco-onnx      YOLO26 family
- yolov3-coco-onnx               YOLOv3
- yolov4-416-coco, yolov4-csp-leaky-coco   Darknet YOLOv4 (new in 1.7)
- yolox-s/m-coco-onnx, yolox-x-crowdhuman-onnx
- yolonas-s/m/l-coco-onnx        YOLO-NAS
- ssd-mobilenetv1/v2-coco-poc-onnx
- retinaface-*                   Face detection (WiderFace)

Oriented bounding boxes (DOTAv1):
- yolov8n/l-obb-dotav1-onnx
- yolo11n/l-obb-dotav1-onnx
- yolo26n/s/m/l/x-obb-dotav1-onnx

Classification (ImageNet):
- resnet18/34/50/101/152-imagenet (plus resnet10t via timm)
- efficientnet_b0..b4-imagenet
- mobilenetv2-imagenet, mobilenetv3_small/large-imagenet
- mobilenetv4_small/medium/large/aa_large-imagenet (timm)
- densenet121, squeezenet1.0/1.1, inception_v3, regnet_x/y,
  resnext50_32x4d, wide_resnet50

Pose (COCO keypoints):
- yolov8n/s/m/lpose-coco
- yolo11n/lpose-coco-onnx
- yolo26n/s/m/l/xpose-coco-onnx

Instance segmentation (COCO):
- yolov8n/s/m/lseg-coco
- yolo11n/lseg-coco-onnx
- yolo26n/s/m/l/xseg-coco-onnx

Semantic segmentation (Cityscapes):
- unet_fcn_256/512-cityscapes
- yolo26n/s/m/l/xsem-cityscapes-onnx

Depth:
- fastdepth-nyudepthv2-onnx      Monocular depth

Face:
- facenet-lfw                    Face recognition
- retinaface-*                   Face detection

Re-identification and other:
- osnet-x1-0-market1501-onnx, sbs-s50-market1501-onnx   Re-ID
- lprnet                         License plate recognition
- real-esrgan-x4plus-onnx        Super resolution

LLM:
- llama-3-1-8b / llama-3-2-1b / llama-3-2-3b (1024-4core-static)
- phi3-mini-512-static, phi3-mini-1024/2048-4core-static
- velvet-2b-1024-4core-static
```

Treat this table as illustrative only. Verify exact model names against
`./deploy.py --help`, `ax_models/**/*.yaml`, or Voyager SDK RAG before
recommending them.

### Step 11: Check Model Availability

```bash
# Verify model is listed
./deploy.py --help | grep -F "<model-name>"

# Verify YAML exists
find ax_models -name "<model-name>.yaml" -o -name "*<model-name>*.yaml"

# Verify compiled or downloaded payload
find build/<model-name> -type f \( -name "*.axnet" -o -name "model.json" \) -print
```

Availability is not hardware validation. Only label a model validated after
a bounded `inference.py` run on a probed Metis host succeeds and produces an
output artifact.
