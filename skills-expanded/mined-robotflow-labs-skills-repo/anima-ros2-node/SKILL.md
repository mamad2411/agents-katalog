# /ros2-node — Turn Any ANIMA Module Into a ROS2 Node

Every ANIMA module must be a ROS2 node. This skill analyzes an existing module, builds the ROS2 layer (messages, node, Docker, launch file), and validates everything works. Based on the MONAD reference implementation (D-034).

Run this on every module. No exceptions.

## Usage

```
/ros2-node                        # Asks which module folder
/ros2-node project_hermes         # Specific module
/ros2-node 01-LLMDet              # By folder name
```

## Instructions

### PHASE 0: DEEP ANALYSIS — Understand the Module First

Before generating ANY code, you MUST fully understand what the module does. Read everything:

```
1. pyproject.toml          — name, version, dependencies, entry points
2. src/{module}/server.py  — FastAPI routes (these become ROS2 services)
3. src/{module}/engine.py  — Core inference (this is what the node wraps)
4. src/{module}/api/       — API endpoints (map to ROS2 topics/services)
5. src/{module}/config.py  — Configuration (becomes ROS2 parameters)
6. src/{module}/schemas.py — Pydantic models (map to ROS2 message fields)
7. Dockerfile              — Existing Docker setup
8. docker-compose.yml      — Existing compose config
9. README.md               — What the module does
10. CLAUDE.md              — Project-specific instructions
11. tests/                 — Existing test patterns
12. anima_module.yaml      — ANIMA manifest (if exists)
```

**Critical questions to answer before writing code:**

1. **What are the inputs?** (camera image? point cloud? text? sensor data?)
2. **What are the outputs?** (detections? depth map? masks? trajectories? poses?)
3. **What standard ROS2 message types match?** (see Message Type Reference below)
4. **Does it need services (request/response) or just pub/sub (streaming)?**
5. **What's the core engine class?** (the thing the node wraps)
6. **Does it need continuous mode?** (subscribe to camera, process every frame)
7. **What backends exist?** (demo, cpu, gpu, mlx — these become ROS2 parameters)
8. **Are there model weights needed?** (affects Dockerfile and startup)

**Output**: A module profile that drives ALL subsequent code generation.

```
MODULE PROFILE:
  Name: hermes
  Display: HERMES — Communication Protocol Engine
  Category: communication
  Engine class: src/hermes/engine.py::CommunicationEngine

  INPUTS:
    - text commands (string)
    - robot state (geometry_msgs/Pose)

  OUTPUTS:
    - command responses (string)
    - action plans (custom message)

  SERVICES:
    - /hermes/execute_command (text → action plan)
    - /hermes/get_status (→ status)

  TOPICS:
    - /hermes/status (1Hz, RELIABLE)
    - /hermes/actions (on-demand, BEST_EFFORT)

  PARAMETERS:
    - backend (demo/full)
    - device (cpu/cuda/mps)
    - model_path (string)

  ROS2 MSG TYPES NEEDED:
    - std_msgs/String
    - geometry_msgs/Pose
    - Custom: hermes_msgs/ActionPlan
```

---

### PHASE 1: CHECK EXISTING STATE

Before creating anything, check what already exists:

```bash
# Check for existing ROS2 packages
ls {module}_msgs/ 2>/dev/null
ls {module}_node/ 2>/dev/null
ls Dockerfile.ros2 2>/dev/null

# Check if docker-compose already has ros2 profile
rg "ros2" docker-compose.yml 2>/dev/null

# Check for existing ROS2 imports
rg "rclpy|ros2|sensor_msgs|vision_msgs" src/ 2>/dev/null
```

**If ROS2 packages already exist**: Review them, validate against the MONAD pattern, fix any gaps.
**If nothing exists**: Build from scratch following the phases below.

Also check if the **basic Docker** is working:

```bash
# Does the normal Dockerfile exist and work?
ls Dockerfile 2>/dev/null
```

**If no Dockerfile at all**: Build the base Dockerfile FIRST (following `/test-mvp-production` Phase 3 template), THEN build `Dockerfile.ros2` on top. A module needs to work as a FastAPI service before becoming a ROS2 node.

---

### PHASE 2: CREATE MESSAGE PACKAGE ({module}_msgs/)

Location: `{MODULE_DIR}/{module}_msgs/`

#### 2.1 Determine Message Types

Map the module's outputs to ROS2 messages. Use STANDARD types wherever possible:

**Standard Message Type Reference:**

