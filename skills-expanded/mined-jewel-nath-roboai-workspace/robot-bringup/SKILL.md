---
name: robot-bringup
description: >
  Bring up a complete ROS2 robot stack on the onboard computer: systemd services, layered launch
  files, ordered startup, udev rules, watchdog, and production monitoring. Use when configuring
  robot startup on boot, systemd for ROS2, launch composition, udev for cameras/serial, or debugging
  boot-time failures.
category: devops
tags: [ros2, systemd, launch, udev, bringup, production]
version: "1.0.0"
---

# Robot Bringup

This skill covers bringing up a full ROS2-based robot stack on the onboard computer: systemd services, layered launch files, udev rules for deterministic device naming, ordered startup with health checks, and production monitoring. For a first power-on checklist see [guides/robot-bringup.md](../../guides/robot-bringup.md).

## When to Use

- Configuring the robot to start its full ROS2 stack on boot via systemd
- Writing systemd unit files that source ROS2 workspaces and set DDS environment
- Composing layered launch files (hardware, drivers, perception, application) into one bringup
- Setting up ordered startup with health checks to avoid race conditions
- Writing udev rules for deterministic device naming (cameras, LiDARs, serial)
- Configuring CycloneDDS or FastDDS for multi-machine ROS2 discovery
- Implementing watchdog and heartbeat monitoring for production
- Setting up log rotation and graceful shutdown for long-running deployments
- Debugging boot-time failures, service ordering, or device enumeration races

## Quick Start

```bash
# 1. Create environment file (systemd does not load .bashrc)
sudo mkdir -p /etc/robot
echo 'ROS_DISTRO=humble
RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
ROS_DOMAIN_ID=0' | sudo tee /etc/robot/ros2.env

# 2. Create systemd service
sudo tee /etc/systemd/system/robot-bringup.service << 'EOF'
[Unit]
Description=Robot ROS2 Bringup
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=robot
Group=robot
EnvironmentFile=/etc/robot/ros2.env
ExecStart=/bin/bash -c 'source /opt/ros/${ROS_DISTRO}/setup.bash && source /home/robot/ros2_ws/install/setup.bash && exec ros2 launch my_robot_bringup bringup.launch.py'
Restart=on-failure
RestartSec=5
KillSignal=SIGINT
TimeoutStopSec=30

[Install]
WantedBy=multi-user.target
EOF

# 3. Enable and start
sudo systemctl daemon-reload
sudo systemctl enable robot-bringup.service
sudo systemctl start robot-bringup.service
sudo systemctl status robot-bringup.service
```

## Core Concepts

### The Robot Bringup Stack

Startup flows from hardware through drivers, perception, and application. Each layer depends on the one below.

```
┌─────────────────────────────────────────────────────────────────────┐
│                        APPLICATION LAYER                             │
│  Navigation, manipulation, mission planning                          │
├─────────────────────────────────────────────────────────────────────┤
│                        PERCEPTION LAYER                              │
│  SLAM, detection, sensor fusion                                     │
├─────────────────────────────────────────────────────────────────────┤
│                         DRIVER LAYER                                 │
│  Camera, LiDAR, IMU, motor drivers                                  │
├─────────────────────────────────────────────────────────────────────┤
│                        HARDWARE LAYER                                │
│  udev rules, device enumeration, firmware check                     │
├─────────────────────────────────────────────────────────────────────┤
│                      ROS2 ENVIRONMENT                               │
│  Source workspace, RMW, ROS_DOMAIN_ID, DDS config                  │
├─────────────────────────────────────────────────────────────────────┤
│                    SYSTEMD TARGETS & SERVICES                       │
│  network-online.target → robot-bringup.target                       │
└─────────────────────────────────────────────────────────────────────┘
```

### Launch Layer Architecture

Organize launch files to mirror the stack so each layer can be tested in isolation.

```
bringup.launch.py
├── hardware.launch.py     (udev checks, device readiness)
├── drivers.launch.py      (camera, LiDAR, IMU, motors)
├── perception.launch.py   (SLAM, detection)
└── application.launch.py (navigation, mission)
```

## Common Patterns

### systemd Service Unit with Watchdog

Place in `/etc/systemd/system/`. Use `EnvironmentFile` for ROS2; do not rely on `.bashrc`.

```ini
[Unit]
Description=Robot ROS2 Bringup Stack
After=network-online.target robot-hw.target
Wants=network-online.target
Requires=robot-hw.target

[Service]
Type=notify
User=robot
Group=robot
WorkingDirectory=/home/robot
EnvironmentFile=/etc/robot/ros2.env

ExecStartPre=/usr/local/bin/robot-device-check.sh
ExecStart=/bin/bash -c '\
  source /opt/ros/${ROS_DISTRO}/setup.bash && \
  source /home/robot/ros2_ws/install/setup.bash && \
  exec ros2 launch my_robot_bringup bringup.launch.py'

ExecStop=/bin/kill -INT $MAINPID
TimeoutStopSec=30
Restart=on-failure
RestartSec=5
StartLimitIntervalSec=120
StartLimitBurst=5
WatchdogSec=30
KillMode=mixed
KillSignal=SIGINT
StandardOutput=journal
SyslogIdentifier=robot-bringup

[Install]
WantedBy=multi-user.target
```

