---
name: whisper
description: Transcribe and translate speech in 99 languages.
version: 1.0.0
author: Orchestra Research
license: MIT
dependencies: [openai-whisper, transformers, torch]
platforms: [linux, macos]
metadata:
  hermes:
    tags: [Whisper, Speech Recognition, ASR, Multimodal, Multilingual, OpenAI, Speech-To-Text, Transcription, Translation, Audio Processing]

---

# Whisper——强大的语音识别引擎

OpenAI推出的多语言语音识别模型。

## 何时使用Whisper

**适用场景：**
- 文本转语音（支持99种语言）
- 播客/视频字幕生成
- 会议记录自动生成
- 英文翻译
- 噪音环境下的音频转写
- 多语言音频处理

**核心数据：**
- **GitHub星标数超72,900个**
- 支持99种语言
- 基于680,000小时的音频数据训练
- 采用MIT许可证

**可选替代方案：**
- **AssemblyAI**：托管式API，支持说话人分离功能
- **Deepgram**：实时流式语音识别服务
- **Google Speech-to-Text**：基于云端的解决方案

## 快速入门

### 安装指南

```bash
# Requires Python 3.8-3.11
pip install -U openai-whisper

# Requires ffmpeg
# macOS: brew install ffmpeg
# Ubuntu: sudo apt install ffmpeg
# Windows: choco install ffmpeg
```

### 基本转录功能

```python
import whisper

# Load model
model = whisper.load_model("base")

# Transcribe
result = model.transcribe("audio.mp3")

# Print text
print(result["text"])

# Access segments
for segment in result["segments"]:
    print(f"[{segment['start']:.2f}s - {segment['end']:.2f}s] {segment['text']}")
```

## 模型尺寸

```python
# Available models
models = ["tiny", "base", "small", "medium", "large", "turbo"]

# Load specific model
model = whisper.load_model("turbo")  # Fastest, good quality
```

| 模型 | 参数量 | 仅英文支持 | 多语言支持 | 计算速度 | VRAM占用 |
|-------|----------|------------|------------|---------|----------|
| tiny | 39M | ✓ | ✓ | 约32倍 | 约1 GB |
| base | 74M | ✓ | ✓ | 约16倍 | 约1 GB |
| small | 244M | ✓ | ✓ | 约6倍 | 约2 GB |
| medium | 769M | ✓ | ✓ | 约2倍 | 约5 GB |
| large | 1550M | ✗ | ✓ | 1倍 | 约10 GB |
| turbo | 809M | ✗ | ✓ | 约8倍 | 约6 GB |

**推荐方案**：如需最佳的速度与质量，建议使用 `turbo` 模型；进行原型开发时则可选择 `base` 模型。

## 文本转录选项

### 语言设置

```python
# Auto-detect language
result = model.transcribe("audio.mp3")

# Specify language (faster)
result = model.transcribe("audio.mp3", language="en")

# Supported: en, es, fr, de, it, pt, ru, ja, ko, zh, and 89 more
```

### 任务选择

```python
# Transcription (default)
result = model.transcribe("audio.mp3", task="transcribe")

# Translation to English
result = model.transcribe("spanish.mp3", task="translate")
# Input: Spanish audio → Output: English text
```

### 初始提示词

```python
# Improve accuracy with context
result = model.transcribe(
    "audio.mp3",
    initial_prompt="This is a technical podcast about machine learning and AI."
)

# Helps with:
# - Technical terms
# - Proper nouns
# - Domain-specific vocabulary
```

### 时间戳

```python
# Word-level timestamps
result = model.transcribe("audio.mp3", word_timestamps=True)

for segment in result["segments"]:
    for word in segment["words"]:
        print(f"{word['word']} ({word['start']:.2f}s - {word['end']:.2f}s)")
```

### 温度值回退机制

```python
# Retry with different temperatures if confidence low
result = model.transcribe(
    "audio.mp3",
    temperature=(0.0, 0.2, 0.4, 0.6, 0.8, 1.0)
)
```

## 命令行使用方式

```bash
# Basic transcription
whisper audio.mp3

# Specify model
whisper audio.mp3 --model turbo

# Output formats
whisper audio.mp3 --output_format txt     # Plain text
whisper audio.mp3 --output_format srt     # Subtitles
whisper audio.mp3 --output_format vtt     # WebVTT
whisper audio.mp3 --output_format json    # JSON with timestamps

# Language
whisper audio.mp3 --language Spanish

# Translation
whisper spanish.mp3 --task translate
```

