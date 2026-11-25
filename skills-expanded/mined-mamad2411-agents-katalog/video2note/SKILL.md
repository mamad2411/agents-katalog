---
name: video2note-skill
description: >-
  Turn local video/audio files or Bilibili URLs into three Markdown deliverables
  using fully local speech recognition (Qwen3-ASR on MLX, Apple Silicon): a raw
  transcript, a lightly edited readable version, and a beginner-friendly course
  note. Use when the user mentions video transcription, speech-to-text, 视频转文字,
  B站/Bilibili links, lecture notes from a recording, mlx-qwen3-asr, or asks for
  three-version course materials.
---

# 本地视频 / B 站链接 → ASR → 三版本讲义

把视频转成可检索文字，产出三份文档。**全程本地推理，不调云端 API。**

## 能力边界

| 输入 | 方式 |
| --- | --- |
| 本地视频/音频 | `scripts/transcribe.py` |
| B 站链接 | `scripts/fetch_bilibili.py` → `scripts/transcribe.py` |

| 输出 | 文件 | 执行者 |
| --- | --- | --- |
| ① 原始转录 | `output/<name>.txt` | 脚本 |
| ② 整理版 | `output/<name>_整理版.md` | **Agent** |
| ③ 入门讲义 | `output/<name>_入门讲义.md` | **Agent** |

②③ 需要理解内容与领域术语，**必须由 Agent 撰写**，不要指望 ASR 脚本自动生成。

## 运行前提

仅支持 **Apple Silicon**（MLX 依赖）。首次使用需在 skill 目录内建好虚拟环境：

```bash
cd <skill 目录>          # 本 SKILL.md 所在目录
uv venv --python cpython-3.12-macos-aarch64-none .venv
source .venv/bin/activate
uv pip install -r requirements.txt
brew install ffmpeg
```

## 环境门禁（每次必做）

**所有命令必须在该 `.venv` 内执行**，勿用系统 Anaconda 自带的 `yt-dlp`（实测会 SSL 握手失败）。

```bash
source .venv/bin/activate
export PATH="/opt/homebrew/bin:$PATH"
python scripts/check_env.py     # 校验 arm64 / ffmpeg / yt-dlp / mlx-qwen3-asr
```

`check_env.py` 非 0 退出就先修环境，不要硬着头皮往下跑。

模型路径按以下优先级选一个，转录时用 `--model` 指定：

1. `./models/Qwen3-ASR-0.6B`
2. HF 4bit 缓存 `~/.cache/huggingface/hub/models--mlx-community--Qwen3-ASR-0.6B-4bit/snapshots/<hash>/`

## 端到端：B 站链接

```bash
source .venv/bin/activate
export PATH="/opt/homebrew/bin:$PATH"

# 1. 下载（脚本内部走 python -m yt_dlp）
python scripts/fetch_bilibili.py "https://www.bilibili.com/video/BVxxxx" --outdir videos

# 2. 确认 mp4 已落地（非 iCloud 占位、体积合理）
ls -lh videos/*.mp4

# 3. 转录（--context 填 3–8 个领域专名）
python scripts/transcribe.py videos/*.mp4 \
  --language zh \
  --context "资产 负债 现金流 投资" \
  --model "$SNAP" \
  --outdir output

# 4. 校验 txt → 写 ②③（见 templates.md）
```

会员画质 / 需登录时加 cookies：

```bash
python scripts/fetch_bilibili.py "URL" --cookies cookies.txt
```

## 端到端：本地文件

```bash
python scripts/transcribe.py /path/to/lecture.mp4 \
  --language zh --context "热词" --outdir output
```

超过 30 分钟的长任务挂防休眠，合盖也不掉速：

```bash
python scripts/transcribe.py ... &
caffeinate -is -w $! &
```

## Agent 执行清单

```
- [ ] 0. source .venv/bin/activate + python scripts/check_env.py
- [ ] 1. 获取音源（B 站先 fetch；本地文件检查 iCloud dataless）
- [ ] 2. 转录（--context 与内容相关，勿堆砌过长）
- [ ] 3. 校验 txt（见下表），不合格就排查音轨而不是继续写讲义
- [ ] 4. 写 _整理版.md
- [ ] 5. 写 _入门讲义.md
```

### txt 校验（按音频时长）

| 音频时长 | 正常 txt 体量（中文口播） | 异常信号 |
| --- | --- | --- |
| ~10 min | 5–15 KB | <3 KB，或全文都是热词复读 |
| ~2.5 h | 90–110 KB | <50 KB，或抽样 peak 极低 |

粗算：`txt 字节数 ÷ 音频分钟数` 落在 **800–1200** 属正常口播课。

判定坏音轨时删掉 txt，抽中间 20 秒测 peak（命令见 [reference.md](reference.md)）。

## 三版本写作

完整模板见 [templates.md](templates.md)。

| 版本 | 要点 |
| --- | --- |
| 整理版 | 轻度编辑；保留案例与数字；删热词回声；存疑处加脚注 |
| 入门讲义 | 以 `## 0. 这一讲在讲什么` 起笔；多用表格；结尾要点回顾 + 术语表 |

**短视频**（<15 min）：整理版 10–30KB、入门讲义 5–15KB 即可，不要硬拉长度。

**长课**（~2.5 h）：整理版宜 60–90KB，入门讲义 15–25KB。

## 排错速查

| 现象 | 处理 |
| --- | --- |
| B 站下载报 `SSL EOF` | 没在 `.venv` 里跑，或 yt-dlp 过旧 |
| 下不到 1080P | 正常，会员画质需 `--cookies` |
| txt 极短或只有热词 | 静音/坏音轨，重新下载视频 |
| 文件是 iCloud `dataless` 占位 | 先「保持下载」，或复制到非 iCloud 目录 |

更多见 [reference.md](reference.md)。

## 文件索引

| 路径 | 用途 |
| --- | --- |
| `scripts/check_env.py` | 运行前环境自检 |
| `scripts/transcribe.py` | ffmpeg 抽音频 + MLX ASR + 清洗 |
| `scripts/fetch_bilibili.py` | B 站 URL → 本地 mp4 |
| `scripts/watch_and_transcribe.sh` | 目录监控批量转录 |
| [reference.md](reference.md) | 安装、模型、caffeinate、排错 |
| [templates.md](templates.md) | 三版本 Markdown 模板与听写对照表 |
