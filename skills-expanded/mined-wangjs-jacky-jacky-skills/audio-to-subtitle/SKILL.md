---
name: audio-to-subtitle
description: "音视频转字幕工具。当用户需要将 mp3/wav/m4a/mp4 等音视频文件转录为 SRT/VTT/TXT/MD 字幕格式时触发。支持本地 MLX-Whisper 和豆包云端两种引擎，交互式选择。"
---

<role>
你是音频转字幕专家，擅长利用 Apple Silicon 的 MLX 框架和国产云端 ASR 服务，将音频文件高效转录为高质量字幕。
</role>

<purpose>
当用户需要将本地音视频文件（mp3/wav/m4a/mp4/mkv 等）转录为字幕文件（SRT/VTT/TXT/MD）时，提供一站式转录方案。支持本地 MLX-Whisper（隐私、免费、快速）和豆包云端（中文优化、大模型 ASR）两种引擎。
</purpose>

<trigger>
```
音频转字幕
把这段音频转成文字
音频转录
生成字幕文件
audio to subtitle
转录音频
mp3 转 srt
语音转文字
音频转写
```
</trigger>

<gsd:workflow>
  <gsd:meta>
    <name>audio-to-subtitle</name>
    <owner>video-processing</owner>
    <requires>python3, mlx-whisper, ffmpeg, AskUserQuestion</requires>
    <checkpoints>
      <checkpoint order="1">环境依赖检查通过</checkpoint>
      <checkpoint order="2">音频文件存在且格式支持</checkpoint>
      <checkpoint order="3">用户明确选择转录引擎</checkpoint>
      <checkpoint order="4">用户确认输出格式</checkpoint>
    </checkpoints>
    <constraints>
      <constraint>引擎选择不可默认、不可跳过，必须等用户明确选择</constraint>
      <constraint>禁止自动回退：当用户选择的引擎失败时，必须通过 AskUserQuestion 让用户决定下一步，绝对不能自作主张切换引擎</constraint>
      <constraint>云端 API 密钥不得硬编码，必须通过环境变量或配置文件读取</constraint>
      <constraint>长音频（>30min）必须提醒用户分段处理以避免内存压力</constraint>
      <constraint>MacBook Air 无风扇，批量任务建议串行处理避免过热降频</constraint>
    </constraints>
  </gsd:meta>

  <gsd:goal>将用户指定的音频文件转录为目标格式的字幕文件，输出到指定目录。</gsd:goal>

  <!-- ==================== Phase 1: 环境检查 ==================== -->
  <gsd:phase name="precheck" order="1">
    <gsd:step>并行检查 Python3、mlx-whisper、ffmpeg 是否已安装</gsd:step>
    <gsd:step>检查引擎配置状态：
      - 本地引擎：验证 MLX-Whisper 模型是否可用（尝试加载默认模型）
      - 豆包引擎：检查 API 凭证是否存在（~/.audio2subtitle/config.json 或环境变量）
    </gsd:step>
    <gsd:step>确认输入音频/视频文件路径和格式（注意文件名中的特殊字符如 #）</gsd:step>
    <gsd:step>获取文件时长信息，如 >30min 则提醒用户</gsd:step>
    <gsd:checkpoint>环境依赖就绪，引擎配置验证通过，音频文件可访问</gsd:checkpoint>
  </gsd:phase>

  <!-- ==================== Phase 2: 参数配置（3 步顺序交互） ==================== -->
  <gsd:phase name="config" order="2">

    <!-- Step 1: 引擎选择（独立的交互步骤） -->
    <gsd:step>
      📝 【Step 1/3：选择引擎 — 必须单独执行，不可合并】

      使用 AskUserQuestion 让用户选择转录引擎：
      - local：本地 MLX-Whisper（免费、快速、隐私保护，Apple Silicon 优化）
      - doubao：豆包云端 ASR（中文优化、大模型增强，适合高难度音频）

      规则：
      - 此步骤不可跳过、不可默认选择
      - 必须等待用户明确选择后才进入下一步
      - 禁止在这一步同时询问模型、格式等其他问题
    </gsd:step>

    <!-- Step 2: 引擎相关配置（分支逻辑） -->
    <gsd:step>
      🔄 【Step 2/3：引擎相关配置 — 根据选择分支处理】

      【分支 A - 用户选择 local】：
        1. 使用 AskUserQuestion 选择 Whisper 模型：
           - large-v3-turbo（推荐，最快，准确率很高）
           - large-v3（最佳准确率，稍慢）
           - medium（轻量任务）
        2. 继续进入 Step 3

      【分支 B - 用户选择 doubao】：
        1. 检查豆包 API 凭证（~/.audio2subtitle/config.json 或环境变量 DOUBAO_APP_ID / DOUBAO_ACCESS_TOKEN）
        2. 如果凭证缺失 → 🛑 Human-Action 检查点：引导用户配置凭证
           方式一（推荐）：运行 python3 scripts/transcribe.py --setup-doubao
           方式二：手动写入 ~/.audio2subtitle/config.json
           配置完成后验证文件写入成功
        3. 凭证就绪 → 跳过模型选择，直接进入 Step 3
    </gsd:step>

    <!-- Step 3: 通用配置 -->
    <gsd:step>
      📝 【Step 3/3：输出格式】

      使用 AskUserQuestion 选择输出格式：
      - MD（推荐，带时间轴，适合笔记整理）
      - SRT（通用字幕格式）
      - VTT（Web 字幕格式）
      - TXT（纯文本，无时间戳）
    </gsd:step>

    <gsd:step>确认输出目录（默认与音频同目录）</gsd:step>

    <gsd:checkpoint>用户已确认所有转录参数</gsd:checkpoint>
  </gsd:phase>

  <!-- ==================== Phase 3: 转录执行 ==================== -->
  <gsd:phase name="transcribe" order="3">
    <gsd:step>展示参数确认表（引擎 / 模型 / 格式 / 输出目录 / 时长）</gsd:step>
    <gsd:step>执行转录脚本（加 --yolo 跳过脚本内交互，因为 Claude 侧已完成交互确认）</gsd:step>

    <!-- 错误处理：豆包 API 失败 -->
    <gsd:step>
      🛑 【豆包 API 失败时 — Decision 检查点，禁止自动回退】

      当豆包引擎转录失败（DoubaoApiError）时，按以下流程处理：

      1. ✅ 展示诊断报告（脚本已输出到 stderr）
      2. ✅ 解释错误原因：
         - 凭证未配置 → 说明需要获取 APP ID 和 Access Token
         - 认证失败 → 提示检查凭证是否正确
         - resource not granted → 说明火山引擎账号未开通对应服务，提供控制台链接：
           https://console.volcengine.com/speech/service/subscription
      3. 🔄 使用 AskUserQuestion 让用户选择下一步（Decision 检查点）：
         - 选项 A：去开通服务，修复豆包配置后重试
         - 选项 B：改用本地 MLX-Whisper 引擎转录
         - 选项 C：取消本次操作
      4. 根据用户选择执行（不是自动决定）

      绝对禁止的行为：
      - ❌ 未经用户同意自动回退到另一个引擎
      - ❌ 在用户不知情的情况下切换引擎
      - ❌ 假设用户想用本地引擎"先完成再说"
    </gsd:step>

    <gsd:step>处理完成后验证输出文件完整性</gsd:step>
    <gsd:checkpoint>转录完成，字幕文件已生成</gsd:checkpoint>
  </gsd:phase>

  <!-- ==================== Phase 4: 输出交付 ==================== -->
  <gsd:phase name="deliver" order="4">
    <gsd:step>报告输出文件路径、大小和段落数</gsd:step>
    <gsd:step>展示字幕前几行预览</gsd:step>
    <gsd:step>如质量不佳，建议切换引擎或模型重新转录</gsd:step>
  </gsd:phase>
