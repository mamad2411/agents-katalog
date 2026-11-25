---
name: pixel-art
description: "Pixel art w/ era palettes (NES, Game Boy, PICO-8)."
version: 2.0.0
author: dodo-reach
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [creative, pixel-art, arcade, snes, nes, gameboy, retro, image, video]
    category: creative
    credits:
      - "Hardware palettes and animation loops ported from Synero/pixel-art-studio (MIT) — https://github.com/Synero/pixel-art-studio"
---

# 像素艺术

可将任何图像转换为复古风格的像素艺术，还可根据需求为其添加动画效果，生成带有符合时代特色的特效（雨滴、萤火虫、雪花、余烬）的短 MP4 或 GIF 文件。

该功能附带两个脚本：

- `scripts/pixel_art.py` — 将照片转换为像素艺术 PNG 格式（采用 Floyd-Steinberg 随机化算法）
- `scripts/pixel_art_video.py` — 将像素艺术 PNG 转换为动画 MP4 文件（也可生成 GIF）

这两个脚本均可直接导入或运行。若需符合特定时代风格的色彩（如 NES、Game Boy、PICO-8 等平台风格），可使用预设的硬件调色板；若希望呈现街机或 SNES 风格，则可使用自适应的 N 色量化功能。

## 适用场景

- 用户希望从源图像生成复古像素艺术
- 用户要求采用 NES、Game Boy、PICO-8、C64、街机或 SNES 的风格
- 用户需要制作短循环动画（如雨景、夜空、雪景等）
- 用于海报、专辑封面、社交媒体帖子、精灵图、角色设计或头像制作

## 工作流程

在生成之前，需先与用户确认风格。不同的预设会产生截然不同的输出结果，重新生成会耗费较多资源。

### 第一步 — 提供风格选项

调用 `clarify` 函数并传入 4 个具有代表性的预设。根据用户的实际需求选择合适的预设集——无需一次性展示全部 14 个选项。

当用户的需求不明确时，系统会显示默认菜单：

```python
clarify(
    question="Which pixel-art style do you want?",
    choices=[
        "arcade — bold, chunky 80s cabinet feel (16 colors, 8px)",
        "nes — Nintendo 8-bit hardware palette (54 colors, 8px)",
        "gameboy — 4-shade green Game Boy DMG",
        "snes — cleaner 16-bit look (32 colors, 4px)",
    ],
)
```

当用户已为某个时代指定名称（例如“80年代街机游戏”“Gameboy时代”）时，可直接跳过`clarify`步骤，使用对应的预设配置。

### 第2步 — 提供动画效果（可选）

如果用户要求生成视频/GIF，或者输出内容通过动态效果能更佳呈现，可询问用户希望展示哪一场景：

```python
clarify(
    question="Want to animate it? Pick a scene or skip.",
    choices=[
        "night — stars + fireflies + leaves",
        "urban — rain + neon pulse",
        "snow — falling snowflakes",
        "skip — just the image",
    ],
)
```

请勿连续两次以上调用 `clarify` 函数。若需设定风格，则调用一次；若涉及动画制作，则还需再调用一次以设定场景。如果用户在请求中已明确指定了具体的风格和场景，则无需使用 `clarify` 函数。

### 第三步 — 生成图像

首先运行 `pixel_art()` 函数；如果用户要求生成动画，可在其输出结果的基础上继续调用 `pixel_art_video()` 函数。

## 预设选项目录

| 预设名称 | 影视时代 | 调色板数量 | 块尺寸 | 最适合用于 |
|--------|---------|-----------|-------|----------|
| `arcade` | 80年代街机 | 动态调整的16种颜色 | 8像素 | 强烈视觉冲击力的海报、角色形象设计 |
| `snes` | 16位游戏机 | 动态调整的32种颜色 | 4像素 | 角色形象、细节丰富的场景绘制 |
| `nes` | 8位游戏机 | NES标准色系（54种颜色） | 8像素 | 还原真实的NES游戏风格 |
| `gameboy` | DMG掌上游戏机 | 4种绿色色调 | 8像素 | 单色风格的Game Boy游戏画面 |
| `gameboy_pocket` | 口袋型掌上游戏机 | 4种灰色色调 | 8像素 | 单色风格的Game Boy Pocket游戏画面 |
| `pico8` | PICO-8游戏机 | 固定的16种颜色 | 6像素 | 带有奇幻风格的游戏机外观 |
| `c64` | Commodore 64电脑 | 固定的16种颜色 | 8像素 | 8位家用电脑风格 |
| `apple2` | Apple II高分辨率显示器 | 固定的6种颜色 | 10像素 | 极具复古感、仅支持6种颜色的风格 |
| `teletext` | BBC文字电视服务 | 纯色的8种颜色 | 10像素 | 鲜艳醒目的基础色彩风格 |
| `mspaint` | Windows画图程序 | 固定的24种颜色 | 8像素 | 具有怀旧感的桌面风格 |
| `mono_green` | CRT荧光屏效果 | 2种绿色色调 | 6像素 | 终端/CRT显示器的视觉风格 |
| `mono_amber` | CRT琥珀色屏幕效果 | 2种琥珀色色调 | 6像素 | 琥珀色监控器风格的画面 |
| `neon` | 霓虹赛博风 | 10种霓虹色彩 | 6像素 | 气泡波/赛博朋克风格 |
| `pastel` | 柔和淡彩风 | 10种淡彩色调 | 6像素 | 可爱柔和的视觉风格 |
命名调色板存储在 `scripts/palettes.py` 文件中（完整列表请参见 `references/palettes.md`——共计有 28 个命名调色板）。任何预设值均可被覆盖：

