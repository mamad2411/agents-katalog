---
name: google_meet
description: Join a Google Meet call, transcribe live captions, optionally speak in realtime, and do the followup work afterwards. Use when the user asks the agent to sit in on a meeting, take notes, summarize, respond in-call, or action items from it.
version: 0.2.0
platforms:
  - linux
  - macos
metadata:
  loki:
    tags: [meetings, google-meet, transcription, realtime-voice]
---

# google_meet

## When to use

The user says any of:

- "join my Meet at <url>"
- "take notes on this meeting"
- "summarize the meeting and send followups"
- "sit in on my standup"
- "be a bot in this call and speak up when X"

## Two modes

| Mode | What the bot does |
|---|---|
| `transcribe` (default) | Joins, enables captions, scrapes a transcript. Listen-only. |
| `realtime` | Same as transcribe PLUS speaks into the meeting via OpenAI Realtime. The agent calls `meet_say(text)` and the bot's voice comes out of the call. |

Pick `realtime` only when the user actually wants the agent to speak. It costs real money (OpenAI Realtime is pay-per-audio-minute) and requires a virtual audio device set up on the machine running the bot.

## Two locations

| Location | When |
|---|---|
| Local (default) | Gateway machine runs the Playwright bot directly. |
| Remote node (`node="<name>"`) | Bot runs on a different machine that has a signed-in Chrome and (for realtime) a configured audio bridge. Useful when the gateway runs on a headless Linux box but the user's real signed-in Chrome lives on their Mac. |

## Prerequisites the user must handle once

Easiest path — run the built-in installer:

```bash
loki plugins enable google_meet
loki meet install                 # pip deps + Chromium (transcribe only)
loki meet install --realtime      # + pulseaudio-utils / brew blackhole+ffmpeg
loki meet auth                    # optional; skips guest-lobby wait
loki meet setup                   # preflight checks
```

`loki meet install --realtime` prompts before running `sudo apt-get` (Linux)
or `brew install` (macOS). Pass `--yes` to skip the prompt. It will NOT touch
your macOS default-input setting — you have to select BlackHole 2ch in
System Settings yourself before starting a realtime meeting.

Or do it manually:
```bash
pip install playwright websockets && python -m playwright install chromium

# For realtime mode, additionally:
#   Linux:  sudo apt install pulseaudio-utils
#   macOS:  brew install blackhole-2ch ffmpeg
#           → System Settings → Sound → Input → BlackHole 2ch
#   Then set OPENAI_API_KEY or LOKI_MEET_REALTIME_KEY in ~/.loki/.env
```

For a remote node:
```bash
# on the user's Mac (where Chrome is signed in):
pip install playwright websockets && python -m playwright install chromium
loki plugins enable google_meet
loki meet node run --display-name my-mac    # persistent server
# copy the printed token

# on the gateway:
loki meet node approve my-mac ws://<mac-ip>:18789 <token>
loki meet node ping my-mac                   # confirm reachable
```

Run `loki meet setup` to preflight local prereqs.

## Flow

1. **Join** — call `meet_join(url=..., mode=..., node=...)`. Returns immediately.
2. **Announce yourself** — no auto-consent. Say (in whatever channel the user is watching): "A Loki agent bot is in this call taking notes."
3. **Poll** — `meet_status()` for liveness, `meet_transcript(last=20)` for recent captions. Don't re-read the whole transcript every turn.
4. **Speak (realtime only)** — `meet_say(text="...")` queues text for TTS. The speech lags by ~2s. Don't spam it.
5. **Leave** — `meet_leave()` when done, or set `duration="30m"` on `meet_join` for auto-leave.
6. **Follow up** — read `meet_transcript()` in full, summarize, and use regular tools to send the recap, file issues, schedule followups.

## Tool reference

| Tool | Parameters | Use |
|---|---|---|
| `meet_join` | `url`, `mode?`, `guest_name?`, `duration?`, `headed?`, `node?` | Start bot |
| `meet_status` | `node?` | Liveness + progress |
| `meet_transcript` | `last?`, `node?` | Read captions |
| `meet_leave` | `node?` | Close bot |
| `meet_say` | `text`, `node?` | Speak in realtime meeting |

`node?` on all tools: pass a registered node name (or `"auto"` for the sole node) to operate a remote bot instead of a local one. Omit for local.

## Important limits

- Captions are only as good as Google Meet's live captions. English-biased, lossy on overlapping speakers.
- Guest mode sits in the lobby until a host admits. Warn the user; `loki meet auth` avoids this.
- **Lobby timeout**: if the host doesn't admit the bot within 5 minutes (configurable via `LOKI_MEET_LOBBY_TIMEOUT` env), the bot leaves and `meet_status` reports `leaveReason: "lobby_timeout"`.
- **One active meeting per install per location.** A second `meet_join` leaves the first.
- **Windows not supported.**
- Realtime mode needs a virtual audio device. If the audio bridge setup fails, the bot falls back to transcribe mode and flags it in `meet_status().error`.
- `meet_say` requires `mode='realtime'` on the originating `meet_join`. Calling it against a transcribe-mode meeting returns a clear error.
- **Barge-in is best-effort.** When a caption arrives attributed to a real participant while the bot is generating audio, the bot sends `response.cancel` to OpenAI Realtime. Captions take ~500ms to show up, so the bot will talk over the first second or so of a human interruption.

## Status dict reference

`meet_status()` returns (subset shown, there are more):

| Key | Meaning |
|---|---|
| `inCall` | Past the lobby. False while waiting for admission. |
| `lobbyWaiting` | Clicked "Ask to join", waiting on host. |
| `joinAttemptedAt` / `joinedAt` | Timestamps for lobby-click and actual admission. |
| `captioning` | Caption observer is installed. |
| `transcriptLines` / `lastCaptionAt` | Transcript progress. |
| `realtime` / `realtimeReady` | Realtime mode provisioned / WS connected. |
| `realtimeDevice` | Audio device name the bot is feeding (e.g. `loki_meet_src`). |
| `audioBytesOut` / `lastAudioOutAt` | How much PCM the OpenAI session has produced. |
| `lastBargeInAt` | Timestamp of the most recent `response.cancel` sent. |
| `leaveReason` | `duration_expired`, `lobby_timeout`, `denied`, `page_closed`, or null. |
| `error` | Last error (soft — bot may still be running). |

## Transcript location

Local:
```
$LOKI_HOME/workspace/meetings/<meeting-id>/transcript.txt
```

Remote node: transcript lives on the node host's disk. Use `meet_transcript(node=...)` to read it over RPC.

## Safety

- URL regex: only `https://meet.google.com/...` URLs pass.
- No calendar scanning. No auto-dial.
- Remote nodes use bearer-token auth; tokens are generated on the node (32 hex chars, persisted in `$LOKI_HOME/workspace/meetings/node_token.json`) and must be copied to the gateway via `loki meet node approve`.
- `meet_say` text is rate-limited by the OpenAI Realtime session; spam-protection is the bot's problem, not yours, but still — don't queue hundreds of lines.
