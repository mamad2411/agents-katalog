---
name: manim-builder
description: Compile and render Manim scenes to video files. Use when user has a .py scene file that needs to be rendered to mp4/gif, or when previewing animation results. Handles: rendering scenes, quality settings (4k, high, medium, low), exporting to different formats (mp4, gif, png), and previewing results.
---

# Manim Builder

编译 Manim 代码并渲染为视频文件。

## Quick Start

```bash
# 基础编译
python scripts/build.py scene.py MyScene

# 指定质量
python scripts/build.py scene.py MyScene --quality high

# 导出 GIF
python scripts/build.py scene.py MyScene --format gif
```

## 编译流程

```
scene.py 文件 → Manim 编译 → manim_outputs/ 目录
```

输出文件位置: `manim_outputs/<scene_name>_<timestamp>/output/<quality>/MyScene.mp4`

## 质量选项

| 质量 | 分辨率 | 参数 | 文件大小 |
|------|--------|------|----------|
| `low` | 480p | `--quality low` 或 `-ql` | 最小 |
| `medium` | 720p | `--quality medium` 或 `-qm` | 中等 |
| `high` | 1080p | `--quality high` 或 `-qh` | 较大 |
| `4k` | 2160p | `--quality 4k` 或 `-qk` | 最大 |

**默认质量**: high (1080p)

## 导出格式

### MP4 视频（默认）
```bash
python scripts/build.py scene.py MyScene
```

### GIF 动画
```bash
python scripts/build.py scene.py MyScene --format gif
```

### PNG 序列
```bash
python scripts/build.py scene.py MyScene --format png
```

## 使用场景

### 场景 1: 编译单个场景
```bash
python scripts/build.py my_animation.py SineWave
```

### 场景 2: 高质量渲染
```bash
python scripts/build.py my_animation.py SineWave --quality 4k
```

### 场景 3: 批量编译
```bash
# 编译文件中的所有场景
python scripts/build.py my_animation.py --all
```

### 场景 4: 自定义输出
```bash
# 指定输出目录
python scripts/build.py scene.py MyScene --output ./my_videos
```

## 命令行参数

```
usage: build.py [-h] [--scene SCENE] [--quality {low,medium,high,4k}]
                [--format {mp4,gif,png}] [--output OUTPUT]
                file

positional arguments:
  file                  Scene .py 文件路径

options:
  -h, --help            显示帮助信息
  --scene SCENE         场景类名（默认: Scene）
  --quality {low,medium,high,4k}
                        渲染质量（默认: high）
  --format {mp4,gif,png}
                        输出格式（默认: mp4）
  --output OUTPUT       输出目录（默认: manim_outputs/<scene_name>_<timestamp>/）
```

## 预览结果

### 命令行查看文件
```bash
# 查找生成的视频
find manim_outputs -name "*.mp4"

# 使用默认播放器打开
xdg-open manim_outputs/my_animation_<timestamp>/output/high/MyScene.mp4
```

### 在代码中预览
```python
from manim import *

class MyScene(Scene):
    def construct(self):
        # ... 动画代码 ...
        # 预览时自动打开视频
        pass
```

## 常见问题

### 问题 1: 找不到 manim 命令
```bash
# 安装 manim
pip install manim

# 验证安装
manim --version
```

### 问题 2: 渲染时间过长
```bash
# 使用低质量预览
python scripts/build.py scene.py MyScene --quality low

# 渲染部分场景（在代码中指定）
class MyScene(Scene):
    def construct(self):
        # 只渲染前 N 秒
        self.wait(2)  # 预览时只渲染 2 秒
```

### 问题 3: LaTeX 公式不显示
```bash
# 安装 LaTeX
sudo apt-get install texlive-full  # Ubuntu/Debian
brew install mactex                 # macOS
```

### 问题 4: 内存不足
```bash
# 使用低质量渲染
python scripts/build.py scene.py MyScene --quality medium

# 或禁用某些效果
# 在代码中添加:
config.quality = "medium_quality"
```

## 质量设置参考

详见 `references/options.md` 获取完整的质量配置选项。

## 编译示例

完整示例见 `scripts/build.py` 源码。
