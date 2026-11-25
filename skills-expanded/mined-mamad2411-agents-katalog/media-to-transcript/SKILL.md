---
name: media-to-transcript
description: Convert audio/video URLs or local media into corrected Markdown transcripts through Volcengine recording-file ASR 2.0. Reuses the existing video-transcript downloader for Bilibili, Douyin, Xiaohongshu, YouTube, extracts audio when input is video, uploads local audio to R2, splits media longer than 3 minutes into parallel AUC tasks, submits volc.seedasr.auc with compact source context, then performs AI correction with topic/context/glossary. Use when the user asks for "逐字稿", "提取逐字稿", "视频转文字", "音频转文字", "转写", "听写视频", "提取视频文案", or wants a polished transcript.
---

# Media To Transcript

Use this skill to turn audio or video into a final Markdown transcript. The only ASR backend for this skill is Volcengine recording-file recognition 2.0:

- submit endpoint: `https://openspeech.bytedance.com/api/v3/auc/bigmodel/submit`
- query endpoint: `https://openspeech.bytedance.com/api/v3/auc/bigmodel/query`
- resource id: `volc.seedasr.auc`

Do not use another ASR backend for this skill.

## Workflow

1. Run the doctor if this is the first run, after environment changes, or after an error:

```bash
SKILL_DIR="<SKILL_ROOT>/media-to-transcript"
rtk python3 "$SKILL_DIR/scripts/media_to_transcript.py" --doctor
```

2. Run the pipeline from the notes vault root:

```bash
SKILL_DIR="<SKILL_ROOT>/media-to-transcript"
rtk python3 "$SKILL_DIR/scripts/media_to_transcript.py" "<URL或本地媒体路径>" --topic "视频主题或关键词" --language zh-CN
```

The script automatically builds AUC `context` from available media metadata such as title, platform, author, duration, description, and short source URL. It keeps this ASR context under 500 Chinese characters. User-provided `--topic`, `--context`, and `--context-file` are also included in the same 500-character AUC context budget.

For downloaded or local media longer than 180 seconds, the script splits audio into 3-minute chunks, uploads each chunk, submits AUC tasks in parallel, and merges the returned utterances back onto the original timeline.

3. Read the generated `correction-prompt.md` and `raw-transcript.md`.
4. Apply the AI correction rules in `references/correction-guidelines.md`.
5. Save the corrected transcript to the `finalTranscriptTarget` path printed by the script, and show the full transcript to the user unless they explicitly only asked for a file.

## CLI

```bash
SKILL_DIR="<SKILL_ROOT>/media-to-transcript"

# Video URL: download video, extract mp3, upload to R2, then run AUC ASR
rtk python3 "$SKILL_DIR/scripts/media_to_transcript.py" "https://www.bilibili.com/video/BVxxx" --topic "AI 编程工具评测"

# Local audio/video
rtk python3 "$SKILL_DIR/scripts/media_to_transcript.py" "/path/to/audio.mp3" --media-kind audio --topic "访谈"

# Add context or terminology hints for ASR and correction
rtk python3 "$SKILL_DIR/scripts/media_to_transcript.py" video.mp4 \
  --topic "Claude Code 和 Codex 使用经验" \
  --context "技术词: Codex, Claude Code, MCP, HyperFrames, R2" \
  --context-file "AI Wiki/raw/some-material.md"

# Enable Volcengine utterance emotion labels when explicitly useful
rtk python3 "$SKILL_DIR/scripts/media_to_transcript.py" video.mp4 --emotion --topic "访谈"

# Convert an existing AUC result JSON into raw transcript + correction prompt
rtk python3 "$SKILL_DIR/scripts/media_to_transcript.py" --from-asr-json asr/auc-result.json --title "视频标题"
```

## Outputs

Each run writes a timestamped directory under `outputs/` unless `--out-dir` is provided:

