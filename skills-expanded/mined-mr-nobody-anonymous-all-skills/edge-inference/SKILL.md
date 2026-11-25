---
name: edge-inference
description: "Use when deploying ML inference on embedded robotics hardware — Jetson Orin Nano, Google Coral, or Raspberry Pi with accelerators. Provides platform selection criteria, TensorRT ONNX→engine conversion with FP16/INT8 calibration, quantization accuracy tradeoffs, latency vs batching math, thermal throttling mitigation, and inference watchdog patterns for production robots."
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


# Edge Inference for Robotics

Expert knowledge for running neural network inference on robot-mounted compute. Covers platform selection, TensorRT workflows, quantization, thermal management, and production reliability patterns.

## 1. Platform Selection — The Real Numbers

| Spec | Jetson Orin Nano 8GB | Coral USB Accelerator | Coral Dev Board (mini) | RPi 5 + NCS2* | RPi 5 + Hailo-8L |
|---|---|---|---|---|---|
| Peak compute | 40 TOPS (INT8, sparse) / ~20 dense | 4 TOPS (INT8 only) | 4 TOPS | 1 TOPS (FP16) | 13 TOPS (INT8) |
| Power | 7W / 15W modes (25W on Super) | 2W (USB) | 3W | 2W | 2.5W typical |
| RAM for model | shared 8GB LPDDR5 | 8MB on-chip SRAM only | 8MB SRAM | 512MB | shared host RAM via PCIe |
| Framework | TensorRT, ONNX-RT, PyTorch | TFLite (EdgeTPU compiler) | TFLite | OpenVINO | HailoRT |
| FP16 support | Yes | No — INT8 only | No | Yes | No (INT8/INT4) |
| Dynamic shapes | Yes (optimization profiles) | No — fully static | No | Limited | No |
| Price (2025) | ~$249 (Super dev kit) | ~$60 | ~$100 | discontinued | ~$70 (M.2 HAT kit) |
| Boot-to-inference | ~25s (Ubuntu) | host-dependent | ~15s | host | host |

*NCS2 discontinued 2023 — do not design new robots around it. Listed because fleets still run it.

**Decision tree:**
- Need transformers, multi-model pipelines, or anything >10MB of weights resident → **Jetson Orin Nano**. The Coral's 8MB SRAM forces weight streaming over USB for big models, killing throughput (a model >~6MB compiled drops from 400 FPS to <40 FPS on Coral).
- Single small CNN (MobileNet/EfficientDet-Lite class, <6MB INT8), battery-critical, <3W budget → **Coral USB** on any host. 2W for ~400 inferences/sec MobileNetV2 is unbeatable perf/W.
- RPi-based robot needing object detection ~30 FPS at low cost → **RPi 5 + Hailo-8L M.2 HAT** (the official "AI Kit"). YOLOv8s at ~30 FPS, 640×640.
- ROS 2 stack, CUDA libraries, Isaac ROS, visual SLAM, multiple cameras → Jetson, no contest. Coral/Hailo can't run cuVSLAM, nvblox, or anything CUDA.

**Coral gotcha:** EdgeTPU compiler only maps ops it supports; unsupported ops fall back to CPU **and everything after the first unsupported op runs on CPU** — the compiler partitions once, not per-op. One stray op in the middle of your graph CPU-bounds the whole tail. Check with `edgetpu_compiler -s model.tflite` and read the "Operations mapped to Edge TPU" count.

**Jetson Orin Nano power modes** (set before benchmarking — results are meaningless otherwise):
```bash
sudo nvpmodel -m 0        # MAXN (15W, or 25W on Super with JetPack 6.2)
sudo nvpmodel -m 1        # 7W mode
sudo jetson_clocks        # lock clocks to max (disables DVFS) — do this for benchmarks
sudo nvpmodel -q          # verify current mode
tegrastats                # live power/temp/util monitor
```
A model benchmarked at MAXN with jetson_clocks will run ~40-60% slower at 7W with DVFS. Quote both numbers in your design docs.

## 2. TensorRT Workflow: ONNX → Engine

### 2.1 Export PyTorch → ONNX correctly

