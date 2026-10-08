---
name: realtime-audio-architecture
description: Real-time audio playback patterns for macOS Apple Silicon. TRIGGERS - audio jitter, tts choppy, sounddevice
allowed-tools: Read, Bash, Glob, Grep, WebSearch
---

# Real-Time Audio Architecture on macOS

Battle-tested patterns and anti-patterns for jitter-free audio playback on macOS Apple Silicon, learned from building the Kokoro TTS pipeline.

> **Self-Evolving Skill**: This skill improves through use. If instructions are wrong, parameters drifted, or a workaround was needed — fix this file immediately, don't defer. Only update for real, reproducible issues.

## Decision Framework

When building audio playback in Python on macOS, choose based on this hierarchy:

```
1. Write-based sd.OutputStream     ← DEFAULT CHOICE
2. Callback-based sd.OutputStream  ← Only if you need sample-level control
3. afplay subprocess               ← Only for one-shot playback of existing files
4. macOS say                       ← NEVER for production TTS
```

## Patterns (DO)

### Pattern 1: Write-Based sounddevice.OutputStream

**The default choice for Python audio playback.** `stream.write()` blocks in PortAudio's C code until the device buffer has space. No Python code runs on the audio thread, so the GIL is irrelevant.

```python
import sounddevice as sd
import numpy as np

def open_audio_stream() -> sd.OutputStream:
    # Refresh PortAudio to discover hot-plugged devices (Bluetooth, HDMI)
    sd._terminate()
    sd._initialize()
    stream = sd.OutputStream(
        samplerate=24000,
        channels=1,
        dtype="float32",
        blocksize=2048,    # ~85ms blocks at 24kHz
        latency="high",    # large internal buffer (not live, so latency is fine)
    )
    stream.start()
    return stream

# Open per request — close after each to follow device changes
stream = open_audio_stream()

# Play audio — blocks in C code, no GIL contention
audio = np.array([...], dtype=np.float32).reshape(-1, 1)
WRITE_BLOCK = 4096  # ~170ms — responsive to stop, smooth playback
for i in range(0, len(audio), WRITE_BLOCK):
    if interrupted:
        break
    stream.write(audio[i:i + WRITE_BLOCK])

stream.close()  # close after request so next open uses current default device
```

**Why this works:**

- `stream.write()` calls into PortAudio's C layer → no Python on the audio thread
- PortAudio handles all buffering, timing, and device interaction internally
- GIL held by CPU-intensive work (MLX inference, numpy ops) cannot affect audio timing
- Writing in ~170ms blocks allows responsive interrupt checking
- Stream opened per request (not at startup) to follow device changes

**Stop mechanism:** `stream.abort()` immediately stops playback and unblocks `write()`. Reopen the stream for next playback.

**Reference:** [write-based-stream.md](./references/write-based-stream.md)

### Pattern 2: Pipeline Synthesis (Synthesize N+1 While Playing N)

For chunked TTS, overlap synthesis and playback:

```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=1) as pool:
    ahead = pool.submit(synthesize, chunks[0])
    for i in range(len(chunks)):
        audio = ahead.result()
        if i + 1 < len(chunks):
            ahead = pool.submit(synthesize, chunks[i + 1])
        stream.write(audio)  # plays while next chunk synthesizes
```

**Why:** Synthesis takes 500-2000ms per chunk. Without pipelining, there's dead silence between chunks while waiting for synthesis. With pipelining, chunk N+1 is ready by the time chunk N finishes playing (since playback is typically longer than synthesis).

### Pattern 3: Float32 PCM as Native Format

CoreAudio's native sample format is 32-bit float. Use it end-to-end:

```python
# Synthesis output → float32 directly
audio = model.synthesize(text)
if audio.dtype != np.float32:
    audio = audio.astype(np.float32)
    if np.max(np.abs(audio)) > 2.0:  # int16 range
        audio = audio / 32768.0
```

**Why:** Avoids WAV encode/decode overhead. No temp files. No format conversion at playback time. CoreAudio receives the data in its preferred format.

### Pattern 4: Boundary Fades (2ms)

Apply tiny fade-in/out at chunk boundaries to prevent click artifacts:

```python
FADE_SAMPLES = 48  # 2ms at 24kHz

def apply_boundary_fades(audio: np.ndarray) -> np.ndarray:
    if len(audio) < FADE_SAMPLES * 2:
        return audio
    audio = audio.copy()
    audio[:FADE_SAMPLES] *= np.linspace(0, 1, FADE_SAMPLES, dtype=np.float32)
    audio[-FADE_SAMPLES:] *= np.linspace(1, 0, FADE_SAMPLES, dtype=np.float32)
    return audio
```

