# [CLAUDE.md](http://CLAUDE.md)

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

screen-duo is a Linux desktop tool for recording your screen and phone camera simultaneously, syncing them, and compositing the phone feed (head cam) as an overlay on the screen recording.

**User flow:** Launch app → select display → click "Connect iPhone" → open URL in Safari → tap Allow → position overlay → record → pause/resume → stop → auto-composite to MP4.

## Architecture

The project is split into three layers:

**1. Device layer** (`devices/`)

- `screen_capture.py` — captures the selected display. Auto-detects X11 (ffmpeg `x11grab`, with PulseAudio mic) vs Wayland (`$WAYLAND_DISPLAY`). On Wayland it further branches: GNOME/Mutter uses the `org.gnome.Shell.Screencast` D-Bus API (Mutter does not implement `wlr-screencopy`, so `wf-recorder` cannot work there); wlroots compositors (Sway, Hyprland) use `wf-recorder --audio`. The GNOME path also starts a `_MicRecorder` (separate ffmpeg/PulseAudio process) before the D-Bus handshake so the laptop mic is rolling before the clapper fires — this mic file is used for sync and as an audio fallback.
- `phone_capture.py` — probes and lists `/dev/video`* devices, checks if a device has a live feed, and records from a v4l2 device to a file via ffmpeg. Does not control any hardware directly; it reads whatever is already on the v4l2 device.
- `webrtc_server.py` — the iPhone camera + mic bridge. Runs a two-port local server: HTTP on :8080 (serves a `.mobileconfig` CA cert profile for one-time installation on the iPhone) and HTTPS on :8443 (serves the WebRTC camera page). Video frames are piped from aiortc into a v4l2loopback device via ffmpeg. Audio frames are decoded by aiortc and piped as s16le PCM to a separate ffmpeg process during recording segments (`record_audio_to(path)` / `stop_audio_recording()`). Echo cancellation / noise suppression / AGC are disabled so the clapper beep reaches the phone mic for sync detection.
- `iphone_bridge.py` — fallback RTSP/MJPEG/RTMP bridge. Detects the v4l2loopback device and starts an ffmpeg process piping any URL stream into it. Not used by the main UI (which uses WebRTC), but available as a utility.
- `wifi_powersave.py` — disables WiFi PSM (`iw dev <iface> set power_save off`) at recording start and restores it at stop. Requires `/etc/sudoers.d/screen-duo-wifi` (NOPASSWD rule for the iw command). Without this, 802.11 power management batches UDP packets in ~300 ms bursts during idle, dropping WebRTC fps to ~3.

**2. Recording layer** (`recording/`)

- `session.py` — orchestrates a recording session. Manages segments (pause = stop both feeds simultaneously, resume = start new segment pair). Uses simultaneous ffmpeg triggers for sync. Accepts an optional `webrtc_server` reference and calls `record_audio_to` / `stop_audio_recording` at segment boundaries to capture phone mic audio.
- `sync.py` — post-recording sync correction. At the start of each segment a clapper flash is shown on screen and a beep plays through the laptop speaker. `sync.py` finds these markers to compute drift: `_find_screen_flash` scans the screen video for the white frame; `_find_audio_spike` finds the beep onset in any audio file (phone mic or laptop mic).
- `compositor.py` — post-recording ffmpeg compositing. Per-segment sync loop: (1) find mic/phone-audio offset (clapper beep vs screen flash) to correct for GNOME D-Bus handshake pre-roll, (2) trim all streams, (3) losslessly concat via `concat` demuxer, (4) ffmpeg overlay + encode. Audio priority: phone mic (WebRTC) > laptop mic (GNOME `_MicRecorder`) > embedded screen audio.
- `clapper.py` — triggers the clapper flash (full-screen white `FlashWidget`) and a 1 kHz audio beep via `paplay`/`aplay`.

**3. UI layer** (`ui/`)

- Built with PySide6.
- `main_window.py` — display selector, camera dropdown, iPhone WebRTC connect controls (shows cert URL + camera URL), record/pause/stop controls, and a 5 fps screen preview. Camera probing and device checks run on background threads to keep the UI responsive.
- `overlay_widget.py` — draggable box the user positions on the preview (default: top-right). Phone feed is scaled to fill the box. Capture runs on a background thread (not the Qt main thread) to avoid UI lag.
- Preview during recording is a lightweight OpenCV overlay, not the final composited render.

## Key constraints

