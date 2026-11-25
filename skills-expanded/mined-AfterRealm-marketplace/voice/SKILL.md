---
name: voice
description: >
  Use when the user wants to start a voice conversation with the Claude Desktop App,
  enable a hold-to-talk hotkey, use voice input in French / Spanish / German / Japanese /
  any non-English language, dictate prompts by speaking instead of typing, or invokes
  "/voice", "voice mode", "speak to Claude", "voice chat", "hands-free", "talk to Claude",
  or similar. Walks the user through choosing language and Whisper model size, then
  launches a standalone Python voice loop that records mic, runs local Whisper STT,
  and pastes the transcript into whatever window is focused (typically Claude Desktop).
  Fills the gap where official voice mode is English-only.
---

# Voice mode launcher

This skill gets the user from zero to a running voice-input loop in one go.
It asks the user four quick setup questions (language, model size, hotkey,
voice sensitivity), installs Python deps on first run, and launches the
script as a detached background process.

## Step 1 — Prerequisites

Run these checks. If either fails, tell the user what to install and stop:

```bash
python -c "import sys; assert sys.version_info >= (3,10), f'need 3.10+, have {sys.version}'; print(sys.version)"
```
Needs Python 3.10+. If `python` is not found, try `python3` (macOS/Linux) or `py` (Windows).
If missing: "Install Python 3.10 or newer from python.org, then restart Claude."

```bash
claude --version
```
Needs the Claude CLI. If missing: "Install the Claude CLI first — https://claude.com/claude-code"

## Step 2 — First-run setup (venv + auto-install deps)

Install into a **plugin-local venv**, not the user's system Python. This dodges
PEP 668 on modern Debian/Ubuntu/Fedora (where `pip install --user` is refused),
and keeps faster-whisper's heavy deps isolated so uninstall is just `rm -rf .venv`.

First check whether the venv already exists and has the deps:

```bash
# Windows
"${CLAUDE_PLUGIN_ROOT}/.venv/Scripts/python.exe" -c "import faster_whisper, sounddevice, soundfile, pynput, numpy, yaml" 2>&1

# macOS / Linux
"${CLAUDE_PLUGIN_ROOT}/.venv/bin/python" -c "import faster_whisper, sounddevice, soundfile, pynput, numpy, yaml" 2>&1
```

If the venv doesn't exist, create it (tell the user "Setting up voice mode (one-time, ~200 MB)..."):

```bash
# Windows
python -m venv "${CLAUDE_PLUGIN_ROOT}/.venv"
"${CLAUDE_PLUGIN_ROOT}/.venv/Scripts/python.exe" -m pip install --upgrade pip
"${CLAUDE_PLUGIN_ROOT}/.venv/Scripts/python.exe" -m pip install -r "${CLAUDE_PLUGIN_ROOT}/scripts/requirements.txt"

# macOS / Linux
python3 -m venv "${CLAUDE_PLUGIN_ROOT}/.venv"
"${CLAUDE_PLUGIN_ROOT}/.venv/bin/python" -m pip install --upgrade pip
"${CLAUDE_PLUGIN_ROOT}/.venv/bin/python" -m pip install -r "${CLAUDE_PLUGIN_ROOT}/scripts/requirements.txt"
```

If venv creation itself fails with "ensurepip is not available" on Debian/Ubuntu,
the user needs `sudo apt install python3-venv`. Surface that hint and stop.

If install itself fails, surface the error and stop.

## Step 3 — Ask the user for language, model, and hotkey

Use **AskUserQuestion** with these FOUR questions (send all four in one call
for a single round-trip — four is the AskUserQuestion tool maximum):

**Question 1 — "What language will you be speaking?"**

- **English** → code `en`
- **French** → `fr`
- **Spanish** → `es`
- **German** → `de`
- **Italian** → `it`
- **Portuguese** → `pt`
- **Japanese** → `ja`
- **Chinese** → `zh`
- **Auto-detect** → leave blank (works but less reliable on short clips)
- **Other** → ask for the ISO 639-1 code (e.g. `ru`, `nl`, `ko`, `ar`, `hi`)

