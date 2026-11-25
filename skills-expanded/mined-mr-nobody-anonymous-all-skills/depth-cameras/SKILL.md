---
name: depth-cameras
description: "Use when integrating, configuring, or debugging depth cameras (Intel RealSense, Luxonis OAK-D, Azure Kinect, Orbbec) on a robot. Covers stereo/ToF/structured-light tradeoffs, depth-RGB alignment, point cloud generation, hole filling, minimum-range blind zones, multi-camera IR interference, and outdoor sunlight failure modes — with correct intrinsics math, ROS2 patterns, and production-validated parameter values."
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


# Depth Cameras: Selection, Integration, and Failure Modes

Depth cameras are the most commonly misused sensor in robotics. The depth image *looks*
dense and trustworthy, but every pixel carries a noise model, a validity envelope, and
a set of systematic biases that depend on the underlying technology. Code that treats
depth as ground truth fails on real hardware — usually at the worst time (sunlight,
black objects, close range). This skill gives you the technology tradeoffs, the exact
math for projection and alignment, working code patterns, and the failure-mode catalog.

---

## 1. The Three Technologies — What Actually Differs

| Property | Active Stereo (RealSense D4xx, OAK-D Pro) | Time-of-Flight (Azure Kinect, Orbbec Femto, RealSense L515*) | Structured Light (original Kinect v1, RealSense SR300) |
|---|---|---|---|
| How depth is computed | Triangulation: disparity between two IR cameras, IR projector adds texture | Phase shift of modulated IR pulse, per-pixel | Triangulation: deformation of a known projected dot pattern |
| Depth error growth | **Quadratic** with distance: σ_z ∝ z² | **Roughly constant** (mm-level) until SNR collapses | Quadratic with distance |
| Works on textureless surfaces | Yes (projector provides texture) — but degrades in bright IR ambient where projector is washed out; falls back to passive stereo which needs scene texture | Yes (independent of texture) | Yes until pattern is washed out |
| Works in direct sunlight | **Partially** — passive stereo path still works; depth gets noisier, not absent | **No** — sunlight IR floods the sensor, depth drops out massively | **No** — pattern completely washed out |
| Black / IR-absorbing objects | Poor (low return signal AND low texture) | Poor (low return → low SNR → invalid or biased pixels) | Poor |
| Transparent / specular objects | Fails (sees through glass or returns the reflection's depth) | Fails (multipath; returns mixed depth) | Fails |
| Multipath errors (corners, concave surfaces) | Minimal | **Significant** — concave corners read too far, floors near walls bow | Minimal |
| Multi-camera interference | Mild — projectors *add* texture for each other; cross-talk mostly benign, can even help | **Severe** — same modulation frequencies cause beating artifacts; needs frequency/time multiplexing | Severe — overlapping patterns confuse decoding |
| Edge behavior | "Flying pixels" + disparity edge fattening (~edge smearing of a few pixels) | Flying pixels at depth discontinuities (mixed-pixel effect) | Edge shadowing (occlusion between projector and camera) |
| Typical range | 0.3–10 m (usable accuracy to ~3–4 m on D435) | 0.25–5.5 m (Azure Kinect NFOV) | 0.4–4 m |
| Frame rate / resolution | Up to 90 fps at 848×480 (D435) | 30 fps, up to 1024×1024 (K4A WFOV) | 30 fps |

\* L515 is LiDAR-like MEMS ToF; discontinued but still in the field.

**Selection rules of thumb:**
- **Outdoor or mixed indoor/outdoor robot** → active stereo (D435/D455/OAK-D). It is the only technology that degrades gracefully in sunlight.
- **Indoor manipulation needing mm accuracy at <1.5 m** → ToF (Azure Kinect/Femto Bolt) or high-res stereo (D405 for 7 cm–50 cm range).
- **Multiple cameras with overlapping views** → stereo strongly preferred; ToF requires explicit sync/multiplexing (Section 8).
- **Long baseline = better long-range accuracy.** D455 (95 mm baseline) has ~2× the depth accuracy of D435 (50 mm baseline) at the same range. Use the stereo error model below to size this.

### Stereo depth error model (use this to budget accuracy)

Depth from disparity: `z = f · B / d`, where f = focal length in pixels, B = baseline in meters, d = disparity in pixels.

Differentiating: depth RMS error for disparity noise σ_d (typically **0.05–0.1 px** subpixel error for a good ASIC):

```
σ_z = (z² / (f · B)) · σ_d
```

**Worked example — RealSense D435** (B = 0.050 m, f ≈ 645 px at 848×480, σ_d ≈ 0.08 px):

- At z = 1 m:  σ_z = (1.0² / (645 · 0.050)) · 0.08 = **2.5 mm**
- At z = 3 m:  σ_z = (9 / 32.25) · 0.08 = **22 mm**
- At z = 6 m:  σ_z = (36 / 32.25) · 0.08 = **89 mm**

Same numbers for D455 (B = 0.095 m, f ≈ 640 px at 848×480): at 3 m, σ_z ≈ **12 mm**.

If your grasp planner needs ±5 mm at 1.5 m, a D435 is marginal (σ_z ≈ 5.6 mm, so ±2σ ≈ ±11 mm) — you need a D455, a D405 at close range, or temporal averaging. **Do this calculation before buying hardware, not after the demo fails.**

ToF error model: σ_z is roughly constant with range but scales as `1/√(amplitude)` — black and distant objects get noisy simultaneously. Azure Kinect spec: ≤17 mm + systematic <11 mm typical, but multipath can add **several cm** of bias in concave geometry, which no amount of averaging removes.

---

## 2. Minimum Range Blind Zones — The #1 Integration Mistake

Every depth camera has a **MinZ** below which depth is invalid. Stereo MinZ exists because maximum disparity search is finite: `MinZ = f · B / d_max`. Closer objects exceed the disparity search window and either return **nothing or, worse, a wrong (too-far) depth from aliased matching.**

| Camera | MinZ (default mode) | Notes |
|---|---|---|
| RealSense D435/D435i | ~28 cm at 848×480 | Scales with resolution: ~17.5 cm at 424×240 (disparity is searched in pixels, so half resolution ⇒ half MinZ) |
| RealSense D455 | ~52 cm at 848×480 | Longer baseline pushes MinZ out |
| RealSense D405 | ~7 cm | Purpose-built short range; MaxZ ~50 cm usable |
| OAK-D / OAK-D Pro | ~35 cm (70 cm without extended disparity) | Enable `setExtendedDisparity(true)` to halve MinZ at cost of compute |
| Azure Kinect NFOV | 25 cm (unbinned) / 50 cm... no — 25 cm NFOV, 25 cm WFOV binned | Below MinZ, ToF returns invalid (0), not wrong values — safer failure |
| Orbbec Femto Bolt | 25 cm | K4A-compatible |

**Production consequences:**

1. **Obstacle avoidance:** an object inside MinZ is *invisible*. A robot that drives forward until an obstacle "disappears" from the depth image will then hit it. **Always fuse a secondary close-range sensor** (ultrasonic, 1D ToF like VL53L1X, bump skirt) or enforce a software standoff: never let the camera-to-nearest-known-obstacle distance fall below MinZ + margin.
2. **Manipulation:** a wrist-mounted D435 cannot see the object during the final 28 cm of approach. Either use a D405, mount the camera with a view angle that keeps the target beyond MinZ throughout approach, or switch to open-loop final approach from the last valid observation.
3. **Stereo aliasing inside MinZ:** RealSense can emit *plausible-looking wrong depth* for surfaces closer than MinZ (wrap-around matches). Filter with a disparity-domain check or trust the `confidence`/second-peak threshold settings. On RealSense, raising the `Disparity Shift` advanced parameter trades MaxZ for a closer MinZ — e.g., disparity shift 50 on D435 brings MinZ to ~12 cm but caps MaxZ around 1 m. Set it explicitly for short-range cells:

```python
import pyrealsense2 as rs
dev = pipeline_profile.get_device()
adv = rs.rs400_advanced_mode(dev)
table = adv.get_depth_table()
table.disparityShift = 50      # 0 = default. Raises near limit, lowers far limit.
table.depthUnits = 100         # 100 µm units instead of default 1000 µm → finer
                               # quantization for short range (D405 default).
adv.set_depth_table(table)
```

---

## 3. Intrinsics, Deprojection, and Point Cloud Generation

### The math

Pinhole model. Pixel (u, v) with depth z deprojects to camera-frame 3D:

```
x = (u - cx) / fx * z
y = (v - cy) / fy * z
z = z
```

Camera frame convention: **+Z forward, +X right, +Y down** (optical frame). ROS body
frames are +X forward, +Z up — the `*_optical_frame` in a URDF carries the fixed
rotation (rpy ≈ `-π/2, 0, -π/2`). Getting this rotation wrong is the most common
"my point cloud is sideways" bug.

**Critical:** the depth value in a RealSense/K4A depth image is **Z-depth (distance along
the optical axis)**, not ray length. Do NOT divide by cos(θ). If you are working with a
sensor that returns radial distance (some ToF SDKs in raw mode), convert first.

**Use the intrinsics streamed from the device, not the datasheet.** Each unit is
factory-calibrated; fx/fy/cx/cy differ per device and per resolution/crop mode. On
RealSense: `profile.get_stream(rs.stream.depth).as_video_stream_profile().get_intrinsics()`.
The depth stream from the ASIC is already rectified — distortion model is
`brown_conrady` with zero coefficients (D4xx) — so no undistortion is needed on depth.
The **RGB stream is NOT rectified**; it has real distortion coefficients you must apply
when aligning or texturing.

### Vectorized point cloud (NumPy — never loop over pixels)

```python
import numpy as np

def depth_to_points(depth: np.ndarray, fx, fy, cx, cy, depth_scale=0.001,
                    z_min=0.30, z_max=4.0):
    """depth: (H,W) uint16. Returns (N,3) float32 points in camera optical frame.
    z_min/z_max MUST reflect the camera's validated range (Section 2)."""
    z = depth.astype(np.float32) * depth_scale
    valid = (z > z_min) & (z < z_max)          # 0 = invalid on every depth camera
    v, u = np.nonzero(valid)
    z = z[valid]
    x = (u - cx) / fx * z
    y = (v - cy) / fy * z
    return np.column_stack((x, y, z))
```

For C++/ROS2, use `depth_image_proc::PointCloudXyzrgbNode` (composable, zero-copy
intra-process) rather than hand-rolling. For GPU pipelines, do the deprojection in the
same CUDA kernel as your downstream consumer — copying full point clouds over PCIe at
30 fps is the bottleneck, not the math.

**Performance reality check:** an 848×480 cloud is ~400k points, ~4.8 MB as XYZ float32,
145 MB/s at 30 fps. Publishing `PointCloud2` over the ROS2 network DDS at full rate will
saturate a 1 GbE link with two cameras. Options, in order of preference:
1. Ship the **depth image + intrinsics** (compressed, ~10× smaller) and deproject at the consumer.
2. Composable nodes with intra-process comms (no serialization).
3. Voxel-downsample at the producer (`pcl::VoxelGrid`, leaf 5–10 mm for manipulation, 3–5 cm for navigation) before publishing.

---

## 4. Depth↔RGB Alignment — Do It Right or Suffer Colored Ghosts

Depth and RGB cameras sit at different positions with different intrinsics. To get the
color of a depth pixel (or the depth of a color pixel), you must reproject through the
extrinsic transform between the two sensors.

**Two directions — they are NOT symmetric:**

- **Align depth → color** (`rs.align(rs.stream.color)`, K4A `transformation_depth_image_to_color_camera`): resamples depth into the color camera's frame. Output resolution = color resolution. Use for: semantic segmentation → 3D, colored point clouds, "what is the depth of this detected bounding box."
- **Align color → depth**: resamples color into the depth frame. Preserves every original depth measurement (no depth interpolation!). Use when depth fidelity matters more than color fidelity (precision measurement, mapping).

**Why depth→color is subtly dangerous:** the resampling interpolates and z-buffers depth
values. At object boundaries you get occlusion holes (regions the depth camera couldn't
see from the color camera's viewpoint) and the SDK fills/discards them. If you then run
plane fitting or grasp pose estimation on *aligned* depth, you are fitting to resampled
data. For metrology-grade work, operate in the depth frame and project results to color
only for visualization.

**The 3-step alignment algorithm** (what the SDK does — know it so you can debug it):
1. Deproject depth pixel (u_d, v_d, z) to 3D point P_d in depth-camera frame (Section 3 math).
2. Transform: `P_c = R · P_d + t` using the depth→color extrinsic (factory-calibrated, read from device: `depth_profile.get_extrinsics_to(color_profile)`).
3. Project P_c into the color image using the **color intrinsics including distortion**. Z-buffer collisions (multiple depth pixels landing on one color pixel: keep nearest).

**Common alignment bugs and their symptoms:**

| Symptom | Cause |
|---|---|
| Color "halo" shifted a few px around objects, worse close-up | Used datasheet/default extrinsics instead of per-device factory calibration |
| Misalignment grows toward image corners | Forgot color-camera distortion in step 3 |
| Misalignment only on moving objects | RGB and depth frames not from the same timestamp — enable hardware-synced framesets (`pipeline.wait_for_frames()` returns matched framesets; do NOT pair latest-arrived images from separate callbacks) |
| Everything off by a constant ~1 frame of motion | Depth and RGB sensors run at different exposures; use `rs.option.frames_queue_size` and frameset metadata `get_frame_metadata(rs.frame_metadata_value.sensor_timestamp)` to verify pairing |
| Alignment fine at 1 m, wrong at 0.4 m | Wrong direction of extrinsic (inverted transform) — error scales with parallax, i.e., inversely with depth |

```python
# RealSense: correct aligned colored-depth acquisition
import pyrealsense2 as rs
pipe, cfg = rs.pipeline(), rs.config()
cfg.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 30)
cfg.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
profile = pipe.start(cfg)
align = rs.align(rs.stream.color)              # depth -> color frame
depth_scale = profile.get_device().first_depth_sensor().get_depth_scale()  # 0.001 typ.

frames  = pipe.wait_for_frames()               # hardware-matched frameset
frames  = align.process(frames)
depth   = np.asanyarray(frames.get_depth_frame().get_data())   # now color-resolution
color   = np.asanyarray(frames.get_color_frame().get_data())
intr    = frames.get_depth_frame().profile.as_video_stream_profile().get_intrinsics()
# NOTE: after align, depth intrinsics == color intrinsics. Use intr from the
# ALIGNED frame, not the raw depth stream profile.
```

In ROS2 with `realsense2_camera`: set `align_depth.enable:=true` and consume
`/camera/aligned_depth_to_color/image_raw` with `/camera/color/camera_info`. Never pair
raw depth with color camera_info — the intrinsics won't match.

---

## 5. Filtering and Hole Filling — What to Use, What to Refuse

Raw depth has three defect classes: **invalid pixels (0)** (no return / no stereo match),
**flying pixels** (mixed foreground/background at edges), and **speckle noise**.

### Recommended RealSense post-processing chain (order matters)

```python
dec    = rs.decimation_filter(2)          # 2x downsample; do this FIRST (cheaper chain)
d2disp = rs.disparity_transform(True)     # filter in disparity domain (noise is
                                          # uniform in disparity, quadratic in depth)
spat   = rs.spatial_filter(0.5, 20, 2, 0) # alpha=0.5, delta=20, magnitude=2, holes=0
temp   = rs.temporal_filter(0.4, 20, 3)   # alpha=0.4, delta=20, persistence=3
disp2d = rs.disparity_transform(False)
# hole_filling = rs.hole_filling_filter(1)  # see warning below before enabling

f = depth_frame
for flt in (dec, d2disp, spat, temp, disp2d):
    f = flt.process(f)
```

Starting values above are the field-proven defaults. Tune `delta` (edge-preservation
threshold, in disparity steps) up if surfaces look "shattered", down if edges smear.

### Hole filling: the honest guidance

**For any geometric decision-making (obstacle avoidance, grasping, footstep planning):
do NOT hole-fill. An invalid pixel is information** — "I don't know what's here" — and
must propagate as unknown space, not be painted over with a neighbor's depth. Hole
filling is for visualization and for dense-input neural networks only.

If you must fill (e.g., a CNN requires dense depth):
- `rs.hole_filling_filter(mode)`: mode 1 = "farthest from around" is the least dangerous
  for navigation (fills holes with *far* values → never invents a phantom near obstacle...
  but DOES erase real near obstacles that failed to return depth — black objects!). Mode 2
  "nearest" is conservative for collision but creates phantom obstacles.
- Better: classical inpainting on the *inverse depth* image (OpenCV `cv2.inpaint` with
  Navier-Stokes, radius 3–5 px) restricted to small holes (<~200 px area). Leave large
  holes unfilled and mask them for the network.
- Best for SLAM/recon: don't fill per-frame; let multi-view fusion (TSDF — Open3D
  `ScalableTSDFVolume`, voxel 5–10 mm, sdf_trunc = 4× voxel) fill holes with *real
  observations from other viewpoints*.

### Flying pixel removal (essential for ToF, useful for stereo)

A flying pixel has neighbors at very different depths. Remove points whose depth differs
from the local median by more than a range-scaled threshold:

```python
import cv2
med = cv2.medianBlur(depth, 5)
z = depth.astype(np.float32)
# threshold scales with z² for stereo (per Section 1 error model); linear for ToF
thresh = 0.0025 * (z * depth_scale)**2 / depth_scale + 8   # stereo, in depth units
flying = np.abs(z - med.astype(np.float32)) > thresh
depth[flying] = 0
```

In PCL: `StatisticalOutlierRemoval` (meanK=20, stddev=1.0) or faster
`RadiusOutlierRemoval` (radius = 2× expected point spacing at max range, min_neighbors=5).

### High Accuracy vs. High Density presets (RealSense)

Load JSON presets via advanced mode. **High Accuracy** raises the stereo confidence
threshold → fewer pixels, but the ones you get are trustworthy (use for measurement,
grasping). **High Density** lowers it → more coverage, more garbage (use for obstacle
coverage where a false negative is worse than noise). Default ships in between. This
single setting changes fill-rate by 2–3× — set it deliberately.

---

## 6. Multi-Camera Setups and IR Interference

### Stereo (RealSense D4xx, OAK-D): mostly safe

The projectors emit pseudo-random dot patterns that *add scene texture*. Two overlapping
D435s generally **improve** each other (more texture). Known exceptions:
- Direct projector-into-lens geometry (cameras facing each other <1 m) causes saturation blobs — offset mounting angles by >15°.
- For >4 cameras in a small cell, alternate `emitter_enabled` via hardware sync if you see speckle correlation artifacts (rare).

Hardware sync (for temporal alignment of captures, e.g., moving robot or moving scene):
wire the SYNC pins (pin 5 = SYNC, pin 9 = GND on the D435 9-pin connector), set one
camera `inter_cam_sync_mode = 1` (master), others `= 2` (slave). Without wiring, expect
up to half-frame (16 ms) skew — at 1 m/s robot speed that is 16 mm of inconsistency
between camera observations.

### ToF (Azure Kinect, Femto): interference is severe and MUST be engineered around

Two unsynchronized K4A units with overlapping views produce **beating artifacts**: large,
slowly-moving regions of corrupted depth. Mitigations, in order of robustness:

1. **Time multiplexing via sync cable** (the official solution): daisy-chain 3.5 mm sync
   cables, master + subordinates, and offset each subordinate's
   `subordinate_delay_off_master_usec` by ≥ **160 µs** (the laser pulse duration window)
   per camera. Up to 9 devices. Capture rate unaffected; only the laser firing is staggered.
   ```c
   config.wired_sync_mode = K4A_WIRED_SYNC_MODE_SUBORDINATE;
   config.subordinate_delay_off_master_usec = 160 * device_index;
   ```
2. Different FPS/mode combinations shift modulation timing — partial mitigation only. Don't rely on it.
3. Physical separation / non-overlapping FoV.

**Mixing technologies:** a RealSense projector in a K4A's view adds broadband IR → raises
K4A noise floor mildly (usually acceptable). A K4A's flood illuminator in a RealSense
view adds texture-free uniform IR → can wash out the RealSense pattern at close range.
Test the actual geometry; there's no formula.

### Multi-camera extrinsic calibration

Factory calibration covers *within-device* sensors only. Camera-to-camera and
camera-to-robot extrinsics are on you:
- Static rigs: ChArUco board (12×9, 30 mm squares for ~1 m working distance) visible to
  pairs of cameras; solve with OpenCV `calibrateCamera`+`solvePnP` per camera, chain
  transforms. Reprojection error budget: <0.5 px.
- Hand-eye (wrist camera): `cv2.calibrateHandEye` with ≥15 robot poses spanning ≥60° of
  rotation diversity; Tsai or Daniilidis method. Rotation-poor pose sets give garbage
  translation — this is the classic hand-eye failure.
- Validate with a held-out object: measure the same physical point from all cameras;
  3D disagreement should be < 2× your depth σ_z at that range. If it's centimeters,
  your extrinsics are wrong, not your depth.

---

## 7. Outdoor and Sunlight Operation

Sunlight contains massive broadband IR (~1 kW/m² total irradiance; the in-band IR at
850/860 nm swamps any eye-safe projector or laser).

**What happens per technology:**
- **ToF**: ambient IR fills the pixel wells → SNR collapse → depth invalidation over most
  of the sunlit scene. Azure Kinect outdoors in direct sun is effectively blind beyond
  ~1 m. There is no parameter fix. Do not deploy ToF as the primary outdoor depth sensor.
- **Structured light**: pattern contrast → 0. Total failure.
- **Active stereo**: the projector is washed out, but **sunlight itself textures the
  scene** — passive stereo matching often *improves* outdoors on natural surfaces.
  Failures concentrate on: textureless sunlit surfaces (smooth concrete, painted metal),
  hard shadow boundaries (exposure can't cover both sides), and lens flare.

**Outdoor stereo configuration checklist (RealSense D455/D435):**
1. `emitter_enabled = 0` outdoors (saves power; pattern is useless in sun anyway). If the
   robot transitions indoor↔outdoor, leave the emitter ON — it helps indoors and is
   merely ignored in sun — but consider auto-switching on ambient light if power matters.
2. Enable auto-exposure but cap it: `rs.option.auto_exposure_limit` ≈ 8500 µs at 30 fps
   to prevent motion blur on a moving robot; or manual exposure ~100–1000 µs in bright sun
   with `rs.option.gain` at minimum (16) first, raising gain only after exposure maxes.
3. Watch for **rolling-shutter artifacts**: D435 depth sensors are global shutter (good),
   but the D435 *RGB* sensor is rolling shutter — fast motion skews RGB relative to
   depth. D455 RGB is also global shutter; prefer D455 for fast outdoor platforms.
4. Thermal: direct sun heats the camera; RealSense depth has a temperature-dependent
   bias (~0.1–0.2 mm per °C per meter, varies per unit). Let the camera warm up
   ~15 min before calibration-grade measurements; shade the housing.
5. Validate fill-rate at noon, not at 5 pm. Log `% valid pixels` as a runtime health
   metric and have the planner respond when it drops (slow down, increase standoff).

**Wet surfaces, glass, chain-link fences** fail every technology: water is specular,
glass is transparent at IR, fences alias in stereo matching. Fuse with non-optical
sensing (radar, ultrasonic) for these or geofence them out.

---

## 8. ROS2 Integration Patterns

### RealSense (`realsense2_camera`, ROS2)

```yaml
# Launch parameters that matter (params.yaml or launch args)
depth_module.depth_profile: 848x480x30
rgb_camera.color_profile: 1280x720x30
align_depth.enable: true
pointcloud.enable: false            # generate clouds at the consumer (Section 3)
depth_module.enable_auto_exposure: true
clip_distance: 4.0                  # hard MaxZ clamp matching your error budget
decimation_filter.enable: true
spatial_filter.enable: true
temporal_filter.enable: true
hole_filling_filter.enable: false   # see Section 5
unite_imu_method: 2                 # linear_interpolation, for D435i/D455 IMU
```

- Use the camera's **optical frames** from the driver's TF tree; do not hand-author them.
- QoS: depth images come as `SensorDataQoS` (best-effort). A reliable-QoS subscriber
  **silently receives nothing** — the #1 "no data but no error" bug. Match with
  `rclcpp::SensorDataQoS()`.
- USB: D4xx needs USB 3.x. On a 2.x link it silently degrades to low resolutions.
  Check `rs-enumerate-devices` output for "3.2". Use a **screw-lock USB-C cable**;
  vibration-induced re-enumeration mid-mission is a real fleet failure. Add a udev-based
  auto-restart and treat "device disconnected" in the driver log as a recoverable fault.
- Multiple cameras: pass `serial_no` per node; never rely on enumeration order.

### OAK-D (DepthAI)

Depth is computed on-device (no host CPU cost). Key pipeline settings:

```python
import depthai as dai
stereo = pipeline.create(dai.node.StereoDepth)
stereo.setDefaultProfilePreset(dai.node.StereoDepth.PresetMode.HIGH_DENSITY)
stereo.initialConfig.setMedianFilter(dai.MedianFilter.KERNEL_5x5)
stereo.setLeftRightCheck(True)        # rejects occlusion mismatches — keep ON
stereo.setSubpixel(True)              # 8x finer disparity → required for the
                                      # σ_d ≈ 0.08 px error model to hold
stereo.setExtendedDisparity(False)    # True halves MinZ, costs fps; mutually
                                      # exclusive with subpixel on some firmware
stereo.setDepthAlign(dai.CameraBoardSocket.CAM_A)  # align to RGB on-device
```

OAK-D Pro adds an active IR projector — enable it indoors:
`device.setIrLaserDotProjectorBrightness(800)` (mA, max 1200; start at 800).

### Azure Kinect / Femto (k4a)

`K4A_DEPTH_MODE_NFOV_UNBINNED` (640×576, 75°×65°, 0.25–3.86 m) is the default choice;
`WFOV_2X2BINNED` for wide-angle navigation (0.25–2.88 m usable). Do alignment with
`k4a_transformation_*` functions (they use the factory calibration correctly). Remember
the sync-cable requirement for multi-camera (Section 6).

---

## 9. Debugging Methodology — Depth Looks Wrong, Now What

Work this list in order; each step isolates a layer.

1. **Vendor viewer first.** `realsense-viewer`, `k4aviewer`, DepthAI demo. If depth is
   bad in the vendor tool, it's hardware/environment, not your code. Saves hours.
2. **Check the validity mask.** Render `depth == 0` as a binary image. Holes on black
   objects, glass, beyond-range, inside-MinZ are *expected physics*, not bugs.
3. **Flat-wall test (quantifies noise + bias).** Aim at a flat matte wall, 1.0 m,
   perpendicular. Fit a plane (RANSAC, 1 cm threshold) to the central 200×200 px region.
   - RMS plane residual ≈ predicted σ_z (Section 1)? If 3× worse → dirty lens, failed
     calibration, or wrong preset.
   - Plane distance vs. tape measure: bias >1% at 1 m on stereo → run on-chip
     self-calibration (RealSense: Tare + On-Chip Calib via `rs-fw-update`/SDK) or factory
     reset calibration.
   - Wall "bowed" (center nearer than edges): residual distortion → recalibrate; on ToF,
     some bowing near walls is multipath and is physics.
4. **Check temporal stability.** Pixel-wise std over 100 static frames. "Breathing" depth
   on stereo = projector/exposure flicker (check 50/60 Hz `power_line_frequency` option);
   on ToF with another ToF nearby = interference (Section 6).
5. **Check timestamps and frame pairing** before blaming alignment (Section 4 table).
6. **Check the depth scale.** Depths exactly 1000× off = forgot `depth_scale`. Depths
   ~10× off on D405 = its default unit is 100 µm, not 1 mm. Always read the scale from
   the device.
7. **USB/bandwidth.** Dropped frames, corrupted stripes, or fps below requested →
   `dmesg` for USB resets, check hub topology (cameras on separate root hubs), reduce
   resolution before blaming the camera.
8. **Reproduce with a recording.** `rs-record`/`k4arecorder` a `.bag`/`.mkv` of the
   failure; iterate on filters offline. Production tip: ship a ring-buffer recorder
   triggered on perception anomalies — depth failures are environmental and you will
   not reproduce them at your desk.

---

## 10. Production Hardening Checklist

- [ ] Depth error budget computed (Section 1 formula) for the worst-case working range, and verified with the flat-wall test on **each** unit before deployment (unit-to-unit calibration variance is real).
- [ ] MinZ blind zone covered by a secondary sensor or software standoff (Section 2).
- [ ] All invalid-depth (0) pixels propagate as *unknown*, never as free or filled space.
- [ ] Hole filling disabled for geometric decisions; enabled only for viz/CNN inputs.
- [ ] Frame pairing uses hardware-matched framesets; alignment uses per-device factory extrinsics + color distortion.
- [ ] Multi-ToF rigs use sync cables with ≥160 µs laser offsets; multi-cam extrinsics validated to <2× σ_z.
- [ ] QoS = SensorDataQoS on all image subscribers; serial numbers pinned per camera.
- [ ] Screw-lock USB; auto-recovery on device disconnect; `% valid pixels` exported as a health metric with planner response.
- [ ] Sunlight behavior tested at solar noon; ToF not used as primary outdoor depth.
- [ ] Thermal warm-up (15 min) before any calibration; firmware versions pinned and recorded per unit.
- [ ] Anomaly-triggered ring-buffer recording (.bag/.mkv) deployed for field debugging.

## Quick Reference — Exact Starting Values

| Parameter | Value | Where |
|---|---|---|
| Stereo subpixel disparity noise σ_d | 0.05–0.1 px | Error model |
| RealSense spatial filter | alpha 0.5, delta 20, magnitude 2 | Sec. 5 |
| RealSense temporal filter | alpha 0.4, delta 20, persistence 3 | Sec. 5 |
| StatisticalOutlierRemoval | meanK 20, stddev 1.0 | Sec. 5 |
| TSDF fusion | voxel 5–10 mm, trunc 4× voxel | Sec. 5 |
| K4A multi-cam laser offset | ≥160 µs per subordinate | Sec. 6 |
| Outdoor AE exposure cap | ~8500 µs @30 fps (moving robot) | Sec. 7 |
| OAK-D Pro IR projector | 800 mA (max 1200) | Sec. 8 |
| Voxel downsample leaf | 5–10 mm manipulation / 3–5 cm nav | Sec. 3 |
| Hand-eye calibration | ≥15 poses, ≥60° rotation diversity | Sec. 6 |
| Flat-wall acceptance | RMS residual ≤ 2× predicted σ_z, bias ≤1% | Sec. 9 |