</gsd:workflow>

# Audio to Subtitle - 音频转字幕工具

基于 Apple Silicon MLX 框架的高性能音频转字幕工具，支持本地和云端混合转录。

## ⚠️ 用户交互点总结

| 阶段 | 标记 | 交互内容 | 检查点类型 |
|------|------|----------|------------|
| Phase 1 | ✅ | 环境检查结果 | auto-verify |
| Phase 2 Step 1 | 📝 | 选择转录引擎（local / doubao） | decision |
| Phase 2 Step 2A | 📝 | 选择 Whisper 模型（仅 local 引擎） | decision |
| Phase 2 Step 2B | 🛑 | 配置豆包 API 凭证（仅 doubao 引擎、凭证缺失时） | human-action |
| Phase 2 Step 3 | 📝 | 选择输出格式（MD / SRT / VTT / TXT） | decision |
| Phase 3 | 🔄 | 豆包失败时选择下一步（仅 doubao 引擎、失败时） | decision |
| Phase 4 | ✅ | 验证输出结果 | auto-verify |

**LLM 执行提示**：
- 🛑 → **必须等待用户完成操作**（如配置 API 凭证），不能跳过
- 📝 → **需要用户输入**，使用 AskUserQuestion
- ✅ → **自动验证后报告结果**，不需要用户操作
- 🔄 → **需要用户选择**，提供选项，不能自动决定

