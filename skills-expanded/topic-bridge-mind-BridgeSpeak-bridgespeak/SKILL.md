---
name: bridgespeak
description: >
  Give the agent a voice. Synthesizes spoken audio from text using OpenAI's
  `gpt-realtime-2` model and plays it on the user's speakers. Activate when
  the user asks the agent to speak, say, read aloud, narrate, announce,
  pronounce, vocalize, or play audio of any text — including summaries of
  long output, status notifications, completion announcements, error
  read-outs, accessibility narration, or hands-free dictation playback.
  Cross-platform (macOS / Linux / Windows). Requires `OPENAI_API_KEY` and
  Python 3.9+ with the `websockets` package. Supports voice selection,
  speaking style instructions, and a `--no-play` mode for headless / SSH
  environments. Critical for agents that need to speak status to a busy
  builder, narrate code review findings hands-free, or read long-form
  output aloud during driving / cooking / multitasking.
license: MIT
compatibility: >
  macOS, Linux, Windows. Needs Python 3.9+ with `websockets` package
  (`pip install websockets`). Needs a system audio player: `afplay` (macOS,
  preinstalled), `paplay`/`aplay`/`ffplay`/`mpv` (Linux), or PowerShell's
  `Media.SoundPlayer` / `ffplay` (Windows). Falls back to file-only mode
  via `--no-play` when no player is available.
allowed-tools: Bash(bash:*) Bash(python3:*) Bash(python:*) Bash(afplay:*) Bash(paplay:*) Bash(aplay:*) Bash(ffplay:*) Bash(mpv:*) Bash(powershell:*) Bash(pwsh:*)
metadata:
  author: bridgemind
  version: "1.0.0"
  hermes:
    tags: [voice, tts, audio, openai, realtime, accessibility]
    category: voice
    required_environment_variables:
      - OPENAI_API_KEY
  openclaw:
    kind: package
    requires:
      - python3
references:
  - ./references/realtime-protocol.md
  - ./references/voices.md
  - ./references/api-key-setup.md
  - ./references/troubleshooting.md
---

You are operating with **BridgeSpeak** — the ability to convert text into spoken audio and play it on the user's machine. You speak by shelling out to the bundled `speak.sh` (or `speak.ps1` on Windows) script, which connects to OpenAI's Realtime API (`gpt-realtime-2`), receives streamed PCM16 audio, wraps it as WAV, and pipes it to the system's native audio player.

> **The user said "speak" → you call `speak.sh` with the text. That's it.**

You do not need to render audio yourself. You do not need to handle WebSockets, base64, PCM headers, or audio drivers. Everything is encapsulated in the script. Your job is to (a) recognize when speech is the right output, (b) pick a sensible voice, and (c) keep utterances short and useful.

---

## Quick Reference

### Default invocation

```bash
bash "${CLAUDE_SKILL_DIR}/../../scripts/speak.sh" "Build complete. All 47 tests passed."
```

If `${CLAUDE_SKILL_DIR}` is not available in your harness, use the absolute path to the installed skill's `scripts/` directory (or the symlink the user installed to `~/.claude/skills/bridgespeak/scripts/speak.sh`).

### With voice and tone

```bash
bash speak.sh --voice marin "Production deploy succeeded."
bash speak.sh --voice cedar --instructions "speak calmly and slowly" "Reading the changelog."
```

### Headless / SSH / file-only

```bash
bash speak.sh --no-play --output ./summary.wav "Long-form narration..."
```

---

## When to Speak

Speak when:

- The user explicitly asks ("read this aloud", "say it", "speak the summary", "narrate the diff").
- A long-running task completes and the user asked to be notified by voice.
- An accessibility need is stated (low vision, RSI, hands-busy context).
- A short status read-out adds value over silent text (e.g., during a multi-minute build).

Do **not** speak:

- For every response by default. Speech is the user's choice — wait for the trigger.
- Long passages without the user asking. Audio at OpenAI Realtime pricing (~$0.24/min) adds up fast. **Default to speaking summaries, not full output.**
- Anything secret, sensitive, or PII unless the user explicitly asked it spoken aloud (room may not be private).
- In SSH / CI / no-DAC environments unless `--no-play --output` is set explicitly.

---

## Choosing a Voice

OpenAI offers ten voices on `gpt-realtime-2`. Default to **`marin`** (the recommended flagship voice) unless the user asks otherwise.

| Voice | Character |
|---|---|
| `marin` | Flagship — natural, warm, recommended default |
| `cedar` | Flagship — deeper, calm, authoritative |
| `alloy` | Neutral, balanced |
| `ash` | Crisp, professional |
| `ballad` | Smooth, narrative |
| `coral` | Warm, friendly |
| `echo` | Mid, neutral-male |
| `sage` | Even, contemplative |
| `shimmer` | Bright, expressive |
| `verse` | Poetic, animated |