### ROS2 Environment File

Store in `/etc/robot/ros2.env` and load via `EnvironmentFile` in the unit.

```bash
ROS_DISTRO=humble
RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
ROS_DOMAIN_ID=42
CYCLONEDDS_URI=file:///etc/robot/cyclonedds.xml
ROS_LOCALHOST_ONLY=0
ROS_LOG_DIR=/var/log/ros2
RCUTILS_LOGGING_USE_STDOUT=0
ROBOT_NAME=my_robot_01
```

### Layered systemd Services

Split drivers, perception, and application into separate services with explicit ordering.

```ini
# robot-drivers.service
[Unit]
After=network-online.target robot-hw.target
Requires=robot-hw.target
[Install]
WantedBy=robot-bringup.target

# robot-perception.service
[Unit]
After=robot-drivers.service
Requires=robot-drivers.service
[Install]
WantedBy=robot-bringup.target

# robot-application.service
[Unit]
After=robot-perception.service
Requires=robot-perception.service
[Install]
WantedBy=robot-bringup.target
```

### udev Rules for Cameras

Stable symlinks so `/dev/video0` is not used directly. Find attributes with `udevadm info --name=/dev/video0 --attribute-walk`.

```bash
# /etc/udev/rules.d/99-robot-cameras.rules
SUBSYSTEM=="video4linux", ATTRS{idVendor}=="1234", ATTRS{idProduct}=="5678", \
  KERNELS=="1-1.2:1.0", ATTR{index}=="0", \
  SYMLINK+="robot/camera_front", MODE="0666", GROUP="video"
```

### udev Rules for Serial Devices

Stable names for IMU, LiDAR, motor controller (e.g. `/dev/robot/imu`, `/dev/robot/lidar`).

```bash
# /etc/udev/rules.d/99-robot-serial.rules
SUBSYSTEM=="tty", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6001", \
  ATTRS{serial}=="AB0CDEFG", \
  SYMLINK+="robot/imu", MODE="0666", GROUP="dialout"

SUBSYSTEM=="tty", ATTRS{idVendor}=="10c4", ATTRS{idProduct}=="ea60", \
  ATTRS{serial}=="0001", SYMLINK+="robot/lidar", MODE="0666", GROUP="dialout"
```

Reload: `sudo udevadm control --reload-rules && sudo udevadm trigger`.

### Health Check Script (ExecStartPre)

Block driver startup until devices exist.

```bash
#!/bin/bash
# /usr/local/bin/robot-device-check.sh
set -euo pipefail
REQUIRED_DEVICES=("/dev/robot/camera_front" "/dev/robot/lidar" "/dev/robot/imu")
TIMEOUT=30
for device in "${REQUIRED_DEVICES[@]}"; do
  elapsed=0
  while [ ! -e "$device" ]; do
    [ "$elapsed" -ge "$TIMEOUT" ] && { echo "Missing $device"; exit 1; }
    sleep 1; elapsed=$((elapsed+1))
  done
done
exit 0
```

### DDS Peers for Multi-Machine

In CycloneDDS XML, list peers explicitly when multicast is unavailable.

```xml
<CycloneDDS>
  <Domain>
    <Discovery>
      <Peers>
        <Peer address="10.0.0.10"/>
        <Peer address="10.0.0.20"/>
      </Peers>
    </Discovery>
  </Domain>
</CycloneDDS>
```

## Anti-Patterns

### Sourcing setup.bash only in .bashrc

systemd does not load `.bashrc`. Service will not see ROS2. Use `EnvironmentFile` and source in `ExecStart`: `source /opt/ros/${ROS_DISTRO}/setup.bash && ...`.

### No startup ordering

All nodes start in parallel; navigation may call a service not yet advertised. Use `After=` and `Requires=` between systemd units (drivers → perception → application).

### Restart=always without rate limiting

Broken service restarts in a tight loop. Use `Restart=on-failure`, `RestartSec=5`, `StartLimitIntervalSec=120`, `StartLimitBurst=5`.

### Using network.target instead of network-online.target

`network.target` does not guarantee connectivity. Use `After=network-online.target` and `Wants=network-online.target`.

### No log rotation

Logs and journal fill the disk. Configure logrotate for `$ROS_LOG_DIR` and set journald `SystemMaxUse=1G` in `/etc/systemd/journald.conf`.

### Hardcoded device paths (/dev/ttyUSB0)

Enumeration order changes on reboot. Use udev rules and stable symlinks (e.g. `/dev/robot/imu`) in node parameters.

### Running the stack as root

Security and permission issues. Create a `robot` user, set `User=robot` and `Group=robot`, and grant device access via udev `GROUP` and `MODE`.

### No graceful shutdown

On stop, actuators keep last commanded velocity. In nodes that command motors, register shutdown handlers to command zero velocity and engage brakes before exit.

## Configuration Reference

