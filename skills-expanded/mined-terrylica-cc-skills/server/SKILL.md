---
name: server
description: "Start/stop Kokoro TTS HTTP server. TRIGGERS - start tts server, kokoro server, tts http, stop tts server."
allowed-tools: Read, Write, Edit, Bash, Glob, AskUserQuestion
---

# Kokoro TTS Server

Manage the Kokoro TTS HTTP server — an OpenAI-compatible `/v1/audio/speech` endpoint on localhost:8779.

> **Self-Evolving Skill**: This skill improves through use. If instructions are wrong, parameters drifted, or a workaround was needed — fix this file immediately, don't defer. Only update for real, reproducible issues.

## Server Overview

The server provides:

- `GET /health` — Health status JSON
- `GET /v1/models` — List available models
- `POST /v1/audio/speech` — Synthesize text to audio (WAV, MP3, Opus, PCM)

## Quick Start

### Start (foreground, for testing)

```bash
~/.local/share/kokoro/.venv/bin/python ~/.local/share/kokoro/tts_server.py
```

### Start (launchd, for production)

Per the macOS launchd policy, the launchd plist must launch a compiled Swift binary (not a bash script). Guide the user through:

1. Compile Swift launcher binary
2. Create launchd plist at `~/Library/LaunchAgents/com.terryli.kokoro-tts-server.plist`
3. Bootstrap: `launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.terryli.kokoro-tts-server.plist`

### Stop

```bash
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.terryli.kokoro-tts-server.plist
```

### Verify

```bash
curl -s http://127.0.0.1:8779/health | python3 -m json.tool
```

Expected: `{"status": "ok", "provider": "kokoro-tts-mlx", "model": "mlx-community/Kokoro-82M-bf16", "device": "mlx-metal"}`

## Environment Variables

| Variable               | Default     | Purpose                |
| ---------------------- | ----------- | ---------------------- |
| `KOKORO_SERVER_PORT`   | `8779`      | Listen port            |
| `KOKORO_SERVER_HOST`   | `127.0.0.1` | Bind address           |
| `KOKORO_DEFAULT_VOICE` | `af_heart`  | Default voice          |
| `KOKORO_DEFAULT_LANG`  | `en-us`     | Default language       |
| `KOKORO_DEFAULT_SPEED` | `1.0`       | Speech speed (0.1–5.0) |
| `KOKORO_PLAY_LOCAL`    | `0`         | Play via afplay        |

## Troubleshooting

| Issue               | Cause                  | Solution                                   |
| ------------------- | ---------------------- | ------------------------------------------ |
| Port already in use | Another server running | `lsof -i :8779` to find, kill it           |
| Model load fails    | Not installed          | Run `/kokoro-tts:install` first            |
| Slow first request  | Warmup synthesis       | Normal — first request triggers model load |


## Post-Execution Reflection

After this skill completes, check before closing:

1. **Did the command succeed?** — If not, fix the instruction or error table that caused the failure.
2. **Did parameters or output change?** — If the underlying tool's interface drifted, update Usage examples and Parameters table to match.
3. **Was a workaround needed?** — If you had to improvise (different flags, extra steps), update this SKILL.md so the next invocation doesn't need the same workaround.

Only update if the issue is real and reproducible — not speculative.
