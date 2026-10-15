---
name: image-cropper
description: >-
  裁剪 AI 生成图片的底部水印区域，输出到 cropped 文件夹。
  当用户要求"裁剪图片"、"去水印"、"裁剪水印"、"crop image"、
  "remove watermark"，或需要将 AI 生成的图片处理为论文可用版本时使用。
---

# 图片水印裁剪器

## 概述

本技能调用 `crop_watermark.py` 脚本，裁剪 AI 生成图片底部的水印区域。裁剪后的图片保存到 `ai_generated/cropped/`，可直接用于论文。

## 何时使用本技能

- 用户要求"裁剪图片"、"去水印"、"裁剪水印"时。
- `ai_generated/original/` 中有新的 AI 生成图片需要处理时。
- 用户说"裁剪"、"crop"、"remove watermark"时。

## 何时不使用本技能

- 生成 Mermaid 图表。请改用 `mermaid-renderer`。
- 生成画图提示词。请改用 `diagram-prompt-generator`。

## 操作步骤

### 步骤 1：确认原图位置

检查 `Docs/images/ai_generated/original/` 中是否有待裁剪的图片。

```bash
ls Docs/images/ai_generated/original/
```

如果没有图片，提示用户先将 AI 生成的图片放入 `original/` 文件夹。

### 步骤 2：执行裁剪

运行裁剪脚本，批量处理 `original/` 下所有图片：

```bash
cd Docs/images
python crop_watermark.py --batch
```

裁剪参数（默认值）：
- 底部裁剪：22%（对应提示词中要求的 20-25% 底部留白）
- 右侧裁剪：0%

如需自定义比例：

```bash
python crop_watermark.py --batch 0.25 0.00   # 底部 25%，右侧 0%
python crop_watermark.py original/xxx.png     # 单张裁剪
```

### 步骤 3：确认输出

检查 `Docs/images/ai_generated/cropped/` 中的裁剪结果，向用户报告处理了多少张图片。

## 文件结构

```
Docs/images/
├── crop_watermark.py          ← 裁剪脚本
├── ai_generated/
│   ├── original/              ← 放入待裁剪的原图
│   ├── cropped/               ← 裁剪后可直接用于论文
│   └── README.md
```