| Parameter / setting | Type | Default | Description |
|---------------------|------|---------|-------------|
| ROS_DISTRO | env | - | humble, iron, jazzy |
| RMW_IMPLEMENTATION | env | rmw_fastrps_cpp | rmw_cyclonedds_cpp recommended |
| ROS_DOMAIN_ID | env | 0 | 0–101 for isolation |
| CYCLONEDDS_URI | env | - | Path to CycloneDDS XML |
| WatchdogSec | systemd | - | Interval for sd_notify(WATCHDOG=1) |
| RestartSec | systemd | 5 | Delay before restart |
| StartLimitBurst | systemd | 5 | Max restarts in StartLimitIntervalSec |
| StartLimitIntervalSec | systemd | 120 | Window for rate limit |

## Troubleshooting

| Symptom | Cause | Solution |
|---------|-------|----------|
| "command not found" for ros2 | Environment not loaded in systemd | Use EnvironmentFile and source in ExecStart |
| Nodes start then crash repeatedly | Missing device or config | Add ExecStartPre health check; check journal with `journalctl -u robot-bringup -f` |
| Topics not visible on another machine | DDS discovery | Set ROS_DOMAIN_ID same on both; use CycloneDDS peer list |
| /dev/ttyUSB0 wrong device after reboot | Enumeration order | Add udev rules and use stable symlinks in params |
| Service never reaches "active" | Dependency not ready | Use network-online.target; add After= for driver service |
| Disk full after days | Unbounded logs | Configure logrotate and journald SystemMaxUse |
| Robot keeps moving on shutdown | No safe state on SIGINT | Implement shutdown handler (zero velocity, brakes) in actuator nodes |

## Workflow Integration

- After hardware is wired and udev rules are in place, use this skill to define systemd and launch layers; see [guides/hardware-integration.md](../../guides/hardware-integration.md) for wiring to first topic.
- Use [guides/robot-bringup.md](../../guides/robot-bringup.md) for the first power-on and verification steps.
- For navigation and perception config, use `nav2` and `sensor-fusion-slam` skills; for security and hardening before deployment use `safety-systems`.

---

## Core Concepts — Working Code

### Concept 1: systemd Service for ROS 2 Nodes (Type=simple)

The minimum viable unit that correctly sources the ROS 2 workspace and survives crashes.

```ini
# /etc/systemd/system/robot-hardware.service
[Unit]
Description=OrbiBot Hardware Node (motor driver + IMU)
Documentation=https://github.com/your-org/orbibot
After=network.target
# Device must exist before this service starts
ConditionPathExists=/dev/motordriver

[Service]
Type=simple
User=robot
Group=robot

# --- Environment (never rely on .bashrc) ---
EnvironmentFile=/etc/robot/ros2.env

# --- Executable ---
ExecStart=/bin/bash -lc '\
  source /opt/ros/${ROS_DISTRO}/setup.bash && \
  source /home/robot/ros2_ws/install/setup.bash && \
  exec ros2 run orbibot_hardware hardware_node'

# --- Shutdown: send SIGINT (graceful) then SIGKILL after timeout ---
KillSignal=SIGINT
KillMode=mixed
TimeoutStopSec=15

# --- Restart policy ---
Restart=on-failure
RestartSec=5
StartLimitIntervalSec=120
StartLimitBurst=5

# --- Logging ---
StandardOutput=journal
StandardError=journal
SyslogIdentifier=robot-hardware

[Install]
WantedBy=multi-user.target
```

Key points:
- `Type=simple` — systemd considers the service started once `ExecStart` forks; no readiness notification required.
- `After=network.target` — only requires the network stack to be up, not a full connection (use `network-online.target` only if the node dials remote hosts at startup).
- `ConditionPathExists` — prevents the service from starting if the device symlink is absent, avoiding a restart loop.
- `KillSignal=SIGINT` — ROS 2 nodes shut down cleanly on SIGINT (same as Ctrl-C); SIGTERM skips the rclpy shutdown hook.

### Concept 2: Layered Launch File Composition

Each layer is a separate `.launch.py` that is included by the next. The top-level `bringup.launch.py` composes all layers.

```python
# my_robot_bringup/launch/bringup.launch.py
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    use_sim_time = DeclareLaunchArgument(
        'use_sim_time', default_value='false',
        description='Use /clock topic for simulation'
    )

    pkg_bringup = FindPackageShare('my_robot_bringup')

    # Layer 1 — hardware (serial bridge, IMU publisher)
    hardware = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([pkg_bringup, 'launch', 'hardware.launch.py'])
        ]),
        launch_arguments={'use_sim_time': LaunchConfiguration('use_sim_time')}.items()
    )

    # Layer 2 — sensors (LiDAR, camera)
    sensors = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([pkg_bringup, 'launch', 'sensors.launch.py'])
        ]),
        launch_arguments={'use_sim_time': LaunchConfiguration('use_sim_time')}.items()
    )

    # Layer 3 — localization (EKF, Madgwick)
    localization = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([pkg_bringup, 'launch', 'localization.launch.py'])
        ]),
        launch_arguments={'use_sim_time': LaunchConfiguration('use_sim_time')}.items()
    )

    # Layer 4 — navigation (Nav2, costmaps)
    navigation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([pkg_bringup, 'launch', 'navigation.launch.py'])
        ]),
        launch_arguments={'use_sim_time': LaunchConfiguration('use_sim_time')}.items()
    )

    return LaunchDescription([
        use_sim_time,
        hardware,
        sensors,
        localization,
        navigation,
    ])
```

