---
name: object-detection-edge
description: "Use when deploying object detection on robot edge hardware (Jetson, Coral, Raspberry Pi) — selecting and training YOLO-family models, TensorRT/INT8 quantization, hitting fps/latency budgets, building custom datasets for robot viewpoints, adding multi-object tracking (SORT/ByteTrack), and estimating object distance from bounding boxes. Provides exact export/quantization workflows, parameter starting values, and the failure modes that break detection on real robots."
category: robotics
domain: robotics
subdomain: general
version: 1.0.0
license: MIT
risk: low
source:
  repository: "rahulbachina/robotics-skills"
  commit: "e69d9828fb"
  imported_at: "2026-09-20"
  license: "MIT"
platforms:
  - claude-code
  - cursor
  - codex
  - gemini
  - antigravity
  - copilot
---


# Object Detection on Edge Hardware for Robots

Detection on a robot is not a Kaggle problem. The model must run at a fixed latency budget on a thermally constrained device, survive motion blur and weird viewpoints, feed a tracker with stable IDs, and never silently degrade. This skill covers the full pipeline: model selection → training on robot-realistic data → quantized deployment → tracking → metric distance from detections.

---

## 1. Hardware and Model Selection — Decide This First

### The latency budget comes from the control loop, not from benchmarks

Work backwards from what the robot does with the detection:

| Use case | Required end-to-end latency | Min fps |
|---|---|---|
| Obstacle avoidance while moving (1 m/s) | < 100 ms (camera→decision) | 10–15 |
| Person following | < 150 ms | 8–10 |
| Visual servoing / grasping a moving object | < 50 ms | 20–30 |
| Inventory scan / inspection (robot stops) | < 1 s | 1–2 |

**End-to-end latency = capture + preprocess + inference + postprocess (NMS) + tracking + transport to consumer.** Inference is often only half of it. A "30 fps" model with 60 ms of pipeline overhead is a 10 fps system. Measure the whole pipeline with timestamps at each stage before blaming the model.

A robot moving at 1 m/s with 200 ms total perception latency has moved 20 cm before it can react. That is the number that matters, not mAP.

### Hardware reality table (typical, 640×640 input, batch 1)

| Platform | Model | Precision | Inference latency | Notes |
|---|---|---|---|---|
| Jetson Orin Nano 8GB | YOLOv8n / YOLO11n | TensorRT FP16 | 6–10 ms | The default robot choice in 2025+ |
| Jetson Orin Nano 8GB | YOLOv8s | TensorRT INT8 | 8–12 ms | Best accuracy/latency tradeoff |
| Jetson Orin NX 16GB | YOLOv8m | TensorRT FP16 | 10–15 ms | |
| Jetson Xavier NX (legacy) | YOLOv8n | TensorRT FP16 | 15–25 ms | |
| Coral Edge TPU (USB/M.2) | YOLOv8n (full-int8, 320–448 input) | INT8 | 15–30 ms | Strict op support; SiLU must be replaced or falls back to CPU |
| Raspberry Pi 5 (CPU only) | YOLOv8n, 320 input, NCNN | INT8/FP16 | 80–150 ms | Usable only for slow robots |
| Raspberry Pi 5 + Hailo-8L (AI Kit) | YOLOv8s | INT8 | 10–20 ms | Now a serious Jetson alternative |

Rules of thumb:
- **Jetson → TensorRT, always.** Running PyTorch or ONNX Runtime on a Jetson leaves 3–5× performance on the table.
- **Coral → only if your model compiles fully to the TPU.** One unsupported op partitions the graph and CPU fallback destroys latency. Check with `edgetpu_compiler -s model.tflite` — you want exactly 1 subgraph mapped to TPU.
- **Pi without accelerator → reduce input size before reducing model size.** 320×320 YOLOv8n beats 640×640 "nano-est" model for fps, and small robots usually only need near-field detection where objects are large.
- **Lock Jetson clocks before benchmarking:** `sudo nvpmodel -m 0 && sudo jetson_clocks`. Unlocked clocks give you variable latency that looks like a software bug.

### Model family selection