```python
import torch

model.eval()                                  # MUST — BN/dropout in train mode poisons the graph
dummy = torch.randn(1, 3, 640, 640)           # batch=1 if static; see dynamic axes below

torch.onnx.export(
    model, dummy, "model.onnx",
    opset_version=17,                         # 17+ for TensorRT 8.6/10.x; 13 minimum
    input_names=["images"],
    output_names=["output"],
    dynamic_axes={"images": {0: "batch"},     # ONLY if you actually need dynamic batch
                  "output": {0: "batch"}},
    do_constant_folding=True,
)
```

Then simplify — TensorRT chokes on redundant ONNX patterns (Gather/Unsqueeze chains from `.shape` calls):
```bash
pip install onnxsim
python -m onnxsim model.onnx model_sim.onnx
python -c "import onnx; m=onnx.load('model_sim.onnx'); onnx.checker.check_model(m)"
```

**Export mistakes everyone makes:**
- Exporting with `model.train()` active — silent, produces garbage accuracy.
- Python `if x.shape[0] > 1:` in forward() → traced as constant, breaks dynamic batch. Use `torch.jit.script` semantics or remove data-dependent control flow.
- NMS inside the ONNX graph. TensorRT supports `EfficientNMS_TRT` plugin but plain ONNX `NonMaxSuppression` is slow/fragile. For YOLO: export without NMS, do NMS on CPU, or use the TRT plugin via `trtexec --plugins` / Ultralytics `format=engine`.
- Mismatched normalization: if you bake `/255` and mean/std into the model, do NOT also do it in preprocessing. Pick one place. This is the #1 "engine runs but detects nothing" bug.

### 2.2 Build the engine

**FP16 (do this first, always):**
```bash
trtexec --onnx=model_sim.onnx \
        --saveEngine=model_fp16.engine \
        --fp16 \
        --memPoolSize=workspace:2048 \
        --verbose 2>&1 | tail -20
```

**Dynamic batch (only if needed — static is faster to build and slightly faster to run):**
```bash
trtexec --onnx=model_sim.onnx --saveEngine=model_fp16.engine --fp16 \
        --minShapes=images:1x3x640x640 \
        --optShapes=images:4x3x640x640 \
        --maxShapes=images:8x3x640x640
```
TensorRT optimizes kernels for `optShapes`. Running at batch=1 with opt=8 costs ~10-20% vs a batch=1-optimized engine.

**Engine portability rule:** engines are specific to (GPU compute capability, TensorRT version). An engine built on a desktop 4090 will NOT load on Orin (SM 8.7). Build on-device, or cross-compile with `--hardwareCompatibilityLevel` (TRT ≥8.6, perf penalty). Always rebuild after JetPack upgrades. Cache engines keyed by `(model_hash, trt_version, gpu_name)`:

```python
import tensorrt as trt, hashlib, os

def engine_path(onnx_path):
    h = hashlib.sha256(open(onnx_path, "rb").read()).hexdigest()[:12]
    return f"/var/cache/trt/{h}_trt{trt.__version__}.engine"

def load_or_build(onnx_path):
    p = engine_path(onnx_path)
    if os.path.exists(p):
        return open(p, "rb").read()
    logger = trt.Logger(trt.Logger.WARNING)
    builder = trt.Builder(logger)
    network = builder.create_network(
        1 << int(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH))
    parser = trt.OnnxParser(network, logger)
    if not parser.parse(open(onnx_path, "rb").read()):
        raise RuntimeError([parser.get_error(i) for i in range(parser.num_errors)])
    config = builder.create_builder_config()
    config.set_memory_pool_limit(trt.MemoryPoolType.WORKSPACE, 2 << 30)
    config.set_flag(trt.BuilderFlag.FP16)
    blob = builder.build_serialized_network(network, config)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "wb").write(blob)
    return bytes(blob)
```

Engine build on Orin Nano takes 2-10 min for a YOLO-class model. Never build in the robot's startup critical path without the cache above.

### 2.3 INT8 calibration

INT8 needs a calibration dataset: **500-1000 images from your robot's actual camera, in deployment conditions** (lighting, lens, mounting angle). COCO images calibrating a robot that looks at a warehouse floor = accuracy cliff.

