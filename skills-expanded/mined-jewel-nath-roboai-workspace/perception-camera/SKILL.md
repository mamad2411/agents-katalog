---
name: perception-camera
description: Cameras on ROS 2 Jazzy - usb_cam, v4l2_camera, camera_ros, RealSense and OAK drivers, camera_calibration and
  camera_info_url, image_proc rectification, optical frames, image_transport and compressed topics, cv_bridge,
  depth_image_proc point clouds, apriltag_ros tag poses, and running a detection or segmentation model on the stream.
license: Apache-2.0
metadata:
  sources: [robotics-agent-skills]
  evidence: researched
  last_verified: 2026-11-23
---

# Camera perception

Lets an agent bring up a camera with correct calibration, frames and timestamps, then turn its
images into rectified streams, point clouds, tag poses and detections, and prove each step.
Written for Jazzy from the sources of image_pipeline 5.0.13, image_common 5.1.8, vision_opencv
4.1.0, usb_cam 0.8.1, realsense2_camera 4.59.2, depthai-ros 2.13.0 and apriltag_ros 3.4.0; the
recipes were not run. Lyrical and Humble differences are at the end.

## When to use

- Connecting a USB/UVC webcam, a Raspberry Pi camera, an Intel RealSense or a Luxonis OAK.
- `camera_info` is all zeros, or rectified images, point clouds or tag distances look wrong.
- Rectifying, resizing or compressing images; images over Wi-Fi; recording camera bags.
- Writing a node that reads images with `cv_bridge`, or runs a detector or segmenter and
  publishes `vision_msgs`.
- Turning depth images into point clouds or 3D positions of detected objects.
- Detecting AprilTags for docking, object poses or checking a camera mount.

Elsewhere: lidar, point-cloud processing and lidar-camera extrinsics in
[perception-lidar](../perception-lidar/SKILL.md); SLAM, visual odometry and camera-IMU calibration
(Kalibr) in [perception-slam](../perception-slam/SKILL.md); camera links in the URDF in
[ros2-robot-description](../ros2-robot-description/SKILL.md); simulated cameras in
[sim-gazebo](../sim-gazebo/references/sensors.md); video to a browser in
[ros2-web-bridge](../ros2-web-bridge/references/camera-streaming.md); hand-eye calibration of arm
cameras in `manip-moveit2` and the sensor calibration playbook (Phase 6); TensorRT and Jetsons in
`learn-edge-deployment`.

## Quick start

```bash
sudo apt install ros-jazzy-usb-cam ros-jazzy-image-pipeline ros-jazzy-image-transport-plugins \
  ros-jazzy-rqt-image-view v4l-utils
source /opt/ros/jazzy/setup.bash
v4l2-ctl --list-devices
ros2 run usb_cam usb_cam_node_exe --ros-args -r __ns:=/camera \
  -p video_device:=/dev/video0 -p pixel_format:=mjpeg2rgb -p frame_id:=camera_optical_frame
ros2 topic hz /camera/image_raw
ros2 run camera_calibration cameracalibrator --size 8x6 --square 0.025 --ros-args \
  -r image:=/camera/image_raw -r camera/set_camera_info:=/camera/usb_cam/set_camera_info
ros2 launch image_proc image_proc.launch.py namespace:=camera
ros2 run rqt_image_view rqt_image_view /camera/image_rect_color
```

After CALIBRATE and COMMIT, `usb_cam` stores the calibration and `image_rect_color` shows straight
edges straight. For a robot, use the parameter and launch files in
[references/drivers.md](references/drivers.md).

## Workflow

1. **Pick the driver and install it from apt.** USB: `usb_cam` (MJPEG decode) or `v4l2_camera`;
   libcamera and Pi modules: `camera_ros`; RealSense: `realsense2_camera`; OAK: `depthai_ros_driver`
   (2.x on Jazzy; OAK4 needs DepthAI v3 from source); ZED: `zed-ros2-wrapper`, not in rosdistro,
   needs the ZED SDK. Use stable device paths (`/dev/v4l/by-id/...`, `serial_no`). Table and
   parameters: [references/drivers.md](references/drivers.md).
   *Check:* `ros2 topic hz /camera/image_raw` shows the configured rate, and
   `ros2 topic echo --once --no-arr /camera/camera_info` has the image's width and height.

