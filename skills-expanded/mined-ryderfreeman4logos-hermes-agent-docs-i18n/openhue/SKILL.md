---
name: openhue
description: "Control Philips Hue lights, scenes, rooms via OpenHue CLI."
version: 1.0.0
author: community
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Smart-Home, Hue, Lights, IoT, Automation]
    homepage: https://www.openhue.io/cli
prerequisites:
  commands: [openhue]
---

# OpenHue CLI

通过终端，借助 Hue Bridge 控制 Philips Hue 灯具及场景。

## 先决条件

```bash
# Linux (pre-built binary)
curl -sL https://github.com/openhue/openhue-cli/releases/latest/download/openhue-linux-amd64 -o ~/.local/bin/openhue && chmod +x ~/.local/bin/openhue

# macOS
brew install openhue/cli/openhue-cli
```

首次使用时，需按下 Hue Bridge 上的按钮进行配对。该桥接设备必须处于同一局域网内。

## 适用场景

- “打开/关闭灯光”
- “调节客厅灯光的亮度”
- “设置场景”或“电影模式”
- 控制特定的 Hue 房间、区域或单个灯泡
- 调整亮度、颜色或色温

## 常用命令

### 列出资源

```bash
openhue get light       # List all lights
openhue get room        # List all rooms
openhue get scene       # List all scenes
```

### 控制灯光

```bash
# Turn on/off
openhue set light "Bedroom Lamp" --on
openhue set light "Bedroom Lamp" --off

# Brightness (0-100)
openhue set light "Bedroom Lamp" --on --brightness 50

# Color temperature (warm to cool: 153-500 mirek)
openhue set light "Bedroom Lamp" --on --temperature 300

# Color (by name or hex)
openhue set light "Bedroom Lamp" --on --color red
openhue set light "Bedroom Lamp" --on --rgb "#FF5500"
```

### 控制室

```bash
# Turn off entire room
openhue set room "Bedroom" --off

# Set room brightness
openhue set room "Bedroom" --on --brightness 30
```

### 场景

```bash
openhue set scene "Relax" --room "Bedroom"
openhue set scene "Concentrate" --room "Office"
```

## 快速预设

```bash
# Bedtime (dim warm)
openhue set room "Bedroom" --on --brightness 20 --temperature 450

# Work mode (bright cool)
openhue set room "Office" --on --brightness 100 --temperature 250

# Movie mode (dim)
openhue set room "Living Room" --on --brightness 10

# Everything off
openhue set room "Bedroom" --off
openhue set room "Office" --off
openhue set room "Living Room" --off
```

## 备注

- Bridge设备必须与运行Hermes的机器处于同一局域网内。
- 首次使用时，需手动按下Hue Bridge上的按钮进行授权。
- 颜色功能仅适用于支持色彩显示的灯泡（不支持纯白光型号）。
- 灯光名称及房间名称对大小写敏感——可使用`openhue get light`命令查看确切名称。
- 该功能可与cron作业结合使用，实现定时控制灯光亮度（例如睡前调暗灯光，醒来时调亮）。