| Module Output | ROS2 Standard Type | When to Use |
|---------------|-------------------|-------------|
| Object detections (2D) | `vision_msgs/Detection2DArray` | Bounding boxes + labels |
| Object detections (3D) | `vision_msgs/Detection3DArray` | 3D bounding boxes |
| Segmentation masks | `sensor_msgs/Image` (mono8) | Binary/semantic masks |
| Depth maps | `sensor_msgs/Image` (32FC1) | Depth estimation |
| Point clouds | `sensor_msgs/PointCloud2` | 3D point data |
| Poses | `geometry_msgs/PoseStamped` | Position + orientation |
| Trajectories | `nav_msgs/Path` | Sequence of poses |
| Velocities | `geometry_msgs/Twist` | Linear + angular velocity |
| Text/commands | `std_msgs/String` | NL commands, status text |
| Occupancy grids | `nav_msgs/OccupancyGrid` | 2D maps |
| Camera info | `sensor_msgs/CameraInfo` | Intrinsics/extrinsics |
| IMU data | `sensor_msgs/Imu` | Acceleration + gyroscope |
| Joint states | `sensor_msgs/JointState` | Robot arm joint positions |
| Transforms | `tf2_msgs/TFMessage` | Coordinate frame transforms |

**Rule: Only create custom messages when NO standard type fits.** Custom messages break ecosystem compatibility.

#### 2.2 Create Custom Messages (only if needed)

If the module has outputs that don't fit standard types, create custom messages.

**package.xml** template:
```xml
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>{module}_msgs</name>
  <version>0.1.0</version>
  <description>ROS2 messages for ANIMA {MODULE_DISPLAY_NAME}</description>
  <maintainer email="ilessio@aiflowlabs.io">ilessio</maintainer>
  <license>Apache-2.0</license>

  <buildtool_depend>ament_cmake</buildtool_depend>
  <buildtool_depend>rosidl_default_generators</buildtool_depend>

  <depend>builtin_interfaces</depend>
  <depend>std_msgs</depend>
  <depend>sensor_msgs</depend>
  <!-- Add vision_msgs, geometry_msgs, nav_msgs as needed -->

  <exec_depend>rosidl_default_runtime</exec_depend>
  <member_of_group>rosidl_interface_packages</member_of_group>
</package>
```

**CMakeLists.txt** template:
```cmake
cmake_minimum_required(VERSION 3.8)
project({module}_msgs)

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(builtin_interfaces REQUIRED)
find_package(std_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  # Messages
  "msg/YourOutput.msg"
  "msg/{Module}Status.msg"
  # Services
  "srv/YourService.srv"
  DEPENDENCIES builtin_interfaces std_msgs sensor_msgs
)

ament_package()
```

**Status message** (EVERY module gets one):
```
# msg/{Module}Status.msg
std_msgs/Header header
string backend
string device
bool ready
float32 fps
string[] notes
```

#### 2.3 Create Service Definitions

Map FastAPI POST endpoints to ROS2 services:

```
# FastAPI endpoint:              → ROS2 service:
# POST /segment {image, prompt}  → srv/Segment.srv
# POST /detect {image}           → srv/Detect.srv
# POST /estimate_depth {image}   → srv/EstimateDepth.srv
# GET  /health                   → (no service — use status topic)
```

---

### PHASE 3: CREATE NODE PACKAGE ({module}_node/)

Location: `{MODULE_DIR}/{module}_node/`

#### 3.1 Package Structure

```
{module}_node/
├── package.xml
├── setup.py
├── setup.cfg
├── resource/{module}_node        # Empty ament marker file
├── launch/
│   └── {module}.launch.py
└── {module}_node/
    ├── __init__.py
    ├── node.py                   # Main ROS2 Node class
    ├── conversions.py            # Message ↔ numpy conversions
    └── qos.py                    # QoS profiles
```

#### 3.2 node.py — The Core (FOLLOW MONAD EXACTLY)

