---
name: voyager-new-app
description: Create or modify a standalone Python application using the Voyager SDK InferenceStream/create_inference_stream API for Axelera AI Metis hardware. Use when the user explicitly asks for app code, monitoring, analytics, REST API, custom UI, multi-stream logic, alerts, or business logic around an existing/validated pipeline. Do not use for generic complete pipeline launch, RUN_HERE.sh packaging, or hardware validation; use voyager-launch first for end-to-end runnable solutions.
argument-hint: "<app type and requirements>"
allowed-tools: Read, Bash, Glob, Grep, Edit, Write, Task, mcp__voyager__*
---

# Create New Application

Create a Python application for Axelera AI hardware using Voyager SDK InferenceStream

## Use This Skill When / Not When

- Use when: the user wants a standalone Python app (REST API, alerts, custom
  UI, multi-stream business logic) around a validated pipeline.
- Not when: they need the initial end-to-end runnable pipeline -- route to
  voyager-launch and run it first.
- Not when: they only want YAML -- route to voyager-new-pipeline.

## Instructions

Create an application with the specified requirements: **$ARGUMENTS**

If the request is primarily for a complete validated video/demo result, browser popup, or user-facing output viewer, use `voyager-launch` first. Its launch harness creates and opens `viewer/index.html` after Metis validation.

### Step 0: Data Source & Environment Selection

{{INCLUDE common/voyager-sdk-setup.md}}

### Step 0.5: Axelera Voyager Project & Task Integration

{{INCLUDE common/voyager-task-integration.md}}

### Step 1: Application Requirements Analysis

- Parse application type from arguments
- If not specified, ask for:
  - Application purpose (monitoring, analytics, demo, production)
  - Model/pipeline to use
  - Input sources (cameras, video files, streams)
  - Output requirements (display, file, API, custom processing)
  - Business logic requirements

### Step 2: Application Template Selection

Based on requirements, choose appropriate template:

- **Simple Demo**: Basic display with inference results
- **Analytics**: Data collection and metrics
- **Monitoring**: Multi-stream with alerts
- **Custom Processing**: Full control over inference results
- **REST API**: HTTP endpoint for inference

### Step 3: Basic Application Structure

Create application file with this structure:

```python
#!/usr/bin/env python
# Copyright <year>
# Application: <description>

from axelera.app import config, create_inference_stream, display

# Configuration
MODEL = "<model-name>"
SOURCES = ["<source1>", "<source2>"]

# Create inference stream
stream = create_inference_stream(
    network=MODEL,
    sources=SOURCES,
)

def process_frame(frame_result):
    """Process a single inference result."""
    image = frame_result.image
    meta = frame_result.meta
    stream_id = frame_result.stream_id

    # Add custom processing here
    pass

def main(window, stream):
    """Main inference loop."""
    for frame_result in stream:
        process_frame(frame_result)
        window.show(frame_result.image, frame_result.meta, frame_result.stream_id)

        if window.is_closed:
            break

# Run application
with display.App(renderer=True) as app:
    wnd = app.create_window("Application Title", (1280, 720))
    app.start_thread(main, (wnd, stream), name='InferenceThread')
    app.run()

stream.stop()
```

### Step 4: Working with Detection Results

```python
# Access detection metadata. `detections` is the task name from the model YAML.
for frame_result in stream:
    for detection in frame_result.detections:
        box = detection.box  # xyxy in original image coordinates
        score = float(detection.score)
        class_id = int(detection.class_id)
        try:
            label = detection.label.name
        except (AttributeError, NotImplementedError):
            label = f"cls:{class_id}"

        print(f"{label}: {score:.2f} at {box}")
```

Do not invent generic attributes such as `frame_result.persons`,
`frame_result.vehicles`, or `detection.confidence`. Voyager exposes task
outputs by task name through `frame_result.<task_name>` and
`frame_result.meta[task_name]`; first verify the task name in the model YAML
or the SDK example you copied.

### Step 5: Working with Pose Estimation

```python
# Use the actual keypoint task name from the pipeline YAML.
for frame_result in stream:
    keypoints_meta = frame_result.meta["keypoint_detections"]
    for pose in keypoints_meta.objects:
        keypoints = pose.keypoints  # numpy array, usually (K, 2) or (K, 3)
        print(keypoints)
```

### Step 6: Working with Segmentation

```python
# Use the actual segmentation task name from the pipeline YAML.
for frame_result in stream:
    seg_meta = frame_result.meta["segmentation"]
    if hasattr(seg_meta, "class_map"):
        class_map = seg_meta.class_map
    elif hasattr(seg_meta, "masks"):
        masks = [seg_meta.get_mask(i) for i in range(len(seg_meta.masks))]
```

### Step 7: Working with Classification

