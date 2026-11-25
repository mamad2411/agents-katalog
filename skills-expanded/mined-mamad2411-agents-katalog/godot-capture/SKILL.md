---
name: godot-capture
description: |
  Headless screenshot and video capture for any Godot project — C# (.NET) or GDScript — (Xvfb/Vulkan), plus the final result bundle layout. Use when you need automated screenshots or a video of the running game.
---

# Godot Capture

Screenshot and video capture for Godot projects. Hardware Vulkan gives proper rendering performance (shadows, SSR, SSAO, glow) and is required for video capture. Without a hardware GPU, screenshots can still work via software Vulkan (`llvmpipe`/`lavapipe`), but video capture should be skipped.

In example commands, `{task}` is a short slug for an intermediate capture run.

## Language: C# (.NET) or GDScript?

The capture infrastructure is identical for both languages: `.capture/run_godot`, the Xvfb/GPU detection, `--write-movie`, `--fixed-fps`, and the `ffmpeg` encode work the same regardless of how the project is scripted. The ONLY difference is that C# (.NET) projects must run `dotnet build` before capture so the latest DLLs are embedded; GDScript projects skip the build step and run capture directly.

Working directory is the Godot project root.

## Default Capture Shape

- Use dedicated `SceneTree` scripts under `test/` for automated capture. Do not make gameplay scripts depend on capture-only state.
- Always invoke `godot` through `.capture/run_godot` once Setup has run, so the right renderer and `xvfb-run` wrap are picked automatically.
- For final proof, capture a PNG sequence first, then encode `video.mp4` with `ffmpeg`.
- Use `--fixed-fps` so motion is deterministic and frame timing matches the encoded video.
- Keep `screenshots/` out of Godot import scope with `screenshots/.gdignore`.

## Setup (run once per session)

Detects platform and whether Vulkan exposes a hardware GPU. Writes `.capture/run_godot` — a persistent wrapper script compatible with `timeout`.

