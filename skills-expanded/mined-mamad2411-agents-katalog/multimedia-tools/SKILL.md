---
name: multimedia-tools
description: 多媒体音视频图像处理工具(FFmpeg/ImageMagick)。当用户需要进行视频格式转换(MP4/WebM/MOV/AVI/MKV等)、视频压缩优化(CRF编码/web预设/archive预设)、视频剪辑裁剪(trim/cut/切片)、提取音频(MP3/WAV/FLAC等)、视频缩放调整分辨率(resize/scale)、视频添加水印(watermark/logo/文字叠加)、图片格式转换(JPEG/PNG/WebP/GIF/TIFF/BMP)、图片压缩优化(质量压缩/文件瘦身)、图片缩放裁剪(resize/crop/thumbnail)、批量处理多媒体文件(batch processing)、生成视频缩略图(thumbnail/screenshot)、处理GIF动画(转换/压缩/优化)、视频截图提取帧(frame extraction)、调整视频码率/帧率(bitrate/fps)、旋转视频/图片(rotate/flip)、音频格式转换等相关任务时立即使用。支持跨平台(Windows/macOS/Linux)，输出JSON格式便于程序集成。
trigger:
  - 视频转换
  - 视频压缩
  - 图片压缩
  - 格式转换
  - 视频剪辑
  - 提取音频
  - 视频水印
  - 图片水印
  - 批量处理
  - 生成缩略图
  - FFmpeg
  - ImageMagick
  - 视频裁剪
  - 图片裁剪
  - 视频转码
  - GIF处理
  - 视频截图
  - 音频提取
  - 分辨率调整
  - 文件瘦身
---

# Multimedia Tools Guide

## Overview

This toolkit provides unified access to **FFmpeg** (video processing) and **ImageMagick** (image processing) for common multimedia operations. All scripts return JSON output for programmatic integration.

### Prerequisites

- FFmpeg: Install from https://ffmpeg.org/download.html
- ImageMagick: Install from https://imagemagick.org/script/download.php

Verify installation:
```bash
ffmpeg -version
magick -version
```

## Quick Start

### Video Conversion
```bash
python scripts/video/convert_video.py input.mov output.mp4
```

### Image Conversion
```bash
python scripts/image/convert_image.py photo.jpg photo.png
```

### Video Compression with Preset
```bash
python scripts/video/compress_video.py input.mp4 output.mp4 --preset web
```

### Image Compression with Preset
```bash
python scripts/image/compress_image.py photo.jpg output.jpg --preset web
```

## Video Processing

### Format Conversion
Convert between video formats while maintaining quality.

**Supported formats**: MP4, WebM, MOV, AVI, MKV

```bash
python scripts/video/convert_video.py input.mov output.mp4
python scripts/video/convert_video.py input.avi output.webm
```

### Resize & Scale
Adjust video resolution while maintaining aspect ratio or force dimensions.

```bash
# Scale to width, maintain aspect ratio
python scripts/video/resize_video.py input.mp4 output.mp4 --width 1280

# Scale to height, maintain aspect ratio
python scripts/video/resize_video.py input.mp4 output.mp4 --height 720

# Force exact dimensions
python scripts/video/resize_video.py input.mp4 output.mp4 --width 1280 --height 720
```

### Compression with Presets

Compress videos with scenario-based quality presets:

**Presets**:
- **web**: CRF 28, fast preset, optimized for streaming
- **archive**: CRF 18, slow preset, high quality for storage
- **default**: CRF 23, medium preset, balanced

```bash
python scripts/video/compress_video.py input.mp4 output.mp4 --preset web
python scripts/video/compress_video.py input.mp4 output.mp4 --preset archive
```

### Audio Extraction
Extract audio track from video files.

```bash
python scripts/video/extract_audio.py input.mp4 output.mp3
python scripts/video/extract_audio.py input.mov output.wav
```

### Trimming
Cut video by time range.

```bash
# Extract 00:30 to 01:30
python scripts/video/trim_video.py input.mp4 output.mp4 --start 00:00:30 --end 00:01:30

# Extract first 30 seconds
python scripts/video/trim_video.py input.mp4 output.mp4 --start 00:00:00 --duration 00:00:30
```

### Watermarking
Add custom watermarks to videos with position and opacity controls.

**Positions**: top-left, top-right, bottom-left, bottom-right, center

```bash
# Default position (bottom-right), full opacity
python scripts/video/add_watermark.py input.mp4 watermark.png output.mp4

# Custom position and opacity (0.0-1.0)
python scripts/video/add_watermark.py input.mp4 watermark.png output.mp4 --position top-left --opacity 0.7
```

### Batch Processing
Process multiple videos in a directory.

```bash
python scripts/video/batch_process_video.py input_folder/ output_folder/ --operation convert --format mp4
python scripts/video/batch_process_video.py input_folder/ output_folder/ --operation compress --preset web
```

## Image Processing

### Format Conversion
Convert between image formats.

**Supported formats**: JPEG, PNG, WebP, GIF, TIFF, BMP

```bash
python scripts/image/convert_image.py photo.jpg photo.png
python scripts/image/convert_image.py image.png image.webp
```

### Resize & Scale
Adjust image dimensions.

```bash
# Scale to width, maintain aspect ratio
python scripts/image/resize_image.py photo.jpg output.jpg --width 1920

# Scale to percentage
python scripts/image/resize_image.py photo.jpg output.jpg --scale 50
```

### Compression with Presets

Compress images with scenario-based quality presets:

**Presets**:
- **web**: Quality 85, metadata stripped, optimized for web
- **print**: Quality 95, 300 DPI, print-ready
- **thumbnail**: Quality 75, small size (200px width)
- **default**: Quality 85, balanced

