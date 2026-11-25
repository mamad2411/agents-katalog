---
name: ops-docker-ci
description: >-
  Containerise, test and ship a ROS 2 workspace: ros/osrf images, multi-stage Dockerfile with rosdep and colcon,
  docker compose, DDS or Zenoh discovery between containers, GPU and X11, ARM64 buildx, GitHub Actions with
  action-ros-ci or industrial_ci. Use for a Dockerfile, compose.yaml or CI workflow, or when containers miss topics.
license: Apache-2.0
metadata:
  sources: [robotics-agent-skills]
  evidence: researched
  last_verified: 2026-11-18
---

# Docker and CI for ROS 2

Lets an agent put a colcon workspace into images, connect the containers of one robot, and build
and test it in GitHub Actions. Written for ROS 2 Jazzy (Ubuntu 24.04) on a Linux Docker host;
Lyrical and Humble differences are at the end. The recipes were researched, not run.

## When to use

- Writing or fixing a `Dockerfile`, `.dockerignore`, `compose.yaml` or `.github/workflows/*.yml`
  for a ROS 2 workspace.
- Nodes in different containers, or a container and the host, do not see each other or get no data.
- A container needs a display, a GPU, a serial port or a camera; or an ARM64 image is needed.
- Not for: writing packages and nodes ([ros2-core](../ros2-core/SKILL.md)); starting the robot at
  boot with systemd (the later `bringup` skill).

## Quick start

Workspace `./src/<packages>`, plus the `Dockerfile`, `.dockerignore` and
`docker/ros_entrypoint.sh` from [references/dockerfile.md](references/dockerfile.md):

```bash
docker build --target build -t my_robot:build .
docker run --rm my_robot:build bash -c \
  'source install/setup.bash && colcon test --event-handlers console_direct+ && colcon test-result --verbose'
docker build --target runtime -t my_robot:jazzy .
docker run --rm -it --network host --ipc host -e ROS_DOMAIN_ID=42 my_robot:jazzy   # robot.launch.py
```

## Workflow

### 1. Choose the base images

| Image | Adds | Use for | Size |
|---|---|---|---|
| `ros:jazzy-ros-core` | rclcpp, rclpy, launch, common_interfaces; no colcon or rosdep | runtime stage | 158 MB |
| `ros:jazzy-ros-base` (= `ros:jazzy`) | colcon, rosdep, vcstool, compilers, rosbag2, tf2, urdf | deps and build stages, CI | 299 MB |
| `ros:jazzy-perception` | image_pipeline, vision_opencv, perception_pcl, laser_filters | camera and lidar containers | 1084 MB |
| `osrf/ros:jazzy-simulation` | ros_gz (Gazebo Harmonic) | headless simulation | 732 MB |
| `osrf/ros:jazzy-desktop`, `-desktop-full` | RViz, rqt, demos | development machines | 1262, 1423 MB |

Sizes are compressed amd64 downloads on Docker Hub, checked 2026-11-18. The `ros:` images are
built for amd64 and arm64; the `osrf/ros` desktop and simulation tags for amd64 only.

Name the distro in every tag (`ros:latest` is Lyrical now) and add the Ubuntu codename
(`ros:jazzy-ros-base-noble`) or a digest for repeatable builds.

Check: `docker run --rm ros:jazzy-ros-base-noble printenv ROS_DISTRO` prints `jazzy`.

### 2. Write the multi-stage Dockerfile