```bash
set -e
mkdir -p .capture
touch .capture/.gdignore

PLATFORM=$(uname -s)
GPU=none
GPU_KIND=software

# --- Timeout command ---
if command -v timeout &>/dev/null; then
    TIMEOUT_CMD=timeout
elif command -v gtimeout &>/dev/null; then
    TIMEOUT_CMD=gtimeout
else
    cat > .capture/ptimeout << 'PERL'
#!/usr/bin/env perl
use POSIX; my $s=shift; my $p; $SIG{ALRM}=sub{kill 'TERM',$p;exit 124};
alarm $s; die "fork: $!" unless defined($p=fork); exec @ARGV unless $p; waitpid $p,0; exit($?>>8);
PERL
    chmod +x .capture/ptimeout
    TIMEOUT_CMD="$(pwd)/.capture/ptimeout"
fi

# --- GPU detection ---
NVIDIA_ICD=/usr/share/vulkan/icd.d/nvidia_icd.json
if [[ "$PLATFORM" == "Darwin" ]]; then
    GPU=metal
    GPU_KIND=hardware
elif command -v vulkaninfo &>/dev/null; then
    if vulkaninfo --summary 2>&1 | grep -Eq "deviceType *= PHYSICAL_DEVICE_TYPE_(DISCRETE_GPU|INTEGRATED_GPU|VIRTUAL_GPU)"; then
        GPU=vulkan
        GPU_KIND=hardware
    fi
fi

# --- Resolve the Godot binary ---
# `godot` is often NOT on PATH — on macOS it lives inside an .app bundle, and
# on Linux it may be a versioned name. Resolve it once and symlink it to
# `.capture/godot` so the wrapper never depends on PATH.
GODOT_BIN=""
for c in godot godot4 Godot; do
    if command -v "$c" &>/dev/null; then GODOT_BIN=$(command -v "$c"); break; fi
done
if [[ -z "$GODOT_BIN" && "$PLATFORM" == "Darwin" ]]; then
    # Prefer a plain (GDScript) build; fall back to the mono/.NET one for C# projects.
    for app in "/Applications/Godot.app" "/Applications/Godot_mono.app" "$HOME/Applications/Godot.app"; do
        [[ -x "$app/Contents/MacOS/Godot" ]] && { GODOT_BIN="$app/Contents/MacOS/Godot"; break; }
    done
fi
if [[ -z "$GODOT_BIN" ]]; then
    echo "ERROR: could not find the Godot binary. Set GODOT_BIN and re-run, e.g.:"
    echo "  ln -sf /path/to/Godot .capture/godot"
    exit 1
fi
ln -sf "$GODOT_BIN" .capture/godot
echo "Godot binary: $GODOT_BIN"

# --- Persistent run_godot wrapper ---
cat > .capture/run_godot << 'WRAPPER'
#!/usr/bin/env bash
set -o pipefail
NVIDIA_ICD=/usr/share/vulkan/icd.d/nvidia_icd.json
NOISE="leaked RID|Leaked instance|ObjectDB instances"
SELF_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GODOT="$SELF_DIR/godot"   # symlink written by Setup — never relies on PATH
cmd=()

# Linux without a display session → xvfb
if [[ "$(uname -s)" != "Darwin" && -z "${DISPLAY:-}" && -z "${WAYLAND_DISPLAY:-}" ]]; then
    cmd+=(xvfb-run -a -s '-screen 0 1920x1080x24')
fi

# Renderer
if [[ "$(uname -s)" == "Darwin" ]]; then
    cmd+=("$GODOT" --path . --rendering-method forward_plus)
elif [[ -f "$NVIDIA_ICD" ]]; then
    cmd+=(env "VK_ICD_FILENAMES=$NVIDIA_ICD" "$GODOT" --path . --rendering-method forward_plus)
elif command -v vulkaninfo &>/dev/null && vulkaninfo --summary 2>&1 | grep -Eq "deviceType *= PHYSICAL_DEVICE_TYPE_(DISCRETE_GPU|INTEGRATED_GPU|VIRTUAL_GPU)"; then
    cmd+=("$GODOT" --path . --rendering-method forward_plus)
else
    cmd+=("$GODOT" --path . --rendering-driver vulkan)
fi

"${cmd[@]}" "$@" 2>&1 | { grep -v "$NOISE" || true; }
WRAPPER
chmod +x .capture/run_godot

# --- Env for sourcing in subsequent bash calls ---
GPU_AVAILABLE=$([[ "$GPU_KIND" == "hardware" ]] && echo true || echo false)
cat > .capture/env << ENV
GPU_AVAILABLE=$GPU_AVAILABLE
TIMEOUT_CMD=$TIMEOUT_CMD
ENV

mkdir -p screenshots
touch screenshots/.gdignore

echo "=== Capture ready: Platform=$PLATFORM  GPU=$GPU ==="
$GPU_AVAILABLE || echo "WARNING: No GPU — screenshots via lavapipe, video capture skipped"
```

After setup: source `.capture/env` for `$GPU_AVAILABLE` and `$TIMEOUT_CMD`. Use `.capture/run_godot` instead of bare `godot` for all rendering.

## Two traps that make capture "hang" or come out blank

Both of these cost real time when hit — read before your first run.

1. **`--headless` does NOT render.** In headless mode `get_viewport().get_texture().get_image()` comes back blank/empty, so a script that screenshots the viewport produces nothing. Use headless ONLY for `--import`. For any actual pixels you need an offscreen render: either `--write-movie` (the video path) or run **headful** (no `--headless`) with a script that calls `save_png`. On macOS/Metal and on a GPU-backed Linux box, a headful `run_godot` renders fine offscreen without a visible window.

