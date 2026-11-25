---
name: segment-anything-model
description: "SAM: zero-shot image segmentation via points, boxes, masks."
version: 1.0.0
author: Orchestra Research
license: MIT
dependencies: [segment-anything, transformers>=4.30.0, torch>=1.7.0]
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Multimodal, Image Segmentation, Computer Vision, SAM, Zero-Shot]

---

# Segment Anything Model（SAM）

关于如何使用 Meta AI 的 Segment Anything Model 进行零样本图像分割的完整指南。

## 何时使用 SAM

**以下情况可使用 SAM：**
- 需要在无需针对特定任务进行训练的情况下对图像中的任意对象进行分割
- 构建基于点提示/边界框提示的交互式标注工具
- 为其他视觉模型生成训练数据
- 需要实现向新图像领域的零样本迁移
- 构建物体检测/分割流程
- 处理医疗、卫星或特定领域的图像

**核心特性：**
- **零样本分割**：无需微调即可处理任何图像领域的数据
- **灵活的提示方式**：支持点、边界框或先前的掩码作为输入
- **自动分割**：可自动生成所有物体的掩码
- **高精度**：基于来自 1100 万张图像的 11 亿个掩码进行训练
- **多种模型尺寸**：ViT-B（速度最快）、ViT-L、ViT-H（精度最高）
- **ONNX 导出功能**：可在浏览器和边缘设备上部署

**可选择的其他方案：**
- **YOLO/Detectron2**：用于带类别标签的实时物体检测
- **Mask2Former**：用于带分类信息的语义/全景分割
- **GroundingDINO + SAM**：用于基于文本提示的分割
- **SAM 2**：用于视频分割任务

## 快速入门

### 安装

```bash
# From GitHub
pip install git+https://github.com/facebookresearch/segment-anything.git

# Optional dependencies
pip install opencv-python pycocotools matplotlib

# Or use HuggingFace transformers
pip install transformers
```

### 下载检查点

```bash
# ViT-H (largest, most accurate) - 2.4GB
wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth

# ViT-L (medium) - 1.2GB
wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_l_0b3195.pth

# ViT-B (smallest, fastest) - 375MB
wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth
```

### SamPredictor 的基本使用方法

```python
import numpy as np
from segment_anything import sam_model_registry, SamPredictor

# Load model
sam = sam_model_registry["vit_h"](checkpoint="sam_vit_h_4b8939.pth")
sam.to(device="cuda")

# Create predictor
predictor = SamPredictor(sam)

# Set image (computes embeddings once)
image = cv2.imread("image.jpg")
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
predictor.set_image(image)

# Predict with point prompts
input_point = np.array([[500, 375]])  # (x, y) coordinates
input_label = np.array([1])  # 1 = foreground, 0 = background

masks, scores, logits = predictor.predict(
    point_coords=input_point,
    point_labels=input_label,
    multimask_output=True  # Returns 3 mask options
)

# Select best mask
best_mask = masks[np.argmax(scores)]
```

### HuggingFace Transformers

```python
import torch
from PIL import Image
from transformers import SamModel, SamProcessor

# Load model and processor
model = SamModel.from_pretrained("facebook/sam-vit-huge")
processor = SamProcessor.from_pretrained("facebook/sam-vit-huge")
model.to("cuda")

# Process image with point prompt
image = Image.open("image.jpg")
input_points = [[[450, 600]]]  # Batch of points

inputs = processor(image, input_points=input_points, return_tensors="pt")
inputs = {k: v.to("cuda") for k, v in inputs.items()}

# Generate masks
with torch.no_grad():
    outputs = model(**inputs)

# Post-process masks to original size
masks = processor.image_processor.post_process_masks(
    outputs.pred_masks.cpu(),
    inputs["original_sizes"].cpu(),
    inputs["reshaped_input_sizes"].cpu()
)
```

## 核心概念

### 模型架构

<!-- ascii-guard-ignore -->
```
SAM Architecture:
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Image Encoder  │────▶│ Prompt Encoder  │────▶│  Mask Decoder   │
│     (ViT)       │     │ (Points/Boxes)  │     │ (Transformer)   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                       │                       │
   Image Embeddings      Prompt Embeddings         Masks + IoU
   (computed once)       (per prompt)             predictions
```
### 模型版本

| 模型 | 检查点文件 | 大小 | 速度 | 准确率 |
|-------|------------|------|-------|----------|
| ViT-H | `vit_h` | 2.4 GB | 最慢 | 最高 |
| ViT-L | `vit_l` | 1.2 GB | 中等 | 良好 |
| ViT-B | `vit_b` | 375 MB | 最快 | 良好 |

