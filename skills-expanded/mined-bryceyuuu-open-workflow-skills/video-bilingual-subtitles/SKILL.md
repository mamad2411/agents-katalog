---
name: video-bilingual-subtitles
description: "Transcribe video or audio, translate captions, align timestamps, and export SRT/ASS or hardcoded video. Use when the user asks for video bilingual subtitles or an equivalent workflow."
license: MIT
compatibility: "Cross-agent Agent Skills format. Core stack: FFmpeg / faster-whisper / optional translation API. Check runtime dependencies before execution."
metadata:
  project: "open-workflow-skills"
  version: "2.0.0"
  category: "content-media"
  status: "verified"
  implementation-status: "tested-reference"
  automation-level: "L2-L3"
  search-keywords: "video-bilingual-subtitles, Video Bilingual Subtitles, 视频双语字幕, AI subtitle generator, automatic subtitles, bilingual subtitles, video transcription, SRT generator, 中英双语字幕, 视频自动字幕, 视频转文字, AI content automation, content automation, video automation"
  quality-score: "4.5/5"
---
# Video Bilingual Subtitles / 视频双语字幕

## Purpose / 用途

**中文**

完成音轨提取、转写、翻译、时间轴校准和字幕渲染，可输出 SRT、ASS 或硬字幕视频。

**English**

Transcribe video or audio, translate captions, align timestamps, and export SRT/ASS or hardcoded video.

## Status / 状态

- **Workflow status:** 🟢 Verified Workflow / 已验证工作流
- **Implementation:** ✅ Tested reference implementation / 已测试参考实现
- **Audit grade:** A
- **Quality score:** 4.5/5
- **Automation level:** L2-L3
- **Category:** Content & Media / 内容创作与媒体

> Workflow status describes how well the workflow itself is understood. Implementation status separately tells you whether this repository ships runnable code for it. Integration skills still require external services or authorization; experimental skills may need more human review.

## Search aliases / 搜索关键词

`video-bilingual-subtitles` · `Video Bilingual Subtitles` · `视频双语字幕` · `AI subtitle generator` · `automatic subtitles` · `bilingual subtitles` · `video transcription` · `SRT generator` · `中英双语字幕` · `视频自动字幕` · `视频转文字` · `AI content automation` · `content automation` · `video automation`

## When to use / 何时使用

Use this skill when the user explicitly requests **video bilingual subtitles**, or when the requested outcome clearly matches this workflow.

Do not activate it merely because the topic is related. Confirm the input, desired output, and any consequential external action.

## Inputs / 输入

- Video/audio file or URL
- Desired language/style/output constraints

## Outputs / 输出

- Transcript JSON
- SRT/ASS captions
- Optional rendered video

## Core stack / 核心工具

`FFmpeg / faster-whisper / optional translation API`

## Permissions / 权限

- `filesystem:read`
- `filesystem:write`
- `network:optional`

Treat permissions as capabilities to request or verify, **not as permissions automatically granted by installing the skill**.

## Workflow / 工作流

1. **Probe or load timestamped transcript**
2. **Transcribe media when an ASR backend is available**
3. **Validate monotonic timestamps**
4. **Apply optional bilingual translations**
5. **Generate UTF-8 SRT**
6. **Optionally burn subtitles with FFmpeg**
7. **Verify subtitle timing and output existence**

## Dependency suggestions / 依赖建议

- macOS: `brew install ffmpeg`
- Ubuntu/Debian: `sudo apt-get update && sudo apt-get install -y ffmpeg`
- Local ASR: `python3 -m pip install faster-whisper`

The Agent Skill itself should remain installable even when optional runtimes are absent. Report missing runtime dependencies instead of silently installing privileged software.

## Runnable reference / 可运行参考实现

This skill ships a tested reference runtime in `scripts/run.py`. From a cloned repository:

```bash
ows doctor video-bilingual-subtitles
ows run video-bilingual-subtitles -- --help
ows test video-bilingual-subtitles
```

`runtime.json` declares the entrypoint and optional system commands. Runtime dependencies are checked separately from installing the Skill definition.

## Install / 安装

### Inspect before installing

```bash
npx skills add BryceYuuu/open-workflow-skills --list
```

### Install this skill into the current project

```bash
npx skills add BryceYuuu/open-workflow-skills --skill video-bilingual-subtitles
```

### Install for a specific supported agent

```bash
npx skills add BryceYuuu/open-workflow-skills --skill video-bilingual-subtitles --agent codex
```

`npx skills` is a community ecosystem CLI, not an OpenAI-official installer. Review third-party skills and scripts before granting shell, filesystem, network, or credential access.

## Example invocation / 调用示例

**中文**

> 使用 `video-bilingual-subtitles` 工作流处理我提供的输入。先检查依赖和权限，不覆盖源文件；执行后给我输出路径、验证结果和需要人工审核的部分。

**English**

> Use the `video-bilingual-subtitles` workflow for the provided input. Check dependencies and permissions first, preserve the source, validate the result, and report outputs plus any human-review items.

## Validation / 验证

At minimum:

- Verify all expected outputs exist and are readable.
- Verify the source was not unintentionally overwritten.
- Verify structured outputs against their expected schema or invariants.
- Record warnings, skipped steps, external dependencies, and failed checks.
- Never mark the workflow successful solely because a model produced text.

See `references/QUALITY.md` for skill-specific quality expectations.

## Safety / 安全

- Do not invent source facts or claim an external action succeeded without verification.
- Preserve source files unless the user explicitly requests in-place modification.
- Surface missing dependencies, permissions, credentials, and failed checks clearly.

## Failure handling / 失败处理

If a dependency, credential, connected service, browser session, file, or required permission is unavailable:

1. Stop the affected step.
2. Preserve completed safe outputs.
3. State exactly what is missing.
4. Do not fabricate a successful result.
5. Suggest the minimum next action needed to continue.

## Files / 文件

- `SKILL.md` — workflow instructions
- `references/QUALITY.md` — quality/evaluation guidance
- `tests/cases.yaml` — example evaluation cases

- `runtime.json` — runtime manifest
- `scripts/run.py` — runnable reference implementation
- `tests/smoke.py` — deterministic smoke test
