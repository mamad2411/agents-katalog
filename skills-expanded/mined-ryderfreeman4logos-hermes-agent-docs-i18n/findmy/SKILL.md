---
name: findmy
description: "Track Apple devices/AirTags via FindMy.app on macOS."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [FindMy, AirTag, location, tracking, macOS, Apple]
---

# 查找我的（Apple）

通过 macOS 上的 FindMy.app 来追踪 Apple 设备及 AirTags。由于 Apple 并未为 FindMy 提供命令行接口，因此该技能通过 AppleScript 打开该应用，并借助屏幕截图功能来获取设备位置信息。

## 先决条件

- 已安装 FindMy 应用且已登录 iCloud 的 **macOS** 系统
- 设备/AirTags 已在 FindMy 中完成注册
- 终端需具备屏幕录制权限（系统设置 → 隐私与安全性 → 屏幕录制）
- **非必需但推荐**：为提升界面自动化效果，可安装 `peekaboo` 工具：
  `brew install steipete/tap/peekaboo`

## 适用场景

- 用户询问“我的[设备/宠物/钥匙/包]在哪儿？”
- 追踪 AirTag 的位置
- 查看 iPhone、iPad、Mac、AirPods 等设备的位置
- 长时间监测宠物或物品的移动轨迹（如 AirTag 的巡逻路线）

## 方法一：AppleScript + 屏幕截图（基础版）

### 打开 FindMy 并导航至目标设备

```bash
# Open Find My app
osascript -e 'tell application "FindMy" to activate'

# Wait for it to load
sleep 3

# Take a screenshot of the Find My window
screencapture -w -o /tmp/findmy.png
```

接着使用 `vision_analyze` 功能来读取截图内容：
```
vision_analyze(image_url="/tmp/findmy.png", question="What devices/items are shown and what are their locations?")
```

### 在标签页之间切换

```bash
# Switch to Devices tab
osascript -e '
tell application "System Events"
    tell process "FindMy"
        click button "Devices" of toolbar 1 of window 1
    end tell
end tell'

# Switch to Items tab (AirTags)
osascript -e '
tell application "System Events"
    tell process "FindMy"
        click button "Items" of toolbar 1 of window 1
    end tell
end tell'
```

## 方法二：Peekaboo UI自动化（推荐）

如果已安装`peekaboo`，可使用它来实现更可靠的UI操作：

```bash
# Open Find My
osascript -e 'tell application "FindMy" to activate'
sleep 3

# Capture and annotate the UI
peekaboo see --app "FindMy" --annotate --path /tmp/findmy-ui.png

# Click on a specific device/item by element ID
peekaboo click --on B3 --app "FindMy"

# Capture the detail view
peekaboo image --app "FindMy" --path /tmp/findmy-detail.png
```

接着使用视觉功能进行分析：
```
vision_analyze(image_url="/tmp/findmy-detail.png", question="What is the location shown for this device/item? Include address and coordinates if visible.")
```

## 工作流：随时间追踪 AirTag 的位置

用于监控 AirTag（例如追踪猫咪的活动路线）：

```bash
# 1. Open FindMy to Items tab
osascript -e 'tell application "FindMy" to activate'
sleep 3

# 2. Click on the AirTag item (stay on page — AirTag only updates when page is open)

# 3. Periodically capture location
while true; do
    screencapture -w -o /tmp/findmy-$(date +%H%M%S).png
    sleep 300  # Every 5 minutes
done
```

首先利用视觉分析功能对每张截图进行解析，提取其中的坐标信息，进而规划出最优路线。

## 局限性

- FindMy **不提供 CLI 或 API 接口**，必须通过界面自动化方式操作
- AirTags 仅会在 FindMy 页面处于活跃显示状态时更新位置信息
- 位置定位的精确度取决于 FindMy 网络中附近的苹果设备数量
- 拍摄截图需要获得屏幕录制权限
- AppleScript 界面自动化功能在不同版本的 macOS 上可能会出现兼容性问题

## 规则

1. 在追踪 AirTags 时，需确保 FindMy 应用始终处于前台运行状态——若将其最小化，位置更新将会停止
2. 应使用 `vision_analyze` 函数来读取截图内容，切勿尝试直接解析像素数据
3. 对于需要持续追踪的场景，建议通过定时任务定期抓取并记录设备位置
4. 需尊重用户隐私，仅可追踪用户自己拥有的设备或物品