The individual layer files (`hardware.launch.py`, `sensors.launch.py`, …) each declare their own nodes and load their own parameter files. This means:
- You can test just `hardware.launch.py` without starting Nav2.
- Each layer's parameters live in `config/<layer>_params.yaml`.
- CI can launch only the layers that have hardware simulators available.

### Concept 3: udev Rules for Persistent Device Naming

Find USB attributes with `udevadm info --name=/dev/ttyUSB0 --attribute-walk | grep -E 'idVendor|idProduct|serial'`.

```bash
# /etc/udev/rules.d/99-orbibot.rules
#
# Identify by vendor:product + serial number so the symlink survives
# hot-plug, hub changes, and reboots.
#
# RPLidar A1 (CP210x bridge, serial "0001")
SUBSYSTEM=="tty", \
  ATTRS{idVendor}=="10c4", ATTRS{idProduct}=="ea60", \
  ATTRS{serial}=="0001", \
  SYMLINK+="lidar", MODE="0666", GROUP="dialout"

# Yahboom ROSMaster V3.0 (CH340 bridge, serial "ABCD1234")
SUBSYSTEM=="tty", \
  ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", \
  ATTRS{serial}=="ABCD1234", \
  SYMLINK+="motordriver", MODE="0666", GROUP="dialout"

# RealSense D435 — give the video nodes a stable group
SUBSYSTEM=="usb", \
  ATTRS{idVendor}=="8086", ATTRS{idProduct}=="0b07", \
  MODE="0664", GROUP="video"
```

After editing, apply immediately:

```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
ls -la /dev/lidar /dev/motordriver   # verify symlinks exist
```

Reference the stable path in YAML parameters:

```yaml
# orbibot_hardware/config/hardware_params.yaml
hardware_node:
  ros__parameters:
    serial_port: /dev/motordriver   # stable udev symlink, not /dev/ttyUSB0
    baud_rate: 115200
```

### Concept 4: Ordered Startup with Dependency Checking

Use `RegisterEventHandler(OnProcessStart)` to gate a node on a prerequisite publishing its first message, or use a readiness topic.

```python
# my_robot_bringup/launch/hardware.launch.py
import launch
from launch import LaunchDescription
from launch.actions import RegisterEventHandler, TimerAction, LogInfo
from launch.event_handlers import OnProcessStart
from launch_ros.actions import Node


def generate_launch_description():
    hardware_node = Node(
        package='orbibot_hardware',
        executable='hardware_node',
        name='hardware_node',
        output='screen',
    )

    # Start the robot_state_publisher only after hardware_node is running.
    # For strict readiness (topic-based), replace with a lifecycle event.
    rsp_delayed = TimerAction(
        period=2.0,   # give hardware_node 2 s to advertise topics
        actions=[
            Node(
                package='robot_state_publisher',
                executable='robot_state_publisher',
                name='robot_state_publisher',
                output='screen',
            )
        ]
    )

    log_hw_started = RegisterEventHandler(
        OnProcessStart(
            target_action=hardware_node,
            on_start=[LogInfo(msg='hardware_node started — launching RSP')]
        )
    )

    return LaunchDescription([
        hardware_node,
        log_hw_started,
        rsp_delayed,
    ])
```

For production use `OnProcessExit` or lifecycle transitions instead of a fixed delay.

### Concept 5: Graceful Shutdown — SIGINT Handler in Python Nodes

ROS 2 Python nodes must handle SIGINT to zero actuators before exit.

```python
# orbibot_hardware/orbibot_hardware/hardware_node.py
import signal
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class HardwareNode(Node):
    def __init__(self):
        super().__init__('hardware_node')
        self._cmd_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self._driver = None  # replace with real driver handle
        self.get_logger().info('HardwareNode ready')

    def shutdown(self) -> None:
        """Send zero velocity and close the serial port on exit."""
        self.get_logger().info('Shutdown requested — zeroing velocities')
        stop = Twist()
        self._cmd_pub.publish(stop)
        if self._driver is not None:
            self._driver.stop()
            self._driver.close()
        self.destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = HardwareNode()

    # Register handler so systemd SIGINT (KillSignal=SIGINT) triggers cleanup
    def _sigint_handler(signum, frame):
        node.shutdown()
        rclpy.shutdown()

    signal.signal(signal.SIGINT, _sigint_handler)
    signal.signal(signal.SIGTERM, _sigint_handler)  # also handle SIGTERM

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.shutdown()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
```

### Concept 6: Watchdog — systemd Watchdog + Application Heartbeat

`Type=notify` lets the service report readiness and feed the systemd watchdog.