2. **Get the frames right.** The URDF holds `camera_link` (x forward) and a fixed child
   `camera_optical_frame` (z forward, x right, y down; REP 103). Images, `camera_info`, depth and
   points are stamped in the optical frame: set the driver's `frame_id` (`usb_cam`, `camera_ros`)
   or `camera_frame_id` (`v4l2_camera`). RealSense and OAK publish their own optical frames: put
   only their root in the URDF (RealSense: `sensor_d435` macro with default
   `use_nominal_extrinsics:=false`), never both. URDF snippet:
   [ros2-robot-description](../ros2-robot-description/references/sensors-control-display.md).
   *Check:* `ros2 run tf2_ros tf2_echo base_link camera_optical_frame` gives the measured mount,
   and `view_frames` shows one parent per camera frame.

3. **Calibrate the intrinsics.** USB cameras arrive uncalibrated (`k` all zeros). Run
   `cameracalibrator` with the board's interior-corner count and measured square size, at the
   resolution you will run, and cover the whole view including corners and tilts. COMMIT writes
   through the driver's `set_camera_info`; SAVE leaves `ost.yaml` in
   `/tmp/calibrationdata.tar.gz`. Keep the YAML in your package and point `camera_info_url` at it
   (`package://...` or `file:///...`). RealSense and OAK publish factory calibration. Details:
   [references/calibration.md](references/calibration.md).
   *Check:* `cameracheck` on the rectified stream reports low linearity and reprojection errors
   across the image, and a second calibration gives nearly the same fx, fy, cx, cy.

4. **Rectify and shape the stream.** Compose `image_proc` components (`RectifyNode`,
   `DebayerNode`, `ResizeNode`, `CropDecimateNode`) in one container next to the driver.
   `camera_info` follows the image remap in Jazzy. The nodes are lazy (they work only while their
   output has a subscriber) and publish reliable. Launch file:
   [references/drivers.md](references/drivers.md).
   *Check:* `ros2 topic hz /camera/image_rect` ticks and no node logs "is uncalibrated".

5. **Move images efficiently.** With `image_transport_plugins` every publisher adds
   `<topic>/compressed` (JPEG/PNG), `/compressedDepth` (depth), `/zstd` and `/theora`. Send
   compressed colour over Wi-Fi and into bags, depth only as `compressedDepth`, and keep full-rate
   raw images inside one process. Subscribe to sensor data best effort (REP 2003). Parameters,
   `republish` and QoS overrides: [references/image-pipeline.md](references/image-pipeline.md).
   *Check:* `ros2 topic bw` on the compressed topic is a fraction of the raw one, and the remote
   viewer stays smooth.

6. **Read images in your own node.** Python: `CvBridge().imgmsg_to_cv2(msg, 'bgr8')`, or
   `compressed_imgmsg_to_cv2` for `<topic>/compressed`; subscribe best effort with depth 1 when
   processing is slower than the camera. C++: `#include <cv_bridge/cv_bridge.hpp>`,
   `cv_bridge::toCvShare(msg, "bgr8")`, `image_transport::create_camera_subscription`. Copy the
   input header into every output. Keep apt's OpenCV and NumPy for ROS; put model frameworks in a
   venv with `--system-site-packages` and `numpy<2`.
   *Check:* output stamps equal input stamps, and `ros2 topic delay /<output>` stays flat.

7. **Depth to 3D.** Depth is 32FC1 metres (canonical, NaN invalid) or 16UC1 millimetres (0 invalid)
   per REP 118. Prefer the driver's alignment and cloud (RealSense `align_depth.enable`,
   `pointcloud.enable`; OAK aligns by default); otherwise `depth_image_proc` (`PointCloudXyzNode`,
   `RegisterNode`, `PointCloudXyzrgbNode`). For one pixel: median of valid depths around it, then
   `PinholeCameraModel.project_pixel_to_3d_ray` (a unit vector) scaled to that depth.
   [references/image-pipeline.md](references/image-pipeline.md),
   [references/detection-node.md](references/detection-node.md).
   *Check:* in RViz with fixed frame `base_link`, the cloud overlays the scene, a flat wall is flat,
   and a measured distance matches.

