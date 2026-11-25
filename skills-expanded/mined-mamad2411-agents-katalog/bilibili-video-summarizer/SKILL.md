---
name: bilibili-video-summarizer
description: 支持下载B站视频，自动分析B站视频内容，下载视频并拆解成帧图片，使用AI分析并生成详细的总结。
---

# bilibili-video-summarizer

## Description

这是一个专业的B站视频分析和总结工具，可以自动下载B站视频、提取关键帧、生成视频摘要、并使用AI分析内容，生成报告。

## When to Use

- `/bilibili-video-summarizer` 命令
- 用户想要下载B站视频
- 用户请求分析B站视频
- 用户提供B站视频链接并要求分析

## 环境要求

### 必需
- Python 3.8+
- yt-dlp（视频下载）
- ffmpeg（帧提取）
- requests（API调用）

## 执行步骤

### 1. 创建和激活虚拟环境

如果没有虚拟环境需要执行

```bash
# 进入scripts目录
cd scripts

# 如果还没有虚拟环境，创建一个
python3 -m venv env

# 激活虚拟环境
source env/bin/activate
```

### 2. 安装依赖

python依赖安装

```bash
# 在虚拟环境中安装依赖
pip install -r requirements.txt
```

如果没有ffmpeg，则进行安装

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# CentOS/RHEL
sudo yum install ffmpeg
```

验证安装:
```bash
ffmpeg -version
```

### 3. 使用方式

执行以下命令会将视频下载到本地，并生成帧图片，包含视频信息的json

#### 基础用法

```bash
# 最简单的用法 - 下载视频（默认最高质量）
python cli.py "https://www.bilibili.com/video/BVxxxxxx"

# 或直接使用BV号
python cli.py "BVxxxxxx"
```

#### 高级用法

```bash
# 下载到指定目录
python cli.py "BVxxxxxx" --output-dir ./my_videos

# 下载最低质量版本（更快、更省空间）
python cli.py "BVxxxxxx" --format worst

# 下载并自动生成 HTML 图文报告
python cli.py "BVxxxxxx" --generate-report

# 下载到自定义目录
python cli.py "https://b23.tv/pMvOT7B" --output-dir ./videos
```

#### 命令行参数

```
位置参数:
  url                   B站视频URL或BV号

可选参数:
  --output-dir, -o     视频保存目录，默认: downloads

  --format             视频格式选择: best(最高质量) | worst(最低质量) | 或其他yt-dlp格式ID
                       默认: best

  --generate-report    下载完成后自动生成 HTML 图文报告
```

#### 支持的B站链接格式

- BV号: `BVxxxxxx`
- 完整URL: `https://www.bilibili.com/video/BVxxxxxx`
- 短链接: `https://b23.tv/xxxxxxx`

### 4. 文件结构
每次下载会在 `downloads` 目录下或指定目录下创建如下结构：

```
downloads/
└── BV1zxfNYqEoF/              # 以 BV 号命名的文件夹
    ├── BV1zxfNYqEoF_info.json # 视频信息（API数据）
    ├── video_title.mp4        # 下载的视频文件
    └── images/                # 提取的帧图目录
        ├── BV1zxfNYqEoF_0001.jpg
        ├── BV1zxfNYqEoF_0002.jpg
        └── ...
```

### 5.分析生成的帧图以及json数据

输出的格式可以参考下方内容，如果用户需要更细致的视频分析，你需要按照图片的顺序帧进行分析，生成更详细的视频分镜描述，并将内容写入到md文档中，放在视频的同级目录下（与视频文件同一级）。目前帧图的提取数量规则为：30秒以内：每秒 2 帧，30-120秒：每秒 1 帧，120-600秒：每秒 0.5 帧（每2秒1帧），10分钟以上：每秒 0.2 帧（每5秒1帧）

---

## 输出格式

```markdown
## 视频分析结果

### 视频信息

- 基本信息：标题、时长、BV号、上传者
- 统计数据：浏览、点赞、评论、收藏、投币等
- 视频属性：分类、分辨率、发布时间等

### AI生成标题

xxx

### AI摘要

xxx

### 核心要点

1. xxx
2. xxx

### 生成文件

- 视频: /tmp/video_analysis/{ID}/video.mp4
- 音频: /tmp/video_analysis/{ID}/audio.mp3
- SRT字幕: /tmp/video_analysis/{ID}/subtitle.srt
- 纯文本: /tmp/video_analysis/{ID}/text.txt
```

---


## Tags

`bilibili`, `video-summarizer`, `ai`, `tutorial`, `ffmpeg`,





