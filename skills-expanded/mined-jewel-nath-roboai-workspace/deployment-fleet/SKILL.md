---
name: deployment-fleet
description: OTA firmware and software updates, fleet management for multiple robots, centralized logging, remote diagnostics, and production monitoring for deployed robot systems.
category: devops
tags: [deployment, fleet, ota, logging, monitoring, diagnostics, production, ci-cd, ansible]
version: "1.0.0"
---

# Deployment and Fleet Management

Managing multiple deployed robots requires disciplined OTA update pipelines, centralized observability, and reproducible configuration management. This skill covers the full lifecycle: CI/CD → image build → OTA push → health monitoring → rollback.

## When to Use

- Setting up OTA software updates for ROS2 workspaces on deployed robots
- Managing a fleet of 2+ robots with Ansible playbooks
- Aggregating `/diagnostics` and ROS2 logs to a central Grafana/Loki stack
- Building a CI/CD pipeline that produces tested Docker images for robots
- Implementing rollback triggers on failed health checks post-deployment
- Structuring per-robot configuration with fleet-wide defaults
- Setting up ROS2 bag rotation and remote log ingestion
- Hardening remote access (VPN, SSH keys, certificate rotation)
- Validating pre-deployment readiness before pushing to production

## Quick Start

```bash
# --- On the robot: bootstrap the update agent ---
sudo apt install ansible rsync python3-pip

# Install deployment tools on the control machine
pip install ansible paramiko

# Clone fleet playbooks
git clone https://github.com/your-org/robot-fleet-ops ~/fleet-ops
cd ~/fleet-ops

# Test connectivity to all robots
ansible all -i inventory/robots.ini -m ping

# Deploy latest workspace to all robots
ansible-playbook -i inventory/robots.ini playbooks/deploy_workspace.yml

# Check fleet status
ansible all -i inventory/robots.ini -m command -a "systemctl status orbibot"
```

**Minimal health check endpoint on the robot:**

```python
# health_server.py — lightweight HTTP health check for deployment validation
from http.server import HTTPServer, BaseHTTPRequestHandler
import subprocess
import json

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            status = self._check_health()
            code   = 200 if status['healthy'] else 503
            self.send_response(code)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(status).encode())

    def _check_health(self) -> dict:
        ok = subprocess.run(
            ['systemctl', 'is-active', '--quiet', 'orbibot'],
            capture_output=True
        ).returncode == 0
        return {'healthy': ok, 'service': 'active' if ok else 'failed'}

    def log_message(self, *args):
        pass  # Suppress access log

if __name__ == '__main__':
    HTTPServer(('0.0.0.0', 9090), HealthHandler).serve_forever()
```

## Core Concepts

### 1. OTA Update Strategy for ROS2 Workspaces

Two complementary approaches: rsync-based workspace sync (fast, incremental) and Docker image swap (atomic, rollback-safe).

**Approach A — rsync workspace sync (fast, ~seconds for small changes):**

```bash
#!/usr/bin/env bash
# scripts/deploy_workspace.sh — run on the control machine
set -euo pipefail

ROBOT_HOST="${1:?Usage: deploy_workspace.sh <robot_host>}"
ROBOT_USER="orbibot"
LOCAL_WS="$HOME/robot_ws/install"
REMOTE_WS="/home/orbibot/robot_ws/install"
BACKUP_DIR="/home/orbibot/robot_ws/install.bak"
HEALTH_URL="http://${ROBOT_HOST}:9090/health"

echo "==> Pre-deployment health check"
status=$(curl -sf "$HEALTH_URL" | python3 -c "import sys,json; d=json.load(sys.stdin); sys.exit(0 if d['healthy'] else 1)")
echo "    Robot is healthy, proceeding"

echo "==> Backing up current workspace on robot"
ssh "${ROBOT_USER}@${ROBOT_HOST}" "cp -a ${REMOTE_WS} ${BACKUP_DIR} || true"

echo "==> Syncing workspace"
rsync -avz --delete \
  --exclude='*.pyc' \
  --exclude='__pycache__' \
  "$LOCAL_WS/" \
  "${ROBOT_USER}@${ROBOT_HOST}:${REMOTE_WS}/"

echo "==> Restarting robot service"
ssh "${ROBOT_USER}@${ROBOT_HOST}" "sudo systemctl restart orbibot"

echo "==> Waiting for service to stabilize (15s)"
sleep 15

echo "==> Post-deployment health check"
curl -sf "$HEALTH_URL" | python3 -c \
  "import sys,json; d=json.load(sys.stdin); sys.exit(0 if d['healthy'] else 1)" || {
    echo "==> HEALTH CHECK FAILED — rolling back"
    ssh "${ROBOT_USER}@${ROBOT_HOST}" \
      "cp -a ${BACKUP_DIR} ${REMOTE_WS} && sudo systemctl restart orbibot"
    exit 1
  }

echo "==> Deployment successful"
```

**Approach B — Docker image swap (atomic, immutable):**

```bash
#!/usr/bin/env bash
# scripts/deploy_image.sh
set -euo pipefail

ROBOT_HOST="${1:?}"
IMAGE_TAG="${2:?Usage: deploy_image.sh <host> <image_tag>}"
REGISTRY="registry.your-org.com"
IMAGE="${REGISTRY}/orbibot:${IMAGE_TAG}"

echo "==> Pulling image on robot"
ssh "orbibot@${ROBOT_HOST}" "docker pull ${IMAGE}"

echo "==> Updating docker-compose tag"
ssh "orbibot@${ROBOT_HOST}" "
  sed -i 's|image: .*orbibot:.*|image: ${IMAGE}|' /home/orbibot/compose/docker-compose.yml
  docker compose -f /home/orbibot/compose/docker-compose.yml up -d --force-recreate
"

echo "==> Waiting for container health"
for i in $(seq 1 12); do
  status=$(ssh "orbibot@${ROBOT_HOST}" "docker inspect --format='{{.State.Health.Status}}' orbibot_main" 2>/dev/null || echo "starting")
  [ "$status" = "healthy" ] && { echo "==> Healthy after ${i}×5s"; break; }
  echo "    Status: $status (attempt $i/12)"
  sleep 5
  if [ "$i" = "12" ]; then
    echo "==> TIMEOUT — rolling back"
    ssh "orbibot@${ROBOT_HOST}" "docker compose -f /home/orbibot/compose/docker-compose.yml rollback || true"
    exit 1
  fi
done
```