```python
# Extend HardwareNode to use sd_notify watchdog
import os
import socket
import threading
import time


class WatchdogMixin:
    """
    Feeds the systemd watchdog via sd_notify socket.
    Call start_watchdog() after node init; the background thread
    sends WATCHDOG=1 at half the WatchdogSec interval.
    """

    def start_watchdog(self, interval_sec: float = 10.0) -> None:
        self._watchdog_interval = interval_sec
        self._watchdog_running = True
        self._watchdog_thread = threading.Thread(
            target=self._watchdog_loop, daemon=True
        )
        self._watchdog_thread.start()
        self._sd_notify('READY=1')

    def stop_watchdog(self) -> None:
        self._watchdog_running = False

    def _watchdog_loop(self) -> None:
        while self._watchdog_running:
            self._sd_notify('WATCHDOG=1')
            time.sleep(self._watchdog_interval / 2)

    @staticmethod
    def _sd_notify(state: str) -> None:
        notify_socket = os.environ.get('NOTIFY_SOCKET')
        if not notify_socket:
            return
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        try:
            sock.connect(notify_socket)
            sock.sendall(state.encode())
        finally:
            sock.close()


class HardwareNodeWithWatchdog(WatchdogMixin, HardwareNode):
    def __init__(self):
        super().__init__()
        # WatchdogSec=30 in unit file → send keepalive every 15 s
        self.start_watchdog(interval_sec=15.0)
```

Matching unit file excerpt:

```ini
[Service]
Type=notify
NotifyAccess=main
WatchdogSec=30
# If no WATCHDOG=1 received in 30 s, systemd kills and restarts the service
Restart=on-failure
```

---

## Common Patterns — Extended

### Pattern: Complete hardware.launch.py with Parameter File

```python
# my_robot_bringup/launch/hardware.launch.py
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    hw_pkg = get_package_share_directory('orbibot_hardware')
    hw_params = os.path.join(hw_pkg, 'config', 'hardware_params.yaml')

    use_sim_time = DeclareLaunchArgument(
        'use_sim_time', default_value='false'
    )

    hardware_node = Node(
        package='orbibot_hardware',
        executable='hardware_node',
        name='hardware_node',
        parameters=[
            hw_params,
            {'use_sim_time': LaunchConfiguration('use_sim_time')}
        ],
        output='screen',
        emulate_tty=True,
    )

    description_pkg = get_package_share_directory('orbibot_description')
    urdf_file = os.path.join(description_pkg, 'urdf', 'robot.urdf.xacro')

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[
            {'robot_description': open(urdf_file).read()},
            {'use_sim_time': LaunchConfiguration('use_sim_time')},
        ],
        output='screen',
    )

    return LaunchDescription([
        use_sim_time,
        hardware_node,
        robot_state_publisher,
    ])
```

### Pattern: Complete sensors.launch.py (LiDAR + Camera)

```python
# my_robot_bringup/launch/sensors.launch.py
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    sensors_pkg = get_package_share_directory('orbibot_sensors')

    use_sim_time = DeclareLaunchArgument(
        'use_sim_time', default_value='false'
    )

    rplidar = Node(
        package='rplidar_ros',
        executable='rplidar_composition',
        output='screen',
        parameters=[
            os.path.join(sensors_pkg, 'config', 'rplidar_params.yaml'),
            {'use_sim_time': LaunchConfiguration('use_sim_time')},
        ],
    )

    realsense = Node(
        package='realsense2_camera',
        executable='realsense2_camera_node',
        name='camera',
        output='screen',
        parameters=[
            os.path.join(sensors_pkg, 'config', 'realsense_params.yaml'),
            {'use_sim_time': LaunchConfiguration('use_sim_time')},
        ],
    )

    return LaunchDescription([
        use_sim_time,
        rplidar,
        realsense,
    ])
```

### Pattern: Production Journald + Logrotate Configuration

```ini
# /etc/systemd/journald.conf.d/robot.conf
# Keep 1 GB total, rotate when a single journal file exceeds 100 MB,
# compress after 1 day, discard after 7 days.
[Journal]
SystemMaxUse=1G
SystemKeepFree=500M
SystemMaxFileSize=100M
MaxRetentionSec=7day
Compress=yes
```

Apply: `sudo systemctl restart systemd-journald`

```
# /etc/logrotate.d/ros2-logs
/var/log/ros2/*.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    create 0640 robot robot
    sharedscripts
    postrotate
        systemctl kill --kill-who=main --signal=HUP robot-bringup.service 2>/dev/null || true
    endscript
}
```

### Pattern: Resource Limits in Service Unit

Protect the Raspberry Pi 5 from runaway nodes consuming all CPU or memory.

```ini
[Service]
# CPU quota: allow up to 300% of one core (3 cores worth)
CPUQuota=300%

# Memory hard limit: OOM-kill this unit before the kernel picks a victim
MemoryMax=1.5G
MemorySwapMax=256M

# Restrict to real-time scheduling ceiling (prevent PREEMPT starvation)
LimitRTPRIO=10

# Open file descriptors (ROS 2 DDS opens many sockets)
LimitNOFILE=65536
```

### Pattern: Checking Service Health from the Command Line