## 核心架构

```
音频文件 → ffmpeg 预处理 → MLX-Whisper / 豆包 ASR → 格式化 → SRT/VTT/TXT/MD
                                                          ↕
                                                自动分段（长音频）
```

## 环境要求

| 依赖 | 安装方式 | 说明 |
|------|----------|------|
| Python 3.10+ | `brew install python` | 运行时 |
| mlx-whisper | `pip install mlx-whisper` | Apple Silicon 优化的 Whisper |
| ffmpeg | `brew install ffmpeg` | 音频格式转换 |
| MLX 模型 | 首次运行自动下载 | HuggingFace 托管 |

### 首次安装

```bash
# 优先使用 Agent 当前加载到的 Skill 目录；也可显式设置该变量。
AUDIO_TO_SUBTITLE_SKILL_DIR="${AUDIO_TO_SUBTITLE_SKILL_DIR:-}"
if [ -z "$AUDIO_TO_SUBTITLE_SKILL_DIR" ]; then
  for candidate in \
    "$HOME/.j-skills/linked/audio-to-subtitle" \
    "$HOME/.claude/skills/audio-to-subtitle" \
    "$HOME/.codex/skills/audio-to-subtitle" \
    "$HOME/.agents/skills/audio-to-subtitle"; do
    if [ -f "$candidate/scripts/setup.sh" ]; then
      AUDIO_TO_SUBTITLE_SKILL_DIR="$candidate"
      break
    fi
  done
fi

[ -n "$AUDIO_TO_SUBTITLE_SKILL_DIR" ] || {
  echo "未找到 audio-to-subtitle；请设置 AUDIO_TO_SUBTITLE_SKILL_DIR" >&2
  exit 1
}
bash "$AUDIO_TO_SUBTITLE_SKILL_DIR/scripts/setup.sh"
```

或手动安装：

```bash
pip install mlx-whisper
brew install ffmpeg
```

## 支持格式

### 输入

| 格式 | 扩展名 | 说明 |
|------|--------|------|
| MP3 | `.mp3` | 最常见音频 |
| WAV | `.wav` | 无损音频 |
| M4A | `.m4a` | Apple 常用 |
| FLAC | `.flac` | 无损压缩 |
| MP4 | `.mp4` | 视频（自动提取音频） |
| MKV | `.mkv` | 视频（自动提取音频） |
| MOV | `.mov` | Apple 视频 |
| WebM | `.webm` | 网页视频 |

### 输出

| 格式 | 扩展名 | 说明 |
|------|--------|------|
| SRT | `.srt` | 通用字幕格式 |
| VTT | `.vtt` | Web 字幕格式 |
| TXT | `.txt` | 纯文本（无时间戳） |
| MD | `.md` | Markdown（带时间轴） |

## 转录引擎

### 本地引擎：MLX-Whisper

| 模型 | 内存占用 | 速度 | 准确率 | 适用场景 |
|------|---------|------|--------|---------|
| **large-v3-turbo** | ~3GB | ⚡ 最快 | 很好 | **首选**，日常使用 |
| large-v3 | ~4GB | 很快 | 最佳 | 极致准确率 |
| medium | ~2GB | 快 | 良好 | 轻量任务 |

> **Apple Silicon 优势**：24GB 统一内存直接当显存用，无需 GPU 数据拷贝，比原版 Whisper 快 4-70 倍。

### 云端引擎：豆包（可选）

> **必须开通以下服务才能使用豆包引擎**

#### 必须开通的服务

在火山引擎控制台开通：https://console.volcengine.com/speech/service/subscription