```python
"""
ANIMA {MODULE_DISPLAY_NAME} — ROS2 Node

Wraps the {Module}Engine directly. No REST layer in between.
ROS2 topics for streaming, services for request/response.
"""
import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup, ReentrantCallbackGroup

# Import the core engine (the ONLY dependency on module internals)
from {module}.engine import {Module}Engine  # or whatever the main class is

class {Module}Node(Node):
    def __init__(self):
        super().__init__('{module}_node')

        # ── Parameters ──
        self.declare_parameter('backend', 'demo')
        self.declare_parameter('device', 'cpu')
        self.declare_parameter('camera_topic', '/camera/image_raw')
        # ... module-specific parameters

        # ── Engine (core inference, no ROS2 deps) ──
        backend = self.get_parameter('backend').value
        device = self.get_parameter('device').value
        self._engine = {Module}Engine(backend=backend, device=device)

        # ── Callback Groups ──
        self._service_cb = MutuallyExclusiveCallbackGroup()
        self._timer_cb = ReentrantCallbackGroup()

        # ── Publishers ──
        self._status_pub = self.create_publisher(
            {Module}Status, '/{module}/status', STATUS_QOS)
        # ... output topic publishers

        # ── Services ──
        # Map each FastAPI endpoint to a service
        self.create_service(
            {Service}Srv, '/{module}/{service_name}',
            self._handle_{service}, callback_group=self._service_cb)

        # ── Status Timer (1Hz) ──
        self.create_timer(1.0, self._publish_status, callback_group=self._timer_cb)

        self.get_logger().info(f'{MODULE} node ready (backend={backend}, device={device})')

    # ── Service Handlers ──
    # Each wraps engine method with ROS2 conversion
    def _handle_{service}(self, request, response):
        try:
            # 1. Convert ROS2 msg → numpy/python
            # 2. Call engine method
            # 3. Convert result → ROS2 msg
            # 4. Set response fields
            response.success = True
        except Exception as e:
            self.get_logger().error(f'{service} failed: {e}')
            response.success = False
            response.error = str(e)
        return response

    # ── Status Publisher ──
    def _publish_status(self):
        msg = {Module}Status()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.backend = self.get_parameter('backend').value
        msg.device = self.get_parameter('device').value
        msg.ready = True
        # ... populate from engine state
        self._status_pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = {Module}Node()
    executor = MultiThreadedExecutor(num_threads=4)
    executor.add_node(node)
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
```

**CRITICAL RULES:**
- The node wraps the engine DIRECTLY — no HTTP calls, no REST API in between
- Image conversion uses PURE NUMPY — no cv_bridge dependency
- Services use `MutuallyExclusiveCallbackGroup` — prevents concurrent inference
- Status timer uses `ReentrantCallbackGroup` — never blocked by inference
- Camera subscription is LAZY — only created when continuous mode starts
- All errors caught and returned in response — node never crashes

#### 3.3 conversions.py — Pure Numpy, No cv_bridge

```python
"""Message ↔ numpy conversion. No cv_bridge dependency."""
import numpy as np

def image_msg_to_numpy(msg) -> np.ndarray:
    """sensor_msgs/Image → HxWx3 RGB numpy array."""
    buf = np.frombuffer(msg.data, dtype=np.uint8)
    if msg.encoding in ('rgb8',):
        return buf.reshape(msg.height, msg.width, 3)
    elif msg.encoding in ('bgr8',):
        return buf.reshape(msg.height, msg.width, 3)[:, :, ::-1]
    elif msg.encoding in ('mono8',):
        grey = buf.reshape(msg.height, msg.width)
        return np.stack([grey]*3, axis=-1)
    # ... handle rgba8, bgra8, 16UC1, 32FC1
    raise ValueError(f'Unsupported encoding: {msg.encoding}')

def numpy_to_image_msg(arr, stamp, frame_id, encoding='mono8'):
    """numpy array → sensor_msgs/Image."""
    from sensor_msgs.msg import Image
    msg = Image()
    msg.header.stamp = stamp
    msg.header.frame_id = frame_id
    msg.height, msg.width = arr.shape[:2]
    msg.encoding = encoding
    msg.step = msg.width * arr.dtype.itemsize * (arr.shape[2] if arr.ndim == 3 else 1)
    msg.data = arr.tobytes()
    return msg
```

#### 3.4 qos.py — Standard QoS Profiles

```python
"""ANIMA standard QoS profiles (same across all modules)."""
from rclpy.qos import QoSProfile, ReliabilityPolicy, DurabilityPolicy, HistoryPolicy

# For inference output (masks, detections, depth) — drop if subscriber is slow
OUTPUT_QOS = QoSProfile(
    reliability=ReliabilityPolicy.BEST_EFFORT,
    durability=DurabilityPolicy.VOLATILE,
    history=HistoryPolicy.KEEP_LAST,
    depth=1,
)

# For status — late subscribers get last status immediately
STATUS_QOS = QoSProfile(
    reliability=ReliabilityPolicy.RELIABLE,
    durability=DurabilityPolicy.TRANSIENT_LOCAL,
    history=HistoryPolicy.KEEP_LAST,
    depth=1,
)

# For camera input — match typical camera driver QoS
CAMERA_QOS = QoSProfile(
    reliability=ReliabilityPolicy.BEST_EFFORT,
    durability=DurabilityPolicy.VOLATILE,
    history=HistoryPolicy.KEEP_LAST,
    depth=1,
)
```

#### 3.5 Launch File

```python
"""ROS2 launch file for ANIMA {MODULE_DISPLAY_NAME}."""
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('camera_topic', default_value='/camera/image_raw'),
        DeclareLaunchArgument('backend', default_value='demo'),
        DeclareLaunchArgument('device', default_value='cpu'),
        DeclareLaunchArgument('config_path', default_value=''),

        Node(
            package='{module}_node',
            executable='{module}_node',
            name='{module}_node',
            output='screen',
            parameters=[{
                'camera_topic': LaunchConfiguration('camera_topic'),
                'backend': LaunchConfiguration('backend'),
                'device': LaunchConfiguration('device'),
                'config_path': LaunchConfiguration('config_path'),
            }],
        ),
    ])
```

