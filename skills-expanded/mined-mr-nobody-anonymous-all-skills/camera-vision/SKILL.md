---
name: camera-vision
description: "Use when building robot vision pipelines — camera calibration, undistortion, color tracking under varying light, AprilTag/ArUco pose estimation, stereo depth, shutter/exposure selection for moving robots, and embedded OpenCV optimization. Provides the math, exact parameters, and failure modes needed to ship vision that works on real hardware."
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


# Camera Vision for Robots

Vision on a robot is not vision on a laptop. The robot moves, lighting changes, the CPU is small, and a bad pose estimate steers a machine into a wall. This skill covers the pipeline from photons to poses: calibration, undistortion, robust color tracking, fiducial pose estimation, stereo depth, sensor selection, exposure control, and embedded optimization. Every section includes the failure modes that actually kill deployments.

---

## 1. The Pinhole Camera Model (the math you actually use)

Everything downstream — pose estimation, stereo, projection — depends on this model. Know it cold.

A 3D point in the camera frame `P = (X, Y, Z)` projects to pixel `(u, v)`:

```
u = fx * (X / Z) + cx
v = fy * (Y / Z) + cy
```

- `fx, fy` — focal lengths **in pixels** (focal length in mm ÷ pixel pitch in mm). For a square-pixel sensor fx ≈ fy.
- `cx, cy` — principal point, usually near image center but never exactly (typical offset: 5–30 px on cheap modules).
- `Z` — depth along the optical axis. Division by Z is why distant objects are small and why you cannot recover depth from one image without extra information (known object size, a fiducial, or a second view).

The intrinsic matrix:

```
K = [ fx   0  cx ]
    [  0  fy  cy ]
    [  0   0   1 ]
```

**Worked example.** A camera with fx = 600 px sees an AprilTag of physical width 0.10 m spanning 60 px. Depth estimate:

```
Z = fx * real_width / pixel_width = 600 * 0.10 / 60 = 1.0 m
```

This one-liner is a sanity check you should run constantly. If solvePnP says the tag is at 3 m but this says 1 m, your intrinsics or tag-size config is wrong.

**Field of view from intrinsics:**

```
HFOV = 2 * atan(image_width / (2 * fx))
```

640 px wide, fx = 600 → HFOV = 2·atan(0.533) = 56.1°. If your datasheet says 90° and you compute 56°, you calibrated at a different resolution than you're running (see §2 pitfalls).

### Distortion model

Real lenses bend straight lines. OpenCV's standard model (Brown–Conrady), applied to normalized coordinates `x = X/Z, y = Y/Z, r² = x² + y²`:

```
x_dist = x(1 + k1·r² + k2·r⁴ + k3·r⁶) + 2·p1·x·y + p2·(r² + 2x²)
y_dist = y(1 + k1·r² + k2·r⁴ + k3·r⁶) + p1·(r² + 2y²) + 2·p2·x·y
```

- `k1, k2, k3` — radial distortion. Barrel (k1 < 0 typical for wide lenses): lines bow outward. Pincushion (k1 > 0): inward.
- `p1, p2` — tangential distortion from lens/sensor misalignment. Usually small (|p| < 0.005) on decent modules.
- For fisheye lenses (>120° FOV) this model **diverges at the edges** — use `cv2.fisheye` calibration instead (equidistant model). Forcing the standard model onto a fisheye lens gives garbage k3 values (|k3| > 1 is a red flag) and edge errors of tens of pixels.

Typical magnitudes: a Raspberry Pi Camera v2: k1 ≈ -0.01 to -0.05. A 170° "action cam" lens: k1 ≈ -0.3, must use the fisheye model.

---

## 2. Calibration: Checkerboard Workflow

### What you need

- A checkerboard printed flat. **Glue it to glass, acrylic, or aluminum.** A sheet of paper taped to a wall has millimeter-scale waves that directly corrupt your intrinsics. This is the #1 source of bad calibrations.
- Inner-corner count, e.g. a "9×6" board = 9×6 *inner* corners (10×7 squares). OpenCV counts inner corners, not squares. Asymmetric (9×6, not 8×8) so orientation is unambiguous.
- Measure the square size with calipers, not the print dialog. Printers scale. An error of 2% in square size is a 2% error in every distance you ever measure.

### Capture protocol (this determines calibration quality more than anything else)