```python
import tensorrt as trt
import numpy as np
import pycuda.driver as cuda
import pycuda.autoinit

class Calibrator(trt.IInt8EntropyCalibrator2):
    def __init__(self, image_dir, batch_size=8, cache="calib.cache"):
        super().__init__()
        self.cache_file = cache
        self.batch_size = batch_size
        self.files = sorted(glob.glob(f"{image_dir}/*.npy"))  # pre-preprocessed!
        self.idx = 0
        self.device_input = cuda.mem_alloc(batch_size * 3 * 640 * 640 * 4)

    def get_batch_size(self):
        return self.batch_size

    def get_batch(self, names):
        if self.idx + self.batch_size > len(self.files):
            return None
        batch = np.stack([np.load(f) for f in
                          self.files[self.idx:self.idx + self.batch_size]])
        self.idx += self.batch_size
        cuda.memcpy_htod(self.device_input, np.ascontiguousarray(batch, dtype=np.float32))
        return [int(self.device_input)]

    def read_calibration_cache(self):
        if os.path.exists(self.cache_file):
            return open(self.cache_file, "rb").read()

    def write_calibration_cache(self, cache):
        open(self.cache_file, "wb").write(cache)

# in build config:
config.set_flag(trt.BuilderFlag.INT8)
config.set_flag(trt.BuilderFlag.FP16)        # keep FP16 fallback for layers INT8 hurts
config.int8_calibrator = Calibrator("calib_images/")
```

**Critical:** calibration images must go through the EXACT same preprocessing as inference (resize method, RGB vs BGR, normalization). A BGR/RGB mismatch in calibration costs 5-15 mAP silently.

Use `IInt8EntropyCalibrator2` (default choice). `MinMaxCalibrator` only for models with genuinely wide activation ranges (some transformers).

## 3. Quantization Accuracy Tradeoffs

Typical accuracy deltas vs FP32 (detection mAP@50-95, well-calibrated):

| Model class | FP16 | INT8 PTQ | INT8 QAT |
|---|---|---|---|
| ResNet/MobileNet classifiers | −0.0 to −0.1% | −0.3 to −1% | ≈FP32 |
| YOLOv8/YOLO11 detectors | −0.0 to −0.2 | −1 to −3 mAP | −0.3 to −1 |
| Small models (<5M params) | ~0 | −2 to −6 | −1 to −2 |
| Transformers/ViT | ~0 | −2 to −10 (PTQ struggles) | −1 to −3 |
| Depth/segmentation (dense regression) | ~0 | visible artifacts possible | usually fine |

Rules:
- **FP16 is free.** ~2× speedup on Orin vs FP32, accuracy loss within noise. Always ship at least FP16.
- **INT8 gains another ~1.5-1.8× on Orin** (not 2× — memory bandwidth and the FP16-fallback layers eat into it). Worth it for big models or tight power budgets; skip it if FP16 already meets your latency target (Karpathy rule: don't buy speed you don't need with accuracy you do).
- Small models quantize worse — fewer channels means each quantization bucket covers more dynamic range.
- First and last layers are most sensitive. If INT8 accuracy is bad, force them to FP16:
```python
for i in range(network.num_layers):
    layer = network.get_layer(i)
    if layer.name in ("first_conv", "head_conv"):
        layer.precision = trt.float32   # or float16
```
- If PTQ drops >2 mAP and you need INT8: do QAT (`pytorch-quantization` / `torchao`) — train 1-3 epochs with fake-quant, re-export. QAT recovers most of the gap.
- Coral has no choice: full INT8 PTQ via TFLite converter with `representative_dataset`. Same rule — representative data from the real camera.

**Accuracy gate (enforce in CI):** run the quantized engine on a held-out eval set before deploying. Define a hard floor (e.g., ≥97% of FP32 mAP). A robot misdetecting obstacles because someone skipped the eval is a safety incident, not a perf bug.

## 4. Latency vs Batching

Robots are latency systems, not throughput systems. The control loop cares about photon-to-action time.

Measured-class numbers, YOLOv8n 640×640 FP16 on Orin Nano 8GB (15W, clocks locked):
- batch=1: ~8-10 ms GPU time → can hold 60+ FPS single camera
- batch=4: ~24 ms total → 6 ms/image throughput, but **the first image waited up to 3 frame-times to fill the batch**