8. **AprilTags.** `apriltag_node` on `image_rect` with `qos_profile: sensor_data`, the printed
   `family`, and `size` measured where the black and white borders meet. It publishes
   `detections` and TF from the optical frame to `tag36h11:<id>` or your frame names.
   [references/apriltag.md](references/apriltag.md).
   *Check:* `tf2_echo camera_optical_frame tag36h11:0` gives z equal to a tape-measured distance,
   at the image centre and near its edges.

9. **Run a model on the stream.** Check the model's licence first (Ultralytics is AGPL-3.0;
   SAM, SAM 2, Grounding DINO and YOLOX are Apache-2.0; FoundationPose is non-commercial). Feed it
   the newest frame only, publish `vision_msgs/Detection2DArray` (or `Detection3DArray` with depth)
   with the image header, and pair each resized stream with its own `camera_info`. Node, adapter
   and licence table: [references/detection-node.md](references/detection-node.md).
   *Check:* `ros2 topic hz /detections` meets the target rate, `ros2 topic delay /detections`
   stays within the latency budget, and boxes land on the right objects.

## Traps

| Symptom | Cause | Fix |
|---|---|---|
| Driver cannot open the device, or opens a node with no frames | Wrong `/dev/videoN` (metadata node), device busy, user not in `video` | `v4l2-ctl --list-devices`; `/dev/v4l/by-id/`; close other users; add the group |
| Low frame rate at high resolution | Uncompressed YUYV over USB | `pixel_format: mjpeg2rgb`, a lower size, or another USB controller |
| "Rectified topic ... requested but camera publishing ... is uncalibrated" | `k` is zero: no calibration loaded | Calibrate; set `camera_info_url` as a URL |
| "Invalid camera info URL", "calibration file ... not found", "does not match name" | Plain path instead of `file:///`, or `camera_name` differs from the file | URL form; same `camera_name` in driver and file |
| Rectified image bent, zoomed or black at the edges after a mode change | Calibrated at another resolution, or poor corner coverage | Recalibrate at the running resolution, boards into the corners |
| Cloud or detections rotated 90° in RViz | Data stamped in `camera_link` instead of the optical frame | Optical frame in the URDF; driver `frame_id` set to it |
| TF warns of two parents, camera frames jump | Driver publishes TF and the URDF holds the same frames | `publish_tf:=false` with nominal extrinsics, or URDF root only |
| Subscriber silent, "incompatible QoS" | Reliable subscriber on a best-effort publisher (`apriltag_ros` defaults to reliable) | Sensor-data QoS; `qos_profile: sensor_data` |
| `image_proc` or `depth_image_proc` output silent | Nothing subscribes (lazy), `camera_info` not beside the image, stamps differ | Subscribe; check `<ns>/camera_info`; raise `queue_size` |
| Calibrator stuck on "Waiting for service camera/set_camera_info" | Service has another name | Remap to `ros2 service list` output, or `--no-service-check` and SAVE |
| Detections seconds behind reality | Queued frames in front of a slow model | Best effort, depth 1, newest frame only; watch `ros2 topic delay` |
| `cv_bridge` import fails with a NumPy 1.x/2.x error | pip put NumPy 2 in the path | venv with `numpy<2`, apt `python3-opencv` |
| Coloured cloud has colours offset from geometry | Depth not registered to the colour camera | `align_depth.enable:=true` or `RegisterNode` with TF |
| 3D points too far or too close by a constant factor | Unit ray treated as z = 1, or 16UC1 millimetres read as metres | Scale the ray by `z / ray[2]`; divide 16UC1 by 1000 |
| Distant depth missing after compression | `compressedDepth` sets 16UC1 pixels beyond `depth_max` (10 m) to 0; JPEG on depth | Raise `depth_max`; never JPEG depth |
| Tag distances off by a constant factor | `size` measured on the outer printed edge | Measure where black and white borders meet |
| RealSense or OAK not found | udev rules missing, USB 2 port or cable | Vendor udev rules; USB 3 |
| Wi-Fi saturated, bags huge | Raw images across machines | Compressed sub-topics; record `/compressed` with `camera_info` |