```python
pixel_art("in.png", "out.png", preset="snes", palette="PICO_8", block=6)
```

## 场景目录（适用于视频）

| 场景 | 效果 |
|-------|------|
| `night` | 闪烁的星星 + 萤火虫 + 飘落的树叶 |
| `dusk` | 萤火虫 + 闪光粒子 |
| `tavern` | 灰尘微粒 + 温暖的闪光效果 |
| `indoor` | 灰尘微粒 |
| `urban` | 雨滴 + 霓虹灯脉动光效 |
| `nature` | 树叶 + 萤火虫 |
| `magic` | 闪光粒子 + 萤火虫 |
| `storm` | 雨滴 + 闪电 |
| `underwater` | 气泡 + 微弱闪光 |
| `fire` | 火炭 + 闪光粒子 |
| `snow` | 雪花 + 闪光粒子 |
| `desert` | 热浪光效 + 灰尘 |

## 调用方式

### Python（导入方式）

```python
import sys
import os
sys.path.insert(0, os.path.expanduser("~/.hermes/skills/creative/pixel-art/scripts"))
from pixel_art import pixel_art
from pixel_art_video import pixel_art_video

# 1. Convert to pixel art
pixel_art("/path/to/photo.jpg", "/tmp/pixel.png", preset="nes")

# 2. Animate (optional)
pixel_art_video(
    "/tmp/pixel.png",
    "/tmp/pixel.mp4",
    scene="night",
    duration=6,
    fps=15,
    seed=42,
    export_gif=True,
)
```

### 命令行界面

```bash
cd ~/.hermes/skills/creative/pixel-art/scripts

python pixel_art.py in.jpg out.png --preset gameboy
python pixel_art.py in.jpg out.png --preset snes --palette PICO_8 --block 6

python pixel_art_video.py out.png out.mp4 --scene night --duration 6 --gif
```

## 流处理原理

**像素转换：**
1. 提升对比度、色彩饱和度及清晰度（颜色调色板较少的情况下效果更显著）
2. 在量化之前将图像简化为块状结构，以简化色调区域
3. 使用 `Image.NEAREST` 方法按“块”进行缩小处理（采用硬像素方式，不进行插值）
4. 采用 Floyd-Steinberg 随机化算法进行量化——量化依据可以是自适应的 N 色调色板，也可以是预定义的硬件色调色板
5. 再次使用 `Image.NEAREST` 方法将图像放大回原始尺寸

在缩小处理之后再进行量化，可以确保随机化效果与最终的像素网格保持一致。若在缩小之前就进行量化，则会在那些最终会消失的细节上浪费误差扩散资源。

**视频叠加：**
- 每一帧都复制基础帧（用于静态背景）
- 叠加每帧独立的粒子渲染效果（每种特效对应一个函数）
- 通过 ffmpeg 使用 `libx264 -pix_fmt yuv420p -crf 18` 进行编码
- 如需生成 GIF 格式，可使用 `palettegen` 和 `paletteuse` 工具

## 依赖项

- Python 3.9 及以上版本
- Pillow 库（可通过 `pip install Pillow` 安装）
- PATH 环境变量中需包含 ffmpeg（仅视频处理需要——Hermes 会自动安装该软件）

## 常见问题与注意事项

- 调色板键名区分大小写（如 `"NES"`、`"PICO_8"`、`"GAMEBOY_ORIGINAL"`）。
- 非常小的图像源（宽度小于100像素）在8-10像素的块大小下会被压缩。若图像过小，建议先进行放大处理。
- 分数形式的 `block` 或 `palette` 值会导致量化错误——请确保使用正整数。
- 动画粒子数量是根据约640x480分辨率的画布设计的。对于超大尺寸的图像，可能需要使用不同的种子值进行二次处理，以调整粒子密度。
- `mono_green` / `mono_amber` 选项会强制将颜色饱和度设为 `0.0`（即去饱和处理）。若尝试覆盖该设置并保留色度，双色调色板可能会在图像的平滑区域产生条纹。
- `clarify` 循环：每轮最多调用两次（先处理风格，再处理场景）。避免向用户频繁提出过多选择。

## 验证标准

- 输出路径下会生成PNG格式文件。
- 在预设的块大小下，能够看到清晰的方形像素块。
- 颜色数量与预设值一致（可通过肉眼观察图像或运行 `Image.open(p).getcolors()` 来确认）。
- 视频为有效的MP4格式（可使用 `ffprobe` 打开），且文件大小大于零。

## 出处说明

`pixel_art_video.py` 文件中定义的硬件调色板以及程序化动画循环，均源自 [pixel-art-studio](https://github.com/Synero/pixel-art-studio)（MIT许可证）。详细信息请参阅该技能目录下的 `ATTRIBUTION.md` 文件。