```bash
# Live status
sudo systemctl status robot-bringup.service

# Follow logs (most recent 100 lines, then live)
journalctl -u robot-bringup.service -n 100 -f

# Filter for errors only
journalctl -u robot-bringup.service -p err -f

# Show all robot services in one view
journalctl -u 'robot-*.service' -f

# List all robot units and their states
systemctl list-units 'robot-*.service'

# Check if watchdog deadline is being met
systemctl show robot-bringup.service --property=WatchdogTimestampMonotonic

# Restart a single layer without full reboot
sudo systemctl restart robot-hardware.service
```

---

## Anti-Patterns — With Code Examples

### Anti-Pattern 1: Giant Single Launch File

❌ **Wrong** — all nodes in one flat launch file, no layer separation:

```python
# bringup.launch.py  (DON'T DO THIS)
def generate_launch_description():
    return LaunchDescription([
        Node(package='orbibot_hardware', executable='hardware_node'),
        Node(package='rplidar_ros',      executable='rplidar_composition'),
        Node(package='realsense2_camera',executable='realsense2_camera_node'),
        Node(package='robot_localization',executable='ekf_node'),
        Node(package='slam_toolbox',     executable='async_slam_toolbox_node'),
        Node(package='nav2_bringup',     executable='bringup_launch'),
        # 20 more nodes...
    ])
```

✅ **Correct** — layer files included from top-level bringup:

```python
# bringup.launch.py
def generate_launch_description():
    pkg = FindPackageShare('my_robot_bringup')
    def layer(name):
        return IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                PathJoinSubstitution([pkg, 'launch', f'{name}.launch.py'])
            )
        )
    return LaunchDescription([
        layer('hardware'),
        layer('sensors'),
        layer('localization'),
        layer('navigation'),
    ])
```

### Anti-Pattern 2: No Restart Policy

❌ **Wrong** — service dies permanently on first crash:

```ini
[Service]
Type=simple
ExecStart=/bin/bash -c 'source ... && ros2 launch ...'
# No Restart= means the service stays dead after a crash
```

✅ **Correct** — recover automatically with rate limiting:

```ini
[Service]
Type=simple
ExecStart=/bin/bash -c 'source ... && ros2 launch ...'
Restart=on-failure
RestartSec=5
StartLimitIntervalSec=120
StartLimitBurst=5
# After 5 failed restarts in 120 s, systemd stops retrying and alerts
```

### Anti-Pattern 3: Hardcoded /dev/ttyUSB0

❌ **Wrong** — device path changes depending on plug-in order:

```yaml
# hardware_params.yaml
hardware_node:
  ros__parameters:
    serial_port: /dev/ttyUSB0   # breaks if another USB device is plugged in first
```

✅ **Correct** — use a udev symlink by vendor+serial:

```bash
# /etc/udev/rules.d/99-orbibot.rules
SUBSYSTEM=="tty", ATTRS{idVendor}=="1a86", ATTRS{idProduct}=="7523", \
  ATTRS{serial}=="ABCD1234", SYMLINK+="motordriver", MODE="0666", GROUP="dialout"
```

```yaml
# hardware_params.yaml
hardware_node:
  ros__parameters:
    serial_port: /dev/motordriver   # stable, survives reboots and hub changes
```

### Anti-Pattern 4: Ignoring Shutdown Signals

❌ **Wrong** — node exits abruptly, motors keep last speed:

```python
def main():
    rclpy.init()
    node = HardwareNode()
    rclpy.spin(node)   # on SIGINT, spin() raises KeyboardInterrupt and exits
    # no cleanup — serial port left open, motors still spinning
```

✅ **Correct** — zero velocity and close hardware on exit:

```python
def main():
    rclpy.init()
    node = HardwareNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.get_logger().info('Zeroing motors before exit')
        node.publish_zero_velocity()
        node.close_serial()
        node.destroy_node()
        rclpy.try_shutdown()
```

### Anti-Pattern 5: No Device Presence Check Before Drivers

❌ **Wrong** — driver starts and crashes repeatedly because device is not ready:

```ini
[Service]
ExecStart=/bin/bash -c 'source ... && ros2 run rplidar_ros rplidar_composition'
Restart=on-failure
RestartSec=1   # fast loop, spamming journal with errors
```

✅ **Correct** — block startup until device symlink exists:

```ini
[Service]
ExecStartPre=/usr/local/bin/wait-for-device.sh /dev/lidar 30
ExecStart=/bin/bash -c 'source ... && ros2 run rplidar_ros rplidar_composition'
Restart=on-failure
RestartSec=5
```

```bash
#!/bin/bash
# /usr/local/bin/wait-for-device.sh
# Usage: wait-for-device.sh <device_path> <timeout_seconds>
DEVICE=$1
TIMEOUT=${2:-30}
echo "Waiting for $DEVICE (timeout ${TIMEOUT}s)..."
for i in $(seq 1 "$TIMEOUT"); do
  [ -e "$DEVICE" ] && { echo "$DEVICE ready"; exit 0; }
  sleep 1
done
echo "ERROR: $DEVICE not found after ${TIMEOUT}s" >&2
exit 1
```