- **YOLOv8 / YOLO11 (Ultralytics):** default choice. Anchor-free, trains easily, exports cleanly, huge ecosystem. AGPL-3.0 license — if you ship closed-source commercial product, you need an Ultralytics license or use an alternative.
- **YOLOX / YOLOv6 / RT-DETR:** Apache-2.0 alternatives. YOLOX-nano/tiny is a solid permissive-license pick. RT-DETR avoids NMS entirely (deterministic latency) but is heavier.
- **YOLO-NAS, PP-YOLOE:** good accuracy but check export toolchain maturity for your target before committing.
- Sizes: start with **`n` (nano)** and only move up if validation mAP on YOUR data is insufficient at the required fps. Most robot tasks (person, pallet, door, specific tools) are 1–10 classes with large-ish objects — nano is usually enough.

---

## 2. Deployment: TensorRT and INT8 Quantization Workflow

### The golden path on Jetson (Ultralytics YOLO)

```python
from ultralytics import YOLO

model = YOLO("best.pt")  # your trained weights

# FP16 — do this first, it's nearly free accuracy-wise
model.export(format="engine", half=True, imgsz=640, device=0)
# → best.engine, built ON THE JETSON (engines are not portable across GPUs/JetPack)

# INT8 — needs calibration data
model.export(
    format="engine",
    int8=True,
    imgsz=640,
    data="dataset.yaml",   # calibration images drawn from your val set
    device=0,
)
```

**Critical: build the engine on the exact target device and JetPack/TensorRT version you deploy on.** A `.engine` file built on a desktop 4090 or a different JetPack will fail to load or silently select different kernels. Bake engine-build into your robot provisioning step, cache by `(model_hash, trt_version, gpu)`.

### INT8 calibration — where people get it wrong

INT8 post-training quantization (PTQ) computes per-tensor scale factors from a calibration dataset. The quality of those scales is entirely determined by the calibration data.

1. **Use 300–1000 images sampled from your real deployment distribution** — same camera, same lighting range, same mounting angle. Calibrating on COCO images for a model deployed on a warehouse robot gives wrong activation ranges and several points of mAP loss.
2. Include the hard conditions: low light, motion blur, backlight. If calibration only sees easy frames, the quantizer clips the activation ranges that occur in hard frames.
3. **Always validate INT8 against FP16 on your val set.** Acceptable: ≤1–2 points mAP50-95 drop. If you lose more:
   - Re-check calibration set (most common cause).
   - Try entropy vs minmax calibrator (TensorRT `IInt8EntropyCalibrator2` is the default and usually right).
   - Use mixed precision: keep first conv and detection head in FP16 (`--layerPrecisions` / layer-wise fallback in trtexec, or Ultralytics handles sensible defaults).
   - If still bad, do **QAT (quantization-aware training)** — fine-tune for ~10 epochs with fake-quant nodes (e.g., `pytorch-quantization` / NVIDIA TAO). QAT recovers nearly all PTQ loss but costs a training cycle.
4. Expected gain: INT8 is typically **1.3–1.8× faster than FP16** on Orin-class devices and halves memory. On small (nano) models the speedup is smaller because they're memory-bound — sometimes FP16 nano is the better deal than INT8 nano. Benchmark both.

### trtexec sanity benchmark (do this before integrating)

```bash
/usr/src/tensorrt/bin/trtexec --loadEngine=best.engine \
    --iterations=200 --avgRuns=100 --useSpinWait
# Look at "GPU Compute Time: mean" — that's your inference number.
# Also note "Host Walltime" vs GPU time to spot H2D/D2H copy overhead.
```

### Coral Edge TPU specifics

- Export path: PyTorch → ONNX → TF → **full-integer** TFLite → `edgetpu_compiler`. Or `model.export(format="edgetpu")` in Ultralytics which automates it.
- Must be **full INT8 including input/output** (`uint8`/`int8` I/O), with a representative dataset function for calibration.
- SiLU/Swish activations are not TPU-supported in older compiler versions — Ultralytics export handles substitution, but verify with `edgetpu_compiler -s`: every op should say "Mapped to Edge TPU". Any "Operation will run on CPU" line at the middle of the network = latency disaster (data ping-pongs between TPU and CPU).
- Keep input ≤ 448×448; the TPU has 8 MB SRAM and larger models stream weights from USB, which dominates latency on the USB Coral.

### Pipeline overhead — the silent fps killer

```
camera (V4L2/Argus) → colorspace convert → resize/letterbox → normalize → NCHW
```
On Jetson, do this on GPU: use **DeepStream**, **jetson-utils**, or NVMM buffers in GStreamer (`nvvidconv`, `nvstreammux`). A CPU `cv2.resize` + `np.transpose` on a 1080p frame costs 5–15 ms — often more than nano-model inference. Also:
- Pin host memory and use CUDA streams for async H2D/D2H if writing raw TensorRT.
- NMS: export with NMS fused into the engine (Ultralytics `nms=True` on export, or EfficientNMS_TRT plugin). Python-side NMS on hundreds of candidates costs milliseconds and jitters.