Batching math: at 30 FPS camera, filling batch=4 adds up to 100 ms of queueing latency. For a robot at 1 m/s that's 10 cm of blind travel. **Use batch=1 for control-loop perception. Batch only when (a) multiple cameras produce frames simultaneously — batch those, they share a timestamp — or (b) offline/non-realtime analysis.**

End-to-end latency budget (where time actually goes on Jetson):
```
camera exposure+readout   8-20 ms   (you can't fix this in software)
USB/CSI transfer          2-15 ms   (CSI << USB webcam)
CPU preprocess (resize,   3-12 ms   ← often slower than inference! Use GPU:
  normalize, HWC→CHW)               cv2.cuda, NPP, or DALI/nvjpeg on Jetson
H2D copy                  0.5-2 ms  (use pinned memory: cuda.pagelocked_empty)
GPU inference             8-10 ms
D2H copy + postprocess    1-5 ms    (NMS on CPU; keep tensors small)
```
**Pin host memory and use CUDA streams** — pageable-memory copies are 2-3× slower and serialize:

```python
import pycuda.driver as cuda

h_in  = cuda.pagelocked_empty(trt.volume(in_shape), dtype=np.float32)
d_in  = cuda.mem_alloc(h_in.nbytes)
h_out = cuda.pagelocked_empty(trt.volume(out_shape), dtype=np.float32)
d_out = cuda.mem_alloc(h_out.nbytes)
stream = cuda.Stream()

def infer(frame_chw):
    np.copyto(h_in, frame_chw.ravel())
    cuda.memcpy_htod_async(d_in, h_in, stream)
    context.execute_async_v3(stream.handle)        # TRT 10; v2 on TRT 8
    cuda.memcpy_dtoh_async(h_out, d_out, stream)
    stream.synchronize()
    return h_out.reshape(out_shape)
```

**Frame dropping policy:** always process the NEWEST frame, drop stale ones. A queue that buffers frames gives you smooth FPS numbers and a robot reacting to 500 ms-old images.
```python
# ROS 2: queue_size=1 + best-effort QoS = automatic newest-frame behavior
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
qos = QoSProfile(reliability=ReliabilityPolicy.BEST_EFFORT,
                 history=HistoryPolicy.KEEP_LAST, depth=1)
self.create_subscription(Image, "/camera/image_raw", self.cb, qos)
```

## 5. Thermal Throttling

This is the silent killer of robot perception. Bench tests pass; the robot fails 20 minutes into a mission.

**Jetson Orin Nano thermals:**
- Throttle (soft) begins ~ **95-97 °C** on the CPU/GPU thermal zones; hardware shutdown ~105 °C.
- The dev kit's stock fan keeps MAXN sustainable in open air at ~25 °C ambient. Inside a sealed robot chassis at 35 °C ambient it will NOT — expect throttling within 10-20 min of continuous inference.
- Throttling cuts GPU clocks from ~625 MHz (Nano) progressively; inference latency can rise 50-100%. Your 10 ms model becomes 18 ms and your control loop misses deadlines.

**Monitor it — every production robot should run this:**
```python
def read_temps():
    temps = {}
    import glob
    for zone in glob.glob("/sys/devices/virtual/thermal/thermal_zone*"):
        ttype = open(f"{zone}/type").read().strip()
        temps[ttype] = int(open(f"{zone}/temp").read()) / 1000.0  # millidegC
    return temps   # keys like 'cpu-thermal', 'gpu-thermal', 'tj-thermal'
```
Or `tegrastats --interval 1000` and parse. Log GPU temp + inference latency together — the correlation is your throttling smoking gun.