### Anti-Pattern 6: Sourcing .bashrc in ExecStart

❌ **Wrong** — systemd runs in a clean environment; `.bashrc` is never loaded:

```ini
[Service]
ExecStart=/bin/bash -c 'source ~/.bashrc && ros2 launch ...'
# Fails silently: ros2 not found, workspace not sourced
```

✅ **Correct** — source explicitly in ExecStart and use EnvironmentFile:

```ini
[Service]
EnvironmentFile=/etc/robot/ros2.env
ExecStart=/bin/bash -c '\
  source /opt/ros/${ROS_DISTRO}/setup.bash && \
  source /home/robot/ros2_ws/install/setup.bash && \
  exec ros2 launch my_robot_bringup bringup.launch.py'
```

---

## Configuration Reference — Extended

### systemd Unit Parameters

| Parameter | Type | Recommended value | Description |
|---|---|---|---|
| `Type` | string | `simple` (basic) or `notify` (watchdog) | `notify` requires `sd_notify(READY=1)` from the process |
| `User` / `Group` | string | `robot` | Never run as root |
| `EnvironmentFile` | path | `/etc/robot/ros2.env` | Loaded before ExecStart; no shell expansion |
| `ExecStartPre` | path | `/usr/local/bin/wait-for-device.sh` | Runs before ExecStart; non-zero exit blocks the service |
| `KillSignal` | signal | `SIGINT` | ROS 2 nodes clean up on SIGINT; SIGTERM skips rclpy shutdown |
| `KillMode` | string | `mixed` | Send KillSignal to main PID, SIGKILL to remaining group |
| `TimeoutStopSec` | seconds | `15` | Time allowed for graceful shutdown before SIGKILL |
| `Restart` | string | `on-failure` | Restart on non-zero exit or signal; not on `exit(0)` |
| `RestartSec` | seconds | `5` | Pause between restarts |
| `StartLimitBurst` | integer | `5` | Max restarts allowed within StartLimitIntervalSec |
| `StartLimitIntervalSec` | seconds | `120` | Window for restart rate limiting |
| `WatchdogSec` | seconds | `30` | Watchdog timeout; process must send `WATCHDOG=1` |
| `CPUQuota` | percent | `300%` | Max CPU across all cores (300% = 3 cores) |
| `MemoryMax` | bytes | `1.5G` | Hard memory ceiling; OOM-kills the unit |
| `LimitNOFILE` | integer | `65536` | Open file descriptor limit (DDS needs many sockets) |
| `StandardOutput` | string | `journal` | Route stdout to journald |
| `SyslogIdentifier` | string | `robot-bringup` | Tag for `journalctl -u` filtering |

### ROS 2 Environment Variables

| Variable | Default | Description |
|---|---|---|
| `ROS_DISTRO` | — | ROS 2 distribution name (`jazzy`, `humble`, …) |
| `RMW_IMPLEMENTATION` | `rmw_fastrtps_cpp` | Middleware; use `rmw_cyclonedds_cpp` for lower latency |
| `ROS_DOMAIN_ID` | `0` | 0–101; isolates DDS traffic; match across all hosts |
| `CYCLONEDDS_URI` | — | Absolute path to CycloneDDS XML config file |
| `ROS_LOCALHOST_ONLY` | `0` | Set to `1` to disable multicast and confine to loopback |
| `ROS_LOG_DIR` | `~/.ros/log` | Override log output directory |
| `RCUTILS_LOGGING_USE_STDOUT` | `0` | `1` = log to stdout; `0` = log to file |
| `RCUTILS_LOGGING_BUFFERED_STREAM` | `1` | `1` = buffered (faster); `0` = unbuffered (safer for crashes) |
| `ROBOT_NAME` | — | Optional; used by multi-robot namespacing |

### udev Rule Attributes

| Attribute | Example | Description |
|---|---|---|
| `SUBSYSTEM` | `tty`, `video4linux`, `usb` | Device subsystem to match |
| `ATTRS{idVendor}` | `10c4` | USB vendor ID (4 hex digits) |
| `ATTRS{idProduct}` | `ea60` | USB product ID (4 hex digits) |
| `ATTRS{serial}` | `0001` | USB serial string (unique per device) |
| `KERNELS` | `1-1.2:1.0` | Physical USB port path (position-based, fragile) |
| `SYMLINK+` | `lidar` | Creates `/dev/lidar` pointing to the real node |
| `MODE` | `0666` | File permission on the device node |
| `GROUP` | `dialout` | Group ownership (user must be in this group) |

---

## Troubleshooting — Extended