---

## 3. Training Custom Detectors for Robot Viewpoints

### Why COCO-pretrained models fail on robots

COCO images are human-eye-level, human-photographer-framed. Robot cameras are:
- **Low (0.2–0.5 m AGV/AMR height)** — objects seen from below, floors dominate the frame
- **High and tilted (ceiling/mast mounts)** — strong perspective foreshortening
- **Close** — objects clipped by frame edges constantly
- **Moving** — motion blur, rolling-shutter skew

A COCO-pretrained person detector can drop 20–30 points of recall on a 30 cm tall robot looking up at people. You must fine-tune on data from the actual robot viewpoint.

### Dataset collection protocol

1. **Collect from the robot itself**, with the deployment camera, mount, and lens. Record rosbags / videos while driving the robot through deployment-like environments.
2. Sample frames at 1–2 Hz from video (consecutive frames are near-duplicates and inflate dataset size without information; they also leak between train/val).
3. **Split by recording session, never by random frame.** Random-frame splits put near-identical frames in train and val → val mAP lies to you by 10–20 points.
4. Minimum viable: **~1500 annotated instances per class** for fine-tuning from COCO weights; 5000+ for reliable production. Hard classes (small, deformable, reflective) need more.
5. Deliberately capture the tails: each lighting condition (morning/evening/artificial), occlusion levels, distance bands (near/mid/far), motion blur (record while driving at max speed).

### Annotation rules that matter

- Tool: **CVAT** (self-hosted, free, video interpolation support) or **Label Studio**; Roboflow if you want hosted + augmentation pipeline.
- Box convention: **amodal-lite** — box the visible extent, but DO label objects that are >20–30% visible. If you skip partially occluded objects, the model learns occlusion = background and your tracker loses IDs at every occlusion event.
- Label truncated objects at frame edges (box clipped to frame). Robots see edge-truncated objects constantly.
- Consistency beats precision: one annotator's consistent ±3 px sloppiness is fine; two annotators with different occlusion policies is poison. Write a 1-page labeling spec with picture examples before anyone labels.
- Audit: review a random 5% of labels per batch; track per-annotator disagreement.

### Training configuration (Ultralytics, fine-tune from COCO)

```yaml
# train command
# yolo detect train data=dataset.yaml model=yolov8n.pt epochs=100 imgsz=640 batch=64
# Key hyperparameters and why:

lr0: 0.01           # default SGD; for small datasets (<5k imgs) use 0.001–0.005
epochs: 100         # small custom sets converge in 50–150; watch val mAP plateau
patience: 30        # early stopping
imgsz: 640          # match deployment input size! training at 640, deploying at 320 loses mAP
batch: 64           # or max that fits; use batch=-1 for auto

# Augmentation — tune for robot reality:
mosaic: 1.0         # keep ON, but set close_mosaic: 10 (off for last 10 epochs)
degrees: 5.0        # robot cameras are roughly level; ±5° covers vibration/ramps.
                    # If camera can tilt (gimbal, uneven terrain) raise to 15
fliplr: 0.5         # fine for most classes; DISABLE (0.0) if left/right matters
                    # (e.g., reading arrows, asymmetric machinery)
flipud: 0.0         # robots don't see the world upside down — leave off
scale: 0.5          # important: covers distance variation
translate: 0.1
hsv_h: 0.015        # color jitter — raise hsv_v to 0.6 if lighting varies a lot
hsv_s: 0.7
hsv_v: 0.4
mixup: 0.0          # usually unnecessary for <10-class robot problems
erasing: 0.4        # random erasing simulates occlusion — keep on
```

**Augmentations to ADD for robots (offline or custom pipeline, e.g. Albumentations):**
- **Motion blur** (`MotionBlur(blur_limit=9)`) — the #1 missing augmentation; matches what a moving robot actually sees.
- **Gaussian noise / ISO noise** — low-light sensor gain.
- Gamma/brightness extremes — auto-exposure swings when the robot turns toward a window.

**Do NOT augment with:** large rotations (unless the camera really rotates), vertical flips, or unrealistic color shifts that can't occur with your sensor.

### Evaluation that predicts field performance