---

### PHASE 4: CREATE Dockerfile.ros2

Multi-stage build following MONAD pattern. **Includes CycloneDDS and test tools** so the container is self-verifiable.

```dockerfile
# ─── ANIMA {MODULE_DISPLAY_NAME} — ROS2 Container ───
# Build: docker compose --profile ros2 build
# Run:   docker compose --profile ros2 up {module}-ros2
# Test:  docker compose --profile ros2-test run --rm anima_{module}_ros2_test

# Stage 1: Build custom messages
FROM ros:jazzy-ros-base AS msgs-build
WORKDIR /ws/src
COPY {module}_msgs/ /ws/src/{module}_msgs/
WORKDIR /ws
RUN . /opt/ros/jazzy/setup.sh && \
    colcon build --packages-select {module}_msgs

# Stage 2: Node runtime
FROM ros:jazzy-ros-base AS node

# Install CycloneDDS (required for Docker networking) + test tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-jazzy-rmw-cyclonedds-cpp \
    ros-jazzy-ros2cli \
    ros-jazzy-ros2topic \
    ros-jazzy-ros2service \
    ros-jazzy-ros2node \
    && rm -rf /var/lib/apt/lists/*

# Set CycloneDDS as default RMW
ENV RMW_IMPLEMENTATION=rmw_cyclonedds_cpp

# Install uv for Python dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install ANIMA module Python package
WORKDIR /app
COPY pyproject.toml uv.lock* ./
RUN uv pip install --system --no-cache . 2>/dev/null || \
    uv pip install --system --no-cache -e .
COPY src/ src/

# Copy built messages from stage 1
COPY --from=msgs-build /ws/install/ /ws/install/

# Build the ROS2 node package
COPY {module}_node/ /ws/src/{module}_node/
WORKDIR /ws
RUN . /opt/ros/jazzy/setup.sh && \
    . /ws/install/setup.sh && \
    colcon build --packages-select {module}_node

# Entrypoint sources ROS2 workspaces
RUN echo '#!/bin/bash\n\
source /opt/ros/jazzy/setup.bash\n\
source /ws/install/setup.bash\n\
exec "$@"' > /entrypoint.sh && chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["ros2", "launch", "{module}_node", "{module}.launch.py"]
```

**Key additions vs basic Dockerfile:**
- `ros-jazzy-rmw-cyclonedds-cpp` — CycloneDDS (works with `--network host`)
- `ros-jazzy-ros2cli` + `ros2topic/service/node` — CLI tools for self-testing
- `ENV RMW_IMPLEMENTATION=rmw_cyclonedds_cpp` — baked into image
- These tools let the `ros2-test` profile (Phase 9) verify the node without any external deps

---

### PHASE 5: UPDATE docker-compose.yml

Add the ROS2 service under the `ros2` profile:

```yaml
  # ── ROS2 Node ──
  anima_{module}_ros2:
    build:
      context: .
      dockerfile: Dockerfile.ros2
    container_name: anima-{module}-ros2
    network_mode: host              # Required for DDS multicast discovery
    environment:
      - ROS_DOMAIN_ID=0
      - RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
      - {MODULE_UPPER}_BACKEND=demo
      - {MODULE_UPPER}_DEVICE=cpu
    profiles:
      - ros2
    restart: unless-stopped
```

**If docker-compose.yml doesn't exist at all**: Create the full file with BOTH the FastAPI service (default profile) AND the ROS2 service (ros2 profile), following the `/test-mvp-production` templates.

---

### PHASE 6: CREATE TESTS

#### 6.1 Conversion Tests (NO rclpy needed)

```python
"""Test ROS2 message conversions — runs without ROS2 installed."""
import numpy as np
import pytest
from dataclasses import dataclass, field

# Mock ROS2 message classes for testing
@dataclass
class MockImage:
    height: int = 480
    width: int = 640
    encoding: str = 'rgb8'
    data: bytes = b''

# ... test all conversion functions with mocks
```

Create tests for:
- [ ] Every image encoding (rgb8, bgr8, mono8, rgba8, bgra8)
- [ ] Round-trip conversion (numpy → msg → numpy)
- [ ] Empty/edge case inputs
- [ ] Prompt/parameter conversions
- [ ] Unsupported encoding error handling

#### 6.2 Run All Tests

```bash
python -m pytest tests/ -v --tb=short 2>&1
ruff check src/ {module}_node/ tests/ 2>&1
```

**All existing tests MUST still pass.** The ROS2 layer is additive — it cannot break anything.

---

### PHASE 7: UPDATE ANIMA MANIFEST