**Why:** Adjacent chunks may have different DC offsets or phase. A 2ms fade is inaudible but prevents the discontinuity click. Simpler and more reliable than inter-chunk crossfade.

### Pattern 5: launchd QoS for Audio Processes

```xml
<!-- CORRECT: Audio process gets CPU priority -->
<key>Nice</key>
<integer>-10</integer>
<key>ProcessType</key>
<string>Adaptive</string>
```

**Why:**

- `Nice: -10` gives higher CPU scheduling priority (range: -20 highest to 20 lowest)
- `ProcessType: Adaptive` lets macOS boost priority when the process is actively working
- launchd CAN set negative nice values for user agents (runs as root)

### Pattern 6: Centralized Audio Server

One server, one speak queue, shared across all clients (BTT, Telegram bot, CLI):

```
BTT shortcut  →  POST /v1/audio/speak  →  [server queue]  →  synthesize  →  play
Telegram bot  →  POST /v1/audio/speak  →  [server queue]  →  synthesize  →  play
```

**Why:** Prevents audio conflicts. One lock protocol. One process to tune. Clients are thin HTTP POST callers.

### Pattern 7: Audio Device Hot-Switching

PortAudio caches the device list at `Pa_Initialize()` time. Bluetooth devices (AirPods) connecting later are invisible. Two-layer strategy:

```python
def _refresh_audio_devices():
    """Re-init PortAudio to discover hot-plugged devices (~1ms)."""
    sd._terminate()
    sd._initialize()

def open_audio_stream():
    """Open stream with fresh device discovery."""
    _refresh_audio_devices()  # ← discovers AirPods, new HDMI, etc.
    stream = sd.OutputStream(samplerate=24000, channels=1, dtype="float32",
                             blocksize=2048, latency="high")
    stream.start()
    return stream

def maybe_reopen_stream(stream):
    """Between-chunk check for device switching (cached devices only).

    CRITICAL: Do NOT call _refresh_audio_devices() here — it invalidates
    the active stream pointer (PaErrorCode -9988).
    """
    current_default = sd.query_devices(kind='output')['index']
    if stream.device != current_default:
        stream.close()
        return open_audio_stream()
    return stream
```

**Two layers:**

| Layer            | When         | Handles                          | Mechanism                               |
| ---------------- | ------------ | -------------------------------- | --------------------------------------- |
| Between requests | Stream open  | Bluetooth hot-plug, HDMI connect | `_refresh_audio_devices()` + new stream |
| Between chunks   | Mid-playback | Switching between known devices  | `sd.query_devices()` on cached list     |

**CRITICAL:** Never call `sd._terminate()` while a stream is active — it invalidates all PortAudio stream pointers.

**Reference:** [device-routing.md](./references/device-routing.md)

## Anti-Patterns (DON'T)

### Anti-Pattern 1: Callback-Based sd.OutputStream with Python Queue

```python
# DON'T — GIL contention causes jitter
def callback(outdata, frames, time_info, status):
    data = audio_queue.get_nowait()  # needs GIL!
    outdata[:, 0] = data

stream = sd.OutputStream(callback=callback, ...)
```

**Why it fails:** The callback runs on PortAudio's real-time audio thread, but `queue.get_nowait()` acquires Python's GIL to execute. When MLX synthesis (or any CPU-intensive Python work) holds the GIL — even for 10ms — the callback is delayed, causing buffer underruns → audible glitches.

**The callback itself is C-level, but the Python code inside it needs the GIL.** This is the fundamental trap: the sounddevice docs say "callback runs on real-time thread" which is true for the C wrapper, but your Python code inside still contends for the GIL.

### Anti-Pattern 2: Subprocess Per Chunk (afplay)

```python
# DON'T — process spawn + device acquisition per chunk = jitter
for chunk in chunks:
    wav_path = write_temp_wav(chunk)
    subprocess.run(["afplay", wav_path])  # new process each time!
    os.unlink(wav_path)
```

**Why it fails:**

1. **Process spawn overhead:** `fork() + exec()` for each chunk
2. **Audio device re-acquisition:** Each afplay opens the audio device, negotiates format, starts playback, then releases. Gap between chunks = silence + click.
3. **File I/O overhead:** Write WAV to disk, read it back. Unnecessary when you have numpy arrays in memory.
4. **No pipeline:** Can't synthesize next chunk while current plays (process is blocking).

