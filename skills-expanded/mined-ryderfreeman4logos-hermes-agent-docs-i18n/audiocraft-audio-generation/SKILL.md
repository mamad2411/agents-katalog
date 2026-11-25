---
name: audiocraft-audio-generation
description: "AudioCraft: MusicGen text-to-music, AudioGen text-to-sound."
version: 1.0.0
author: Orchestra Research
license: MIT
dependencies: [audiocraft, torch>=2.0.0, transformers>=4.30.0]
platforms: [linux, macos]
metadata:
  hermes:
    tags: [Multimodal, Audio Generation, Text-to-Music, Text-to-Audio, MusicGen]

---

# AudioCraft：音频生成

本指南全面介绍了如何使用 Meta 的 AudioCraft，结合 MusicGen、AudioGen 和 EnCodec 实现文本转音乐及文本转音频的生成功能。

## 何时使用 AudioCraft

**以下情况适合使用 AudioCraft：**
- 需要根据文本描述生成音乐
- 制作音效与环境音频
- 开发音乐生成应用
- 需要基于旋律条件的音乐生成
- 希望获得立体声音频输出
- 需要具备风格迁移功能的可控音乐生成

**核心功能：**
- **MusicGen**：支持基于旋律条件的文本转音乐生成
- **AudioGen**：文本转音效生成
- **EnCodec**：高保真神经网络音频编解码器
- **多种模型规模**：从小型（300M）到大型（3.3B）
- **立体声支持**：可生成完整的立体声音频
- **风格控制**：MusicGen-Style 支持基于参考样本的生成

**可选择的其他方案：**
- **Stable Audio**：适用于较长的商业音乐生成需求
- **Bark**：用于结合音乐/音效的文本转语音功能
- **Riffusion**：基于频谱图的音乐生成工具
- **OpenAI Jukebox**：支持带歌词的原始音频生成

## 快速入门

### 安装

```bash
# From PyPI
pip install audiocraft

# From GitHub (latest)
pip install git+https://github.com/facebookresearch/audiocraft.git

# Or use HuggingFace Transformers
pip install transformers torch torchaudio
```

### 基础文本转音乐功能（AudioCraft）

```python
import torchaudio
from audiocraft.models import MusicGen

# Load model
model = MusicGen.get_pretrained('facebook/musicgen-small')

# Set generation parameters
model.set_generation_params(
    duration=8,  # seconds
    top_k=250,
    temperature=1.0
)

# Generate from text
descriptions = ["happy upbeat electronic dance music with synths"]
wav = model.generate(descriptions)

# Save audio
torchaudio.save("output.wav", wav[0].cpu(), sample_rate=32000)
```

### 使用 HuggingFace Transformers 库

```python
from transformers import AutoProcessor, MusicgenForConditionalGeneration
import scipy

# Load model and processor
processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")
model.to("cuda")

# Generate music
inputs = processor(
    text=["80s pop track with bassy drums and synth"],
    padding=True,
    return_tensors="pt"
).to("cuda")

audio_values = model.generate(
    **inputs,
    do_sample=True,
    guidance_scale=3,
    max_new_tokens=256
)

# Save
sampling_rate = model.config.audio_encoder.sampling_rate
scipy.io.wavfile.write("output.wav", rate=sampling_rate, data=audio_values[0, 0].cpu().numpy())
```

### 使用 AudioGen 实现文本转语音功能

```python
from audiocraft.models import AudioGen

# Load AudioGen
model = AudioGen.get_pretrained('facebook/audiogen-medium')

model.set_generation_params(duration=5)

# Generate sound effects
descriptions = ["dog barking in a park with birds chirping"]
wav = model.generate(descriptions)

torchaudio.save("sound.wav", wav[0].cpu(), sample_rate=16000)
```

## 核心概念

### 架构概览