2. **`--quit-after` is the real exit mechanism — `$TIMEOUT_CMD` is only a backstop.** macOS ships no `timeout`/`gtimeout`, so Setup falls back to a small perl `ptimeout`, and that fallback does **not** reliably kill a Metal Godot process. If you lean on it, a stuck run burns your whole outer wall-clock limit instead of the timeout you asked for. So:
   - Always pass `--quit-after {N}` (or have the script `quit()` itself). That is what actually ends the run.
   - Treat `$TIMEOUT_CMD` as a safety net only; do not assume it will fire.
   - Never wrap capture in a foreground `sleep` to "wait for it" — launch it in the background and poll for the output file instead.
   - Skip `--headless --import` when `.godot/` already exists and no assets changed; a stray `--import` can open editor layout and stall for minutes.

## Single Still (quick hero / UI shot)

When you just need ONE clean PNG (a landing-page hero, a "does this look right" check) and not a video, skip the movie/ffmpeg machinery. Headful render + a script that stages the frame, saves one PNG, and quits — with `--quit-after` as the backstop.

```gdscript
# test/capture_still.gd — extends SceneTree
extends SceneTree
var main: Node3D
var frames := 0
var _done := false

func _initialize() -> void:
    main = load("res://scenes/main.tscn").instantiate()
    root.add_child(main)

func _process(_delta: float) -> bool:
    frames += 1
    if frames == 60:
        pass  # stage the shot: position camera, set time-of-day, hide HUD, etc.
    elif frames == 120 and not _done:
        _done = true
        root.get_viewport().get_texture().get_image().save_png("res://screenshots/still.png")
        print("shot: still")
        quit()
    return false
```

```bash
# Headful (renders), self-quits via the script, --quit-after as a hard backstop.
.capture/run_godot --quit-after 200 --script test/capture_still.gd
```

Run it in the background and poll for `screenshots/still.png` rather than blocking on it. Give the scene enough lead frames (chunk streaming, tweens, `_ready` bootstrap) before the shot frame — a still grabbed too early catches an unloaded world. For a fast edit→look debug loop on UI specifically, `godot-automatic-qa` (inject a one-shot timer, no `.capture/` scaffolding) is lighter than this; use this when you want the shot staged deterministically from a `SceneTree` script.

## Screenshot First

Prove one still or short frame sequence before recording a final clip:

