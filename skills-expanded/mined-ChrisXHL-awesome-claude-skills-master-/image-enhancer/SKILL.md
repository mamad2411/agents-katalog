---
name: image-enhancer
description: 通过增强分辨率、锐度和清晰度来提高图像（尤其是截图）的质量。非常适合准备用于演示、文档或社交媒体帖子的图像。
---

# 图像增强器

此技能获取您的图像和截图并使其看起来更好——更清晰、更锐利、更专业。

## 何时使用此技能

- 提高博客文章或文档的截图质量
- 在社交媒体上分享之前增强图像
- 为演示文稿或报告准备图像
- 放大低分辨率图像
- 锐化模糊照片
- 清理压缩图像

## 此技能做什么

1. **分析图像质量**: 检查分辨率、锐度和压缩伪影
2. **增强分辨率**: 智能放大图像
3. **提高锐度**: 增强边缘和细节
4. **减少伪影**: 清理压缩伪影和噪点
5. **优化用例**: 根据预期用途（网络、打印、社交媒体）进行调整

## 如何使用

### 基本增强

```
Improve the image quality of screenshot.png
```

```
Enhance all images in this folder
```

### 特定改进

```
Upscale this image to 4K resolution
```

```
Sharpen this blurry screenshot
```

```
Reduce compression artifacts in this image
```

### 批量处理

```
Improve the quality of all PNG files in this directory
```

## 示例

**用户**: "Improve the image quality of screenshot-2024.png"

**输出**:
```
正在分析 screenshot-2024.png...

当前规格:
- 分辨率: 1920x1080
- 格式: PNG
- 质量: 良好，但有轻微模糊

已应用增强:
✓ 放大至 2560x1440 (视网膜)
✓ 锐化边缘
✓ 增强文本清晰度
✓ 优化文件大小

保存为: screenshot-2024-enhanced.png
原始文件保留为: screenshot-2024-original.png
```

**灵感来源:** Lenny Rachitsky 他的时事通讯工作流 - 用于其文章中的截图

## 提示

- 始终保留原始文件作为备份
- 最适合截图和数字图像
- 可以批量处理整个文件夹
- 如果需要指定输出格式（PNG 追求质量，JPG 追求较小尺寸）
- 对于社交媒体，提及平台以获得最佳尺寸

## 常见用例

- **博客文章**: 发布前增强截图
- **文档**: 使 UI 截图清晰无比
- **社交媒体**: 为 Twitter, LinkedIn, Instagram 优化图像
- **演示文稿**: 为大屏幕放大图像
- **打印材料**: 提高物理介质的分辨率
