---
name: funasr-transcribe
description: >-
  本地语音转文字（FunASR / SenseVoice）。把音频文件（m4a/mp3/wav 等）转成文字，
  可进一步整理成结构化会议记录。完全本地运行、不上传云端、不需要 API Key。
  触发词：转写、语音转文字、录音转写、会议记录、转录、ASR、speech to text。
  不适用于：已有文字内容的编辑。
---

# FunASR 语音转文字 Skill

本地跑的中文语音转写，基于 FunASR + SenseVoiceSmall。**首次使用必须先跑一遍
`setup.sh`** 安装环境；模型在第一次转写时自动下载（约 1.2G），之后离线可用。

## 0. 首次安装（每台机器一次）

```bash
bash <skill目录>/setup.sh
```

它会在 skill 目录下建 `venv/` 并装好 funasr/torch 等依赖。需要 Python 3.9–3.11。
跨平台：macOS（Apple Silicon 走 MPS）、Linux（有 CUDA 走 GPU，否则 CPU）均可。

装完用自带示例自检（会触发首次模型下载，正常）：
```bash
source <skill目录>/venv/bin/activate
python <skill目录>/scripts/transcribe.py <skill目录>/examples/asr_example.wav
# 期望输出：每一天都要快乐。
```

## 1. 转写（核心功能）

```bash
source <skill目录>/venv/bin/activate
python <skill目录>/scripts/transcribe.py 录音.m4a --out 结果.txt
```

`transcribe.py` 已经把以下都处理好了，无需手动操作：
- **任意格式自动转码**：非 16k WAV 会用 ffmpeg（找不到则 macOS afconvert）转码
- **设备自动选择**：MPS → CUDA → CPU
- **模型缓存自适应**：默认放 skill 目录的 `.modelscope/`，可用 `FUNASR_CACHE` 覆盖
- **标点恢复**：默认开启（`--no-punc` 关闭，更快）
- **去语气词**：默认去掉「嗯/啊/呃…」（`--keep-fillers` 保留）

模型组合：`SenseVoiceSmall`（主 ASR，50+ 语言）+ `fsmn-vad`（切分长音频）
+ `punc_ct-transformer`（标点）。

### 说话人分离（`--spk`）

多人对话（会议、访谈、对谈）加 `--spk`，会多加载 cam++ 声纹模型，
把不同说话人按音色聚类，输出带标注：

```bash
python <skill目录>/scripts/transcribe.py 会议.m4a --out 会议.txt --spk
```

```
[说话人1] 下午三点开会。
[说话人2] 好，那我们先讨论第一个议题。
```

- 说话人编号（1/2/3…）由音色自动聚类，对应谁按内容对号入座
- 首次运行会多下载一个声纹模型
- 与 `--out` 可同时用，写入文件同样带标注

## 2. 整理成会议记录（可选，用对话模型自身能力做）

转写出的原始文本可以让当前对话模型润色成结构化记录，标准：

- **保留原始叙事结构**：不改话题顺序和逻辑关系
- **去口语碎句**：合并重复、消除"说一半重说"
- **保留细节**：人名、数字、时间地点不省略
- **按上下文纠错**：修正 ASR 同音误识与被 VAD 切断的术语
  （例：把识别错的英文缩写、专有名词按上下文还原）
- **加结构**：开头 `## 摘要`（时长/字数/核心议题）→ `## 目录` → `### 1.1` 层级小标题

## 速查

```bash
# 安装
bash setup.sh

# 转写（最常用）
source venv/bin/activate
python scripts/transcribe.py audio.m4a --out out.txt

# 不要标点（更快）/ 保留语气词
python scripts/transcribe.py audio.wav --no-punc --keep-fillers
```

## 模型来源

基于 [FunASR](https://github.com/modelscope/FunASR)（阿里达摩院，MIT）+ ModelScope 上的
`iic/SenseVoiceSmall`（ASR）、`fsmn-vad`（切分）、`punc_ct-transformer`（标点）。
模型首次运行自动下载，许可以各自 ModelScope 页面为准。

## 排错

- **首次很慢**：在下模型（1.2G），看 stderr 进度，下完后续就快。
- **2G 下载中断**：重跑转写命令即可，ModelScope 断点续传不会从头来；确认网络 + 约 3G 磁盘。
- **`~/.modelscope` 权限错误**：脚本已把缓存改到 skill 目录；若仍报错，设
  `export FUNASR_CACHE=/可写路径`。
- **macOS Python 3.13 代码签名冲突**：用 3.9–3.11，setup.sh 已优先挑这些版本。
- **没有 ffmpeg 且非 macOS**：先转成 16k WAV，或安装 ffmpeg。
