---
name: happy-dreamina
description: ByteDance Jimeng (Dreamina) image and video generation via the official `dreamina` CLI. Use this skill whenever the user mentions 即梦, Dreamina, Jimeng, or asks to generate images or videos specifically through ByteDance's Jimeng service. Covers text2image, image2image, text2video, image2video, plus async task query and task-history browsing via list_task. Trigger this skill instead of happy-image-gen or happy-video-gen whenever the user explicitly names 即梦 or dreamina — it uses browser-based login (`dreamina login`) rather than API keys and has access to Jimeng-exclusive models. Common phrases include "用即梦画张...", "Jimeng generate a video of...", "Dreamina 文生视频", "用 dreamina CLI 做图", "查下我即梦的历史任务".
version: 0.1.0
---

# happy-dreamina

Generate images and videos through ByteDance's official `dreamina` CLI. This skill is a thin instruction layer — it does not wrap any SDK. Every action maps to a `dreamina` subcommand the user's shell already has.

## When to invoke this skill

Use this skill whenever any of these hold:

- The user says **即梦**, **Jimeng**, or **Dreamina** (any language).
- The user explicitly names the `dreamina` CLI or its subcommands.
- The user asks about their Jimeng task history, account credit, or login status.

If the user just says "generate an image" or "画张图" **without naming Jimeng**, prefer `happy-image-gen` / `happy-video-gen` instead and do NOT trigger this skill. The reason is that Jimeng uses browser login and is one specific provider — other skills let the user pick from many providers via EXTEND.md defaults.

## Step 0: Preflight (BLOCKING — run both checks before anything else)

Run these in parallel:

1. `command -v dreamina` — is the binary installed?
2. `dreamina user_credit` — is the login alive? A healthy response is JSON containing credit info.

### If `dreamina` is not installed

Tell the user the `dreamina` CLI is missing and offer to install it. The official installer is:

```bash
curl -fsSL https://jimeng.jianying.com/cli | bash
```

This is a **shell install that writes to the user's machine** — do not run it silently. Confirm, then run it, then re-check `command -v dreamina`. See `references/install-and-login.md` for platform notes (macOS, Linux x86_64/arm64). For any other platform (e.g. Windows) or when the installer changes, point the user at the official install page: https://jimeng.jianying.com/ai-tool/install.

### If `user_credit` fails (exit non-zero, or JSON missing credit)

The user is not logged in, or the token expired. Ask them to run:

```bash
dreamina login
```

This opens the default browser for Jimeng authorization. Credentials land in `~/.dreamina_cli/credential.json` automatically — the user never handles the file. If the browser does not open or the flow hangs, escalate to `dreamina login --debug` (see `references/troubleshooting.md`).

**Do not proceed to generation until `dreamina user_credit` succeeds.**

## Step 1: Pick the right subcommand

Map the user's intent to exactly one subcommand:

| User wants to… | Command |
|---|---|
| Generate an image from text | `dreamina text2image` |
| Transform or restyle an existing image | `dreamina image2image` |
| Generate a video from text | `dreamina text2video` |
| Animate a still image (i2v) | `dreamina image2video` |
| Fetch an earlier async result | `dreamina query_result` |
| Browse past jobs | `dreamina list_task` |

## Step 2: Fill in parameters from the user's intent

Use `references/ratio-resolution-map.md` to convert natural language ("竖屏 / 1080P / 高清 / 方图 / 横屏") to flags. Pay attention to what the user did **not** say — fill in safe defaults, do not ask the user to restate obvious things.

### Image generation — `text2image` / `image2image`
- `--prompt="..."` — always double-quote so shell metacharacters (Chinese quotes, commas) do not break.
- `--ratio` — `1:1 / 16:9 / 9:16 / 3:4 / 4:3`. Default `1:1`.
- `--resolution_type` — `1k / 2k / 4k`. Default `2k`; use `1k` for fast draft, `4k` only when the user asks for ultra or print-ready.
- For `image2image` only: **`--images <path>`** (plural — accepts a reference bundle, multiple paths space-separated).
- Always include `--poll=30`.

### Video generation — `text2video` / `image2video`
- `--prompt="..."` — same quoting rule.
- `--duration` — integer seconds. Default `5`.
- `--ratio` — default `16:9` for landscape intent, `9:16` for vertical, `1:1` for square.
- `--video_resolution` — `480P / 720P / 1080P`. Default `720P`.
- For `image2video` only: **`--image <path>`** (singular — a single keyframe).
- Always include `--poll=60` (videos take longer than images).

> ⚠ **Easy to confuse**: `image2image` uses `--images` (plural, reference bundle). `image2video` uses `--image` (singular, one keyframe). Mixing them up gives "unknown flag" errors.

## Step 3: Submit and read the result

Run the command via Bash. On success the CLI prints JSON to stdout — the result URL(s) or local file path(s) if `--download_dir` was passed. Echo the path/URL back to the user.

**Example — text to image**:
```bash
dreamina text2image \
  --prompt="一只戴墨镜的橘猫,背光,电影感" \
  --ratio=1:1 \
  --resolution_type=2k \
  --poll=30
```

**Example — image to video**:
```bash
dreamina image2video \
  --image=./keyframe.png \
  --prompt="镜头缓缓推近,橘猫眼神闪动" \
  --duration=5 \
  --ratio=16:9 \
  --video_resolution=720P \
  --poll=60
```

If the user wants the result downloaded locally rather than a URL, add `--download_dir=./out` (create the directory first).

## Step 4: Handle async timeout

If `--poll` times out, the CLI returns JSON with status `querying` and a `submit_id`. Tell the user you will retry, then:

```bash
dreamina query_result --submit_id=<submit_id> --download_dir=./out
```

If the job is still in progress, wait and retry. If it failed, pull the error message from the `query_result` response and relay it verbatim — do not guess.

## Advanced: history and sessions

- `dreamina list_task --gen_status=success` — list completed jobs.
- `dreamina list_task --submit_id=<id>` — fetch one specific job.
- **Sessions** (v1.3.5+) let the user keep separate workspaces for different projects. Only touch them if the user explicitly asks to "switch session", "work in session X", or "list sessions". Otherwise the default session is fine.

## References

Load these on demand — do not read all up front:

- **`references/cli-commands.md`** — full flag table for every `dreamina` subcommand.
- **`references/install-and-login.md`** — installer details, browser login, credential file location, version upgrade.
- **`references/ratio-resolution-map.md`** — user phrasing ↔ `--ratio` / `--resolution_type` / `--video_resolution` mapping.
- **`references/troubleshooting.md`** — login expired, queue timeout, submit_id recovery, account switching.