## 批量处理

```python
import os

audio_files = ["file1.mp3", "file2.mp3", "file3.mp3"]

for audio_file in audio_files:
    print(f"Transcribing {audio_file}...")
    result = model.transcribe(audio_file)

    # Save to file
    output_file = audio_file.replace(".mp3", ".txt")
    with open(output_file, "w") as f:
        f.write(result["text"])
```

## 实时转录功能

```python
# For streaming audio, use faster-whisper
# pip install faster-whisper

from faster_whisper import WhisperModel

model = WhisperModel("base", device="cuda", compute_type="float16")

# Transcribe with streaming
segments, info = model.transcribe("audio.mp3", beam_size=5)

for segment in segments:
    print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
```

## GPU加速功能

```python
import whisper

# Automatically uses GPU if available
model = whisper.load_model("turbo")

# Force CPU
model = whisper.load_model("turbo", device="cpu")

# Force GPU
model = whisper.load_model("turbo", device="cuda")

# 10-20× faster on GPU
```

## 与其他工具的集成

### 字幕生成

```bash
# Generate SRT subtitles
whisper video.mp4 --output_format srt --language English

# Output: video.srt
```

### 集成 LangChain 功能

```python
from langchain.document_loaders import WhisperTranscriptionLoader

loader = WhisperTranscriptionLoader(file_path="audio.mp3")
docs = loader.load()

# Use transcription in RAG
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

vectorstore = Chroma.from_documents(docs, OpenAIEmbeddings())
```

### 从视频中提取音频

```bash
# Use ffmpeg to extract audio
ffmpeg -i video.mp4 -vn -acodec pcm_s16le audio.wav

# Then transcribe
whisper audio.wav
```

## 最佳实践建议

1. **使用 Turbo 模型** – 能为英文内容带来最佳的速度与质量平衡  
2. **明确指定语言** – 比自动检测更快  
3. **添加初始提示词** – 有助于提升技术术语的处理效果  
4. **启用 GPU 加速** – 处理速度可提升 10–20 倍  
5. **批量处理文件** – 提高整体效率  
6. **转换为 WAV 格式** – 增强兼容性  
7. **拆分过长音频** – 每段时长建议控制在 30 分钟以内  
8. **确认语言支持情况** – 不同语言的生成质量可能存在差异  
9. **选用 faster-whisper 模型** – 其速度是 openai-whisper 的 4 倍  
10. **监控显存使用情况** – 根据硬件条件调整模型规模  

## 性能表现

| 模型类型 | CPU 实时处理系数 | GPU 实时处理系数 |
|---------|------------------|------------------|
| tiny    | 约 0.32           | 约 0.01          |
| base    | 约 0.16           | 约 0.01          |
| turbo   | 约 0.08           | 约 0.01          |
| large   | 约 1.0            | 约 0.05          |

*实时处理系数说明：数值为 0.1 表示处理速度是实时处理的 10 倍*

## 支持的语言

最广泛支持的语言包括：
- 英语（en）
- 西班牙语（es）
- 法语（fr）
- 德语（de）
- 意大利语（it）
- 葡萄牙语（pt）
- 俄语（ru）
- 日语（ja）
- 韩语（ko）
- 中文（zh）

完整语言列表：共支持 99 种语言  

## 局限性

1. **幻觉现象** – 可能会出现重复内容或编造文本  
2. **长音频处理精度** – 音频时长超过 30 分钟时精度会下降  
3. **说话人识别功能缺失** – 不支持语音分段  
4. **口音处理效果差异** – 不同口音的生成质量不尽相同  
5. **背景噪音影响** – 可能降低识别准确性  
6. **实时延迟问题** – 不适合用于实时字幕生成  

## 相关资源

- **GitHub 仓库**：https://github.com/openai/whisper ⭐ 72,900+ 次点赞  
- **研究论文**：https://arxiv.org/abs/2212.04356  
- **模型说明文档**：https://github.com/openai/whisper/blob/main/model-card.md  
- **Colab 实验环境**：可在仓库中找到  
- **许可证**：MIT 许可证