**Mitigations, in order of effectiveness:**
1. **Run at 7W mode if it meets latency targets.** Half the heat, and a 7W-sustained system beats a 15W-throttling one.
2. Duty-cycle the model: 30 FPS camera does not require 30 FPS inference for most tasks. 10 Hz detection + visual tracking between detections cuts GPU load ~3×.
3. Better heatsink/fan; thermal path to chassis (the chassis IS a heatsink — use a thermal pad to the module's TTP).
4. INT8 — less compute per inference = less heat.
5. Fan control: `sudo sh -c 'echo 255 > /sys/devices/platform/pwm-fan/hwmon/hwmon*/pwm1'` (JetPack 5/6 paths vary; `nvfancontrol` config in JetPack 6).

**Coral USB throttling:** the USB stick hits thermal limits in ~2-5 min of sustained max-rate inference and silently halves its clock (`libedgetpu` "max" vs "std" — `std` runtime is pre-throttled to the safe clock). If you ship the `max` runtime, you MUST heatsink it. Symptom: inference time doubles, no error raised.

**RPi 5:** throttles at 85 °C; check `vcgencmd get_throttled` (non-zero = has throttled since boot, bit 2 = currently throttling). Active cooler is mandatory with the Hailo HAT.

## 6. Inference Watchdogs & Production Reliability

GPU inference fails in ways CPU code doesn't: CUDA context corruption, ECC errors, driver hangs after thermal events, slow memory leaks in stream handling. A robot must detect "perception is dead/degraded" and act (stop, slow, fall back).

**Pattern 1 — latency + heartbeat watchdog (run inference in its own process):**

```python
import multiprocessing as mp, time, os, signal

def inference_worker(frame_q, result_q, heartbeat):
    engine = load_engine()                     # init CUDA in the CHILD only —
    while True:                                # CUDA contexts don't survive fork
        frame = frame_q.get()
        t0 = time.monotonic()
        result = engine.infer(frame)
        heartbeat.value = time.monotonic()
        result_q.put((result, time.monotonic() - t0))

class InferenceSupervisor:
    LATENCY_BUDGET = 0.050    # 50 ms hard deadline
    HEARTBEAT_TIMEOUT = 2.0   # no inference completed in 2 s → worker is hung

    def __init__(self):
        mp.set_start_method("spawn", force=True)   # MANDATORY with CUDA
        self.heartbeat = mp.Value("d", time.monotonic())
        self._spawn()
        self.degraded_count = 0

    def _spawn(self):
        self.frame_q, self.result_q = mp.Queue(maxsize=1), mp.Queue(maxsize=1)
        self.proc = mp.Process(target=inference_worker,
                               args=(self.frame_q, self.result_q, self.heartbeat),
                               daemon=True)
        self.proc.start()

    def check(self):
        """Call from your control loop at >= 10 Hz."""
        if not self.proc.is_alive():
            return "DEAD"                            # crashed — restart + safe stop
        if time.monotonic() - self.heartbeat.value > self.HEARTBEAT_TIMEOUT:
            self.proc.kill()                         # hung CUDA call won't respond to SIGTERM
            self._spawn()
            return "RESTARTED"                       # robot should be in safe state already
        return "OK"

    def submit(self, frame):
        try:
            self.frame_q.put_nowait(frame)           # drop frame if worker busy — never block
        except Exception:
            pass
```

Why a separate process, not a thread: a hung CUDA kernel blocks the whole process; a Python thread can't be killed. `spawn` (not fork) because forking a process with an initialized CUDA context corrupts it.

**Pattern 2 — output sanity checks** (the model "works" but produces garbage after corruption):
```python
def sane(dets, latency):
    if latency > 0.050:                 return False  # deadline miss
    if np.any(~np.isfinite(dets)):      return False  # NaN/Inf = corrupted engine state
    if len(dets) > 300:                 return False  # confidence collapse → everything detected
    return True
```
Track a rolling window; 3 consecutive insane outputs → treat as perception failure.

**Pattern 3 — ROS 2 lifecycle + external watchdog:**
- Publish detections with `header.stamp` from the CAMERA frame time, not inference-completion time, so consumers can measure true data age.
- Downstream safety node: if newest detection is older than N ms → reduce speed / stop. This catches every failure mode above with one rule:
```python
age = (self.get_clock().now() - rclpy.time.Time.from_msg(msg.header.stamp)).nanoseconds / 1e9
if age > 0.2:
    self.cmd_vel_pub.publish(Twist())   # stop
```
- systemd unit for the whole node: `Restart=on-failure`, `WatchdogSec=5` + `sd_notify("WATCHDOG=1")` from the heartbeat. Two watchdog layers: in-process (fast, 50 ms granularity) and systemd (catches full-process hangs).

**Startup self-test (run before the robot is allowed to move):**
1. Load engine, run 5 warmup inferences (first 1-2 inferences are 5-20× slower — lazy CUDA init, cuDNN autotuning).
2. Run a golden image with known expected detections; assert IoU > 0.8 against stored reference. Catches wrong engine file, preprocessing drift, broken calibration.
3. Check temps < 70 °C and power mode == expected (`nvpmodel -q`).

## 7. Debugging Checklist

**Engine builds but detects nothing / garbage boxes:**
- [ ] RGB vs BGR mismatch (OpenCV is BGR; most models trained RGB). #1 cause.
- [ ] Double or missing normalization (`/255` and mean/std applied twice or zero times).
- [ ] HWC vs CHW layout — TRT wants NCHW; `frame.transpose(2, 0, 1)` and `ascontiguousarray`.
- [ ] Resize method mismatch: letterbox (YOLO) vs plain resize — boxes will be offset/scaled wrong.
- [ ] Exported in train mode (BN running stats not used).
- [ ] Output decode assumes wrong layout (YOLOv8 outputs `[1,84,8400]` — transposed vs v5's `[1,25200,85]`).

**Engine output differs from PyTorch:**
- [ ] Compare ONNX first: `onnxruntime` on the same input; if ONNX matches PyTorch, the bug is in TRT build or your runner. If ONNX differs, it's the export.
- [ ] `polygraphy run model.onnx --trt --onnxrt --atol 1e-3` — layer-by-layer comparison: `polygraphy debug precision` to find the layer FP16 broke.
- [ ] FP16 overflow in a layer (rare, real in models with large activations) — force that layer FP32.

**Latency higher than benchmarked:**
- [ ] `nvpmodel -q` — robot booted into 7W mode, benchmark ran at MAXN.
- [ ] Thermal throttling — log GPU temp with latency (Section 5).
- [ ] Preprocessing on CPU competing with ROS nodes — check `top`; pin inference process with `taskset`.
- [ ] Pageable memory copies / no streams (Section 4).
- [ ] Measuring first inference (no warmup).
- [ ] Dynamic-shape engine running far from optShapes.

**Intermittent failures in the field:**
- [ ] Power supply sag: Jetson brownouts under inference load spikes if supply can't deliver peak (Orin Nano dev kit needs 5V⎓4A USB-C minimum; budget 2× average current. Check `dmesg | grep -i "soctherm\|throttl\|under-voltage"`).
- [ ] RPi: `vcgencmd get_throttled` bit 0 = under-voltage now, bit 16 = has occurred.
- [ ] Coral USB on a shared USB hub with a camera — bandwidth contention; give the TPU its own root port (USB3).
- [ ] Slow memory leak: watch `tegrastats` RAM over an hour-long soak test; common cause is creating new TRT execution contexts per frame instead of reusing one.

**EdgeTPU model slow:**
- [ ] `edgetpu_compiler -s` — count CPU-mapped ops; one mid-graph fallback CPU-bounds everything after it.
- [ ] Model >6MB → weight streaming over USB. Shrink the model or move to Jetson/Hailo.
- [ ] `std` vs `max` libedgetpu runtime (max needs heatsinking).

## 8. Minimal Known-Good Stack Versions (mid-2025)

| Platform | Stack |
|---|---|
| Jetson Orin Nano | JetPack 6.2 (L4T r36.4), CUDA 12.6, TensorRT 10.3, Ubuntu 22.04 |
| Coral | `libedgetpu1-std`, `pycoral` 2.0, TFLite runtime 2.5 (pinned — pycoral breaks on newer Python; use Python ≤3.9 or the unofficial wheels) |
| RPi 5 + Hailo-8L | Raspberry Pi OS Bookworm 64-bit, `hailo-all` apt package, HailoRT 4.x, `rpicam-apps` post-processing or `hailo-rpi5-examples` |
| ROS 2 | Humble (Ubuntu 22.04 / JetPack 6) with Isaac ROS for NITROS zero-copy on Jetson |

Pin everything. "apt upgrade broke the robot" is a thing — TensorRT minor versions invalidate engine caches (handled if you key the cache per Section 2.2) and occasionally change plugin ABIs.