If `anima_module.yaml` exists, update the interface section to reflect real ROS2 types:

```yaml
interface:
  inputs:
    - name: image
      ros2_type: sensor_msgs/msg/Image
      encoding: [rgb8, bgr8]
      min_hz: 1
  outputs:
    - name: {output_name}
      ros2_type: {the actual ROS2 type used}
      typical_hz: {actual fps}
  services:
    - name: /{module}/{service}
      ros2_type: {module}_msgs/srv/{Service}
```

---

### PHASE 8: VALIDATION CHECKLIST

Run through this checklist. ALL must pass:

```
ROS2 NODE VALIDATION — {MODULE_NAME}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

FILES CREATED:
  [ ] {module}_msgs/package.xml
  [ ] {module}_msgs/CMakeLists.txt
  [ ] {module}_msgs/msg/{Module}Status.msg
  [ ] {module}_msgs/msg/*.msg (custom outputs if needed)
  [ ] {module}_msgs/srv/*.srv (service definitions)
  [ ] {module}_node/package.xml
  [ ] {module}_node/setup.py
  [ ] {module}_node/setup.cfg
  [ ] {module}_node/resource/{module}_node
  [ ] {module}_node/{module}_node/__init__.py
  [ ] {module}_node/{module}_node/node.py
  [ ] {module}_node/{module}_node/conversions.py
  [ ] {module}_node/{module}_node/qos.py
  [ ] {module}_node/launch/{module}.launch.py
  [ ] Dockerfile.ros2
  [ ] tests/test_ros2_conversions.py

FILES MODIFIED:
  [ ] docker-compose.yml (ros2 profile added)
  [ ] anima_module.yaml (interface updated, if exists)

CODE QUALITY:
  [ ] ruff check passes on all new files
  [ ] All existing tests still pass
  [ ] New conversion tests pass
  [ ] Node wraps engine DIRECTLY (no REST in between)
  [ ] Pure numpy conversions (no cv_bridge)
  [ ] MultiThreadedExecutor with 4 threads
  [ ] Service callbacks use MutuallyExclusiveCallbackGroup
  [ ] Status publishes at 1Hz with RELIABLE QoS
  [ ] Output uses BEST_EFFORT QoS

DOCKER:
  [ ] Dockerfile.ros2 builds successfully
  [ ] docker-compose --profile ros2 up starts the node
  [ ] network_mode: host configured
  [ ] RMW_IMPLEMENTATION=rmw_cyclonedds_cpp set

TOPICS (verify when running):
  [ ] /{module}/status publishes at 1Hz
  [ ] /{module}/{output} publishes on inference
  [ ] Services respond to calls
```

---

### PHASE 9: REPORT

Generate a summary:

```
ROS2 NODE CREATED — {MODULE_NAME}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Files created: {N}
Files modified: {N}
Tests: {N} existing + {N} new = {TOTAL} passing
Coverage: {X}%

Topics:
  /{module}/status (1Hz, {Module}Status)
  /{module}/{output} ({OutputType})

Services:
  /{module}/{service} ({module}_msgs/srv/{Service})

Docker:
  docker compose --profile ros2 up anima_{module}_ros2

Pending:
  - Bridge fingerprint update (anima-ros2-bridge)
  - Integration tests with launch_testing (needs rclpy)
```

---

## Module-Specific Guidance

### Perception Modules (AZOTH, MONAD, CHRONOS, LOCI, LOGOS, PRISM)
- **Input**: `sensor_msgs/Image` from camera
- **Output**: `vision_msgs/Detection2DArray`, `sensor_msgs/Image` (depth/mask), etc.
- **Pattern**: Subscribe to camera → process → publish results
- **Continuous mode**: YES — process every frame

### Planning Modules (NEXUS, DAEMON, KAIROS)
- **Input**: Detections, poses, goals
- **Output**: `nav_msgs/Path`, action sequences
- **Pattern**: Service-based (plan on demand, not every frame)
- **Continuous mode**: NO — plan on request

### Control Modules (ATOMOS, PYGMALION, DAEDALUS)
- **Input**: Plans, trajectories, joint states
- **Output**: `geometry_msgs/Twist`, `sensor_msgs/JointState`
- **Pattern**: Subscribe to plan → publish commands at control rate
- **Continuous mode**: YES — control loop

### World Model Modules (GENESIS, MORPHEUS, MNEMOSYNE)
- **Input**: All sensor data
- **Output**: Scene graphs, maps, predictions
- **Pattern**: Accumulate data → maintain state → publish updates
- **Continuous mode**: YES — always updating

### Fleet Modules (AGORA, SYNTHESIS, COLOSSEUM)
- **Input**: Status from multiple robots
- **Output**: Coordination commands
- **Pattern**: Multi-robot pub/sub
- **Continuous mode**: YES — fleet coordination loop