Full guide with use-case mapping: [references/voices.md](./references/voices.md).

Note: once a voice has produced audio in a session, the API locks it for the rest of that session. The script creates one session per invocation, so each call can pick a fresh voice freely.

---

## Steering Tone with `--instructions`

The `instructions` field of `session.update` accepts free-text guidance that shapes delivery without changing the words spoken:

```bash
bash speak.sh --voice cedar --instructions "speak quickly and excitedly, like good news" "PR merged!"
bash speak.sh --voice sage   --instructions "speak slowly and carefully" "Reading the migration plan."
bash speak.sh --voice ballad --instructions "warm, narrative tone" "Once upon a deploy..."
```

Keep instructions to one short sentence — long ones can compete with the text content.

---

## Cost Awareness

`gpt-realtime-2` bills both audio and text tokens:

| Bucket | Price |
|---|---|
| Text input | $4.00 / 1M tokens |
| Text output | $24.00 / 1M tokens |
| Audio input | $32.00 / 1M tokens |
| **Audio output** | **$64.00 / 1M tokens** (~**$0.24/minute** of speech) |

A 30-second status read-out is roughly 1¢. A 5-minute narration is roughly $1.20. **Speak summaries, not full output.** When in doubt, ask the user whether they want the full passage spoken before generating it.

---

## API Key Setup

The script resolves the OpenAI API key in this order:

1. `OPENAI_API_KEY` environment variable (canonical)
2. `~/.config/bridgespeak/config.json` with `{"openai_api_key": "sk-..."}` (chmod 600)
3. Fails with a copy-pasteable setup message — no interactive prompt (deadlocks agent harnesses).

If the user has not set up a key, the script tells them exactly how. You should not paste keys, write keys, or read keys yourself. The user owns provisioning.

Full setup per OS: [references/api-key-setup.md](./references/api-key-setup.md).

---

## Headless / SSH / CI Environments

The script auto-detects when no audio device or player is available and falls back to file-only mode. You can force this with:

```bash
bash speak.sh --no-play "text"               # writes to a temp .wav and prints the path
bash speak.sh --no-play --output out.wav "text"  # writes to the given path
```

Use this proactively when you know the user is on a remote shell (no `$DISPLAY`, `$SSH_CONNECTION` set), and offer to download / transfer the file.

---

## Error Handling

The script exits non-zero on failure with stderr messages:

| Exit | Meaning | What to tell the user |
|---|---|---|
| 0 | Success | — |
| 2 | Bad usage / args | Show usage, fix args |
| 10 | Missing `OPENAI_API_KEY` | Print the setup snippet from the script (already does) |
| 11 | Missing Python or `websockets` lib | Tell user: `pip install websockets` (or `pip3 install websockets`) |
| 12 | OpenAI API error (auth, rate, model) | Surface the error, suggest checking key / billing |
| 13 | Network / WebSocket failure | Retry once, then surface |
| 14 | No audio player found, `--no-play` not set | Re-run with `--no-play --output <path>` |

When the script fails, **do not retry endlessly**. Surface the error to the user with the suggested fix.

---

## Cross-Agent Notes

This skill follows the [agentskills.io](https://agentskills.io) open spec. It works in:

- **Claude Code** — install as a plugin (`claude plugin install bridgespeak@bridgemind-plugins`) or drop into `~/.claude/skills/bridgespeak/`.
- **Hermes** (NousResearch) — install into the `skills/` directory; the `metadata.hermes` block declares `OPENAI_API_KEY` for sandbox passthrough.
- **OpenClaw** — install into `~/.openclaw/workspace/skills/bridgespeak/` (or via `clawdhub`); the `metadata.openclaw` block declares the `python3` requirement.

Shell invocation pattern is identical across all three: agent calls `bash scripts/speak.sh "text"` (or `pwsh scripts/speak.ps1 "text"` on Windows). Long playback can be backgrounded by appending `&` if your harness supports it.

---

## What BridgeSpeak Is Not

- **Not a speech-to-text skill.** This is output only. (See BridgeMind's `bridgevoice` Tauri app for on-device dictation.)
- **Not a live two-way conversation.** The script does one round-trip (text → audio → exit). No microphone capture, no barge-in.
- **Not a TTS API wrapper.** It uses the Realtime model specifically (per project requirement). For cheaper batch TTS, OpenAI's `/v1/audio/speech` endpoint is ~16× cheaper, but is not what this skill provides.
- **Not a sandbox.** It will speak whatever text you give it. Treat user-supplied text the same as any other prompt-injection surface — sanitize or refuse before reading aloud anything that could leak secrets in earshot of others.

---

## One-Line Distillation

> **`bash speak.sh "text"` — that's the whole API. Pick a voice, keep it short, watch the meter.**