1. Run `timeout 60 dotnet build 2>&1`. **[C# only]** — GDScript projects skip this line.
2. Run `$TIMEOUT_CMD 60 .capture/run_godot --headless --import 2>&1` after asset changes.
3. Write a small `test/CaptureStill.cs` or `test/CaptureTask.cs` (GDScript equivalent: `test/capture_task.gd`, which `extends SceneTree` with `func _initialize()`) that loads the scene, positions the camera, waits for the scene to settle, then exits after a few frames. `SceneTree` capture scripts work in both languages.
4. Capture to `screenshots/{task}/`.
5. Inspect the PNGs directly before adding a longer video path.

```bash
source .capture/env

OUT=screenshots/{task}
rm -rf "$OUT"
mkdir -p "$OUT"

timeout 60 dotnet build 2>&1   # [C# only] — omit this line for GDScript projects
$TIMEOUT_CMD 60 .capture/run_godot --headless --import 2>&1
$TIMEOUT_CMD 60 .capture/run_godot \
    --write-movie "$OUT/frame.png" \
    --fixed-fps 10 --quit-after 60 \
    --script test/CaptureTask.cs   # GDScript: --script test/capture_task.gd
```

Godot expands `frame.png` into numbered images such as `frame00000003.png` and writes a companion `frame.wav`. Treat the PNG sequence as the screenshot output.

`$TIMEOUT_CMD` is a safety net — `--quit-after` handles exit normally. Exit code 124 means the timeout fired.

### Frame rate and duration

`--quit-after {N}` is the frame count. Choose based on scene type:

- **Static scenes** (decoration, terrain, UI): `--fixed-fps 1`. Adjust `--quit-after` for however many views are needed (for example 8 frames for a camera orbit).
- **Dynamic scenes** (physics, movement, gameplay): `--fixed-fps 10` minimum. Lower FPS breaks physics — `delta` becomes too large, causing tunneling and erratic behavior. Typical: 3-10s at 10-30 fps.

## Video Path

The proven video flow is: capture PNG frames first, then convert them with `ffmpeg`. Requires hardware GPU — software rendering is too slow. Skip and report if `GPU_AVAILABLE` is false.

Reasons:

- A bad frame sequence is easy to inspect before encoding.
- `ffmpeg` handles H.264/MP4 packaging better than in-engine encoding.

```bash
source .capture/env

if ! $GPU_AVAILABLE; then
    echo "No GPU — skipping video capture"
else
    OUT=screenshots/{task}
    rm -rf "$OUT"
    mkdir -p "$OUT"

    $TIMEOUT_CMD 60 .capture/run_godot \
        --write-movie "$OUT/frame.png" \
        --fixed-fps 30 --quit-after 120 \
        --script test/CaptureTask.cs

    ffmpeg -y -framerate 30 -pattern_type glob -i "$OUT/frame*.png" \
        -c:v libx264 -pix_fmt yuv420p -preset medium -crf 22 -movflags +faststart \
        "$OUT/capture.mp4"
fi
```

`120` frames at `30` fps gives a 4 second clip. Increase frame count only after the short path is working.

## Final Result Bundle

The final deliverable is a proof bundle under `screenshots/result/{N}/`, where `{N}` is the next integer counter for this repo.

Required contents:

- `video.mp4` — encoded at exactly 30 fps and between 15s and 30s long. Prefer 15s / 450 frames; use up to 30s / 900 frames only when the task needs the extra time to prove behavior.
- the raw `frameXXX.png` files used to encode that video, stored in the same folder

The clip has to prove the task across its full duration:

- Show the implemented behavior progressing from start to finish, not in one fleeting moment.
- Vary what is on screen. A clip that loops the same idle pose, replays the same camera orbit, or sits on a single static frame for the whole window proves nothing.
- No dead time. A few good seconds followed by a stuck entity, frozen camera, blank window, or broken state for the rest of the clip is a clear failure, not a partial pass.

Recommended command shape (30 fps × 15s = 450 frames):

```bash
source .capture/env

if ! $GPU_AVAILABLE; then
    echo "No GPU — cannot produce final video bundle"
    exit 1
fi

RESULT=screenshots/result/{N}
rm -rf "$RESULT"
mkdir -p "$RESULT"

timeout 60 dotnet build 2>&1   # [C# only] — omit this line for GDScript projects
$TIMEOUT_CMD 60 .capture/run_godot --headless --import 2>&1
$TIMEOUT_CMD 90 .capture/run_godot \
    --write-movie "$RESULT/frame.png" \
    --fixed-fps 30 --quit-after 450 \
    --script test/Presentation.cs   # GDScript: --script test/presentation.gd

ffmpeg -y -framerate 30 -pattern_type glob -i "$RESULT/frame*.png" \
    -c:v libx264 -pix_fmt yuv420p -preset medium -crf 22 -movflags +faststart \
    "$RESULT/video.mp4"
```

Use `900` frames only when a 30s clip is genuinely needed for coverage.

The encoded MP4 must use the same fps as the captured frame sequence. If those disagree, the resulting motion proof is inaccurate.

## Time and Motion

- Do not let capture depend on real wall-clock frame time.
- Use `--fixed-fps 30` for final proof so Godot advances exactly one 30 fps tick per frame.
- Pre-position cameras before the first captured frame. The first movie frame can render before `_Process()` updates.
- Keep automated capture input separate from keyboard input. If the game normally expects live input, provide deterministic capture-time control in the test script.

## Validation Standard

- `dotnet build` passes **[C# only]** — GDScript projects have no build step
- `.capture/run_godot --headless --import` has run after asset changes
- one screenshot or short frame sequence writes real `.png` files
- one final frame sequence writes multiple distinct frames
- `ffmpeg` converts the validated frame sequence to `video.mp4`

If the frame hashes are identical, do not assume the video path is done. That usually means the capture camera, time stepping, or scripted input is wired incorrectly.