Stages `manifests` → `deps` → `build` → `runtime`, full file in
[references/dockerfile.md](references/dockerfile.md#dockerfile):

- `deps` copies only the `package.xml` files, runs `rosdep update` and `rosdep install`, so source
  edits do not reinstall dependencies.
- `build` copies `src/` and runs `colcon build`.
- `runtime` starts from `ros-core`, installs exec dependencies with `rosdep install -t exec`,
  copies `install/`, and runs as a non-root user through an entrypoint that sources
  `/ws/install/setup.bash`.
- Declare the RMW (`rmw_cyclonedds_cpp`, `rmw_zenoh_cpp`) as an `exec_depend` of the bringup
  package so rosdep installs it.

Check: after editing a `.cpp` file, a rebuild shows `CACHED` for the `deps` steps, and
`docker run --rm my_robot:jazzy ros2 pkg executables my_robot_bringup` lists your executables.

### 3. Test inside the image

Run `colcon test`, then `colcon test-result --verbose`; only the second fails on a failed test.
Check: break one assertion on purpose and the command exits non-zero; then restore it.

### 4. Decide how containers talk

| Layout | Use when |
|---|---|
| `network_mode: host` + `ipc: host` on every service | One robot computer; containers also talk to host tools and other machines |
| One compose bridge network | Isolated sim or test stacks; nothing leaks to the LAN or the host |
| Bridge + `ROS_STATIC_PEERS` | The network drops multicast |
| `rmw_zenoh_cpp` + a `rmw_zenohd` service | Several hosts, Wi-Fi, Docker Desktop, or noisy DDS discovery |

Same `ROS_DOMAIN_ID` (0 to 101 on Linux) and same `RMW_IMPLEMENTATION` everywhere. Compose files
for each layout: [references/compose.md](references/compose.md). Middleware choice:
[choose a ROS 2 middleware](../../wiki/guides/choose-a-ros2-middleware.md).

Check: `docker compose exec <service> ros2 node list` shows nodes of every service, and
`ros2 topic hz <topic>` shows data. Nodes listed but no data points to shared memory (see Traps).

### 5. Devices, display and GPU

- Devices: `devices:` with `/dev/serial/by-id/...` paths, `group_add: [dialout]` or `[video]`.
- Display: `DISPLAY`, the `/tmp/.X11-unix` socket and `xhost +SI:localuser:<user>` with a
  matching container UID.
- NVIDIA: install the NVIDIA Container Toolkit, run `nvidia-ctk runtime configure`, reserve the
  GPU in compose, and set `NVIDIA_DRIVER_CAPABILITIES` to include `graphics` for RViz and Gazebo.
  Details: [references/gpu-display.md](references/gpu-display.md).

Check: `docker compose exec driver ls -l /dev/my_robot_mcu`; `nvidia-smi` works in the container;
`rviz2` opens a window.

### 6. Build for ARM64

`docker buildx build --platform linux/amd64,linux/arm64 --push` with QEMU installed; the Dockerfile
does not change because `ros:` images are multi-arch. Use native arm64 builders for big C++
workspaces. Jetson needs L4T-based images (see the reference).

Check: `docker buildx imagetools inspect ghcr.io/my-org/my_robot:jazzy` lists `linux/arm64`, and
`uname -m` in the image on the robot prints `aarch64`.

### 7. Add CI

- Package CI: `ros-tooling/action-ros-ci@v0.4` inside a `rostooling/setup-ros-docker` container,
  one matrix row per distro; upload `ros_ws/log` and publish the JUnit files.
- Image CI: build the `build` stage with `docker/build-push-action@v7` and a `type=gha` cache, run
  the tests in it, push the runtime image from `main` and tags.
- Wide matrices or ROS-Industrial checks: `industrial_ci`. Workflows for all three:
  [references/github-actions.md](references/github-actions.md).

Check: a pull request with a failing test turns the job red, and the logs artifact is there.

### 8. Keep secrets out

Tokens come from the CI secret store (`${{ secrets.NAME }}`) or `docker build --secret`, are read
with `RUN --mount=type=secret`, and never go into `ARG`, `ENV`, a `COPY`, a `.repos` file or a
workflow file. Prefer checking private repositories out before the build.

Check: `docker history --no-trunc my_robot:jazzy` and `git grep -i -E 'token|password'` show no
credential; workflows set `permissions:` explicitly.

## Traps

**Images and builds**

- `ros:latest` moved to Lyrical (Ubuntu 26.04, Python 3.14). An unpinned `FROM` changes distro.
- `useradd -u 1000` fails on Jazzy and Lyrical images: Ubuntu 24.04+ images already have user
  `ubuntu` with UID 1000. Remove it first or reuse it.
- Runtime image starts but launch fails on missing packages: no `rosdep install -t exec` in it.
- `rosdep` cannot resolve a new key: the cache in `ros-base` is as old as the image; run
  `rosdep update` in the deps stage. `apt-get update` belongs in the same `RUN` as the install.
- `pip install` fails with "externally-managed-environment" on Ubuntu 24.04: use apt `python3-*`
  packages (rosdep keys) or a virtual environment.
- `/ros_entrypoint.sh: no such file` or `bad interpreter`: CRLF line endings from a Windows
  checkout. Add `*.sh text eol=lf` to `.gitattributes`.

**Networking and middleware**

- Fast DDS with `--network host` but without `--ipc host`: `ros2 node list` works, no data
  arrives. Add `ipc: host` to every service, or set `FASTDDS_BUILTIN_TRANSPORTS=UDPv4`.
- Shared memory files belong to the user that made them; mixing root and UID 1000 containers that
  share IPC breaks shared memory transport. Use one UID.
- `ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST` on a bridge network isolates each container, because
  localhost is the container. `ROS_LOCALHOST_ONLY` is deprecated since Iron.
- A hand-written Cyclone DDS peer list with multicast off finds nothing unless
  `ParticipantIndex` is `auto` (Cyclone 0.10 defaults to `none`); `ROS_STATIC_PEERS` sets it.
- Zenoh: no router, no discovery. The router exits on hosts without IPv6 until its listen endpoint
  is `tcp/0.0.0.0:7447`. `ROS_STATIC_PEERS` and the discovery range do not apply to Zenoh.
- Docker Desktop (macOS, Windows) runs containers in a VM; its host networking is opt-in and
  layer 4 only. DDS discovery across it is untested here; Zenoh over TCP is the safer choice.

**Hardware and platforms**

- `osrf/ros:*-desktop` has no arm64 image: build desktop on `ros:jazzy-ros-base` with
  `ros-jazzy-desktop`.
- RViz in a container with an NVIDIA GPU but a black or software-rendered window:
  `NVIDIA_DRIVER_CAPABILITIES` lacks `graphics` (default is `compute,utility`).
- `load: true` with two platforms fails on the classic image store; push multi-platform builds.

**CI**

- `colcon test` exits 0 on failed tests; the job only fails through `colcon test-result`.
- Registry image names must be lowercase; `github.repository` may contain capitals.
- `ros-industrial/industrial_ci` tags are old (0.10.0 predates Jazzy); its docs use `@master`, so
  pin a commit SHA.
- Self-hosted runners running jobs in parallel share one network: isolate tests with
  `ament_add_ros_isolated_gtest` / `ament_add_ros_isolated_pytest_test` or per-job domain IDs.

## Checks

1. `docker build --pull --no-cache --target runtime .` succeeds (no hidden local cache state), and
   the image's `ros2 pkg executables` lists the workspace packages.
2. Tests run in the `build` stage and a failing test makes the command exit non-zero.
3. `docker compose config --quiet` passes; `ros2 node list` and `ros2 topic hz` across services
   show both discovery and data.
4. CI ran on a branch, the matrix covers each target distro, and logs are uploaded.
5. No secret in the Dockerfile, compose file, workflows, `docker history`, or the build context.

## Distro differences

- **Humble** (Ubuntu 22.04 `jammy`, until 2027-05): no `ROS_AUTOMATIC_DISCOVERY_RANGE` or
  `ROS_STATIC_PEERS`; use `ROS_LOCALHOST_ONLY=1` or middleware XML. The image has no `ubuntu`
  user. CI container tag `ubuntu-jammy-ros-humble-ros-base-latest`.
- **Lyrical** (LTS, Ubuntu 26.04 `resolute`): `ros:lyrical` is also `ros:latest`. Python 3.14,
  Qt 6, Gazebo Jetty. Fast DDS 3.6 reads `FASTDDS_DEFAULT_PROFILES_FILE`, where Jazzy's Fast DDS
  2.14 reads `FASTRTPS_DEFAULT_PROFILES_FILE`. Cyclone DDS 11 replaces 0.10. CI container tag
  `ubuntu-resolute-ros-lyrical-ros-base-latest`, or runner `ubuntu-26.04`.

## Related

- Skills: [ros2-core](../ros2-core/SKILL.md) (packages, colcon, tests),
  [ros2-web-bridge](../ros2-web-bridge/SKILL.md) (rosbridge in a container),
  [ros2-control](../ros2-control/SKILL.md) (hardware interfaces in driver containers). Later:
  `bringup` (systemd and launch on the robot), micro-ROS (agent container), Gazebo.
- Wiki: [ROS 2](../../wiki/tools/ros2.md), [colcon](../../wiki/tools/colcon.md),
  [Pixi](../../wiki/tools/pixi.md) (environments without Docker),
  [Fast DDS](../../wiki/software/fast-dds.md), [Cyclone DDS](../../wiki/software/cyclone-dds.md),
  [rmw_zenoh](../../wiki/software/rmw-zenoh.md).
- References: [dockerfile.md](references/dockerfile.md), [compose.md](references/compose.md),
  [gpu-display.md](references/gpu-display.md), [github-actions.md](references/github-actions.md).