### 提示词类型

| 提示词类型 | 描述 | 使用场景 |
|----------|------|----------|
| 点（前景） | 点击物体 | 单个物体选择 |
| 点（背景） | 点击物体外部 | 排除特定区域 |
| 边界框 | 围绕物体的矩形 | 较大的物体 |
| 之前的掩码 | 低分辨率掩码输入 | 迭代优化 |

## 交互式分割

### 点提示词

```python
# Single foreground point
input_point = np.array([[500, 375]])
input_label = np.array([1])

masks, scores, logits = predictor.predict(
    point_coords=input_point,
    point_labels=input_label,
    multimask_output=True
)

# Multiple points (foreground + background)
input_points = np.array([[500, 375], [600, 400], [450, 300]])
input_labels = np.array([1, 1, 0])  # 2 foreground, 1 background

masks, scores, logits = predictor.predict(
    point_coords=input_points,
    point_labels=input_labels,
    multimask_output=False  # Single mask when prompts are clear
)
```

### Box提示词

```python
# Bounding box [x1, y1, x2, y2]
input_box = np.array([425, 600, 700, 875])

masks, scores, logits = predictor.predict(
    box=input_box,
    multimask_output=False
)
```

### 组合提示词

```python
# Box + points for precise control
masks, scores, logits = predictor.predict(
    point_coords=np.array([[500, 375]]),
    point_labels=np.array([1]),
    box=np.array([400, 300, 700, 600]),
    multimask_output=False
)
```

### 逐步优化

```python
# Initial prediction
masks, scores, logits = predictor.predict(
    point_coords=np.array([[500, 375]]),
    point_labels=np.array([1]),
    multimask_output=True
)

# Refine with additional point using previous mask
masks, scores, logits = predictor.predict(
    point_coords=np.array([[500, 375], [550, 400]]),
    point_labels=np.array([1, 0]),  # Add background point
    mask_input=logits[np.argmax(scores)][None, :, :],  # Use best mask
    multimask_output=False
)
```

## 自动口罩生成

### 基本自动分割功能

```python
from segment_anything import SamAutomaticMaskGenerator

# Create generator
mask_generator = SamAutomaticMaskGenerator(sam)

# Generate all masks
masks = mask_generator.generate(image)

# Each mask contains:
# - segmentation: binary mask
# - bbox: [x, y, w, h]
# - area: pixel count
# - predicted_iou: quality score
# - stability_score: robustness score
# - point_coords: generating point
```

### 自定义生成

```python
mask_generator = SamAutomaticMaskGenerator(
    model=sam,
    points_per_side=32,          # Grid density (more = more masks)
    pred_iou_thresh=0.88,        # Quality threshold
    stability_score_thresh=0.95,  # Stability threshold
    crop_n_layers=1,             # Multi-scale crops
    crop_n_points_downscale_factor=2,
    min_mask_region_area=100,    # Remove tiny masks
)

masks = mask_generator.generate(image)
```

### 过滤掩码

```python
# Sort by area (largest first)
masks = sorted(masks, key=lambda x: x['area'], reverse=True)

# Filter by predicted IoU
high_quality = [m for m in masks if m['predicted_iou'] > 0.9]

# Filter by stability score
stable_masks = [m for m in masks if m['stability_score'] > 0.95]
```

## 批量推理

### 多张图片处理

```python
# Process multiple images efficiently
images = [cv2.imread(f"image_{i}.jpg") for i in range(10)]

all_masks = []
for image in images:
    predictor.set_image(image)
    masks, _, _ = predictor.predict(
        point_coords=np.array([[500, 375]]),
        point_labels=np.array([1]),
        multimask_output=True
    )
    all_masks.append(masks)
```

### 单张图片支持多条提示词

```python
# Process multiple prompts efficiently (one image encoding)
predictor.set_image(image)

# Batch of point prompts
points = [
    np.array([[100, 100]]),
    np.array([[200, 200]]),
    np.array([[300, 300]])
]

all_masks = []
for point in points:
    masks, scores, _ = predictor.predict(
        point_coords=point,
        point_labels=np.array([1]),
        multimask_output=True
    )
    all_masks.append(masks[np.argmax(scores)])
```

## ONNX部署

### 导出模型

```bash
python scripts/export_onnx_model.py \
    --checkpoint sam_vit_h_4b8939.pth \
    --model-type vit_h \
    --output sam_onnx.onnx \
    --return-single-mask
```