```bash
python scripts/image/compress_image.py photo.jpg output.jpg --preset web
python scripts/image/compress_image.py photo.png output.png --preset print
```

### Cropping
Crop images to specified dimensions and offset.

```bash
# Crop 800x600 starting at (100, 50)
python scripts/image/crop_image.py photo.jpg output.jpg --width 800 --height 600 --x 100 --y 50

# Crop to center
python scripts/image/crop_image.py photo.jpg output.jpg --width 800 --height 600 --center
```

### Watermarking
Add custom watermarks to images with position and opacity controls.

**Positions**: NorthWest, North, NorthEast, West, Center, East, SouthWest, South, SouthEast

```bash
# Default position (SouthEast), 80% opacity
python scripts/image/add_watermark.py photo.jpg watermark.png output.jpg

# Custom position and opacity (0-100)
python scripts/image/add_watermark.py photo.jpg watermark.png output.jpg --position Center --opacity 50
```

### Batch Processing
Process multiple images in a directory.

```bash
python scripts/image/batch_process_image.py input_folder/ output_folder/ --operation convert --format png
python scripts/image/batch_process_image.py input_folder/ output_folder/ --operation compress --preset web
```

## Common Workflows

### Prepare for Web
Optimize media for web streaming and social media.

```bash
# Video: Compress with web preset
python scripts/video/compress_video.py video.mp4 web_video.mp4 --preset web

# Image: Convert to JPEG, strip metadata
python scripts/image/compress_image.py photo.jpg web_photo.jpg --preset web
```

### Archive Compression
High-quality compression for long-term storage.

```bash
# Video: Archive preset
python scripts/video/compress_video.py video.mp4 archive.mp4 --preset archive

# Image: Maximum quality
python scripts/image/compress_image.py photo.png archive.jpg --preset default --quality 95
```

### Print Preparation
Prepare images for printing.

```bash
# Image: Print preset (300 DPI, high quality)
python scripts/image/compress_image.py photo.jpg print.jpg --preset print
```

### Social Media Optimization
Standard resolutions and formats for social platforms.

```bash
# 1080x1920 (Instagram Reels)
python scripts/video/resize_video.py video.mp4 reel.mp4 --width 1080 --height 1920

# Square thumbnail
python scripts/image/resize_image.py photo.jpg thumb.jpg --width 400 --height 400
```

### Bulk Watermarking
Apply watermarks to entire media libraries.

```bash
# Videos
python scripts/video/batch_process_video.py videos/ watermarked/ --operation watermark --wm watermark.png

# Images
python scripts/image/batch_process_image.py images/ watermarked/ --operation watermark --wm watermark.png
```

## Script Usage

All scripts return JSON output for programmatic integration:

### Success Response
```json
{
  "status": "success",
  "output": "path/to/output",
  "preset_used": "web",
  "operation": "convert",
  "original_size": 15728640,
  "output_size": 5242880
}
```

### Error Response
```json
{
  "status": "error",
  "message": "Input file not found",
  "error_code": "FILE_NOT_FOUND"
}
```

## Utility Scripts

### Check Dependencies
Verify FFmpeg and ImageMagick installation.

```bash
python scripts/utils/check_dependencies.py
```

### Get Video Info
Extract metadata from video files.

```bash
python scripts/utils/get_video_info.py input.mp4
```

### Get Image Info
Extract metadata from image files.

```bash
python scripts/utils/get_image_info.py photo.jpg
```

### Apply Preset
Get preset configuration programmatically.

```bash
python scripts/utils/apply_preset.py --type video --preset web
python scripts/utils/apply_preset.py --type image --preset print
```

## Reference Documentation

For detailed command references, examples, and advanced usage:

- **ffmpeg_commands.md**: Complete FFmpeg command reference and options
- **imagemagick_commands.md**: Complete ImageMagick command reference and options
- **quality_presets.md**: Detailed preset configurations and customization
- **common_workflows.md**: Extended workflow examples and use cases
- **troubleshooting.md**: Common issues and solutions

## Asset Files

### Preset Configurations
Located in `assets/presets/`:

- `video_presets.json`: Video quality presets (web, archive, default)
- `image_presets.json`: Image quality presets (web, print, thumbnail, default)

Customize these files to adjust default quality settings.

### Watermark Templates
Located in `assets/templates/watermark/`:

- `default_watermark.png`: Sample watermark (replace with your own)

## Best Practices

### Video Processing
- Use **web** preset for web content (fast encoding, reasonable quality)
- Use **archive** preset for long-term storage (slow encoding, maximum quality)
- Test on short clips first to verify quality
- Use H.264 codec (libx264) for maximum compatibility

### Image Processing
- Use **web** preset for web images (metadata stripped, optimized quality)
- Use **print** preset for printed materials (high DPI, maximum quality)
- Use **thumbnail** preset for preview images (small size, fast loading)
- Preserve original aspect ratio unless forcing dimensions

### Batch Processing
- Test on small sample sets before processing large batches
- Ensure output directory exists and has sufficient space
- Monitor first few outputs to verify results
- Use appropriate presets for your use case

## Quality Preset Summary

| Media Type | Preset | Quality | Use Case |
|------------|--------|---------|----------|
| Video | web | CRF 28 | Web streaming, social media |
| Video | archive | CRF 18 | Long-term storage |
| Video | default | CRF 23 | Balanced quality |
| Image | web | 85% | Web content |
| Image | print | 95%, 300 DPI | Print materials |
| Image | thumbnail | 75%, 200px | Preview images |
| Image | default | 85% | General use |