- Report **per-class recall at deployment confidence threshold**, not just mAP. A robot that misses 1 in 10 pallets is broken regardless of mAP.
- Build a **hard-case val slice** (night, blur, occlusion) and track it separately. Aggregate mAP hides regressions on the 5% of frames that cause incidents.
- Confidence threshold: deploy at the threshold that hits your required precision on val (for safety-relevant detection, tune for recall and let the tracker filter false positives). Typical starting point: `conf=0.25` feeding a tracker, `conf=0.5` if used raw.
- **Closed-loop test before shipping:** run the full robot behavior with the new model in the real environment. Detection metrics do not capture flicker, latency, or tracker interaction.

### Active learning loop (this is how production fleets actually improve)

1. Deploy with logging of: low-confidence detections (0.2–0.5), frames where tracker lost an ID, frames where downstream behavior aborted.
2. Pull those frames weekly, annotate, add to train set.
3. Retrain, validate on frozen hard-case slice + new data, redeploy.
This loop matters more than any architecture choice. Budget for it.

---

## 4. Tracking: SORT vs ByteTrack vs Per-Frame Detection

### When you need a tracker

Per-frame detection gives you *what is in this frame*. Robots almost always need *the same object over time*: to follow a person, estimate velocity, avoid double-counting, or keep behavior stable when detection flickers. If your downstream code has any notion of "the object", you need a tracker.

Per-frame only is fine for: stateless counting on stationary camera with one object, presence/absence triggers, inspection snapshots.

### Algorithm selection

| Tracker | Cost | Strengths | Use when |
|---|---|---|---|
| **SORT** | ~0 (Kalman + Hungarian on IoU) | Trivial, fast | Few objects, low occlusion, high fps |
| **ByteTrack** | ~0 (same machinery, smarter association) | Recovers low-confidence detections → far fewer ID switches during blur/occlusion | **Default choice for robots** |
| **BoT-SORT** | + camera motion compensation, optional ReID | Handles moving camera better | Camera on fast-moving/turning robot |
| DeepSORT/StrongSORT (ReID embedding) | +5–15 ms (embedding net) | Re-identify after long occlusion | Person tracking with long occlusions; check latency budget first |

**ByteTrack's key idea:** associate high-confidence detections first, then match remaining tracks against *low*-confidence detections (which are usually true objects that got blurry/occluded) instead of discarding them. This single trick removes most ID switches with zero compute cost. It's why ByteTrack is the default.

Ultralytics has both built in:

```python
results = model.track(source=frame_stream, tracker="bytetrack.yaml",
                      persist=True, conf=0.1)  # note LOW conf: ByteTrack
                      # needs the low-score detections; it filters internally
```

### Tuning ByteTrack for a robot (bytetrack.yaml)

```yaml
track_high_thresh: 0.5    # first-pass association threshold
track_low_thresh: 0.1     # second pass — keep low; this is the magic
new_track_thresh: 0.6     # require high conf to BIRTH a track (suppresses FP tracks)
track_buffer: 30          # frames to keep a lost track alive.
                          # = seconds_of_tolerable_occlusion × fps.
                          # At 15 fps and 2 s occlusions → 30. Too high = ID theft
                          # (track jumps to a different object after occlusion)
match_thresh: 0.8         # IoU match threshold
fuse_score: true
```

**Robot-specific gotchas:**
- **Camera motion breaks IoU association.** Kalman in SORT/ByteTrack assumes objects move smoothly in *image* space. When the robot turns fast, everything jumps. Fixes, in order of preference: (1) feed robot odometry/IMU to predict per-frame image shift and compensate boxes before association; (2) use BoT-SORT's GMC (global motion compensation); (3) raise `match_thresh` tolerance / lower fps expectations during turns.
- **Tracker state must be reset** when the stream restarts or you teleport (relocalization). Stale Kalman states produce ghost tracks.
- **Track IDs are not persistent identities.** ID 7 today is not ID 7 after the person left and returned. If your task needs true re-identification, you need a ReID embedding + gallery, which is a separate (and brittle) system — don't pretend `track_buffer: 9999` does this.
- A tracker also **smooths your boxes** — use the Kalman-filtered box, not the raw detection, for downstream distance estimation. It cuts distance jitter substantially.
- Latency note: tracking adds <1 ms. The reason fps still matters: association quality degrades quadratically with inter-frame motion. **15 fps tracked > 5 fps with a fancier detector**, almost always.

---

## 5. Distance Estimation from Bounding Box + Known Height

### The pinhole model (this is the whole trick)