### 2. Ansible Fleet Orchestration

```ini
# inventory/robots.ini
[fleet]
robot-alpha  ansible_host=192.168.1.101 robot_id=alpha  location=warehouse_a
robot-beta   ansible_host=192.168.1.102 robot_id=beta   location=warehouse_a
robot-gamma  ansible_host=192.168.1.103 robot_id=gamma  location=warehouse_b

[fleet:vars]
ansible_user=orbibot
ansible_python_interpreter=/usr/bin/python3
ros_distro=jazzy
workspace_path=/home/orbibot/robot_ws
```

```yaml
# playbooks/deploy_workspace.yml
---
- name: Deploy ROS2 workspace to fleet
  hosts: fleet
  serial: 1               # Rolling deploy: one robot at a time
  max_fail_percentage: 0  # Stop entire deploy if any robot fails

  vars:
    local_workspace: "{{ playbook_dir }}/../install"
    remote_workspace: "{{ workspace_path }}/install"
    backup_path: "{{ workspace_path }}/install.bak"
    health_port: 9090

  pre_tasks:
    - name: Pre-deployment health check
      uri:
        url: "http://{{ ansible_host }}:{{ health_port }}/health"
        method: GET
        status_code: 200
      register: health_result
      failed_when: not health_result.json.healthy

    - name: Backup current workspace
      command: "cp -a {{ remote_workspace }} {{ backup_path }}"
      ignore_errors: true

  tasks:
    - name: Sync install directory
      synchronize:
        src: "{{ local_workspace }}/"
        dest: "{{ remote_workspace }}/"
        delete: true
        rsync_opts:
          - "--exclude=*.pyc"
          - "--exclude=__pycache__"

    - name: Sync per-robot config
      template:
        src: "templates/robot_params.yaml.j2"
        dest: "/home/orbibot/config/robot_params.yaml"

    - name: Restart robot service
      systemd:
        name: orbibot
        state: restarted
      become: true

    - name: Wait for service to be active
      systemd:
        name: orbibot
      register: svc
      until: svc.status.ActiveState == 'active'
      retries: 10
      delay: 3
      become: true

  post_tasks:
    - name: Post-deployment health check
      uri:
        url: "http://{{ ansible_host }}:{{ health_port }}/health"
        method: GET
        status_code: 200
      register: post_health
      failed_when: not post_health.json.healthy

  rescue:
    - name: Rollback workspace on failure
      command: "cp -a {{ backup_path }} {{ remote_workspace }}"
      ignore_errors: true

    - name: Restart after rollback
      systemd:
        name: orbibot
        state: restarted
      become: true

    - name: Fail the play
      fail:
        msg: "Deployment failed on {{ inventory_hostname }}, rolled back"
```

```yaml
# playbooks/check_fleet.yml — quick status check across all robots
---
- name: Check fleet status
  hosts: fleet
  gather_facts: false
  tasks:
    - name: Check orbibot service
      systemd:
        name: orbibot
      register: svc
      become: true

    - name: Check disk space
      command: df -h /home/orbibot
      register: disk

    - name: Check CPU temperature
      command: cat /sys/class/thermal/thermal_zone0/temp
      register: temp
      ignore_errors: true

    - name: Report status
      debug:
        msg: |
          Robot: {{ inventory_hostname }}
          Service: {{ svc.status.ActiveState }}
          Disk: {{ disk.stdout_lines[-1] }}
          Temp: {{ (temp.stdout | int / 1000) | round(1) }}°C
```

```yaml
# templates/robot_params.yaml.j2 — per-robot config from Ansible variables
robot_id: "{{ robot_id }}"
location: "{{ location }}"

hardware:
  serial_port: /dev/motordriver
  baudrate: 921600

navigation:
  max_vel_x: 0.5
  max_vel_y: 0.5

logging:
  level: INFO
  remote_host: "{{ groups['monitoring'][0] }}"
  remote_port: 5140
```

### 3. Centralized Structured Logging

```python
# orbibot_bringup/logging_config.py
"""
Structured JSON logging for ROS2 nodes.
Writes to local file + streams to Loki via syslog.
"""
import logging
import logging.handlers
import json
import time
import os


class RobotJsonFormatter(logging.Formatter):
    """Formats log records as JSON for Loki ingestion."""

    def __init__(self, robot_id: str):
        super().__init__()
        self._robot_id = robot_id

    def format(self, record: logging.LogRecord) -> str:
        return json.dumps({
            'timestamp': time.time(),
            'robot_id':  self._robot_id,
            'level':     record.levelname,
            'logger':    record.name,
            'message':   record.getMessage(),
            'file':      f'{record.filename}:{record.lineno}',
        })


def configure_fleet_logging(robot_id: str,
                             log_dir: str = '/var/log/orbibot',
                             loki_host: str = 'monitoring.local',
                             loki_port: int = 5140) -> None:
    """Configure JSON logging to local file + remote syslog for Loki."""
    os.makedirs(log_dir, exist_ok=True)

    formatter = RobotJsonFormatter(robot_id)
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # Rotating local log: 10 MB × 5 files
    file_handler = logging.handlers.RotatingFileHandler(
        filename=f'{log_dir}/robot.log',
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
    )
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    # Remote syslog → Promtail → Loki
    syslog_handler = logging.handlers.SysLogHandler(
        address=(loki_host, loki_port)
    )
    syslog_handler.setFormatter(formatter)
    root_logger.addHandler(syslog_handler)
```