## Checks

Before reporting a camera pipeline working:

- `ros2 topic hz` on `image_raw`, `image_rect` and every output matches the design rate.
- `camera_info` has non-zero `k`, the image's width and height, and the optical `frame_id`.
- `tf2_echo base_link <optical frame>` matches the measured mount; `view_frames` shows one tree.
- RViz (fixed frame `base_link`): the Camera display overlays TF axes on the image, and point
  clouds sit on the scene.
- A known target (AprilTag, box, wall) at a measured distance reads that distance in the tag TF,
  the point cloud and `detections_3d`.
- `ros2 topic delay` on the final output is within budget and stable over several minutes.
- The licences of the driver, the model code and its weights are recorded in the package.

## Distro differences

- **Lyrical Luth** (Ubuntu 26.04, image_pipeline 7.1, image_common 6.4): `image_transport` C++
  overloads taking `rclcpp::Node *` and `rmw_qos_profile_t` are deprecated; use
  `image_transport::RequiredInterfaces` and `rclcpp::QoS`. `image_transport_py` adds Python
  publishers and subscribers. depthai-ros is 3.x (DepthAI v3) with `driver.launch.py` in place of
  `camera.launch.py`. Ubuntu's OpenCV is 4.10, which has the `cv2.aruco.ArucoDetector` class;
  Jazzy's 4.6 has only the older free functions (`cv2.aruco.detectMarkers`). Jazzy's mislabelled
  `point_cloud_xyzrgb_radial_node` executable is fixed.
- **Humble**: `cv_bridge/cv_bridge.h` (no `.hpp`); `image_geometry` Python has only camelCase
  methods (`fromCameraInfo`, `rectifyPoint`, `projectPixelTo3dRay`); `camera_info` does not
  follow an image remap, so remap it explicitly; most `image_pipeline` nodes lack QoS overrides;
  `republish` takes the transports as positional arguments; no `zstd_image_transport`; the
  radial `depth_image_proc` inputs have their older names.
- `realsense2_camera` 4.59.2 and `apriltag_ros` 3.4.0 are the same release on all three.

## Related

- References: [drivers.md](references/drivers.md), [calibration.md](references/calibration.md),
  [image-pipeline.md](references/image-pipeline.md), [apriltag.md](references/apriltag.md),
  [detection-node.md](references/detection-node.md).
- Wiki: [OpenCV](../../wiki/software/opencv.md), [image_pipeline](../../wiki/software/image-pipeline.md),
  [AprilTag](../../wiki/software/apriltag.md), [tf2](../../wiki/software/tf2.md),
  [URDF](../../wiki/software/urdf.md), [ROS 2](../../wiki/tools/ros2.md),
  [Foxglove](../../wiki/tools/foxglove.md), [Rerun](../../wiki/tools/rerun.md),
  [YOLO](../../wiki/learning/models/yolo.md),
  [Segment Anything](../../wiki/learning/models/segment-anything.md),
  [Grounding DINO](../../wiki/learning/models/grounding-dino.md),
  [FoundationPose](../../wiki/learning/models/foundationpose.md),
  [TUM RGB-D](../../wiki/learning/datasets/tum-rgbd.md).
- Skills: [perception-lidar](../perception-lidar/SKILL.md),
  [perception-slam](../perception-slam/SKILL.md), [ros2-core](../ros2-core/SKILL.md),
  [ros2-robot-description](../ros2-robot-description/SKILL.md),
  [sim-gazebo](../sim-gazebo/SKILL.md), [ros2-web-bridge](../ros2-web-bridge/SKILL.md),
  [ops-docker-ci](../ops-docker-ci/SKILL.md); later `nav-nav2`, `manip-grasping`,
  `learn-edge-deployment`, `ops-bringup`.
- Upstream: the `image_pipeline` docs on its `jazzy` branch (camera_calibration tutorials,
  image_proc and depth_image_proc components, camera_info), REP 103, REP 118, REP 2003, and the
  READMEs of usb_cam, v4l2_camera, camera_ros, realsense-ros, depthai-ros and apriltag_ros.