```
AudioCraft Architecture:
┌──────────────────────────────────────────────────────────────┐
│                    Text Encoder (T5)                          │
│                         │                                     │
│                    Text Embeddings                            │
└────────────────────────┬─────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────┐
│              Transformer Decoder (LM)                         │
│     Auto-regressively generates audio tokens                  │
│     Using efficient token interleaving patterns               │
└────────────────────────┬─────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────┐
│                EnCodec Audio Decoder                          │
│        Converts tokens back to audio waveform                 │
└──────────────────────────────────────────────────────────────┘
```

### 模型版本

| 模型 | 参数规模 | 描述 | 适用场景 |
|-------|----------|-------------|----------|
| `musicgen-small` | 300M | 文本转音乐 | 快速生成 |
| `musicgen-medium` | 1.5B | 文本转音乐 | 平衡性能 |
| `musicgen-large` | 3.3B | 文本转音乐 | 最高质量 |
| `musicgen-melody` | 1.5B | 文本+旋律 | 基于旋律的生成 |
| `musicgen-melody-large` | 3.3B | 文本+旋律 | 最佳旋律效果 |
| `musicgen-stereo-*` | 规模不一 | 立体声输出 | 立体声音乐生成 |
| `musicgen-style` | 1.5B | 风格迁移 | 基于参考样本的风格转换 |
| `audiogen-medium` | 1.5B | 文本转声音 | 制作音效 |

### 生成参数

| 参数 | 默认值 | 描述 |
|-----------|---------|-------------|
| `duration` | 8.0 | 时长（秒），范围为1-120秒 |
| `top_k` | 250 | 前k个样本采样 |
| `top_p` | 0.0 | 核心采样算法（0表示禁用） |
| `temperature` | 1.0 | 采样温度系数 |
| `cfg_coef` | 3.0 | 无分类器引导机制 |

## MusicGen使用指南

### 文本转音乐生成

```python
from audiocraft.models import MusicGen
import torchaudio

model = MusicGen.get_pretrained('facebook/musicgen-medium')

# Configure generation
model.set_generation_params(
    duration=30,          # Up to 30 seconds
    top_k=250,            # Sampling diversity
    top_p=0.0,            # 0 = use top_k only
    temperature=1.0,      # Creativity (higher = more varied)
    cfg_coef=3.0          # Text adherence (higher = stricter)
)

# Generate multiple samples
descriptions = [
    "epic orchestral soundtrack with strings and brass",
    "chill lo-fi hip hop beat with jazzy piano",
    "energetic rock song with electric guitar"
]

# Generate (returns [batch, channels, samples])
wav = model.generate(descriptions)

# Save each
for i, audio in enumerate(wav):
    torchaudio.save(f"music_{i}.wav", audio.cpu(), sample_rate=32000)
```

### 基于旋律条件的生成

```python
from audiocraft.models import MusicGen
import torchaudio

# Load melody model
model = MusicGen.get_pretrained('facebook/musicgen-melody')
model.set_generation_params(duration=30)

# Load melody audio
melody, sr = torchaudio.load("melody.wav")

# Generate with melody conditioning
descriptions = ["acoustic guitar folk song"]
wav = model.generate_with_chroma(descriptions, melody, sr)

torchaudio.save("melody_conditioned.wav", wav[0].cpu(), sample_rate=32000)
```

### 立体声生成

```python
from audiocraft.models import MusicGen

# Load stereo model
model = MusicGen.get_pretrained('facebook/musicgen-stereo-medium')
model.set_generation_params(duration=15)

descriptions = ["ambient electronic music with wide stereo panning"]
wav = model.generate(descriptions)

# wav shape: [batch, 2, samples] for stereo
print(f"Stereo shape: {wav.shape}")  # [1, 2, 480000]
torchaudio.save("stereo.wav", wav[0].cpu(), sample_rate=32000)
```

### 音频续传功能

```python
from transformers import AutoProcessor, MusicgenForConditionalGeneration

processor = AutoProcessor.from_pretrained("facebook/musicgen-medium")
model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-medium")

# Load audio to continue
import torchaudio
audio, sr = torchaudio.load("intro.wav")

# Process with text and audio
inputs = processor(
    audio=audio.squeeze().numpy(),
    sampling_rate=sr,
    text=["continue with a epic chorus"],
    padding=True,
    return_tensors="pt"
)

# Generate continuation
audio_values = model.generate(**inputs, do_sample=True, guidance_scale=3, max_new_tokens=512)
```