```yaml
# infrastructure/loki/loki-config.yaml
auth_enabled: false

server:
  http_listen_port: 3100

ingester:
  lifecycler:
    ring:
      kvstore:
        store: inmemory
      replication_factor: 1
  chunk_idle_period: 1h
  max_chunk_age: 1h

schema_config:
  configs:
    - from: 2024-01-01
      store: boltdb-shipper
      object_store: filesystem
      schema: v11
      index:
        prefix: loki_index_
        period: 24h

storage_config:
  boltdb_shipper:
    active_index_directory: /loki/index
    cache_location: /loki/cache
    shared_store: filesystem
  filesystem:
    directory: /loki/chunks
```

```yaml
# infrastructure/promtail/promtail-config.yaml
server:
  http_listen_port: 9080

clients:
  - url: http://loki:3100/loki/api/v1/push

scrape_configs:
  - job_name: robot_logs
    static_configs:
      - targets: [localhost]
        labels:
          job: orbibot
          __path__: /var/log/orbibot/*.log
    pipeline_stages:
      - json:
          expressions:
            robot_id: robot_id
            level:    level
            logger:   logger
      - labels:
          robot_id:
          level:
          logger:
```

### 4. ROS2 Bag Rotation and Management

```python
# scripts/bag_manager.py — automatic ROS2 bag rotation
"""
Manages ROS2 bag recording with:
- Time-based rotation (new bag every N minutes)
- Disk quota enforcement
- Remote upload to NFS or S3
"""
import subprocess
import time
import os
import shutil
import logging
from pathlib import Path
from datetime import datetime

BAG_DIR        = Path('/data/bags')
MAX_DISK_GB    = 20.0
BAG_DURATION_S = 600       # 10-minute bags
UPLOAD_DIR     = Path('/mnt/fleet-storage/bags')  # NFS mount

log = logging.getLogger(__name__)


def disk_used_gb(path: Path) -> float:
    total, used, free = shutil.disk_usage(path)
    return used / 1e9


def oldest_bag(bag_dir: Path) -> Path | None:
    bags = sorted(bag_dir.glob('*.mcap'), key=lambda p: p.stat().st_mtime)
    return bags[0] if bags else None


def enforce_quota(bag_dir: Path, max_gb: float) -> None:
    """Delete oldest bags until disk usage is below max_gb."""
    while disk_used_gb(bag_dir) > max_gb:
        victim = oldest_bag(bag_dir)
        if victim is None:
            break
        log.warning(f'Quota exceeded: deleting {victim.name}')
        victim.unlink()


def record_bag(bag_dir: Path, duration_s: int, robot_id: str) -> Path:
    """Record a single ROS2 bag for duration_s seconds."""
    stamp   = datetime.now().strftime('%Y%m%d_%H%M%S')
    bag_path = bag_dir / f'{robot_id}_{stamp}'
    bag_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        'ros2', 'bag', 'record',
        '--output', str(bag_path),
        '--storage', 'mcap',
        '--duration', str(duration_s),
        '/scan', '/odom', '/imu/data_raw',
        '/cmd_vel', '/odometry/filtered',
        '/orbibot/system_status',
    ]
    log.info(f'Recording bag: {bag_path}')
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=duration_s + 30)
    if result.returncode != 0:
        log.error(f'Bag recording failed: {result.stderr}')
    return bag_path


def upload_bag(bag_path: Path, upload_dir: Path) -> None:
    """Copy finished bag to shared storage (NFS/CIFS)."""
    if upload_dir.exists():
        dest = upload_dir / bag_path.name
        shutil.copytree(str(bag_path), str(dest), dirs_exist_ok=True)
        log.info(f'Uploaded bag to {dest}')
    else:
        log.warning(f'Upload directory not accessible: {upload_dir}')


def bag_rotation_loop(robot_id: str) -> None:
    """Main rotation loop — run as a systemd service."""
    while True:
        enforce_quota(BAG_DIR, MAX_DISK_GB)
        bag_path = record_bag(BAG_DIR, BAG_DURATION_S, robot_id)
        upload_bag(bag_path, UPLOAD_DIR)
```

```ini
# systemd/orbibot-bags.service
[Unit]
Description=OrbiBot ROS2 Bag Recorder
After=orbibot.service
Requires=orbibot.service

[Service]
Type=simple
User=orbibot
Environment=ROS_DOMAIN_ID=42
ExecStartPre=/bin/bash -c "source /opt/ros/jazzy/setup.bash && source /home/orbibot/robot_ws/install/setup.bash"
ExecStart=/bin/bash -c "source /opt/ros/jazzy/setup.bash && source /home/orbibot/robot_ws/install/setup.bash && python3 /home/orbibot/scripts/bag_manager.py --robot-id ${ROBOT_ID}"
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

### 5. Remote Diagnostics Aggregation

```python
# monitoring/diag_aggregator.py
"""
Subscribes to /diagnostics_agg from all robots (via DDS multicast or rosbridge)
and writes metrics to InfluxDB / pushes alerts to alertmanager.
"""
import rclpy
from rclpy.node import Node
from diagnostic_msgs.msg import DiagnosticArray, DiagnosticStatus
import requests
import json
import time

INFLUX_URL  = 'http://monitoring.local:8086'
INFLUX_ORG  = 'robot-fleet'
INFLUX_BKT  = 'diagnostics'
INFLUX_TOKEN = 'your-influxdb-token'