```python
for frame_result in stream:
    predictions = frame_result.classifications
    for pred in predictions:
        print(f"{pred.label.name}: {pred.score:.2f}")
        for topn, candidate in enumerate(pred.topk[1:], 1):
            print(f"  alt {topn}: {candidate.label.name} {candidate.score:.2f}")
```

### Step 8: Multi-Stream Handling

```python
stream = create_inference_stream(
    network="yolov8n-coco",
    sources=[
        "usb:0",
        "media/video1.mp4",
        "rtsp://camera/stream"
    ],
)

def main(window, stream):
    # Configure per-stream display
    window.options(0, title="Camera 1")
    window.options(1, title="Video Feed")
    window.options(2, title="RTSP Stream")

    for frame_result in stream:
        stream_id = frame_result.stream_id

        # Process based on stream
        if stream_id == 0:
            # Camera-specific logic
            pass
        elif stream_id == 1:
            # Video-specific logic
            pass

        window.show(frame_result.image, frame_result.meta, stream_id)
```

### Step 9: Headless Processing (No Display)

```python
from axelera.app import create_inference_stream

stream = create_inference_stream(
    network="yolov8n-coco",
    sources=["video.mp4"],
)

results = []
for frame_index, frame_result in enumerate(stream):
    # Process without display
    frame_data = {
        "frame_index": frame_index,
        "detections": [
            {
                "label": d.label.name,
                "box": d.box.tolist(),
                "score": float(d.score),
                "class_id": int(d.class_id),
            }
            for d in frame_result.detections
        ]
    }
    results.append(frame_data)

stream.stop()

# Save results
import json
with open("results.json", "w") as f:
    json.dump(results, f, indent=2)
```

### Step 10: REST API Application

```python
from flask import Flask, jsonify, request
from axelera.app import create_inference_stream
import threading

app = Flask(__name__)

# Global inference stream
stream = None
latest_results = {}

def inference_worker():
    global latest_results
    for frame_index, frame_result in enumerate(stream):
        latest_results = {
            "frame_index": frame_index,
            "detections": [
                {"label": d.label.name, "score": float(d.score)}
                for d in frame_result.detections
            ]
        }

@app.route("/start", methods=["POST"])
def start_inference():
    global stream
    source = request.json.get("source", "usb:0")
    stream = create_inference_stream(network="yolov8n-coco", sources=[source])
    threading.Thread(target=inference_worker, daemon=True).start()
    return jsonify({"status": "started"})

@app.route("/results", methods=["GET"])
def get_results():
    return jsonify(latest_results)

@app.route("/stop", methods=["POST"])
def stop_inference():
    if stream:
        stream.stop()
    return jsonify({"status": "stopped"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

### Step 11: Event-Based Processing

Iterate with `stream.with_events()` to react to non-frame events. The real
`FrameEventType` members are `result`, `source_error`, `end_of_source`, and
`end_of_pipeline`; a `FrameEvent` carries `type`, `source_id`, `message`, and
an optional `result` (`FrameResult`).

```python
from axelera.app import create_inference_stream, FrameEventType

stream = create_inference_stream(network="yolov8n-coco", sources=["video.mp4"])

for event in stream.with_events():
    if event.result:
        # Normal frame result
        process_frame(event.result)
    elif event.type == FrameEventType.source_error:
        print(f"Source {event.source_id} error: {event.message}")
    elif event.type == FrameEventType.end_of_source:
        print(f"Source {event.source_id} ended: {event.message}")
    elif event.type == FrameEventType.end_of_pipeline:
        print("Pipeline finished")
        break
```

### Step 12: Output File Location

Save application to:

- Examples: `examples/<app-name>.py`
- Production: Custom location specified by user
- Ensure executable permissions: `chmod +x <app-name>.py`

### Step 13: Testing the Application

Read `.voyager-runtime.json` first. Only run the application locally when
`execution.mode` is `execute_on_device`. On `package_for_linux` hosts, do not
run the app; ship the run commands below in the package instructions and
report that the app was not executed on this host.

```bash
# Run the application (execute_on_device only)
python examples/<app-name>.py

# Or make executable and run
chmod +x examples/<app-name>.py
./examples/<app-name>.py
```

### Step 14: Final Report

Always report:

- Exact command(s) run and exit status
- Runtime mode from `.voyager-runtime.json`
- Artifacts produced (application file, results files, logs)
- Gaps or skipped coverage (for example, app not executed in
  `package_for_linux` mode) before claiming Metis readiness

## Parallel Orchestration

See `common/agent-orchestration.md` for the full lane rules. For this skill:

- Parallelize scaffolding the application code, writing its unit tests, and a
  reviewer pass on the generated code as independent lanes.
- Serialize the on-device app test; exactly one process may use the Metis
  device at a time.
- Reconcile reviewer findings before the final report; reviewers advise,
  validation gates decide.
