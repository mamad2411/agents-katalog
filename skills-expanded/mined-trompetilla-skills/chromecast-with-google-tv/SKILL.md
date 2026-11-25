---
name: chromecast-with-google-tv
description: "Control Chromecast with Google TV via ADB: pair, pause, resume, status, and play/cast YouTube, Tubi, or episodic content in supported streaming apps."
metadata: {"openclaw":{"os":["darwin","linux"],"user-invocable":true,"requires":{"bins":["adb","uv"]},"install":[{"id":"brew-adb","kind":"brew","cask":"android-platform-tools","bins":["adb"],"label":"Install adb (android-platform-tools)"},{"id":"brew-scrcpy","kind":"brew","formula":"scrcpy","bins":["scrcpy"],"label":"Install scrcpy"},{"id":"brew-uv","kind":"brew","formula":"uv","bins":["uv"],"label":"Install uv"},{"id":"go-yt-api","kind":"go","module":"github.com/nerveband/youtube-api-cli/cmd/yt-api@latest","bins":["yt-api"],"label":"Install yt-api (go)"}]}}
---

# Chromecast with Google TV control

Use this skill when I ask to pair Chromecast ADB, cast YouTube or Tubi video content, pause Chromecast playback, resume Chromecast playback, check Chromecast status, play on Google TV, cast to Chromecast, or launch episodic content in another streaming app via global search fallback.

## Intent-to-command mapping

- "Pause the Chromecast" / "pause Chromecast playback" -> `./run pause`
- "Resume Chromecast" / "play Chromecast" -> `./run resume`
- "Check Chromecast status" / "is Chromecast online?" -> `./run status`
- "Pair Chromecast ADB" / "ADB pair Google TV" -> `./run pair --device <ip> --pair-port <port> [--code <pairing_code>]`
- "Play on Google TV" / "cast to Chromecast" -> `./run play "<query_or_id_or_url>"`

## Execution policy

- For pause/resume/status/play intents, execute the mapped command instead of only describing what would happen.
- If a cached/default device is available, do not ask for extra confirmation before running pause/resume/status/play.
- If required device information is missing and no cache/discovery result is available, ask for device details and then run the command.
- Never claim command success unless the command returned exit code 0.
- On command failure, return the real failure output and the next corrective step.

## Setup

This skill always requires `uv` and `adb` in the PATH. No venv required.

- Ensure `uv` and `adb` are available in the PATH.
- Ensure `yt-api` is available in the PATH when resolving a text query to a YouTube ID.
- Ensure `scrcpy` is available in the PATH when using global-search fallback with `--app`, `--season`, and `--episode`.
- Use `./run` as a convenience wrapper around `uv run google_tv_skill.py`.

## Capabilities

This skill provides a small CLI wrapper around ADB to control a Google TV device. It exposes the following subcommands:

- status: show adb devices output
- pair --device <ip> --pair-port <port> [--code <pairing_code>]: run adb pair only (no adb connect)
- play <query_or_id_or_url>: play content via YouTube, Tubi, or global-search fallback.
- pause: send media pause
- resume: send media play

### Usage examples

`./run status --device 192.168.4.64 --port 5555`

`./run pair --device 192.168.4.64 --pair-port 37099 --code 123456`

`./run play "7m714Ls29ZA" --device 192.168.4.64 --port 5555`

`./run play "family guy" --app hulu --season 3 --episode 4 --device 192.168.4.64 --port 5555`

`./run pause --device 192.168.4.64 --port 5555`

### Device selection and env overrides

- You can pass --device (IP) and --port on the CLI.
- Alternatively, set CHROMECAST_HOST and CHROMECAST_PORT environment variables to override defaults.
- If you provide only --device or only --port, the script will use the cached counterpart when available; otherwise it will error.
- The script caches the last successful IP:PORT to `.last_device.json` in the skill folder and will use that cache if no explicit device is provided.
- If no explicit device is provided and no cache exists, the script will attempt ADB mDNS service discovery and use the first IP:PORT it finds.
- IMPORTANT: This skill does NOT perform any port probing or scanning. It will only attempt an adb connect to the explicit port provided or the cached port.
- Pairing uses a dedicated pairing port (`--pair-port`) and does not assume the connect port.
- `pair` does not call adb connect and does not update `.last_device.json`.
- During interactive `play`, `pause`, and `resume`, if reconnect fallbacks still end in authentication/unpaired errors, the skill prompts to pair first, then retries connect.

### YouTube handling

- If you provide a YouTube video ID or URL, the skill will launch the YouTube app directly via an ADB intent restricted to the YouTube package.
- The skill attempts to resolve titles/queries to a YouTube video ID using the `yt-api` CLI (in the PATH). If ID resolution fails, the skill will report failure.
- You can override the package name with `YOUTUBE_PACKAGE` (default `com.google.android.youtube.tv`).

### Tubi handling

- If you provide a Tubi https URL, the skill will send a VIEW intent with that URL (restricted to the Tubi package).
- If the canonical Tubi https URL is needed, the skill can look it up via web_search and supply it to this skill.
- You can override the package name with `TUBI_PACKAGE` (default `com.tubitv`).

### Global-search fallback for non-YouTube/Tubi

- If YouTube/Tubi resolution does not apply and you pass `--app` with another provider (for example `hulu`, `max`, `disney+`), the skill uses a Google TV global-search fallback.
- For this fallback, pass all three: `--app`, `--season`, and `--episode`.
- `scrcpy` must be installed and available in the PATH for this flow.
- The fallback starts `android.search.action.GLOBAL_SEARCH`, waits for the Series Overview UI, opens Seasons, picks season/episode, then confirms `Open in <app>` when available.
- Hulu profile-selection logic is intentionally not handled here.

### Pause / Resume

`./run pause`
`./run resume`

### Dependencies

- The script uses only the Python standard library (no pip packages required).
- The scripts run through `uv` to avoid PEP 668/system package constraints.
- The script always expects `adb` and `uv` to be installed and available in the PATH.
- The script expects `yt-api` only when resolving text queries to YouTube IDs.
- The script expects `scrcpy` only for global-search fallback flows (`--app`, `--season`, and `--episode`).

### Caching and non-destructive defaults

- The script stores the last successful device (ip and port) in `.last_device.json` in the skill folder.
- It will not attempt port scanning; this keeps behavior predictable and avoids conflicts with Google's ADB port rotation.

### Troubleshooting

- If adb connect fails, run `adb connect IP:PORT` manually from your host to verify the current port.
- If adb connect is refused and you're running interactively, the script will prompt you for a new port and update `.last_device.json` on success.

## Implementation notes

- The skill CLI code lives in `google_tv_skill.py` in this folder. It uses subprocess calls to `adb`, `scrcpy`, and `yt-api`, plus an internal global-search helper for fallback playback.
- For Tubi URL discovery, the assistant uses web_search to find canonical Tubi pages and pass the https URL to the skill.