### 使用 ONNX 模型

```python
import onnxruntime

# Load ONNX model
ort_session = onnxruntime.InferenceSession("sam_onnx.onnx")

# Run inference (image embeddings computed separately)
masks = ort_session.run(
    None,
    {
        "image_embeddings": image_embeddings,
        "point_coords": point_coords,
        "point_labels": point_labels,
        "mask_input": np.zeros((1, 1, 256, 256), dtype=np.float32),
        "has_mask_input": np.array([0], dtype=np.float32),
        "orig_im_size": np.array([h, w], dtype=np.float32)
    }
)
```

## 常见工作流程

### 工作流程 1：标注工具

```python
import cv2

# Load model
predictor = SamPredictor(sam)
predictor.set_image(image)

def on_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # Foreground point
        masks, scores, _ = predictor.predict(
            point_coords=np.array([[x, y]]),
            point_labels=np.array([1]),
            multimask_output=True
        )
        # Display best mask
        display_mask(masks[np.argmax(scores)])
```

### 工作流 2：对象提取

```python
def extract_object(image, point):
    """Extract object at point with transparent background."""
    predictor.set_image(image)

    masks, scores, _ = predictor.predict(
        point_coords=np.array([point]),
        point_labels=np.array([1]),
        multimask_output=True
    )

    best_mask = masks[np.argmax(scores)]

    # Create RGBA output
    rgba = np.zeros((image.shape[0], image.shape[1], 4), dtype=np.uint8)
    rgba[:, :, :3] = image
    rgba[:, :, 3] = best_mask * 255

    return rgba
```

### 工作流 3：医学图像分割

```python
# Process medical images (grayscale to RGB)
medical_image = cv2.imread("scan.png", cv2.IMREAD_GRAYSCALE)
rgb_image = cv2.cvtColor(medical_image, cv2.COLOR_GRAY2RGB)

predictor.set_image(rgb_image)

# Segment region of interest
masks, scores, _ = predictor.predict(
    box=np.array([x1, y1, x2, y2]),  # ROI bounding box
    multimask_output=True
)
```

## 输出格式

### 数据掩码结构

```python
# SamAutomaticMaskGenerator output
{
    "segmentation": np.ndarray,  # H×W binary mask
    "bbox": [x, y, w, h],        # Bounding box
    "area": int,                 # Pixel count
    "predicted_iou": float,      # 0-1 quality score
    "stability_score": float,    # 0-1 robustness score
    "crop_box": [x, y, w, h],    # Generation crop region
    "point_coords": [[x, y]],    # Input point
}
```

### COCO RLE 格式

```python
from pycocotools import mask as mask_utils

# Encode mask to RLE
rle = mask_utils.encode(np.asfortranarray(mask.astype(np.uint8)))
rle["counts"] = rle["counts"].decode("utf-8")

# Decode RLE to mask
decoded_mask = mask_utils.decode(rle)
```

## 性能优化

### GPU内存

```python
# Use smaller model for limited VRAM
sam = sam_model_registry["vit_b"](checkpoint="sam_vit_b_01ec64.pth")

# Process images in batches
# Clear CUDA cache between large batches
torch.cuda.empty_cache()
```

### 性能优化

```python
# Use half precision
sam = sam.half()

# Reduce points for automatic generation
mask_generator = SamAutomaticMaskGenerator(
    model=sam,
    points_per_side=16,  # Default is 32
)

# Use ONNX for deployment
# Export with --return-single-mask for faster inference
```

## 常见问题

| 问题 | 解决方案 |
|-------|----------|
| 内存不足 | 使用 ViT-B 模型，减小图像尺寸 |
| 推理速度慢 | 使用 ViT-B 模型，并降低 points_per_side 的数值 |
| 边界遮罩质量差 | 尝试不同的提示词，同时使用框和点信息 |
| 边缘伪影 | 采用 stability_score 过滤机制 |
| 小物体被遗漏 | 提高 points_per_side 的数值 |

## 参考资料

- **[高级用法](references/advanced-usage.md)** - 批量处理、微调及集成方法
- **[故障排除](references/troubleshooting.md)** - 常见问题及解决方案

## 资源链接

- **GitHub**: https://github.com/facebookresearch/segment-anything
- **论文**: https://arxiv.org/abs/2304.02643
- **演示页面**: https://segment-anything.com
- **SAM 2（视频版）**: https://github.com/facebookresearch/segment-anything-2
- **HuggingFace**: https://huggingface.co/facebook/sam-vit-huge
