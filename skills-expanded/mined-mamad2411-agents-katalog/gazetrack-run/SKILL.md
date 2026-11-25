---
name: gazetrack-run
description: How to run, verify and debug the gazetrack pipeline (camera check, environment check, live gaze inference, calibration flow). Use when running or troubleshooting any gazetrack component or when verifying changes end-to-end.
---

# Running and verifying gazetrack

All commands from the project root (`c:\xampp\htdocs\focus`), always with the
project venv: `.venv\Scripts\python.exe` (Python 3.10, torch 2.5.1+cu121).

## Verification ladder (run top to bottom when something is off)

1. `python check_env.py` — imports, CUDA build, GPU kernel launch, weights.
   If it reports a CPU-only torch build, reinstall with the command it prints.
2. `python check_env.py --camera` or `python -m capture.camera --preview` —
   the camera (c922 Pro Stream at index 1; index 0 is the integrated
   webcam) must deliver 1920x1080 at ~30 fps MEASURED. Trust measured fps
   only: FOURCC/focus/exposure readbacks are unreliable (MSMF returns
   garbage, DSHOW reports converted formats). The code opens MSMF with
   W/H/FPS params and no FOURCC on purpose — that is the only OpenCV path
   that gets MJPEG 1080p30 on this camera; do not revert it to DSHOW-first
   or add CAP_PROP_FOURCC to the MSMF params (MSMF fails to open with it).
   If ~5 fps: stream fell to YUY2 (DSHOW fallback engaged) or exposure is
   too long; `verify()` prints the diagnosis. If startup measured fps is
   ~30 but a live-check HUD shows low fps, the bottleneck is processing,
   not the camera.
   Focus: autofocus is off by design; if the image is blurred, run
   `python -m capture.camera --focus-sweep` (W/S focus, E/D exposure,
   ENTER saves to data/camera.yaml; all modes read it automatically).
3. `python -m gaze.mediapipe_head` — landmarks + head-pose axes must stick to
   the face; head yaw/pitch/roll readouts must be near 0 when frontal.
4. `python -m gaze.eth_xgaze` — live gaze: the drawn ray and yaw/pitch values
   must follow the eyes, including under moderate head rotation. At startup
   it prints a "PnP sanity: eye-to-camera distance" line; ~400-1000 mm is
   expected for desktop use. Out-of-range means the 3D face model scale is
   wrong and the patch will crop the eyes (gaze responds to head but not
   eyes, yaw looks stuck). Use `--show-patch` to inspect the normalized
   224x224 crop: BOTH EYES must be visible, centered and roll-corrected. If
   only nose+mouth show, `_PNP_MODEL_POINTS` is not in real mm - see
   CLAUDE.md. The model uses SOLVEPNP_SQPNP to avoid the near-planar mirror
   flip; do not switch it back to ITERATIVE.
5. `python main.py screen --screen-width-cm <W> --screen-height-cm <H>
   --distance-cm <D>` once to set physical geometry (persists to
   data/screen.yaml; resolution auto-detected). Then `calibrate` -> `demo`
   -> `evaluate`. Calibration is required before demo/record/evaluate (clear
   error if `data/calibration.yaml` is missing). Recalibrate after lighting
   or posture changes.
   - There is NO cm default: without screen.yaml, evaluate still reports px
     and %-of-width but omits cm/deg and says so. Rig here is a 49"
     ultrawide (~120 cm, detected 3840x1080); the old 34.4 cm laptop default
     made cm/deg wrong.
   - Calibration protocol on screen: look NATURALLY, move head+eyes as
     usual, hold steady while the ring contracts (head motion is a mapping
     feature, not something to suppress). `calibrate` prints per-target
     residuals, head yaw/pitch coverage, and flags high-variance ("you
     moved") or high-residual ("garbage") targets.
   - `evaluate` reports by zone (center/edge/corner) in px, %-of-width, and
     cm/deg when geometry is set.

## Debug knobs

- Camera: `--index N`, `--focus 0..250` (~50 at 60 cm), `--exposure -6`,
  `--keep-auto-exposure` (debug only; production runs with AE off).
- Inference: `--device cpu` isolates CUDA problems (slow, debug only).
- Weights re-download: delete `models/eth-xgaze_resnet18.pth` or run
  `python -m gaze.eth_xgaze --download-only`.

## Hard rules when touching code

- Layer separation: `gaze/` never knows about screens; `mapping/` never
  touches frames or the CNN (see CLAUDE.md).
- No emojis in any output or UI; sober look (dark gray panel, off-white text).
- Keep `requirements.txt` pinned.