Take 20–40 images where the board:

1. **Fills the corners and edges of the frame** — distortion coefficients are constrained by edge observations. A dataset of board-in-the-center images gives k1/k2 that are pure noise.
2. **Is tilted up to ~45°** in both axes — tilt constrains focal length. All-frontal views make fx/fy poorly observable (they trade off against Z).
3. **Covers a range of distances** — near (board fills frame) to far (board ~1/4 of frame).
4. **Is sharp.** Discard motion-blurred frames. Use a tripod or have the *board* held still per shot.

Calibrate **at the exact resolution and binning mode you will run at**. Intrinsics scale linearly with resolution only if the sensor readout mode is the same; many sensors crop (changing effective FOV) rather than scale when you switch modes. When in doubt, recalibrate per mode.

### Code

```python
import cv2
import numpy as np
import glob

PATTERN = (9, 6)          # inner corners
SQUARE_SIZE = 0.024       # meters, measured with calipers

# Object points: the board's corner grid in its own plane (Z=0)
objp = np.zeros((PATTERN[0] * PATTERN[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:PATTERN[0], 0:PATTERN[1]].T.reshape(-1, 2)
objp *= SQUARE_SIZE

objpoints, imgpoints = [], []
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 1e-3)

for fname in glob.glob("calib/*.png"):
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    found, corners = cv2.findChessboardCorners(
        gray, PATTERN,
        cv2.CALIB_CB_ADAPTIVE_THRESH | cv2.CALIB_CB_NORMALIZE_IMAGE)
    if not found:
        continue
    # Sub-pixel refinement is NOT optional — raw corners are ~0.5 px off
    corners = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
    objpoints.append(objp)
    imgpoints.append(corners)

rms, K, dist, rvecs, tvecs = cv2.calibrateCamera(
    objpoints, imgpoints, gray.shape[::-1], None, None)

print(f"RMS reprojection error: {rms:.3f} px")
print("K =\n", K)
print("dist =", dist.ravel())
```

### Judging the result

| RMS reprojection error | Verdict |
|---|---|
| < 0.3 px | Excellent — good for stereo and precision PnP |
| 0.3–0.5 px | Good — fine for most robot tasks |
| 0.5–1.0 px | Marginal — check board flatness and image sharpness |
| > 1.0 px | Bad — do not ship. Recapture. |

But RMS alone lies: it averages over the dataset. Also check **per-view error** (reproject with `cv2.projectPoints` per image and look for outlier views — one blurred frame can hide a problem) and that **cx, cy are within ~5% of image center**. A cx that's 100 px off-center on a 640-wide image means the corner detector latched onto something wrong or your board pattern dims are swapped.

Sanity checks before trusting a calibration:
- `fx ≈ fy` within ~1% (square pixels). Big mismatch → bad dataset.
- Computed HFOV matches the lens datasheet within a few degrees.
- |k3| < 0.5 for normal lenses. If k3 blew up, you have too few edge observations — either fix the dataset or fix k3 to zero with `flags=cv2.CALIB_FIX_K3`.
- Undistort a frame containing a straight edge (doorframe) — it must be straight in the output.

Save `K` and `dist` with the resolution they were computed at:

```python
np.savez("camera_calib.npz", K=K, dist=dist, width=640, height=480)
```

---

## 3. Undistortion: Do It Once, Do It Right

Two strategies — choose deliberately:

**A. Undistort whole frames** (do this when downstream code assumes a pinhole model — stereo, dense optical flow, visual odometry):

```python
new_K, roi = cv2.getOptimalNewCameraMatrix(K, dist, (w, h), alpha=0)
map1, map2 = cv2.initUndistortRectifyMap(K, dist, None, new_K, (w, h), cv2.CV_16SC2)
# Per frame — remap is the fast path; never call cv2.undistort() in a loop
undistorted = cv2.remap(frame, map1, map2, cv2.INTER_LINEAR)
```

- `alpha=0`: crop to valid pixels only (no black borders). `alpha=1`: keep all pixels including curved black borders. Robots almost always want `alpha=0`.
- **After undistorting with `new_K`, all downstream math must use `new_K`, not `K`.** Mixing them is a classic silent bug — poses will be wrong by a few percent and you'll chase it for days.
- `cv2.CV_16SC2` maps are fixed-point: ~2× faster than float maps on ARM and visually identical.