---

---

### PHASE 9: DOCKER-BASED ROS2 VERIFICATION (no local ROS2 needed)

**This is the key phase.** After building the ROS2 node, verify it works ENTIRELY inside Docker. No agent needs ROS2 installed locally. Everything runs in containers.

#### 9.1 Add Test Service to docker-compose.yml

If not already present, add a `ros2-test` service that builds and validates the ROS2 node:

```yaml
  # ── ROS2 Smoke Test (one-shot, exits after validation) ──
  anima_{module}_ros2_test:
    build:
      context: .
      dockerfile: Dockerfile.ros2
    container_name: anima-{module}-ros2-test
    network_mode: host
    environment:
      - ROS_DOMAIN_ID=99          # Isolated domain so it doesn't clash
      - RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
      - {MODULE_UPPER}_BACKEND=demo
      - {MODULE_UPPER}_DEVICE=cpu
    entrypoint: ["/entrypoint.sh", "bash", "-c"]
    command:
      - |
        echo "=== ROS2 Node Smoke Test: {MODULE_UPPER} ==="
        echo ""

        # 1. Start node in background
        ros2 launch {module}_node {module}.launch.py backend:=demo &
        NODE_PID=$$!
        sleep 5

        # 2. Check node is alive
        echo "--- Checking node list ---"
        ros2 node list | grep {module} && echo "✅ Node found" || echo "❌ Node NOT found"

        # 3. Check topics exist
        echo ""
        echo "--- Checking topics ---"
        ros2 topic list | grep {module}
        TOPIC_COUNT=$$(ros2 topic list | grep {module} | wc -l)
        echo "Found $$TOPIC_COUNT {module} topics"

        # 4. Check status topic is publishing
        echo ""
        echo "--- Checking status topic ---"
        timeout 5 ros2 topic echo /{module}/status --once 2>/dev/null && echo "✅ Status publishing" || echo "⚠️ Status not received (may need more time)"

        # 5. Check services exist
        echo ""
        echo "--- Checking services ---"
        ros2 service list | grep {module}
        SVC_COUNT=$$(ros2 service list | grep {module} | wc -l)
        echo "Found $$SVC_COUNT {module} services"

        # 6. Summary
        echo ""
        echo "=== SUMMARY ==="
        if [ "$$TOPIC_COUNT" -gt 0 ]; then
          echo "✅ ROS2 node is ALIVE with $$TOPIC_COUNT topics and $$SVC_COUNT services"
          kill $$NODE_PID 2>/dev/null
          exit 0
        else
          echo "❌ ROS2 node FAILED — no topics found"
          kill $$NODE_PID 2>/dev/null
          exit 1
        fi
    profiles:
      - ros2-test
```

#### 9.2 Run the Smoke Test

```bash
# Build and run the ROS2 test (one-shot, exits when done)
docker compose --profile ros2-test run --rm anima_{module}_ros2_test
```

This:
1. Builds `Dockerfile.ros2` (msgs + node)
2. Starts the node with `demo` backend (no weights needed)
3. Checks node is discoverable via `ros2 node list`
4. Checks topics exist via `ros2 topic list`
5. Checks status is publishing via `ros2 topic echo`
6. Checks services exist via `ros2 service list`
7. Prints pass/fail summary
8. Exits and removes the container

**Any agent running `/ros2-node` can verify the result by running this single command.** No local ROS2, no manual setup.

#### 9.3 Update /{module}-run Skill

If the module's `/{module}-run` skill exists (from `/test-mvp-production` Phase 8.5), add the ROS2 test mode:

```markdown
### ROS2 Test Mode
\```bash
cd {FULL_MODULE_PATH}
# One-command ROS2 verification (no local ROS2 needed)
docker compose --profile ros2-test run --rm anima_{module}_ros2_test
\```
```

#### 9.4 Validation Checklist

After the test runs, verify:
- [ ] `ros2 node list` shows `/{module}_node`
- [ ] `ros2 topic list` shows `/{module}/status` (minimum)
- [ ] `ros2 topic echo` receives at least one status message
- [ ] `ros2 service list` shows the module's services
- [ ] Exit code is 0

If ANY check fails, fix the node code and re-run.

---

### PHASE 10: POST-ROS2 — COMPLETE THE LOOP

After the ROS2 node is built, these steps close the integration loop. Do them in order.

#### 10.1 Bridge Fingerprint Update

The `anima-ros2-bridge` at `/Users/ilessio/Development/AIFLOWLABS/projects/anima-ros2-bridge/` auto-discovers modules by scanning DDS topics. Two things need updating:

**A) Module Recommendations** (`anima_bridge/discovery/fingerprint.py` line ~157):

The `_MODULE_RECOMMENDATIONS` dict maps sensor types to recommended modules. If this module provides a NEW capability, add it:

```python
# Example: Adding CHRONOS depth recommendation
_MODULE_RECOMMENDATIONS: dict[SensorType, list[str]] = {
    SensorType.RGB_CAMERA: ["AZOTH (detection)", "MONAD (segmentation)", ...],
    SensorType.DEPTH_CAMERA: ["CHRONOS (depth)", ...],
    # Add new module here if it serves a sensor type
}
```

**B) ANIMA Module Topic Detection** — The bridge's scanner currently detects HARDWARE topics (cameras, LiDARs, IMUs). It needs to also detect ANIMA MODULE topics. Check if `scanner.py` recognizes `/{module}/status` and `/{module}/*` patterns. If not, this is a bridge enhancement to propose.

The bridge's `AnimaCapabilities.msg` already has `module_names[]` and `module_statuses[]` fields — these should be populated when ANIMA modules are discovered alongside hardware.

**C) If the bridge repo is not at the expected path**, note as pending:
```
PENDING: Bridge fingerprint update for {MODULE_NAME}
  File: anima-ros2-bridge/anima_bridge/discovery/fingerprint.py
  Add: {MODULE_UPPER} to _MODULE_RECOMMENDATIONS for {sensor_types}
  Add: /{module}/* topic patterns to module detection
```

#### 10.2 MCP Tool Mapping

Each ROS2 service becomes an MCP tool that Claude can call through the bridge. The bridge handles this automatically IF the fingerprint is registered. Verify:

```
anima-bridge topics              # Should show /{module}/* topics
anima-bridge modules             # Should list the module as discovered
```

The chain: **Module ROS2 node → DDS topics → Bridge auto-discovers → MCP tools → Claude controls everything**

#### 10.3 End-to-End Validation

```bash
# Start the ROS2 node
docker compose --profile ros2 up anima_{module}_ros2 -d

# Verify topics exist
ros2 topic list | rg {module}
# Expected: /{module}/status, /{module}/{output}

# Verify status publishing
ros2 topic echo /{module}/status --once
# Expected: backend, device, ready=true, fps

# Verify services
ros2 service list | rg {module}
# Expected: /{module}/{service_name}

# Call a service
ros2 service call /{module}/{service} {module}_msgs/srv/{Service} "{request_yaml}"

# Clean up
docker compose --profile ros2 down
```

#### 10.4 Gazebo Integration (if applicable)

If the module processes camera data, test with the shared simulation:

```bash
# Start Gazebo sim (provides /camera/image_raw)
cd /Users/ilessio/Development/AIFLOWLABS/R&D/ROS2_GAZEBO
docker compose up -d

# Start module (subscribes to /camera/image_raw)
cd /Users/ilessio/Development/AIFLOWLABS/R&D/{module_dir}
docker compose --profile ros2 up anima_{module}_ros2 -d

# Verify it's processing frames
ros2 topic hz /{module}/{output}
# Expected: ~30 Hz (or whatever the module's target fps is)
```

---

### PHASE 11: TEMPLATE EXTRACTION (after 2+ modules done)

Once MONAD + one more module (e.g., AZOTH) share the pattern, extract a template:

```bash
# The cookiecutter/copier template structure:
anima-ros2-template/
├── {{module}}_msgs/
│   ├── package.xml.j2
│   ├── CMakeLists.txt.j2
│   ├── msg/{{Module}}Status.msg
│   └── srv/  # populated per module
├── {{module}}_node/
│   ├── package.xml.j2
│   ├── setup.py.j2
│   ├── {{module}}_node/node.py.j2
│   ├── {{module}}_node/conversions.py
│   ├── {{module}}_node/qos.py        # IDENTICAL across all modules
│   └── launch/{{module}}.launch.py.j2
├── Dockerfile.ros2.j2
└── copier.yml                          # Questions: module name, outputs, services
```

This means new modules get ROS2 scaffolded in **seconds**, not hours. The `/ros2-node` skill will use this template once it exists.

---

### MODULE-SPECIFIC REFERENCE: AZOTH (Next After MONAD)

AZOTH (01-LLMDet) does open-vocabulary object detection. Here's the expected ROS2 mapping:

```
AZOTH ROS2 Profile:
  Engine: src/azoth/engine.py (or similar detection engine)

  Topics:
    /azoth/detections  → vision_msgs/Detection2DArray (BEST_EFFORT, depth=1)
    /azoth/status      → azoth_msgs/MonadStatus (RELIABLE, TRANSIENT_LOCAL)

  Services:
    /azoth/detect      → sensor_msgs/Image + string[] vocabulary → vision_msgs/Detection2DArray
    /azoth/set_vocab   → string[] vocabulary → bool success

  Parameters:
    - camera_topic (default: /camera/image_raw)
    - backend (demo/tensorrt/onnx/mlx)
    - device (cpu/cuda/mps)
    - model_id (default: iSEE-Laboratory/llmdet_tiny)
    - vocabulary (string array — the objects to detect)
    - confidence_threshold (float, default: 0.5)

  Key difference from MONAD:
    - Uses vision_msgs/Detection2DArray (STANDARD — no custom msg needed for output)
    - Still needs azoth_msgs/ for custom services and status
    - Vocabulary is a parameter, not per-request (can be changed via service)
    - Continuous mode: subscribes to camera, publishes detections every frame
```