For an object of known real height `H` (meters), appearing `h` pixels tall, with camera focal length `f_y` (pixels, from intrinsics):

```
Z = f_y * H / h
```

Worked example: person (H = 1.7 m), camera with f_y = 900 px (typical 1080p webcam ~70° VFOV), bbox height h = 300 px:

```
Z = 900 × 1.7 / 300 = 5.1 m
```

Lateral offset from image center (c_x, also from intrinsics):

```
X = (u - c_x) * Z / f_x      # u = bbox center x (pixels)
```

So a full 3D-ish position in the camera frame: `(X, Y≈via same formula with v−c_y, Z)`.

### Implementation

```python
import numpy as np

class BBoxRangeEstimator:
    """Distance from bbox using known object height. Camera must be calibrated."""
    def __init__(self, fx: float, fy: float, cx: float, cy: float,
                 known_heights: dict[int, float]):
        # fx, fy, cx, cy from camera calibration (K matrix), pixels.
        # known_heights: class_id -> real height in meters, e.g. {0: 1.70}
        self.fx, self.fy, self.cx, self.cy = fx, fy, cx, cy
        self.known_heights = known_heights

    def estimate(self, cls_id: int, x1, y1, x2, y2):
        H = self.known_heights.get(cls_id)
        if H is None:
            return None
        h_px = y2 - y1
        if h_px < 8:                      # too small → range error explodes
            return None
        Z = self.fy * H / h_px            # forward distance, camera frame (m)
        u = 0.5 * (x1 + x2)
        X = (u - self.cx) * Z / self.fx   # lateral offset (m), +right
        return X, Z
```