**Question 2 — "Which Whisper model size?"** Include a short description so
the user can choose:

- **tiny** (~75 MB) — Fastest, roughest accuracy. English keywords or quick tests only.
- **base** (~150 MB) — Fast, OK English, poor for other languages.
- **small** (~500 MB) — **Recommended.** Sweet spot: good accuracy in most languages, runs on CPU.
- **medium** (~1.5 GB) — High accuracy but slow on CPU. Good if you have time or a GPU.
- **large-v3** (~3 GB) — Near-human accuracy. Needs an NVIDIA GPU to be usable.

**Question 3 — "Which hotkey should trigger recording?"**

- **F8** → `<f8>` (**Recommended** — single key, no chord, rarely conflicts)
- **F9** → `<f9>`
- **Ctrl + Shift + Space** → `<ctrl>+<shift>+<space>` (may clash with IMEs or Discord push-to-talk on some setups)
- **Ctrl + Shift + V** → `<ctrl>+<shift>+<v>`
- **Other** → ask the user for a pynput hotkey string (each key in angle brackets, plus-separated, e.g. `<ctrl>+<alt>+<v>`)

Do NOT offer Right Alt as an option on Windows. Many keyboard layouts remap
Right Alt to AltGr, which Windows emits as a synthetic Ctrl+Alt combo —
pynput sees two keys and the hotkey never resolves.

**Question 4 — "How do you usually speak when recording?"**

This picks between the default transcription pipeline and the `whisper_mode`
preset, which boosts mic gain and relaxes VAD/Whisper thresholds so quiet
speech doesn't get dropped as silence.

- **Normal speaking voice** → default (no `--whisper-mode` flag)
- **Quietly or whispered** → enable (`--whisper-mode`)
- **Not sure** → default

Defaults if the user skips: `small` model, auto-detect language, `<f8>` hotkey,
normal speaking voice.

## Step 4 — Launch

Build the arg list:
- If user picked a specific language, add `--language <code>`
- Always add `--model <chosen_model>`
- If user picked a non-default hotkey, add `--hotkey "<chosen_hotkey>"`
- If user picked the quiet/whispered option, add `--whisper-mode`

Spawn DETACHED so it survives this conversation:

Use the **venv's** python (created in Step 2), not the system python.

**Windows:** Use PowerShell `Start-Process` with an **array** argument list so paths with spaces or unicode (OneDrive, accented usernames) don't blow up the quoting:

```bash
powershell -NoProfile -Command "Start-Process -FilePath '${CLAUDE_PLUGIN_ROOT}/.venv/Scripts/python.exe' -WorkingDirectory '${CLAUDE_PLUGIN_ROOT}' -ArgumentList @('${CLAUDE_PLUGIN_ROOT}/scripts/open_voice.py', <each-flag-as-its-own-quoted-element>)"
```

Example with `--language fr --model small`:
```bash
powershell -NoProfile -Command "Start-Process -FilePath '${CLAUDE_PLUGIN_ROOT}/.venv/Scripts/python.exe' -WorkingDirectory '${CLAUDE_PLUGIN_ROOT}' -ArgumentList @('${CLAUDE_PLUGIN_ROOT}/scripts/open_voice.py', '--language', 'fr', '--model', 'small')"
```

**macOS / Linux:**
```bash
nohup "${CLAUDE_PLUGIN_ROOT}/.venv/bin/python" "${CLAUDE_PLUGIN_ROOT}/scripts/open_voice.py" <flags> > /dev/null 2>&1 &
```

## Step 5 — Confirm to the user

Tell them concisely:
- A terminal window is now open showing voice-mode logs.
- Default hotkey: **F8** (or whatever they picked) — hold to talk, release to paste the transcript into the focused window.
- For the transcript to land in the Claude Desktop App, click into the chat input before releasing the hotkey. (Focus safety will block paste if the focused window title doesn't contain "Claude".)
- First launch downloads the chosen Whisper model (size depends on choice).
- To stop it: close the terminal window, or kill the python process.

Do NOT try to read the script's output — it runs independently.