ALERT_URL   = 'http://monitoring.local:9093/api/v1/alerts'

STATUS_NAMES = {
    DiagnosticStatus.OK:    'ok',
    DiagnosticStatus.WARN:  'warn',
    DiagnosticStatus.ERROR: 'error',
    DiagnosticStatus.STALE: 'stale',
}


class DiagnosticsCollector(Node):
    """Aggregates /diagnostics_agg and forwards to InfluxDB."""

    def __init__(self, robot_id: str):
        super().__init__('diag_collector')
        self._robot_id = robot_id
        self._session  = requests.Session()
        self._session.headers.update({
            'Authorization': f'Token {INFLUX_TOKEN}',
            'Content-Type':  'text/plain',
        })

        self.create_subscription(
            DiagnosticArray,
            '/diagnostics_agg',
            self._diag_cb,
            10
        )
        self.get_logger().info(f'Diagnostics collector started for {robot_id}')

    def _diag_cb(self, msg: DiagnosticArray) -> None:
        lines = []
        alerts = []

        for status in msg.status:
            level_name = STATUS_NAMES.get(status.level, 'unknown')
            # InfluxDB line protocol
            lines.append(
                f'robot_diagnostics,robot_id={self._robot_id},'
                f'component={status.name.replace(" ", "_")}'
                f' level={status.level}i,status_name="{level_name}"'
                f' {int(time.time() * 1e9)}'
            )
            # Raise alert for ERROR or STALE
            if status.level >= DiagnosticStatus.ERROR:
                alerts.append({
                    'labels': {
                        'alertname':  'RobotComponentFailed',
                        'robot_id':   self._robot_id,
                        'component':  status.name,
                        'severity':   level_name,
                    },
                    'annotations': {
                        'summary': status.message,
                    },
                })

        if lines:
            self._write_influx('\n'.join(lines))

        if alerts:
            self._send_alerts(alerts)

    def _write_influx(self, payload: str) -> None:
        try:
            self._session.post(
                f'{INFLUX_URL}/api/v2/write?org={INFLUX_ORG}&bucket={INFLUX_BKT}',
                data=payload,
                timeout=2.0
            )
        except requests.RequestException as e:
            self.get_logger().warn(f'InfluxDB write failed: {e}',
                                   throttle_duration_sec=30.0)

    def _send_alerts(self, alerts: list) -> None:
        try:
            self._session.post(ALERT_URL, json=alerts, timeout=2.0)
        except requests.RequestException as e:
            self.get_logger().warn(f'Alert send failed: {e}',
                                   throttle_duration_sec=30.0)
```

```json
// infrastructure/grafana/dashboards/fleet_overview.json (excerpt)
{
  "title": "Robot Fleet Overview",
  "panels": [
    {
      "title": "Fleet Health Status",
      "type": "stat",
      "targets": [{
        "expr": "count(robot_diagnostics{level=\"0\"}) by (robot_id)",
        "legendFormat": "{{robot_id}} OK"
      }]
    },
    {
      "title": "CPU Temperature",
      "type": "timeseries",
      "targets": [{
        "expr": "robot_system_temp_celsius",
        "legendFormat": "{{robot_id}}"
      }]
    },
    {
      "title": "Active Alerts",
      "type": "alertlist"
    }
  ]
}
```

### 6. CI/CD Pipeline for Robot Software

```yaml
# .github/workflows/robot_deploy.yml
name: Robot Deployment Pipeline

on:
  push:
    branches: [main]
  workflow_dispatch:
    inputs:
      target_env:
        description: 'Deployment environment (staging/production)'
        default: 'staging'

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    container:
      image: ros:jazzy-ros-base
    steps:
      - uses: actions/checkout@v4

      - name: Install dependencies
        run: |
          apt-get update -q
          rosdep update
          rosdep install --from-paths src --ignore-src -y

      - name: Build workspace
        run: |
          source /opt/ros/jazzy/setup.bash
          colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release

      - name: Run tests
        run: |
          source /opt/ros/jazzy/setup.bash
          source install/setup.bash
          colcon test --packages-skip orbibot_rosmaster_firmware
          colcon test-result --verbose

      - name: Build Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          file: docker/Dockerfile.robot
          push: true
          tags: |
            registry.your-org.com/orbibot:${{ github.sha }}
            registry.your-org.com/orbibot:latest

  deploy-staging:
    needs: build-and-test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/checkout@v4

      - name: Setup SSH key
        run: |
          mkdir -p ~/.ssh
          echo "${{ secrets.ROBOT_SSH_KEY }}" > ~/.ssh/id_ed25519
          chmod 600 ~/.ssh/id_ed25519
          echo "${{ secrets.ROBOT_KNOWN_HOSTS }}" >> ~/.ssh/known_hosts

      - name: Deploy to staging robot
        run: |
          ./scripts/deploy_image.sh staging-robot-01 ${{ github.sha }}

      - name: Run post-deploy tests
        run: |
          pip install pytest requests
          pytest tests/integration/ --robot-host staging-robot-01

  deploy-production:
    needs: deploy-staging
    if: github.event.inputs.target_env == 'production'
    runs-on: ubuntu-latest
    environment: production    # Requires manual approval in GitHub
    steps:
      - uses: actions/checkout@v4

      - name: Install Ansible
        run: pip install ansible

      - name: Deploy to production fleet
        run: |
          ansible-playbook \
            -i inventory/production.ini \
            playbooks/deploy_workspace.yml \
            --extra-vars "image_tag=${{ github.sha }}"
        env:
          ANSIBLE_PRIVATE_KEY_FILE: ~/.ssh/id_ed25519
```

```dockerfile
# docker/Dockerfile.robot — multi-stage, minimal production image
FROM ros:jazzy-ros-base AS builder

