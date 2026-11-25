---
name: voyager-run
description: Execute inference.py for an already-selected Voyager SDK model or pipeline on Axelera AI Metis hardware with an explicit source such as video, image, USB, RTSP, dataset, or fakevideo. Use when the user provides or already has the model/pipeline and wants only a run/test/stream command. Do not create, package, validate, or evaluate a complete new solution from a natural-language request; use voyager-launch for that.
argument-hint: "<model> <source> [options]"
allowed-tools: Read, Bash, Glob, Grep, mcp__voyager__*
---

# Run Inference

Execute inference on Axelera AI hardware with various input sources

## Use This Skill When / Not When

- Use when: a model/pipeline is already selected and the user wants to
  execute `inference.py` with a video, image, USB, RTSP, or dataset source.
- Not when: they want a packaged end-to-end solution with validation
  artifacts -- route to voyager-launch.
- Not when: a custom model must be compiled or quantized first -- route to
  voyager-deploy.

## Instructions

Run inference with the specified configuration: **$ARGUMENTS**

{{INCLUDE common/voyager-sdk-setup.md}}

{{INCLUDE common/voyager-task-integration.md}}

{{INCLUDE common/examples-catalog.md}}

### Step 1: Environment Verification

- Ensure environment is activated:
  ```bash
  source venv/bin/activate
  ```
- Read `.voyager-runtime.json`. Only verify hardware directly when
  `execution.mode` is `execute_on_device`:
  ```bash
  axdevice
  ```
  In `package_for_linux` mode, return Voyager SDK commands and the package-only
  caveat instead of claiming hardware execution.

### Step 2: Parse Arguments

- Model/pipeline name (required)
- Input source (camera, video, image, dataset, RTSP)
- Display options
- Output options
- Examples-first: if the user described a task rather than naming a model, check
  `common/examples-catalog.md` for a ready-made example (or route to `voyager-launch`).

### Step 3: Input Source Configuration

**USB Camera:**

```bash
./inference.py <model> usb:0           # First USB camera
./inference.py <model> usb:1           # Second USB camera
./inference.py <model> usb:0 usb:1     # Multiple cameras
./inference.py <model> usb:0:640x480@30
```

**Video File:**

```bash
./inference.py <model> /path/to/video.mp4
./inference.py <model> media/traffic1_1080p.mp4
```

**Image File:**

```bash
./inference.py <model> /path/to/image.jpg
./inference.py <model> /path/to/images/*.jpg   # Multiple images
```

**RTSP Stream:**

```bash
./inference.py <model> rtsp://user:pass@ip:port/stream
```

**Dataset (for accuracy evaluation):**

```bash
./inference.py <model> dataset         # Use model's default dataset
./inference.py <model> dataset:val     # Explicit dataset split
```

### Step 4: Display Options

```bash
# Validation-safe default
./inference.py <model> <source> --display none --frames 150 --pipe gst --metis auto

# Headless mode (equivalent forms)
./inference.py <model> <source> --no-display
./inference.py <model> <source> --display none

# Explicit live display backend selection; use only when host support is known
./inference.py <model> <source> --display opengl
./inference.py <model> <source> --display opencv
./inference.py <model> <source> --display console
./inference.py <model> <source> --display iterm2
./inference.py <model> <source> --display auto

# Available options: --display {none,opengl,opencv,console,iterm2,auto}

# Custom window size
./inference.py <model> <source> --window-size 1280x720
```

### Step 5: Performance Monitoring

```bash
# Show performance statistics
./inference.py <model> <source> --show-stats

# Save tracer data to CSV
./inference.py <model> <source> --save-tracers metrics.csv

# Append to existing tracer file
./inference.py <model> <source> --save-tracers +metrics.csv
```

### Step 6: Output Options

```bash
# Save annotated output (video or images)
./inference.py <model> <source> -o output.mp4
./inference.py <model> <source> --output /path/to/output/
```

For complete runnable packages or user-facing video results, prefer `voyager-launch`; its harness keeps the raw Voyager `results/output.mp4`, creates `viewer/index.html`, and opens the browser result view by default.

### Step 7: Multi-Stream Configuration

```bash
# Multiple input sources are separate positional source arguments.
./inference.py <model> video1.mp4 video2.mp4

# Mix of sources
./inference.py <model> usb:0 video.mp4 rtsp://stream

# With stream-specific options
./inference.py <model> usb:0:640x480@30 video.mp4
```

### Step 8: Accuracy Evaluation Mode

```bash
# Evaluate on validation dataset
./inference.py <model> dataset --no-display

# Evaluate with specific number of frames
./inference.py <model> dataset --frames 1000 --no-display
```

### Step 9: Troubleshooting

**No display available:**

```bash
# Use --no-display or --display console
./inference.py <model> <source> --no-display
```

**Camera not found:**

```bash
# List available cameras
ls /dev/video*
# Try different index
./inference.py <model> usb:1
```

**Video codec issues:**

```bash
# Check video format
ffprobe video.mp4
# Re-encode only if an H.264 playback copy is explicitly needed
ffmpeg -y -i input.mp4 -an -c:v libx264 -pix_fmt yuv420p -movflags +faststart output.h264.mp4
```

**Low FPS:**

- Check CPU usage
- Try reducing resolution
- Ensure hardware acceleration is working

### Step 10: Example Workflows

```bash
# Quick demo with USB camera
./inference.py yolov5s-v7-coco usb:0

# Accuracy evaluation
./inference.py yolov5s-v7-coco dataset --no-display

# Multi-stream monitoring
./inference.py yolov5m-v7-coco-tracker usb:0 usb:1 rtsp://stream

# Save annotated output and performance data
./inference.py yolov8n-coco video.mp4 -o output.mp4 --save-tracers perf.csv
```

### Step 11: Final Report

Always report:

- Exact command(s) run and exit status
- Runtime mode from `.voyager-runtime.json`
- Artifacts produced (output video/images, tracer CSVs, logs)
- Gaps or skipped coverage (for example, commands provided but not executed
  in `package_for_linux` mode) before claiming Metis readiness