**AZOTH is the ideal second module** because:
1. It uses a STANDARD output type (`vision_msgs/Detection2DArray`) — proves we prefer standards
2. It's the most upstream module (camera → AZOTH → everything else subscribes)
3. It's already production-ready (8 production modules, AZOTH is #1)

---

---

## Reference Codebases (ALWAYS check these)

### 1. MONAD — The Reference Module
**Path**: `/Users/ilessio/Development/AIFLOWLABS/projects/project_monad/` (moved from R&D after MVP validation)
- `monad_msgs/` — custom message/service definitions (ament_cmake)
- `monad_node/monad_node/node.py` — MonadNode wrapping SegmentationEngine (286 lines)
- `monad_node/monad_node/conversions.py` — Image/mask conversion (132 lines, pure numpy)
- `monad_node/monad_node/qos.py` — QoS profiles (33 lines)
- `monad_node/launch/monad.launch.py` — launch file with configurable params
- `Dockerfile.ros2` — multi-stage build (57 lines)
- `tests/test_ros2_conversions.py` — 12 tests, no rclpy needed

### 2. ANIMA ROS2 Bridge — The Discovery & Integration Layer
**Path**: `/Users/ilessio/Development/AIFLOWLABS/projects/anima-ros2-bridge/`

This is the GLUE between modules and the AI agent. Every module must be discoverable by the bridge.

Key files to study:
- `anima_bridge/discovery/fingerprint.py` — Robot fingerprinting engine. When adding a module, its topic patterns must be recognizable here. The bridge auto-detects sensors, controls, and recommends ANIMA modules based on DDS graph analysis.
- `anima_bridge/discovery/scanner.py` — `CapabilityScanner` that monitors topic health (healthy/degraded/stale/dead), measures Hz, detects changes, and auto-generates `hardware_manifest.yaml`.
- `anima_msgs/msg/AnimaCapabilities.msg` — The RUNTIME manifest. Advertises: topic_names, topic_types, topic_hz, service_names, module_names, module_statuses, pipeline_fps, gpu_vram, safety_violations. This is the live truth that the compiler reads.
- `anima_msgs/srv/GetCapabilities.srv` — On-demand capability query.
- `anima_bridge/tools/` — MCP tools that Claude calls. Each module's ROS2 services become MCP tools through the bridge.
- `anima_bridge/safety/` — Safety validation layer.

**When building a new module's ROS2 node, you MUST also**:
1. Check `fingerprint.py` `_SENSOR_PATTERNS` and `_MODULE_RECOMMENDATIONS` — does the bridge know about this module?
2. Add module topic patterns to `fingerprint.py` if missing
3. Ensure the module publishes a `/{module}/status` topic that the scanner can monitor
4. Verify the module appears in `AnimaCapabilities.msg` when running

### 3. ANIMA Discovery Node
**Path**: `/Users/ilessio/Development/AIFLOWLABS/projects/anima-ros2-bridge/anima_discovery/`
- `discovery_node.py` — The ROS2 node that runs DDS discovery
- `package.xml` — ROS2 package for the discovery system

---

## Important Rules

1. **MONAD is the reference module** — when in doubt, look at `projects/project_monad/monad_node/` and `02-IST-ROS/monad_msgs/`
2. **Bridge is the reference integration** — check `anima-ros2-bridge/anima_bridge/discovery/` for how modules get discovered
3. **Never break existing tests** — the ROS2 layer is purely additive
4. **Standard message types first** — only create custom msgs when nothing standard fits
5. **No cv_bridge** — pure numpy conversions only
6. **Engine wrapping, not API wrapping** — the node calls the Python engine directly
7. **Lazy subscriptions** — don't subscribe to camera until continuous mode is requested
8. **CycloneDDS** — always set `RMW_IMPLEMENTATION=rmw_cyclonedds_cpp`
9. **Host networking** — always `network_mode: host` for DDS discovery
10. **Jazzy** — base image is always `ros:jazzy-ros-base`
11. **Profile isolation** — ROS2 service goes under `profiles: [ros2]`, never breaks default
12. **Manifest v2 (D-035)** — `anima_module.yaml` only contains what ROS2 CAN'T express (hardware, performance, safety, capabilities, provenance). Interfaces, params, and wiring are ROS2-native.