## MusicGen-Style 使用指南

### 基于风格的生成

```python
from audiocraft.models import MusicGen

# Load style model
model = MusicGen.get_pretrained('facebook/musicgen-style')

# Configure generation with style
model.set_generation_params(
    duration=30,
    cfg_coef=3.0,
    cfg_coef_beta=5.0  # Style influence
)

# Configure style conditioner
model.set_style_conditioner_params(
    eval_q=3,          # RVQ quantizers (1-6)
    excerpt_length=3.0  # Style excerpt length
)

# Load style reference
style_audio, sr = torchaudio.load("reference_style.wav")

# Generate with text + style
descriptions = ["upbeat dance track"]
wav = model.generate_with_style(descriptions, style_audio, sr)
```

### 仅生成样式（无文本内容）

```python
# Generate matching style without text prompt
model.set_generation_params(
    duration=30,
    cfg_coef=3.0,
    cfg_coef_beta=None  # Disable double CFG for style-only
)

wav = model.generate_with_style([None], style_audio, sr)
```

## AudioGen 使用指南

### 音效生成

```python
from audiocraft.models import AudioGen
import torchaudio

model = AudioGen.get_pretrained('facebook/audiogen-medium')
model.set_generation_params(duration=10)

# Generate various sounds
descriptions = [
    "thunderstorm with heavy rain and lightning",
    "busy city traffic with car horns",
    "ocean waves crashing on rocks",
    "crackling campfire in forest"
]

wav = model.generate(descriptions)

for i, audio in enumerate(wav):
    torchaudio.save(f"sound_{i}.wav", audio.cpu(), sample_rate=16000)
```

## EnCodec 使用指南

### 音频压缩

```python
from audiocraft.models import CompressionModel
import torch
import torchaudio

# Load EnCodec
model = CompressionModel.get_pretrained('facebook/encodec_32khz')

# Load audio
wav, sr = torchaudio.load("audio.wav")

# Ensure correct sample rate
if sr != 32000:
    resampler = torchaudio.transforms.Resample(sr, 32000)
    wav = resampler(wav)

# Encode to tokens
with torch.no_grad():
    encoded = model.encode(wav.unsqueeze(0))
    codes = encoded[0]  # Audio codes

# Decode back to audio
with torch.no_grad():
    decoded = model.decode(codes)

torchaudio.save("reconstructed.wav", decoded[0].cpu(), sample_rate=32000)
```

## 常见工作流程

### 工作流程 1：音乐生成流程

```python
import torch
import torchaudio
from audiocraft.models import MusicGen

class MusicGenerator:
    def __init__(self, model_name="facebook/musicgen-medium"):
        self.model = MusicGen.get_pretrained(model_name)
        self.sample_rate = 32000

    def generate(self, prompt, duration=30, temperature=1.0, cfg=3.0):
        self.model.set_generation_params(
            duration=duration,
            top_k=250,
            temperature=temperature,
            cfg_coef=cfg
        )

        with torch.no_grad():
            wav = self.model.generate([prompt])

        return wav[0].cpu()

    def generate_batch(self, prompts, duration=30):
        self.model.set_generation_params(duration=duration)

        with torch.no_grad():
            wav = self.model.generate(prompts)

        return wav.cpu()

    def save(self, audio, path):
        torchaudio.save(path, audio, sample_rate=self.sample_rate)

# Usage
generator = MusicGenerator()
audio = generator.generate(
    "epic cinematic orchestral music",
    duration=30,
    temperature=1.0
)
generator.save(audio, "epic_music.wav")
```

### 工作流 2：声音设计批量处理