| 服务名称 | resource_id | 价格 | 说明 |
|---------|-------------|------|------|
| **豆包大模型语音识别 - 录音文件识别（模型 2.0）** | `volc.seedasr.auc` | 按量计费 | **必须开通**，标准版 API，支持 base64 直传 |

> 新用户有免费额度。支持最长 2 小时音频。
>
> ⚠️ 注意：开通「大模型语音识别」后，需要在「应用管理」中将应用绑定到该服务。
> 应用管理页面：https://console.volcengine.com/speech/app

#### 不需要开通的服务（脚本已不再使用）

| 服务名称 | resource_id | 状态 |
|---------|-------------|------|
| 大模型录音文件极速版 | `volc.bigasr.auc_turbo` | 不再使用 |
| 录音文件识别（模型 1.0） | `volc.bigasr.auc` | 不可用 |

### 豆包 API 注册指南

1. 访问 https://www.volcengine.com 注册并实名认证
2. 进入 https://console.volcengine.com/speech/service/subscription
3. **开通「豆包大模型语音识别 - 录音文件识别（模型 2.0）」服务** ← 这是必须的
4. 进入 https://console.volcengine.com/speech/app 创建应用，获取 **APP ID** 和 **Access Token**
5. 确保应用已绑定到开通的服务
6. 配置凭证（三选一）：
   - 运行 `python3 scripts/transcribe.py --setup-doubao` 交互式输入
   - 写入 `~/.audio2subtitle/config.json`
   - 设置环境变量 `DOUBAO_APP_ID` + `DOUBAO_ACCESS_TOKEN`

## 使用方式

### 交互模式（推荐）

```bash
# 直接运行，会先确认参数再执行
python3 scripts/transcribe.py audio.mp3
```

### YOLO 模式（跳过交互）

```bash
# 跳过交互，默认使用本地引擎 local
python3 scripts/transcribe.py audio.mp3 --yolo
```

### 单文件转录

```bash
python3 scripts/transcribe.py audio.mp3 -f vtt
python3 scripts/transcribe.py audio.mp3 -m large-v3
python3 scripts/transcribe.py audio.mp3 -o ~/Desktop/subtitles/
python3 scripts/transcribe.py audio.mp3 --engine doubao
python3 scripts/transcribe.py audio.mp3 -l zh
```

### 命令选项

| 选项 | 简写 | 默认值 | 说明 |
|------|------|--------|------|
| `--format` | `-f` | srt | 输出格式 (srt/vtt/txt/md) |
| `--output` | `-o` | 音频同目录 | 输出目录 |
| `--model` | `-m` | large-v3-turbo | Whisper 模型 |
| `--engine` | `-e` | 交互选择 | 转录引擎 (local/doubao) |
| `--language` | `-l` | auto | 音频语言 (zh/en/ja 等) |
| `--batch` | - | false | 批量处理模式 |
| `--yolo` | - | false | YOLO 模式：跳过交互，默认 local |

## MacBook Air 特别注意事项

1. **散热**：无风扇设计，长时间满载会降频，批量任务建议串行处理
2. **内存**：24GB 足够运行 large-v3 模型（4-bit 量化后仅需 ~4GB）
3. **长音频**：>30 分钟建议分段处理（脚本内置自动分段 15 分钟/段）

## 性能参考（MacBook Air M2 24GB）

| 音频时长 | 模型 | 处理时间 | 实时率 |
|---------|------|---------|--------|
| 5 分钟 | large-v3-turbo | ~5 秒 | ~60x |
| 10 分钟 | large-v3-turbo | ~10 秒 | ~60x |
| 30 分钟 | large-v3-turbo | ~30 秒 | ~60x |
| 60 分钟 | large-v3-turbo | ~60 秒 | ~60x |
| 10 分钟 | large-v3 | ~20 秒 | ~30x |

<reference>
  <ref id="audio-to-subtitle-doc" path="SKILL.md" required="false">
    完整的 audio-to-subtitle 使用文档，包含环境要求、支持格式、转录引擎说明和使用方式。
  </ref>
  <ref id="mlx-whisper" url="https://github.com/ml-explore/mlx-examples/tree/main/whisper" required="false">
    MLX-Whisper 官方文档 - Apple Silicon 优化的 Whisper 实现。
  </ref>
  <ref id="doubao-asr" url="https://www.volcengine.com/docs/6561" required="false">
    火山引擎豆包语音识别 API 文档。
  </ref>
</reference>