- `audio/`: extracted/converted mp3 when the input is video or unsupported audio
- `audio/chunks/`: 3-minute mp3 chunks when media exceeds 180 seconds
- `asr/auc-submit.json` or `asr/auc-submit-001.json`: submitted request metadata, with the API key omitted
- `asr/auc-result.json` or `asr/auc-result-001.json`: raw Volcengine recording-file recognition result
- `asr/auc-result-combined.json`: merged AUC result for multi-chunk runs
- `raw-transcript.md`: transcript-shaped draft generated from AUC utterances
- `correction-prompt.md`: prompt for the AI correction pass
- `transcript.md`: target path for the final corrected transcript
- `run-summary.json`: machine-readable paths and metadata

The final user-facing artifact is `transcript.md`. Do not treat `auc-result.json` as final copy; it is ASR evidence for correction.

## Options

| Option | Description |
|---|---|
| `--title <title>` | Override detected title. |
| `--topic <text>` | Topic/theme used during ASR context and correction. Can be repeated. |
| `--context <text>` | Extra terminology or context for ASR/correction. Can be repeated. |
| `--context-file <path>` | Read extra context from a local file. Can be repeated. |
| `--language <lang>` | ASR language. Default: `zh-CN`. |
| `--speaker` | Request speaker clustering when useful for interviews. |
| `--emotion` | Enable AUC utterance emotion detection. Default: off. |
| `--chunk-seconds <seconds>` | Split downloaded/local audio longer than this. Default: `180`. |
| `--concurrency <n>` | Parallel AUC chunk tasks. Default: `3`. |
| `--media-kind <auto|audio|video>` | Force media kind. Default: `auto`. |
| `--download <auto|always|never>` | Download URL before ASR. Default: `auto`; direct public mp3/wav/ogg URLs may skip download. |
| `--out-dir <path>` | Output directory. Default: skill `outputs/<timestamp>-<title>`. |
| `--r2-prefix <prefix>` | R2 object prefix for uploaded local audio. |
| `--from-asr-json <path>` | Skip download/ASR and build transcript artifacts from an existing AUC result JSON. |
| `--json` | Print machine-readable summary to stdout. |
| `--doctor` | Check dependencies and required env vars. |

## API Setup

Preferred key location is your current workspace `.env.r2`, or any environment file loaded by the script:

```bash
VOLCENGINE_SPEECH_API_KEY=你的新版控制台APIKey
```

Accepted key names:

- `VOLCENGINE_SPEECH_API_KEY` (preferred)
- `VOLCENGINE_AUC_API_KEY`
- `SEEDASR_API_KEY`
- `AUC_API_KEY`

If `--doctor` does not find this API key, use this setup path:

1. Open [录音文件识别服务开通](https://console.volcengine.com/speech/new/setting/activate) and enable “录音文件识别 2.0”.
2. Open [API Key 管理](https://console.volcengine.com/speech/new/setting/apikeys) and create an API Key.
3. Put the key into your workspace `.env.r2` as `VOLCENGINE_SPEECH_API_KEY=...`, or export it in the shell before running the script.

Local files still need R2 because AUC requires a public audio URL:

- `R2_ACCESS_KEY_ID`
- `R2_SECRET_ACCESS_KEY`
- `R2_ACCOUNT_ID`
- `R2_BUCKET`
- `R2_PUBLIC_BASE_URL` or `R2_PUBLIC_URL`

Do not print API keys or copy `.env.r2` values into chat.

## Correction Rules

Before writing `transcript.md`, read `references/correction-guidelines.md`. Core constraints:

- Correct ASR mistakes using topic/context/glossary and the surrounding transcript.
- Preserve spoken meaning, order,口语词, repeated words, and uncertainty.
- Do not summarize, rewrite into article prose, invent missing content, or remove substantive speech.
- Convert ASR utterance fragments into readable transcript paragraphs with section-level timestamps.
- Mark unresolved audio as `[听不清]` instead of guessing.