```python
import json
from pathlib import Path
from audiocraft.models import AudioGen
import torchaudio

def batch_generate_sounds(sound_specs, output_dir):
    """
    Generate multiple sounds from specifications.

    Args:
        sound_specs: list of {"name": str, "description": str, "duration": float}
        output_dir: output directory path
    """
    model = AudioGen.get_pretrained('facebook/audiogen-medium')
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    results = []

    for spec in sound_specs:
        model.set_generation_params(duration=spec.get("duration", 5))

        wav = model.generate([spec["description"]])

        output_path = output_dir / f"{spec['name']}.wav"
        torchaudio.save(str(output_path), wav[0].cpu(), sample_rate=16000)

        results.append({
            "name": spec["name"],
            "path": str(output_path),
            "description": spec["description"]
        })

    return results

# Usage
sounds = [
    {"name": "explosion", "description": "massive explosion with debris", "duration": 3},
    {"name": "footsteps", "description": "footsteps on wooden floor", "duration": 5},
    {"name": "door", "description": "wooden door creaking and closing", "duration": 2}
]

results = batch_generate_sounds(sounds, "sound_effects/")
```

### 工作流 3：Gradio 演示版

```python
import gradio as gr
import torch
import torchaudio
from audiocraft.models import MusicGen

model = MusicGen.get_pretrained('facebook/musicgen-small')

def generate_music(prompt, duration, temperature, cfg_coef):
    model.set_generation_params(
        duration=duration,
        temperature=temperature,
        cfg_coef=cfg_coef
    )

    with torch.no_grad():
        wav = model.generate([prompt])

    # Save to temp file
    path = "temp_output.wav"
    torchaudio.save(path, wav[0].cpu(), sample_rate=32000)
    return path

demo = gr.Interface(
    fn=generate_music,
    inputs=[
        gr.Textbox(label="Music Description", placeholder="upbeat electronic dance music"),
        gr.Slider(1, 30, value=8, label="Duration (seconds)"),
        gr.Slider(0.5, 2.0, value=1.0, label="Temperature"),
        gr.Slider(1.0, 10.0, value=3.0, label="CFG Coefficient")
    ],
    outputs=gr.Audio(label="Generated Music"),
    title="MusicGen Demo"
)

demo.launch()
```

## 性能优化

### 内存优化

```python
# Use smaller model
model = MusicGen.get_pretrained('facebook/musicgen-small')

# Clear cache between generations
torch.cuda.empty_cache()

# Generate shorter durations
model.set_generation_params(duration=10)  # Instead of 30

# Use half precision
model = model.half()
```

### 批量处理效率

```python
# Process multiple prompts at once (more efficient)
descriptions = ["prompt1", "prompt2", "prompt3", "prompt4"]
wav = model.generate(descriptions)  # Single batch

# Instead of
for desc in descriptions:
    wav = model.generate([desc])  # Multiple batches (slower)
```

### GPU内存需求

| 模型 | FP32显存需求 | FP16显存需求 |
|-------|-----------|-----------|
| musicgen-small | 约4GB | 约2GB |
| musicgen-medium | 约8GB | 约4GB |
| musicgen-large | 约16GB | 约8GB |

## 常见问题

| 问题 | 解决方案 |
|-------|----------|
| CUDA内存不足 | 使用较小规模的模型，缩短生成时长 |
| 生成质量不佳 | 提高cfg_coef参数值，优化提示词 |
| 生成内容过短 | 检查最大生成时长设置 |
| 音频存在杂音 | 尝试调整温度参数 |
| 立体声功能失效 | 使用立体声版本的模型 |

## 参考资料

- **[高级用法](references/advanced-usage.md)** - 训练、微调与部署指南
- **[故障排除](references/troubleshooting.md)** - 常见问题及解决方案

## 资源链接

- **GitHub仓库**：https://github.com/facebookresearch/audiocraft
- **MusicGen相关论文**：https://arxiv.org/abs/2306.05284
- **AudioGen相关论文**：https://arxiv.org/abs/2209.15352
- **HuggingFace页面**：https://huggingface.co/facebook/musicgen-small
- **演示页面**：https://huggingface.co/spaces/facebook/MusicGen
