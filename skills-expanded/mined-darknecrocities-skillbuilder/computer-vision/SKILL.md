---
name: computer-vision
description: Production Computer Vision pipelines (OpenCV, YOLO, ONNX Runtime, TensorRT, CoreML, MediaPipe, SAM2, ByteTrack, OCR) with bounded frame buffers, EXIF/letterbox hygiene, and deterministic GPU/session disposal.
---

# Computer Vision Engineering (`/computer-vision`)

> **Philosophy**: *Bound every frame queue, normalize orientation before inference, keep coordinates explicit, and release native capture/GPU handles deterministically.*

---

## 1. Progressive Disclosure References

| Resource | Purpose |
| :--- | :--- |
| [references/cv-runtime-and-frame-pipelines.md](references/cv-runtime-and-frame-pipelines.md) | RTSP/Webcam bounded ring buffers, ONNX/TensorRT/CoreML/WebGPU execution providers, latency budgets. |
| [references/detection-tracking-and-ocr.md](references/detection-tracking-and-ocr.md) | Letterbox scaling, ByteTrack/OC-SORT stability, SAM2 masks, OCR deskew & ROI cropping. |
| [scripts/verify_cv_hygiene.py](scripts/verify_cv_hygiene.py) | Audits unreleased `VideoCapture`, unbounded queues, missing EXIF transpose, blocking GUI calls, and implicit ONNX providers. |

---

## 2. CV Runtime Selection Matrix

| Workload | Recommended Stack | Target Hardware | Latency Target |
| :--- | :--- | :--- | :--- |
| **Live Detection / Tracking** | Ultralytics YOLO -> ONNX / TensorRT + ByteTrack | NVIDIA GPU / Jetson / CPU | `8–33 ms` (30+ fps) |
| **Apple Edge Vision** | CoreML (ANE/Metal) / Vision.framework | macOS / iOS Apple Silicon | `5–20 ms` |
| **Browser Client Vision** | ONNX Runtime Web (WebGPU) + MediaPipe WASM (Worker) | Chrome / Safari / Edge | `12–40 ms` |
| **Zero-Shot / Masks** | SAM2 / GroundingDINO (ROI-gated, never every frame) | Server GPU (`>= 8 GB` VRAM) | `80–350 ms` |
| **Document / Scene OCR** | PaddleOCR / DocTR (deskew + crop first) | CPU / GPU | `30–180 ms` |

---

## 3. Non-Negotiable Pipeline Invariants

1. **Bounded Frame Queues (`maxsize=2`)**: Live RTSP/WebRTC/Webcam readers MUST drop oldest frames when inference lags (`drop-oldest`), never accumulate unbounded `Queue()` buffers that OOM the host.
2. **Deterministic Handle Disposal**: Wrap `cv2.VideoCapture` in `try/finally` (`cap.release()`) and dispose ONNX/WebGPU/TensorRT sessions explicitly on shutdown.
3. **EXIF & Color Normalization**: Apply `ImageOps.exif_transpose()` on uploaded images and convert BGR (`cv2`) <-> RGB (`PIL`/PyTorch/ONNX) explicitly before inference.
4. **Explicit Coordinate Contracts**: Tag every bounding box schema with its exact space (`norm_0_1`, `norm_0_1000`, or `px_xyxy`) and un-letterbox detections back to original source dimensions.
5. **Headless Server Hygiene**: Never invoke blocking `cv2.imshow()` or `cv2.waitKey(0)` inside API servers, workers, or Docker containers.

---

## 4. Automated Hygiene Verification

```bash
python3 skills/computer-vision/scripts/verify_cv_hygiene.py --path . --strict
```