| Symptom | Cause | Solution |
|---|---|---|
| `ros2: command not found` in service | Environment not loaded | Use `EnvironmentFile=/etc/robot/ros2.env` and source in `ExecStart` |
| Node crashes on startup, restarts every 5 s | Device absent or permissions wrong | Add `ExecStartPre=wait-for-device.sh`; check `ls -la /dev/motordriver` |
| Topics not visible on laptop | DDS domain mismatch or firewall | Match `ROS_DOMAIN_ID` on all hosts; open UDP 7400-7500 in firewall |
| `/dev/ttyUSB0` maps to wrong device | USB enumeration order non-deterministic | Add udev rule with `ATTRS{serial}` and use stable `/dev/motordriver` |
| Service never becomes `active`, stuck in `activating` | `ExecStartPre` script hanging | Add timeout to device-check script; verify udev rule creates symlink |
| Disk full after long run | ROS 2 logs or journal unbounded | Set `SystemMaxUse=1G` in journald.conf; add `/etc/logrotate.d/ros2-logs` |
| Robot moves after shutdown command | No SIGINT handler in actuator node | Implement `finally` block that publishes zero `Twist` on exit |
| Service killed by OOM before watchdog fires | Memory limit too low for Nav2 + SLAM | Raise `MemoryMax`; disable costmap layers or reduce map resolution |
| Watchdog fires, service restarts mid-run | Node blocked in a long callback | Split blocking work into a thread; keep main rclpy spin loop unblocked |
| `StartLimitBurst` exceeded, service disabled | Repeated crashes in 120 s window | Fix root cause; then `systemctl reset-failed robot-bringup.service` and restart |
| `journalctl` shows no logs for robot service | `SyslogIdentifier` not set | Add `SyslogIdentifier=robot-bringup`; use `journalctl -u robot-bringup.service` |
| Launch file fails silently | Exception in `generate_launch_description()` | Run `ros2 launch --debug my_pkg bringup.launch.py` for full traceback |

---

## Workflow Integration — Extended

### Skill Cross-References

This skill sits at the intersection of several other skills. Use the following map to navigate:

| Task | Go to skill |
|---|---|
| Designing the individual ROS 2 nodes launched here | `ros2_node_creation` |
| Writing or composing the individual `.launch.py` files | `ros2_launch_config` |
| Adding `/diagnostics` publishers and health aggregators | `deployment-fleet` |
| Configuring functional safety (e-stop, watchdog timers) | `safety-systems` |
| Deploying to a fleet of robots | `deployment-fleet` |
| Securing DDS traffic and limiting node permissions | `safety-systems` |
| Packaging the full stack as a Docker image | `docker-ros2-ci` |

### Typical Bring-Up Workflow on Ubuntu 22.04 + ROS 2 Jazzy / Raspberry Pi 5

```bash
# Step 1 — install dependencies
sudo apt install ros-jazzy-rmw-cyclonedds-cpp ros-jazzy-robot-localization

# Step 2 — create robot user and add to device groups
sudo useradd -m -s /bin/bash robot
sudo usermod -aG dialout,video,input robot

# Step 3 — deploy udev rules
sudo cp config/99-orbibot.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules && sudo udevadm trigger
ls -la /dev/motordriver /dev/lidar

# Step 4 — deploy environment file
sudo mkdir -p /etc/robot
sudo cp config/ros2.env /etc/robot/ros2.env

# Step 5 — build workspace as robot user
sudo -u robot bash -c 'source /opt/ros/jazzy/setup.bash && \
  cd /home/robot/ros2_ws && colcon build --symlink-install'

# Step 6 — install systemd units
sudo cp systemd/*.service /etc/systemd/system/
sudo systemctl daemon-reload

# Step 7 — enable on boot
sudo systemctl enable robot-hardware.service
sudo systemctl enable robot-sensors.service
sudo systemctl enable robot-bringup.service

# Step 8 — start and verify
sudo systemctl start robot-bringup.service
sudo systemctl status robot-bringup.service
journalctl -u robot-bringup.service -f

# Step 9 — verify topics
source /opt/ros/jazzy/setup.bash
export ROS_DOMAIN_ID=42
ros2 topic list
ros2 topic hz /scan
ros2 topic hz /odom
```

### Integration with diagnostics aggregators

Add a `DiagnosticUpdater` to your hardware node so `robot_monitor` can surface systemd service health alongside ROS topic health:

```python
# In HardwareNode.__init__
from diagnostic_updater import Updater, DiagnosticStatusWrapper

self._updater = Updater(self)
self._updater.setHardwareID('orbibot-v1')
self._updater.add('Serial Link', self._check_serial_health)

def _check_serial_health(self, stat: DiagnosticStatusWrapper):
    if self._driver and self._driver.is_open:
        stat.summary(DiagnosticStatusWrapper.OK, 'Serial link up')
    else:
        stat.summary(DiagnosticStatusWrapper.ERROR, 'Serial link down')
    stat.add('port', '/dev/motordriver')
    stat.add('baud', '115200')
    return stat
```

See the `deployment-fleet` skill for central aggregation and monitoring across robots.

### Connecting to safety-systems

The watchdog pattern in Concept 6 feeds systemd's watchdog. For application-level safety (e-stop, velocity limits, liveliness checking), combine it with the `safety-systems` skill which covers:
- Software e-stop with latched state
- `/cmd_vel` supervision (zero on timeout)
- Liveliness QoS for critical publishers

The canonical integration point is a `SafetyMonitor` node that subscribes to `/diagnostics_agg` and publishes to `/emergency_stop` — launched in the hardware layer so it starts before any motion-capable node.