**You must use calibrated intrinsics** (`cv2.calibrateCamera` with a checkerboard, or the values from your camera's factory calibration / `camera_info` topic in ROS2). Guessing `f` from the spec-sheet FOV is good to ~5–10%; calibration gets you to ~1%. Also **undistort the image (or at least the bbox corner points) first** — at the edges of a wide-FOV lens, distortion alone produces 10–20% range error.

### Error model — know when to trust it

Differentiating Z = f·H/h:

```
ΔZ/Z = ΔH/H + Δh/h
```

- **Δh (bbox jitter):** detection boxes jitter ±2–4 px. At h = 40 px that's ±5–10% range error; at h = 15 px it's ±20%+. **Practical floor: don't trust ranges when bbox height < ~20 px.** Using the Kalman-smoothed (tracker) box instead of the raw box roughly halves Δh.
- **ΔH (object height variance):** people are 1.5–1.9 m → using H = 1.7 m gives ±12% systematic error per individual (but consistent per track, so velocity estimates are still good). For rigid known objects (pallet, cone, AprilTag-sized fixture) ΔH ≈ 0 and this method is genuinely accurate.
- **Box ≠ full object:** occlusion (legs hidden behind a desk) shrinks h → overestimates... no — shrinking h *increases* Z estimate → object appears farther than it is. **This is the dangerous failure mode for obstacle avoidance: a half-occluded person reads as 2× distance.** Mitigations: use bbox *width* with known width as cross-check; flag tracks whose bottom edge touches another object's box; for people, prefer keypoint-based height (torso keypoints, e.g. shoulder–hip distance scaled) which is robust to leg occlusion.
- **Truncation at frame edge:** if the box touches the top or bottom image border, h is clipped → range is garbage. Always check `y1 <= 2 or y2 >= img_h - 2` and discard/flag.
- Pitch: if the camera pitches (ramp, suspension dive), the *ground-plane* alternative method breaks but the known-height method is unaffected — that's its main virtue. Conversely the known-height method needs per-class height priors; the ground-plane method (`Z = f·camera_height / (v_bottom − c_y)`, requires flat floor + known camera height + pitch) works for any object touching the ground. Production systems often fuse both and cross-check.

### When to stop and use real depth

Bbox-range is a 0-cost monocular hack, good to ~10–15% for cooperative cases. If your application needs better than that, or non-flat terrain, or unknown objects: use a stereo/ToF depth camera (RealSense D4xx, OAK-D, Zed) and read the median depth inside the bbox (median, not mean — mean is corrupted by background pixels inside the box). The fusion pattern:

```python
depth_roi = depth_image[int(y1):int(y2), int(x1):int(x2)]
valid = depth_roi[(depth_roi > 0.3) & (depth_roi < 8.0)]   # clip sensor range
Z = float(np.median(valid)) if valid.size > 100 else None
```

---

## 6. ROS2 Integration Pattern

Reference architecture for a detection node (Jetson, TensorRT):

```
/camera/image_raw (or NVMM/GStreamer direct)        ← prefer image_transport
        │
   [detector node]  — TensorRT engine, GPU preprocess, fused NMS
        │            — ByteTrack association
        │            — bbox→range estimation
        ▼
/detections  (vision_msgs/Detection2DArray, with track id in `id`,
              range packed in results[0].pose or a custom msg)
/detections/markers (visualization_msgs/MarkerArray for RViz)
```

Hard-won rules:
- **Use sensor-data QoS** (`best_effort`, `keep_last`, depth 1) for image subscription. Reliable QoS on images causes queue buildup → seconds of latency that looks like "slow inference".
- **Process the latest frame, drop the rest.** A detector that queues frames falls progressively behind. Pattern: subscriber writes to a 1-slot mailbox; inference loop in its own thread/executor takes whatever is newest.
- **Stamp detections with the CAMERA frame timestamp**, not `now()`. Downstream TF lookups (transforming the detected object into `map`/`base_link` at the moment of capture) need the capture stamp. Using `now()` smears object positions by the full pipeline latency × robot speed.
- Publish a heartbeat/diagnostics topic with measured fps and pipeline latency. The first symptom of thermal throttling on a Jetson is fps sag — you want an alarm, not a mystery.
- On Jetson, watch `tegrastats` under sustained load: a passively cooled Orin Nano throttles after ~10 min at max clocks. Fit a fan; validate fps after 30 min soak, not 30 s.

---

## 7. Production Failure Modes Checklist

Run through this before declaring the system done:

1. **Engine built on wrong device/JetPack** → crash or silent kernel mismatch. Build on target, cache by version.
2. **INT8 calibrated on the wrong distribution** → 3–10 mAP silently gone. Calibrate on deployment-domain images, validate INT8 vs FP16.
3. **CPU preprocessing eating the budget** → "model is fast, system is slow." Profile every stage; GPU-side resize/convert on Jetson.
4. **Val set leaked from train (random frame split)** → great val mAP, terrible field performance. Split by session.
5. **Occluded objects unlabeled** → tracker drops IDs at every occlusion. Label partials.
6. **Confidence threshold tuned on easy data** → night-time recall collapse. Maintain a hard-case slice.
7. **Tracker not reset on stream restart**; **track_buffer too long** → ghost tracks, ID theft.
8. **Camera turns fast → IoU association fails** → ID switch storm. Motion-compensate with odometry or BoT-SORT GMC.
9. **Range from truncated/occluded bbox** → object reported farther than it is (safety hazard). Reject border-touching boxes; cross-check with width.
10. **Uncalibrated/distorted camera for ranging** → 10–20% systematic range error at image edges. Calibrate, undistort.
11. **Thermal throttling after minutes** → fps decays in the field but not on the bench. Soak test 30+ min, monitor temps.
12. **Auto-exposure swings** (robot turns toward window) → frames of total blindness. Lock exposure if environment allows, or train with brightness-extreme augmentation and tolerate it in the tracker (`track_buffer`).
13. **Queue buildup in ROS subscription** → multi-second latency with perfect fps. Sensor-data QoS + latest-frame mailbox.
14. **AGPL license surprise** (Ultralytics) in a closed-source product. Decide licensing before training, not before shipping.

---

## 8. Quick Reference: Starting Values

| Parameter | Start value | Notes |
|---|---|---|
| Model | YOLOv8n / YOLO11n | Move up only if val proves you must |
| Input size | 640 (Jetson) / 320–448 (Pi, Coral) | Train at deploy size |
| Precision | FP16 first, then INT8 | Validate INT8 ≤2 mAP drop |
| Calibration images | 300–1000, deployment domain | |
| Detection conf (→tracker) | 0.1 (ByteTrack handles it) | |
| Detection conf (raw use) | 0.4–0.6, tuned on val | |
| NMS IoU | 0.45–0.7 | 0.7 if objects overlap heavily |
| Tracker | ByteTrack | BoT-SORT if camera moves fast |
| track_buffer | occlusion_seconds × fps | typically 30 @ 15 fps |
| new_track_thresh | 0.6 | |
| Min bbox height for ranging | 20 px | |
| Instances per class (fine-tune) | 1500+ (5000+ production) | |
| Epochs (fine-tune) | 100, patience 30 | |
| Soak test | 30 min, monitor tegrastats | |