- **Pause is segment-based**: pause hard-stops both recordings; resume starts new segments. `ffmpeg concat` stitches segments losslessly at the end. Sync is preserved because each segment pair starts simultaneously.
- **Compositing is post-recording only**: ffmpeg runs at full speed after stop, not in real-time during recording (avoids dropped frames).
- **Phone preview stops during recording**: the OpenCV preview (`overlay_widget.py`) is stopped when ffmpeg starts recording from the same v4l2 device, to avoid a dual-consumer conflict. It restarts when recording returns to idle.
- **Phone connection**: iPhone via WebRTC. screen-duo runs a two-port local server (`webrtc_server.py`). HTTP :8080 serves a `.mobileconfig` CA cert profile — iPhone installs this once in Settings to trust our local CA. HTTPS :8443 serves the camera page — iPhone opens it in Safari, taps Start Camera, taps Allow, and streams. Frames arrive via aiortc, are piped into a v4l2loopback device via ffmpeg, and the rest of the app reads from that device as a normal v4l2 camera. No app, no account, no watermark.

## Tech stack

- Python 3.10+
- PySide6 (UI)
- OpenCV (`opencv-python`) — phone camera preview in overlay widget (background thread)
- ffmpeg via subprocess — screen capture (x11grab/wf-recorder), phone recording (v4l2 input), video concat, compositing, WebRTC frame bridge
- aiortc + aiohttp — WebRTC server: receives iPhone camera stream over local HTTPS
- v4l2loopback — virtual v4l2 device; WebRTC bridge writes frames here, recording reads from here
- scipy — used in `sync.py` for sync correction

## Development setup

```bash
pip install -r requirements.txt
# System deps
sudo apt install v4l2loopback-dkms ffmpeg
sudo modprobe v4l2loopback
```

**iPhone setup (one-time — < 2 minutes, never repeated):**

1. Make sure iPhone and laptop are on the same WiFi
2. In screen-duo: click **Connect iPhone** — two URLs appear
3. Open the **cert URL** (`http://...:8080/ca.mobileconfig`) in Safari → tap **Allow**
4. **Settings → General → VPN & Device Management → screen-duo → Install**
5. **Settings → General → About → Certificate Trust Settings** → enable **screen-duo CA**
6. Open the **camera URL** (`https://...:8443`) in Safari → tap **Start Camera** → tap **Allow**
7. Overlay in screen-duo goes green — streaming

From then on, only step 6 is needed. The cert stays trusted permanently.

Run the app:

```bash
python -m screen_duo
```

## Git workflow

Commit and push once the change has been confirmed working (tested by the user or verified via the app). Do not commit speculatively before testing. Prefer one logical change per commit rather than mixing unrelated edits.

```bash
git add <specific files>
git commit -m "short description of what and why"
git push
```

Commit message rules:

- Imperative mood: "fix overlay thread blocking" not "fixed" or "fixes"
- One line, under 72 chars
- No generic messages like "update files" or "fix stuff"
- No `Co-Authored-By` lines

Push after every commit. This is a solo project with no PR review process — push directly to `main`.

**Documentation:** When you change architecture, setup, or constraints above, update this file in the same commit so the next session has accurate ground truth. Shared agent skills (`git-commit-and-push`, `keep-context-docs-current`, `my-init`) live globally under `**~/.cursor/skills/`** (Cursor) and `**~/.claude/skills/`** (Claude Code).

## TODO

- **Screen preview on Wayland**: `QScreen::grabWindow` is unreliable on native GNOME Wayland (goes through XWayland; may show stale frames, wrong content, or black).
- **UI / overlay performance**: Overlay uses a background capture thread and partial repaints; screen preview is intentionally 5 fps because `grabWindow` is expensive on Wayland.

## Resolved

- **iPhone camera recording choppy (~3 fps) in the saved file** — Fixed in three layers:
  1. **CPU governor**: The i7-1255U runs `intel_pstate` in `powersave`/`balance_power` mode. During a static recording the capture threads are bursty, so cores park at 400 MHz–1.3 GHz. `libx264` at that clock only encoded ~3 fps. Fixed by switching phone recording to `h264_vaapi` (GPU encode in `phone_capture.py`) — immune to CPU clock state.
  2. **System idle (WiFi PSM + CPU governor)**: When the screen was static, the laptop's WiFi radio entered power-save mode (DTIM batching), which delivered WebRTC UDP packets in ~300 ms bursts instead of continuously, causing `track.recv()` to yield only ~3 fps of frames. The GPU fix exposed this. Fixed by running the recording timer at 30 Hz (`_elapsed_timer.start(33)` in `main_window.py`) — 30 redraws/sec through GNOME's compositor keeps the CPU governor and WiFi PSM from hitting deep idle. Timer label now shows `MM:SS.t` (tenths of second) to make the 30 Hz tick meaningful.
  3. **iPhone encoder frame-skipping**: iOS WebRTC drops framerate for static scenes. Fixed by adding `frameRate: {min: 25, ideal: 30}` to `getUserMedia`, `maxFramerate: 30` to `RTCRtpSender` params, and `contentHint = 'motion'` to the video track in `webrtc_server.py`'s HTML page.
  - The "problem disappears when cursor moves" clue was the key: it was an idle-system effect (display damage keeps compositor running → CPU/WiFi stay active), not a code bug per se.