**When afplay IS appropriate:** One-shot playback of an existing file (e.g., notification sound). Not for streaming/chunked audio.

### Anti-Pattern 3: launchd Background QoS for Audio

```xml
<!-- DON'T — macOS actively throttles CPU and I/O -->
<key>Nice</key>
<integer>5</integer>
<key>ProcessType</key>
<string>Background</string>
```

**Why it fails:** `ProcessType: Background` tells macOS this process doesn't need timely CPU access. macOS will:

- Deprioritize CPU scheduling
- Throttle I/O bandwidth
- Potentially defer execution during high system load

For audio playback, this causes sporadic jitter that's hard to reproduce — it only happens when other processes are active.

### Anti-Pattern 4: macOS `say` as TTS Fallback

```bash
# DON'T — quality cliff, unexpected behavior
if ! kokoro_synthesize "$text"; then
    say "$text"  # "fallback"
fi
```

**Why it fails:**

- Massive quality difference (robotic vs neural) confuses users
- `say` has different timing, volume, and behavior
- Creates a "works but badly" state that's harder to debug than a clean failure
- Multiple TTS engines = multiple lock protocols, process management, edge cases

**Instead:** Fail loudly with a notification. Let the user know the TTS server is down and how to fix it.

### Anti-Pattern 5: Static Stream Opened at Startup

```python
# DON'T — stream binds to whatever device was default at process start
stream = sd.OutputStream(samplerate=24000, channels=1, dtype="float32")
stream.start()
# ... reuse forever, never close/reopen
```

**Why it fails:**

1. **Device lock-in:** Stream binds to the default device at open time. Switching system default later has no effect — audio keeps going to the old device.
2. **launchd boot timing:** Server starts at login when MacBook Speakers may be default. External monitor / Bluetooth not yet connected.
3. **PortAudio device cache:** `Pa_Initialize()` scans devices once. Bluetooth devices connecting later are invisible — stream open to them fails silently or crashes the playback worker.

**Instead:** Open stream lazily per request, close after each. Call `sd._terminate()` + `sd._initialize()` before opening to refresh the device list.

## Quick Diagnostic

If you hear jitter/choppiness:

1. **Check process priority:** `ps -o pid,nice,pri,command -p $(pgrep -f tts_server)`
   - Nice should be ≤ 0 (not 5 or higher)
2. **Check playback method:** `grep -c afplay ~/.local/state/launchd-logs/kokoro-tts-server/stdout.log`
   - Should be 0 (no afplay spawning)
3. **Check for GIL contention:** Look for `audio callback status: output underflow` in logs
   - If present → switch from callback to write-based stream
4. **Check launchd QoS:** `plutil -p ~/Library/LaunchAgents/com.terryli.kokoro-tts-server.plist | grep -E 'Nice|ProcessType'`
   - Should be Nice: -10, ProcessType: Adaptive

If audio goes to wrong device:

1. **Check stream device in logs:** `grep "Audio stream opened" ~/.local/state/launchd-logs/kokoro-tts-server/stdout.log | tail -3`
   - Should show the expected device name
2. **Check for PortAudio errors:** `grep "PaErrorCode\|PortAudio error" ~/.local/state/launchd-logs/kokoro-tts-server/stdout.log | tail -5`
   - `PaErrorCode -9988` = stream pointer invalidated (device refresh while stream active)
3. **Check system default:** `~/.local/share/kokoro/.venv/bin/python3 -c "import sounddevice as sd; print(sd.query_devices(kind='output'))"`

## References

- [Write-based stream implementation](./references/write-based-stream.md)
- [launchd QoS reference](./references/launchd-qos.md)
- [Pipeline synthesis pattern](./references/pipeline-synthesis.md)
- [Device routing and hot-switching](./references/device-routing.md)

## See Also

- **`devops-tools:macbook-desktop-mode`** — Complementary skill covering USB device _resilience_ (sleep/wake recovery, uhubctl port cycling, battery longevity, pmset desktop configuration). This skill handles the application/playback layer; that one handles the system/USB layer.

## Post-Execution Reflection

After this skill completes, check before closing:

1. **Did the command succeed?** — If not, fix the instruction or error table that caused the failure.
2. **Did parameters or output change?** — If the underlying tool's interface drifted, update Usage examples and Parameters table to match.
3. **Was a workaround needed?** — If you had to improvise (different flags, extra steps), update this SKILL.md so the next invocation doesn't need the same workaround.

Only update if the issue is real and reproducible — not speculative.