WORKDIR /robot_ws

COPY src/ src/
RUN apt-get update -q && \
    rosdep update && \
    rosdep install --from-paths src --ignore-src -y && \
    . /opt/ros/jazzy/setup.sh && \
    colcon build \
      --symlink-install \
      --cmake-args -DCMAKE_BUILD_TYPE=Release \
      --packages-skip orbibot_rosmaster_firmware && \
    rm -rf build/ log/

# ---- Runtime image ----
FROM ros:jazzy-ros-base AS runtime

COPY --from=builder /robot_ws/install /robot_ws/install

RUN apt-get update -q && apt-get install -y --no-install-recommends \
    python3-smbus2 python3-serial python3-numpy && \
    rm -rf /var/lib/apt/lists/*

ENV ROS_DOMAIN_ID=42

HEALTHCHECK --interval=10s --timeout=5s --start-period=30s --retries=3 \
  CMD curl -sf http://localhost:9090/health | python3 -c \
      "import sys,json; d=json.load(sys.stdin); sys.exit(0 if d['healthy'] else 1)"

COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
```

```bash
#!/bin/bash
# docker/entrypoint.sh
set -e
source /opt/ros/jazzy/setup.bash
source /robot_ws/install/setup.bash
exec ros2 launch orbibot_bringup robot.launch.py "$@"
```

### 7. Configuration Management: Per-Robot Params and Fleet Defaults

```yaml
# config/fleet_defaults.yaml — merged base for all robots
hardware:
  serial_port: /dev/motordriver
  baudrate: 921600
  cmd_timeout: 0.5

navigation:
  max_vel_x: 0.5
  max_vel_y: 0.5
  max_vel_theta: 1.9
  inflation_radius: 0.55

logging:
  level: INFO
  bag_rotation_minutes: 10
  max_bag_storage_gb: 20
```

```yaml
# config/robots/robot-alpha.yaml — overrides for specific robot
robot_id: alpha
location: warehouse_a

hardware:
  # Alpha has LiDAR on /dev/ttyUSB1 (different from default)
  lidar_port: /dev/ttyUSB1

navigation:
  # Alpha navigates a tighter space
  max_vel_x: 0.3
  inflation_radius: 0.45
```

```python
# orbibot_bringup/config_loader.py
"""
Merge fleet defaults with per-robot overrides.
Load order: fleet_defaults.yaml → robots/{robot_id}.yaml → env vars
"""
import yaml
import os
from pathlib import Path

CONFIG_DIR = Path('/home/orbibot/config')


def deep_merge(base: dict, override: dict) -> dict:
    """Recursively merge override into base. Override wins on conflicts."""
    result = dict(base)
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def load_robot_config(robot_id: str | None = None) -> dict:
    """Load merged configuration for this robot."""
    if robot_id is None:
        robot_id = os.environ.get('ROBOT_ID', 'default')

    defaults_path = CONFIG_DIR / 'fleet_defaults.yaml'
    robot_path    = CONFIG_DIR / 'robots' / f'{robot_id}.yaml'

    with open(defaults_path) as f:
        config = yaml.safe_load(f)

    if robot_path.exists():
        with open(robot_path) as f:
            robot_config = yaml.safe_load(f) or {}
        config = deep_merge(config, robot_config)

    # Environment variable overrides (e.g., ORBIBOT_NAVIGATION__MAX_VEL_X=0.2)
    for key, value in os.environ.items():
        if key.startswith('ORBIBOT_'):
            parts = key[8:].lower().split('__')
            node = config
            for part in parts[:-1]:
                node = node.setdefault(part, {})
            node[parts[-1]] = yaml.safe_load(value)

    return config
```

### 8. Security: Remote Access and Certificate Management

```bash
#!/usr/bin/env bash
# scripts/rotate_ssh_keys.sh — rotate SSH keys across fleet
set -euo pipefail

INVENTORY="inventory/robots.ini"
NEW_KEY_FILE="/tmp/new_robot_key_$(date +%s)"

echo "==> Generating new ED25519 key pair"
ssh-keygen -t ed25519 -N "" -f "$NEW_KEY_FILE" -C "orbibot-fleet-$(date +%Y%m%d)"

echo "==> Distributing new public key to fleet"
ansible all -i "$INVENTORY" -m authorized_key \
  --args "user=orbibot key='$(cat ${NEW_KEY_FILE}.pub)' state=present"

echo "==> Testing connectivity with new key"
ansible all -i "$INVENTORY" -m ping \
  --private-key "$NEW_KEY_FILE"

echo "==> Removing old keys (keep only the new one)"
ansible all -i "$INVENTORY" -m authorized_key \
  --args "user=orbibot key='$(cat ${NEW_KEY_FILE}.pub)' exclusive=true"

echo "==> Distributing new private key to authorized operators"
# Store in Vault or distribute to operators via secure channel
vault kv put secret/robot-fleet/ssh_key private_key=@"$NEW_KEY_FILE"

rm -f "$NEW_KEY_FILE" "${NEW_KEY_FILE}.pub"
echo "==> Key rotation complete"
```

```yaml
# playbooks/harden_robots.yml — security hardening playbook
---
- name: Harden robot SSH and network access
  hosts: fleet
  become: true
  tasks:
    - name: Disable password authentication
      lineinfile:
        path: /etc/ssh/sshd_config
        regexp: '^#?PasswordAuthentication'
        line: 'PasswordAuthentication no'
      notify: Restart SSH

    - name: Disable root login
      lineinfile:
        path: /etc/ssh/sshd_config
        regexp: '^#?PermitRootLogin'
        line: 'PermitRootLogin no'
      notify: Restart SSH

    - name: Restrict SSH to management VLAN
      ufw:
        rule: allow
        port: '22'
        src: '10.10.0.0/24'   # Management VLAN only

    - name: Allow ROS2 DDS only from robot subnet
      ufw:
        rule: allow
        src: '10.20.0.0/24'   # Robot subnet for DDS multicast

    - name: Block all other inbound
      ufw:
        state: enabled
        policy: deny

    - name: Configure unattended-upgrades for security patches
      copy:
        content: |
          Unattended-Upgrade::Origins-Pattern {
              "origin=Debian,codename=${distro_codename}-security";
              "origin=Ubuntu,codename=${distro_codename}-security";
          };
          Unattended-Upgrade::Automatic-Reboot "false";
        dest: /etc/apt/apt.conf.d/50unattended-upgrades

  handlers:
    - name: Restart SSH
      systemd:
        name: ssh
        state: restarted
```

## Common Patterns

### Pattern 1: Rollback-Safe Rolling Deploy

```bash
#!/usr/bin/env bash
# scripts/rolling_deploy.sh — deploy with automatic rollback on any failure
set -euo pipefail

WORKSPACE_ARCHIVE="${1:?Usage: rolling_deploy.sh <workspace.tar.gz>}"
INVENTORY="${2:-inventory/robots.ini}"
HEALTH_PORT=9090
WAIT_AFTER_DEPLOY=20   # seconds to stabilize

robots=$(ansible-inventory -i "$INVENTORY" --list | python3 -c "
import sys, json
inv = json.load(sys.stdin)
for host in inv['fleet']['hosts']:
    print(inv['_meta']['hostvars'][host]['ansible_host'])
")

for robot_ip in $robots; do
  echo "==> Deploying to $robot_ip"

  # Health check before
  curl -sf "http://${robot_ip}:${HEALTH_PORT}/health" > /dev/null || {
    echo "    SKIP: $robot_ip not healthy before deploy"
    continue
  }

  # Backup, copy, restart
  ssh "orbibot@${robot_ip}" "cp -a ~/robot_ws/install ~/robot_ws/install.bak" || true
  scp "$WORKSPACE_ARCHIVE" "orbibot@${robot_ip}:/tmp/workspace_new.tar.gz"
  ssh "orbibot@${robot_ip}" "
    tar -xzf /tmp/workspace_new.tar.gz -C ~/robot_ws/
    sudo systemctl restart orbibot
    sleep ${WAIT_AFTER_DEPLOY}
  "

  # Health check after
  if curl -sf "http://${robot_ip}:${HEALTH_PORT}/health" > /dev/null; then
    echo "    OK: $robot_ip healthy after deploy"
  else
    echo "    FAIL: $robot_ip unhealthy — rolling back"
    ssh "orbibot@${robot_ip}" "
      cp -a ~/robot_ws/install.bak ~/robot_ws/install
      sudo systemctl restart orbibot
    "
  fi

  sleep 5  # Brief pause between robots
done
echo "==> Rolling deploy complete"
```

### Pattern 2: Fleet Status Dashboard Script

```python
#!/usr/bin/env python3
# scripts/fleet_status.py — print fleet health to terminal
"""
Usage: python3 fleet_status.py --inventory inventory/robots.ini
"""
import argparse
import configparser
import subprocess
import json
import concurrent.futures
import requests
from dataclasses import dataclass


@dataclass
class RobotStatus:
    name: str
    host: str
    ssh_ok:   bool = False
    service:  str  = 'unknown'
    health:   bool = False
    cpu_temp: float = 0.0
    disk_pct: float = 0.0


def check_robot(name: str, host: str, health_port: int = 9090) -> RobotStatus:
    status = RobotStatus(name=name, host=host)

    # HTTP health check
    try:
        resp = requests.get(f'http://{host}:{health_port}/health', timeout=3)
        status.health = resp.status_code == 200 and resp.json().get('healthy', False)
    except Exception:
        status.health = False

    # SSH checks
    def ssh(cmd):
        result = subprocess.run(
            ['ssh', '-o', 'ConnectTimeout=5', '-o', 'StrictHostKeyChecking=no',
             f'orbibot@{host}', cmd],
            capture_output=True, text=True, timeout=8
        )
        return result.stdout.strip() if result.returncode == 0 else None

    svc = ssh('systemctl is-active orbibot')
    if svc is not None:
        status.ssh_ok  = True
        status.service = svc
        temp_str = ssh('cat /sys/class/thermal/thermal_zone0/temp')
        if temp_str:
            status.cpu_temp = int(temp_str) / 1000.0
        disk_str = ssh("df /home/orbibot --output=pcent | tail -1 | tr -d '%'")
        if disk_str:
            status.disk_pct = float(disk_str)
    return status


def print_fleet_status(inventory_path: str) -> None:
    cfg = configparser.ConfigParser(allow_no_value=True)
    cfg.read(inventory_path)

    robots = {}
    for section in cfg.sections():
        if section == 'fleet:vars':
            continue
        for entry in cfg.options(section):
            parts = entry.split()
            if len(parts) >= 2:
                host = dict(p.split('=') for p in parts[1:]).get('ansible_host', parts[0])
                robots[parts[0]] = host

    print(f"\n{'Robot':<15} {'Host':<16} {'Service':<10} {'Health':<8} {'Temp':>6} {'Disk':>6}")
    print('-' * 70)

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        futures = {ex.submit(check_robot, name, host): name
                   for name, host in robots.items()}
        for future in concurrent.futures.as_completed(futures):
            s = future.result()
            health_str = 'OK' if s.health else 'FAIL'
            temp_str   = f'{s.cpu_temp:.0f}°C' if s.cpu_temp else 'N/A'
            disk_str   = f'{s.disk_pct:.0f}%'  if s.disk_pct else 'N/A'
            print(f'{s.name:<15} {s.host:<16} {s.service:<10} {health_str:<8} '
                  f'{temp_str:>6} {disk_str:>6}')
    print()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--inventory', default='inventory/robots.ini')
    args = parser.parse_args()
    print_fleet_status(args.inventory)
```

### Pattern 3: Pre-Deployment Validation Checklist

```python
# scripts/pre_deploy_check.py
"""
Run before any deployment to verify the target robot is ready.
Exit 0 = safe to proceed. Exit 1 = do not deploy.
"""
import sys
import subprocess
import requests
import shutil
import json

ROBOT_HOST   = sys.argv[1] if len(sys.argv) > 1 else 'localhost'
HEALTH_PORT  = 9090
MIN_DISK_GB  = 2.0
MAX_TEMP_C   = 75.0
MIN_BAT_V    = 11.5


def ssh(cmd: str) -> str | None:
    r = subprocess.run(
        ['ssh', '-o', 'ConnectTimeout=5', f'orbibot@{ROBOT_HOST}', cmd],
        capture_output=True, text=True, timeout=10
    )
    return r.stdout.strip() if r.returncode == 0 else None


def check_item(label: str, passed: bool, details: str = '') -> bool:
    icon = 'PASS' if passed else 'FAIL'
    suffix = f' ({details})' if details else ''
    print(f'  [{icon}] {label}{suffix}')
    return passed


checks_passed = True

print(f'\nPre-deployment validation for {ROBOT_HOST}')
print('=' * 50)

# 1. Health endpoint
try:
    resp = requests.get(f'http://{ROBOT_HOST}:{HEALTH_PORT}/health', timeout=5)
    health = resp.json().get('healthy', False)
except Exception as e:
    health = False
checks_passed &= check_item('Health endpoint', health)

# 2. Disk space
disk_raw = ssh("df /home/orbibot --output=avail --block-size=G | tail -1 | tr -dG")
disk_gb = float(disk_raw) if disk_raw else 0.0
checks_passed &= check_item(
    f'Disk space ≥ {MIN_DISK_GB} GB', disk_gb >= MIN_DISK_GB, f'{disk_gb:.1f} GB free'
)

# 3. CPU temperature
temp_raw = ssh('cat /sys/class/thermal/thermal_zone0/temp')
temp_c = int(temp_raw) / 1000.0 if temp_raw else 999.0
checks_passed &= check_item(
    f'CPU temp ≤ {MAX_TEMP_C}°C', temp_c <= MAX_TEMP_C, f'{temp_c:.1f}°C'
)

# 4. Service running
svc = ssh('systemctl is-active orbibot')
checks_passed &= check_item('orbibot service active', svc == 'active', svc or 'N/A')

# 5. Backup slot available
bak = ssh('test -d ~/robot_ws/install.bak && echo yes || echo no')
checks_passed &= check_item('Backup slot available', True, 'bak exists' if bak == 'yes' else 'fresh')

print('=' * 50)
if checks_passed:
    print('All checks passed. Safe to deploy.\n')
    sys.exit(0)
else:
    print('One or more checks FAILED. Aborting deployment.\n')
    sys.exit(1)
```

## Anti-Patterns

### ❌ Deploying to all robots simultaneously

Pushing to the entire fleet at once means a bad build takes down every robot. There is no "healthy" robot to compare against.

```bash
# WRONG — deploys to all robots in parallel
ansible all -i inventory/robots.ini -m copy -a "src=workspace.tar.gz dest=/tmp/"
ansible all -i inventory/robots.ini -m systemd -a "name=orbibot state=restarted"
```

### ✅ Use rolling deployment with serial: 1 and canary validation

```yaml
# CORRECT — one robot at a time, stop on first failure
- name: Deploy
  hosts: fleet
  serial: 1
  max_fail_percentage: 0
  tasks:
    - name: Deploy and validate
      include_tasks: tasks/deploy_and_validate.yml
```

### ❌ No rollback mechanism

Deploying without a backup means any failed update leaves the robot in a broken state indefinitely.

```bash
# WRONG — no backup, no rollback
rsync workspace/ orbibot@robot:/home/orbibot/robot_ws/install/
ssh orbibot@robot "sudo systemctl restart orbibot"
```

### ✅ Always backup before deploy, auto-rollback on health failure

```bash
# CORRECT — backup first, health check after, rollback on failure
ssh orbibot@robot "cp -a ~/robot_ws/install ~/robot_ws/install.bak"
rsync workspace/ orbibot@robot:/home/orbibot/robot_ws/install/
ssh orbibot@robot "sudo systemctl restart orbibot && sleep 15"
curl -sf http://robot:9090/health || {
  ssh orbibot@robot "cp -a ~/robot_ws/install.bak ~/robot_ws/install && sudo systemctl restart orbibot"
  exit 1
}
```

### ❌ Storing secrets in Ansible inventory or playbooks

SSH keys, API tokens, and robot certificates checked into git are a security incident waiting to happen.

```yaml
# WRONG — secret in plain text in playbook
- name: Set API key
  lineinfile:
    path: /etc/orbibot/env
    line: "ANTHROPIC_API_KEY=sk-ant-api03-..."
```

### ✅ Use Ansible Vault or an external secrets manager

```yaml
# CORRECT — secret encrypted with ansible-vault
- name: Set API key from vault
  lineinfile:
    path: /etc/orbibot/env
    line: "ANTHROPIC_API_KEY={{ vault_anthropic_api_key }}"
# vault_anthropic_api_key stored in group_vars/all/vault.yml (encrypted)
# ansible-vault encrypt group_vars/all/vault.yml
```

### ❌ Unstructured log files make fleet-wide debugging impossible

Plain text logs with no robot identifier cannot be searched across a fleet of 10+ robots.

```python
# WRONG — no robot ID, no structure
import logging
logging.info(f'Battery low: {voltage}V')
```

### ✅ Always include robot_id and structured fields

```python
# CORRECT — structured, searchable across fleet
import json, logging
log = logging.getLogger(__name__)
log.info(json.dumps({'event': 'battery_low', 'robot_id': ROBOT_ID, 'voltage': voltage}))
```

### ❌ Health check that only tests TCP connectivity

A process can be listening on a port while completely deadlocked internally.

```bash
# WRONG — only checks that the port is open
nc -z robot-host 9090 && echo "OK"
```

### ✅ Health check that validates actual ROS2 system state

```python
# CORRECT — validates that the ROS2 node graph is alive
def _check_health(self) -> dict:
    # Check that critical topics are publishing
    odom_ok = subprocess.run(
        ['ros2', 'topic', 'hz', '/odom', '--window', '5', '--once'],
        capture_output=True, timeout=5
    ).returncode == 0
    service_ok = subprocess.run(
        ['systemctl', 'is-active', '--quiet', 'orbibot']
    ).returncode == 0
    return {'healthy': odom_ok and service_ok, 'odom': odom_ok, 'service': service_ok}
```

## Configuration Reference

### Ansible Inventory Variables

| Variable | Type | Example | Description |
|----------|------|---------|-------------|
| `ansible_host` | string | `192.168.1.101` | Robot IP address |
| `ansible_user` | string | `orbibot` | SSH username |
| `robot_id` | string | `alpha` | Unique robot identifier |
| `location` | string | `warehouse_a` | Physical deployment location |
| `ros_distro` | string | `jazzy` | ROS2 distribution name |
| `workspace_path` | string | `/home/orbibot/robot_ws` | Path to ROS2 workspace |
| `health_port` | int | `9090` | HTTP health check port |

### Deployment Script Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `WAIT_AFTER_DEPLOY` | `20` | Seconds to wait after restart before health check |
| `MAX_FAIL_PERCENTAGE` | `0` | Ansible: stop fleet deploy if any robot fails |
| `SERIAL` | `1` | Ansible: how many robots to deploy to simultaneously |
| `BACKUP_DIR` | `install.bak` | Backup directory name (relative to workspace) |

### Bag Rotation Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `BAG_DURATION_S` | `600` | Duration of each bag recording (seconds) |
| `MAX_DISK_GB` | `20.0` | Max disk space for bags before deletion |
| `UPLOAD_DIR` | `/mnt/fleet-storage/bags` | Remote storage mount point |

### Health Check Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `health_port` | `9090` | HTTP port for health endpoint |
| `health_timeout_s` | `5` | HTTP request timeout |
| `stabilize_wait_s` | `15` | Wait after restart before first health check |
| `health_retries` | `12` | Number of retries (× `retry_interval`) |
| `retry_interval_s` | `5` | Seconds between health check retries |

## Troubleshooting

| Symptom | Cause | Solution |
|---------|-------|----------|
| `ansible all -m ping` fails | SSH key not on robot, wrong user | Run `ssh-copy-id orbibot@<host>`; verify `ansible_user` in inventory |
| Deployment hangs at rsync | Large workspace, slow network | Use `--compress` flag in rsync; exclude build artifacts with `--exclude` |
| Post-deploy health check times out | systemd takes >15s to start | Increase `WAIT_AFTER_DEPLOY`; check `systemctl status orbibot` for slow startup |
| Rollback fails, robot unrecoverable | Backup was never created | Add pre-task backup before any deploy step; test rollback on staging first |
| Loki not receiving logs | Promtail can't reach Loki, wrong port | Check `promtail-config.yaml` URL; test with `curl http://loki:3100/ready` |
| Diagnostics not appearing in Grafana | Wrong InfluxDB token or bucket name | Verify with `influx query` on the monitoring host; check collector error logs |
| Bag rotation not uploading | NFS mount not present | Check `df -h /mnt/fleet-storage`; add NFS mount check before upload |
| Robot blocked after firewall hardening | Forgot to allow ROS2 DDS port | `ufw allow from 10.20.0.0/24` for DDS multicast subnet; check `ufw status` |
| Docker image pull fails on robot | Registry unreachable from robot subnet | Configure DNS + firewall egress to registry; consider mirroring registry on LAN |
| Secrets visible in Ansible logs | Using `debug` or `-vvv` with vault vars | Use `no_log: true` on tasks handling secrets; avoid `debug` for secret-containing vars |
| SSH key rotation locks out operators | New key not added before old key removed | Always add new key first, verify login, then remove old key in a separate step |
| Fleet config drift | Manual edits on individual robots | Enforce all config via Ansible; set up periodic `ansible-playbook` run in cron |

## Workflow Integration

**Before this skill:**
- `robot-bringup` — configure systemd services and ordered startup that the deployment pipeline manages
- `docker-ros2-development` — build the Docker images that the deployment pipeline pushes
- `robot-bringup` — instrument nodes with `/diagnostics` before aggregating them centrally

**After this skill:**
- `safety-systems` — validate safety requirements (watchdog, E-stop) are verified in the health check
- `safety-systems` — extend the SSH hardening and firewall rules from this skill with SROS2 and DDS security

**Typical production deployment lifecycle:**
1. Developer merges to `main` → CI builds and tests Docker image
2. Image pushed to registry → CI deploys to staging robot automatically
3. Integration tests run against staging robot
4. Human approves production deploy in GitHub (environment protection)
5. Ansible rolling deploy: backup → rsync → restart → health check → next robot
6. Grafana dashboards confirm all fleet diagnostics are green
7. Bags auto-rotate and upload to shared storage for post-hoc analysis
8. On anomaly: alert fires → engineer SSHes via VPN → inspects logs in Loki