**B. Undistort only the points you care about** (do this for sparse features — tag corners, blob centroids — on embedded CPUs; it costs microseconds instead of milliseconds per frame):

```python
undist_pts = cv2.undistortPoints(pts, K, dist, P=K)  # P=K keeps pixel units
```

**Or C: don't undistort at all** — `cv2.solvePnP` accepts `dist` directly and handles distortion internally. For pure tag-pose pipelines this is the cheapest correct option.

Failure mode: undistorting a frame *and* passing `dist` to solvePnP. That applies the correction twice. After full-frame undistortion, pass `distCoeffs=None` and `new_K`.

---

## 4. HSV Color Tracking That Survives Lighting Changes

Naive RGB thresholding dies the moment a cloud passes. The fixes, in order of importance:

### 4.1 Why HSV, and its trap

HSV separates chromaticity (H), saturation (S), and brightness (V). Lighting changes mostly move V, so thresholding on H+S with a loose V bound is far more stable than RGB boxes.

**The trap: Hue is undefined for gray pixels.** Low-saturation pixels have wildly noisy hue. Always set S_min ≥ 50 (on OpenCV's 0–255 scale), or white walls and specular highlights will flicker in and out of your mask.

**OpenCV's H range is 0–179** (degrees/2, to fit uint8), not 0–255. Red wraps around: it lives at both H≈0–10 and H≈170–179. Handle red with two ranges OR'd together:

```python
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
mask1 = cv2.inRange(hsv, (0,   100, 60), (10,  255, 255))
mask2 = cv2.inRange(hsv, (170, 100, 60), (179, 255, 255))
mask = cv2.bitwise_or(mask1, mask2)
```

Starting thresholds (tune on-site, always):

| Color | H low | H high | S | V |
|---|---|---|---|---|
| Red | 0–10 and 170–179 | | 100–255 | 60–255 |
| Orange | 10 | 25 | 120–255 | 70–255 |
| Yellow | 25 | 35 | 100–255 | 80–255 |
| Green | 40 | 80 | 80–255 | 50–255 |
| Blue | 100 | 130 | 100–255 | 50–255 |

### 4.2 Lock the camera, then trust the thresholds

Auto-exposure and auto-white-balance are your enemy here: AWB literally changes the hue of every pixel between frames. For color tracking:

```python
cap.set(cv2.CAP_PROP_AUTO_WB, 0)
cap.set(cv2.CAP_PROP_WB_TEMPERATURE, 4500)       # match your venue lighting
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)            # 1 = manual on V4L2 (yes, 1; 3 = auto)
cap.set(cv2.CAP_PROP_EXPOSURE, 100)               # driver-specific units — verify with cap.get()
```

V4L2 quirk that wastes hours: for many UVC cameras `CAP_PROP_AUTO_EXPOSURE` uses 1 = manual, 3 = auto (not 0/1). Always read the value back with `cap.get()` and confirm with `v4l2-ctl -d /dev/video0 --list-ctrls`.

If you must run auto-exposure (outdoor robots), prefer thresholding on H and S only, with V_min just high enough to reject shadow noise (~40), and re-tune S_min at the venue.

### 4.3 The full robust pipeline

```python
def track_color(frame, lo, hi, min_area=300):
    blur = cv2.GaussianBlur(frame, (5, 5), 0)          # kill sensor noise pre-threshold
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lo, hi)
    # Morphology: open removes specks, close fills holes. 5x5 ellipse is the workhorse.
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, k)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, k)
    cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = [c for c in cnts if cv2.contourArea(c) > min_area]
    if not cnts:
        return None
    c = max(cnts, key=cv2.contourArea)
    M = cv2.moments(c)
    return (M["m10"] / M["m00"], M["m01"] / M["m00"])   # sub-pixel centroid
```

Beyond thresholds, the things that separate demo code from competition/production code:

- **Area gating + aspect-ratio gating.** A red fire extinguisher across the room passes the hue test; it fails the expected-size-at-expected-distance test.
- **Temporal filtering.** Require the blob to persist N=3 consecutive frames before declaring a detection; low-pass the centroid (`x_f = 0.7·x_f + 0.3·x_new`) before feeding a control loop, or the robot will jitter.
- **On-site calibration ritual.** Lighting at the venue is never lighting at the lab. Build a threshold-tuning mode (sliders or click-to-sample that prints the HSV of the clicked pixel ± a tolerance band) and budget 10 minutes at every venue. Teams that skip this lose.
- For severe mixed lighting, consider CLAHE on the V channel before thresholding, or switch to the LAB color space and threshold on A/B channels — both are more compute, so measure first.

---

## 5. Fiducial Pose Estimation: AprilTag & ArUco

Fiducials give you full 6-DoF pose from a single camera — the highest-value, lowest-cost localization tool in robotics.

### 5.1 Choosing the system

- **AprilTag (tag36h11 family)** — better detection range and lower false-positive rate than classic ArUco dictionaries; the standard in FRC and most research. Use `pupil-apriltags` (Python binding of the UMich detector) or OpenCV ≥ 4.7's `cv2.aruco` which now includes `DICT_APRILTAG_36h11`.
- **ArUco** — built into OpenCV everywhere, fine for most uses. Use `DICT_4X4_50` only if range is short; prefer `DICT_5X5_100` or the AprilTag dict for reliability.

Print tags **with a white border at least one module wide** around the black boundary — detection fails without quiet space. Mount flat (foam board / aluminum, same rule as checkerboards: paper curl = pose error).

### 5.2 Detection range rule of thumb

A tag is reliably detected while its smallest side spans ≥ ~12–15 px, and pose is *usable* above ~25 px. Range:

```
max_range ≈ fx * tag_size / min_pixels
```

fx = 600, 16 cm tag, 20 px minimum → 600 · 0.16 / 20 = **4.8 m**. Need more range? Bigger tag or longer focal length — not a "better detector."

### 5.3 Pose estimation done correctly

```python
import cv2
import numpy as np

TAG_SIZE = 0.16  # meters, the BLACK square's outer edge — measure the print!
# Object points: tag corners in tag frame, center origin, z=0,
# order must match detector corner order (here: OpenCV ArUco order)
obj_pts = np.array([
    [-TAG_SIZE/2,  TAG_SIZE/2, 0],
    [ TAG_SIZE/2,  TAG_SIZE/2, 0],
    [ TAG_SIZE/2, -TAG_SIZE/2, 0],
    [-TAG_SIZE/2, -TAG_SIZE/2, 0],
], dtype=np.float32)

detector = cv2.aruco.ArucoDetector(
    cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_APRILTAG_36h11),
    cv2.aruco.DetectorParameters())

corners, ids, _ = detector.detectMarkers(gray)
for tag_corners, tag_id in zip(corners, ids.ravel() if ids is not None else []):
    ok, rvec, tvec = cv2.solvePnP(
        obj_pts, tag_corners.reshape(4, 2).astype(np.float32),
        K, dist, flags=cv2.SOLVEPNP_IPPE_SQUARE)
    if not ok:
        continue
    R, _ = cv2.Rodrigues(rvec)
    # tvec: tag origin in CAMERA frame. Camera in TAG frame:
    cam_in_tag = -R.T @ tvec
    distance = float(np.linalg.norm(tvec))
```

Critical details:

- **`SOLVEPNP_IPPE_SQUARE`** is the correct solver for a single planar square — faster and more accurate than the iterative default, and it returns both ambiguity solutions if you ask via `solvePnPGeneric`.
- **The planar pose ambiguity is real and will hurt you.** A nearly-frontal tag has two geometrically valid poses (mirrored tilt). Symptom: the tag's normal "flips" between frames. Mitigations: use `cv2.solvePnPGeneric(..., flags=SOLVEPNP_IPPE_SQUARE)` and pick the solution with lower reprojection error; reject frames where the two solutions' errors are within ~25% of each other; prefer viewing tags at an angle; temporally filter rotation and reject flips.
- **Translation accuracy beats rotation accuracy.** Expect ~1% distance error in Z but rotation noise of several degrees on small/distant tags. If you need heading, get it from multiple tags or from tag *position* over time, not from a single tag's rvec.
- **Tag size means the black square**, not the printed page. Measure with a ruler after printing. A 5% size error is a 5% range error everywhere.
- Frame conventions: OpenCV camera frame is X-right, Y-down, Z-forward. ROS optical frames match this; ROS *body* frames (X-forward, Z-up) do not. Every "my tag pose is sideways" bug is this. The fixed rotation between them: optical→body is `R = [[0,0,1],[-1,0,0],[0,-1,0]]`.
- Multiple tags with known world positions → feed all corners of all visible tags into **one** `solvePnP` (SQPNP or ITERATIVE) for a single, much more accurate camera pose. Don't average per-tag poses; averaging rotations naively is wrong and per-tag noise is higher.
- Motion blur kills corner accuracy quietly — pose gets noisy before detection drops. Cap exposure time (see §7) and, in ROS2, always use the **image timestamp**, not arrival time, when fusing tag poses with odometry; 50 ms of timestamp error at 1 m/s is 5 cm of phantom error.

### 5.4 ROS2 integration sketch

Use `image_transport` + `camera_info_manager` so calibration travels with the image stream. Publish poses as `geometry_msgs/PoseWithCovarianceStamped` in the camera optical frame and let `tf2` do frame composition — never hand-chain transforms with manual matrix math scattered through nodes. Set covariance honestly: translation σ ≈ 0.01·Z, rotation σ ≈ 5° for single-tag, so a downstream EKF (`robot_localization`) weights it correctly.

---

## 6. Stereo Depth: Principles and What Breaks

### The one equation

```
Z = f * B / d
```

f = focal length (px), B = baseline (m, distance between camera centers), d = disparity (px, horizontal shift of a feature between left/right rectified images).

**Worked example.** f = 700 px, B = 0.12 m, feature at d = 42 px → Z = 700·0.12/42 = **2.0 m**.

### Error grows with Z² — design the baseline for your range

Differentiating: `dZ = (Z² / (f·B)) · dd`. With sub-pixel matching accuracy dd ≈ 0.25 px:

| Z | error (f=700, B=0.12) |
|---|---|
| 1 m | ±3 mm |
| 2 m | ±12 mm |
| 5 m | ±74 mm |
| 10 m | ±0.30 m |

Rules: max useful range ≈ where error exceeds your tolerance; min range = where disparity exceeds your matcher's search window (`numDisparities`). Wider baseline → better far accuracy but a larger blind zone up close and harder matching (more perspective difference between views). B between Z_max/30 and Z_max/10 is a sane bracket.

### The pipeline

1. **Calibrate both cameras + extrinsics** with `cv2.stereoCalibrate` (capture pairs simultaneously; same checkerboard rules as §2). Stereo RMS < 0.5 px or redo.
2. **Rectify** with `cv2.stereoRectify` + `initUndistortRectifyMap` per camera — makes epipolar lines horizontal so matching is a 1-D search. Verify: a feature must be on the **same row** (±0.5 px) in both rectified images. If rows don't align, every downstream depth is garbage.
3. **Match**: `cv2.StereoSGBM_create` starting values that work:

```python
stereo = cv2.StereoSGBM_create(
    minDisparity=0,
    numDisparities=128,          # multiple of 16; sets min range
    blockSize=5,
    P1=8 * 3 * 5 ** 2,           # 8*channels*blockSize²
    P2=32 * 3 * 5 ** 2,
    uniquenessRatio=10,
    speckleWindowSize=100,
    speckleRange=2,
    disp12MaxDiff=1)
disp = stereo.compute(rectL, rectR).astype(np.float32) / 16.0  # SGBM returns fixed-point ×16
```

The `/16.0` is mandatory and forgotten constantly — symptom: all depths are 16× too small.

### What kills stereo in the field

- **Hardware sync.** The two cameras must expose at the same instant. Unsynced USB webcams on a moving robot produce disparities contaminated by motion — depth error proportional to speed. Use a stereo module with hardware sync (or trigger pins), or accept stereo only when stationary.
- **Textureless surfaces** (white walls, floors) have no features to match → holes or hallucinated depth. SGBM's `uniquenessRatio` rejects most hallucinations; active-IR stereo (RealSense D435 style) projects texture to fix this indoors. Sunlight washes out IR projectors — outdoor performance differs completely from the lab.
- **Calibration drift.** Stereo extrinsics live or die on a rigid baseline. A 3D-printed mount that flexes 0.1° ruins rectification. Aluminum bar, both cameras bolted, recheck row-alignment after every crash.
- Repetitive texture (fences, gratings) aliases the matcher. Reflective floors produce mirrored phantom geometry below ground — filter depth points below the known ground plane.

If you just need obstacle depth and the budget allows, a RealSense/OAK-D class module with onboard depth offloads all of this and frees your CPU. Roll your own stereo when you need a custom baseline, custom optics, or no IR.

---

## 7. Rolling vs Global Shutter, and Exposure Control

### Shutter type: the spec that matters most for moving robots

- **Rolling shutter** (almost all webcams, Pi Cam v1/v2/v3, phone sensors): rows are exposed sequentially, top to bottom, over typically 10–30 ms per frame. Anything that moves during readout is **geometrically skewed** — verticals lean, the checkerboard isn't a plane anymore, tag corners are displaced. Effects: vibration → "jello"; rotation → smear/skew; PnP on a skewed tag → biased pose. The skew at the image bottom vs top is `v_robot · t_readout` worth of apparent displacement — a robot panning at 90°/s with 20 ms readout skews the scene 1.8° across the frame, which is *larger* than your calibration accuracy.
- **Global shutter** (Pi Global Shutter Cam IMX296, OV9281 modules, machine-vision cams, OAK-D's mono pair): all pixels exposed simultaneously. Geometry stays correct under motion.

Decision rule: **camera or scene moves fast during exposure/readout → global shutter.** Drone VIO, fast ground robots doing tag localization while turning, anything vibrating: global shutter. Stationary camera watching a slow scene: rolling is fine and cheaper. If stuck with rolling shutter, mitigate: shorter exposure, higher fps (shorter readout), detect when stationary, and never calibrate from handheld-waving footage — hold still per frame.

### Exposure: motion blur budget

Blur in pixels = `exposure_time · angular_or_linear_speed · fx / Z` (linear) or `exposure · ω · fx` (rotation, rad/s).

**Worked example.** Robot rotates at 1 rad/s (~57°/s), fx = 600 px, exposure 10 ms → blur = 0.01·1·600 = **6 px**. That destroys tag corner accuracy (you want < 1–2 px). At 2 ms exposure: 1.2 px — acceptable.

Rules:
- Budget blur ≤ 1–2 px for fiducials/features, ≤ 0.5 px for calibration frames.
- Solve for exposure: `t_max = blur_budget / (ω · fx)`. Fast robots routinely need 1–4 ms exposures, which means you need **gain** (accept noise — detectors tolerate noise far better than blur) and/or **more light**.
- Prefer fixed manual exposure + manual gain for anything feeding geometry (tags, stereo, VIO). Auto-exposure changes brightness mid-flight and oscillates when the robot faces a window. If auto is unavoidable, use the camera's AE with a center-weighted ROI on the working area and clamp `exposure_max` to your blur budget — most drivers (libcamera, Spinnaker, V4L2 via `v4l2-ctl --set-ctrl=exposure_time_absolute=...`) support an AE upper bound.
- 50/60 Hz flicker: indoor LED/fluorescent lighting beats against exposure. Use exposure = integer multiples of 10 ms (50 Hz) / 8.33 ms (60 Hz) — or short enough (<2 ms) that you instead handle frame-to-frame brightness variation in software (another reason H/S thresholding beats V).

---

## 8. OpenCV on Embedded: Making It Fast Enough

Target reality: a Raspberry Pi 4 does ~15–30 fps of 640×480 ArUco; a Pi Zero 2 maybe 8; a Jetson moves the goalposts entirely. The pipeline is designed around the budget, not optimized after.

### The ordered checklist (do these in order; each is bigger than micro-optimizing)

1. **Resolution is quadratic.** 640×480 has 4× fewer pixels than 1280×960. Detect at low resolution, then refine corners at high resolution only inside the detected ROI if you need the precision:
   ```python
   small = cv2.resize(gray, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
   # detect on small; scale corners ×2; cv2.cornerSubPix on full-res ROI
   ```
2. **Grab grayscale at the source.** Ask the camera for `YUYV` and take the Y plane, or `GREY` if the sensor supports it — skip BGR conversion entirely for tag/feature pipelines. `frame[:, :, 0]` of a YUV frame is free; `cvtColor` on every frame is not.
3. **Kill frame latency, not just frame rate.** `cv2.VideoCapture` buffers frames; processing at 10 fps from a 30 fps camera means you are acting on a 3-frames-old world (100 ms — at 1 m/s that's 10 cm of staleness in your control loop). Set `cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)` and/or run a grab thread that always keeps only the newest frame:
   ```python
   # Grab thread pattern: thread loops cap.grab(); consumer calls cap.retrieve()
   ```
4. **Track, don't re-detect.** Full-frame detection at 5 Hz + ROI-only detection (or KCF/CSRT tracking, or sparse LK optical flow on tag corners) at 30 Hz. Searching a 100×100 ROI is ~30× cheaper than 640×480.
5. **Precompute everything per-session**: undistort maps (§3), morphology kernels, object-point arrays. Allocate output buffers once and pass `dst=` to OpenCV calls to avoid per-frame malloc.
6. **NEON/architecture builds.** pip wheels for ARM are generally fine now, but verify `cv2.getBuildInformation()` shows NEON. On Jetson, use the JetPack OpenCV with CUDA, and push `remap`/`cvtColor`/stereo onto `cv2.cuda_*`. Set `cv2.setNumThreads(n)` deliberately — OpenCV grabbing all cores starves your control loop; leaving it at 1 wastes the other cores. Pin and measure.
7. **Python loop = death.** Any per-pixel Python is 100–1000× too slow. Everything must be vectorized NumPy or an OpenCV call. If a stage genuinely needs custom per-pixel work, write it in C++ (pybind11) or move the platform.
8. **Thermals.** A Pi at sustained 100% CPU in a sealed robot chassis throttles from 1.8 GHz to ~1 GHz within minutes — your "20 fps" pipeline becomes 11 fps in the second half of the match. Heatsink + measured sustained (not peak) fps.

### Measure honestly

```python
import time
t = time.perf_counter()
# ... stage ...
dt_ms = (time.perf_counter() - t) * 1000
```

Profile per stage, every change, on the target hardware, at the target temperature. Laptops lie about embedded performance by 5–20×.

---

## 9. Debugging Methodology: Vision Pipelines Fail Silently

Vision bugs rarely crash; they emit plausible-looking wrong numbers. Debug in pipeline order — each stage's output validated before suspecting the next:

1. **Is the image right?** Save/stream raw frames. Check: focus (lens focus rings ship loose — thread-lock after focusing), exposure (histogram not clipped), correct camera index, correct resolution.
2. **Is calibration right?** Undistort a frame; straight world edges must be straight. Recompute HFOV from fx; compare to datasheet.
3. **Is detection right?** Draw detections (`cv2.aruco.drawDetectedMarkers`, contour overlays) on every debug frame. Most "pose is wrong" bugs are actually "detection corners are wrong."
4. **Is the pose right?** Reproject: `cv2.projectPoints(obj_pts, rvec, tvec, K, dist)` and draw — projected corners must land on detected corners (< 1 px). Then check magnitudes against the §1 hand calculation.
5. **Are the frames/units right?** Meters everywhere (one millimeter/meter mismatch = 1000× error, comically common). Optical vs body frame. `new_K` vs `K`. Degrees vs radians in anything touching rvec.
6. **Is timing right?** Stamp frames at capture; measure capture→action latency end-to-end with an LED test (point camera at an LED, toggle it, measure detection delay).

Keep a debug-view mode in every deployed pipeline (an MJPEG endpoint or `rqt_image_view` topic showing overlays). The ability to *see what the robot sees* at the venue, with thresholds and detections drawn, is the single highest-value tool for field debugging. Log raw frames around every failure — you cannot fix what you didn't record.

### Pre-deployment checklist

- [ ] Calibration RMS < 0.5 px, cx/cy near center, HFOV matches datasheet, straight-line test passes
- [ ] Calibration done at deployed resolution/readout mode; file versioned with the physical camera unit (serial number — lenses differ unit to unit)
- [ ] Exposure manual (or AE-clamped), blur budget computed for max robot speed
- [ ] White balance locked for color pipelines; on-site HSV re-tune procedure rehearsed
- [ ] Tag sizes measured post-print; pose sanity-checked at a taped 1.000 m distance
- [ ] Latency measured end-to-end; frame timestamps (not arrival time) used in fusion
- [ ] Sustained fps measured on target hardware at temperature, with the rest of the robot stack running
- [ ] Failure behavior defined: what does the robot do when vision returns nothing for 0.5 s? (Stop. The answer is stop.)
