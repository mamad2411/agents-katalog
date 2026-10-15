---
name: yunji_agv
description: Cloud-based AGV chassis control skill for Yunji robots using WATER API
---

# Yunji AGV Skill

云迹底盘AGV控制Skill，基于WATER（水滴）软件API v1.8.9，支持移动控制、遥控、点位管理等完整功能。

## Quick Start

### 1. Connect to AGV

```python
from yunji_agv import create_skill

# Create skill instance
skill = create_skill({
    "host": "192.168.10.10",  # AGV IP
    "port": 31001,            # TCP port
    "timeout": 5
})

# Initialize connection
skill.initialize()
```

### 2. Get Robot Status

```python
# Get full status
status = skill.get_status()
print(f"Battery: {status['power_percent']}%")
print(f"Status: {status['move_status']}")

# Get current location
location = skill.get_location(distance_threshold=2.0)
```

### 3. Move to Marker

```python
# Move to predefined marker
result = skill.move(marker="room_101")

# Wait for completion
import time
while True:
    status = skill.get_status()
    if status['move_status'] in ['succeeded', 'failed', 'canceled']:
        break
    time.sleep(1)
```

### 4. Joy Control

```python
# Move forward
skill.move_forward(speed=0.3, duration=2.0)

# Turn left
skill.turn_left(speed=0.5, duration=1.0)

# Stop
skill.stop()
```

### 5. Emergency Stop

```python
# Enable estop
skill.estop(enable=True)

# Disable estop
skill.estop(enable=False)
```

### 6. Disconnect

```python
skill.destroy()
```

## API Categories

| Category | Functions |
|----------|-----------|
| **Navigation** | `move()`, `move_cancel()`, `cruise()` |
| **Joy Control** | `move_forward()`, `move_backward()`, `turn_left()`, `turn_right()`, `stop()` |
| **Status** | `get_status()`, `get_location()`, `get_power()` |
| **Markers** | `markers_list()`, `insert_marker()`, `delete_marker()` |
| **System** | `estop()`, `set_led()`, `set_speed()` |

## Network Configuration

- **Default IP**: 192.168.10.10
- **Port**: 31001
- **Protocol**: TCP Socket

## Coordinate System

- **Position**: X, Y in meters (m)
- **Orientation**: Theta in radians (rad)
- **Floor**: Integer floor number

## Move Status

| Status | Description |
|--------|-------------|
| `idle` | Ready for new task |
| `running` | Moving to target |
| `succeeded` | Task completed successfully |
| `failed` | Task failed |
| `canceled` | Task was canceled |
