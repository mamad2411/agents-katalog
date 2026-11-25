---
name: game-control
description: 使用本机 windows-capture 的受限虚拟 Xbox 手柄和窗口截图能力，执行短时游戏操作、截图并核验状态。适用于用户明确要求控制本机游戏或模拟器时。
license: Apache-2.0
compatibility: Windows 10/11；需要已安装 ViGEmBus，并构建 windows-capture 与 game-control CLI。
allowed_tools: execute
---

# Game Control

使用 `game-control` 操作本机的 `windows-capture` 虚拟 Xbox 360 手柄。它通过同用户 Named Pipe RPC 调用常驻截图工具；不注入进程、不绕过反作弊，也不能把输入限定到某一个窗口。所有可见的 XInput 程序都可能感知虚拟设备。

## 安全边界

- 仅在用户明确要求控制某个本机游戏/模拟器时使用。
- 先调用 `status`，仅在 `available:true` 时继续。
- `press`、`move`、`look` 必须带 `--hold-ms`，取值范围 `1..5000`。禁止拆分或循环命令来规避上限。
- 每个短时操作后优先截图观察结果；不确定状态时先停止，不要猜测和连续输入。
- 在任务结束、错误、切换目标或用户取消时，必须执行 `release-all`。
- 只执行用户明确授权的操作。打开菜单、查看地图、短距离移动是低风险；购买、删除存档、发送消息、联机匹配、修改设置等操作需再次确认。
- 不要控制带反作弊保护的在线游戏；工具不提供规避能力。

## CLI 路径

从仓库根目录设置一次路径：

```powershell
$env:WINDOWS_CAPTURE_EXE = (Resolve-Path 'windows-capture/src/WindowsCapture.App/bin/Release/net8.0-windows10.0.19041.0/windows-capture.exe')
$game = 'windows-capture/src/GameControl.Cli/bin/Release/net8.0/game-control.exe'
```

若 `game-control.exe` 不存在，用 DLL 形式运行：

```powershell
$dotnet = 'C:\Program Files\dotnet\dotnet.exe'
$gameDll = 'windows-capture/src/GameControl.Cli/bin/Release/net8.0/game-control.dll'
```

之后将表中 `& $game ...` 替换为 `& $dotnet $gameDll ...`。

## 命令

| 意图 | 命令 |
|---|---|
| 查看手柄服务 | `& $game status` |
| 把游戏窗口置前 | `& $game focus` |
| 创建虚拟手柄 | `& $game connect` |
| 释放全部按键和摇杆 | `& $game release-all` |
| 移除虚拟手柄 | `& $game disconnect` |
| 短按按钮 | `& $game press --button view --hold-ms 80` |
| 短时移动 | `& $game move --direction forward --hold-ms 400` |
| 短时转视角 | `& $game look --x 0.4 --y 0 --hold-ms 150` |
| 短时按住扳机（举盾 / 瞄准） | `& $game trigger --side left --value 255 --hold-ms 400` |
| 单张截图并落盘 | `& $game screenshot --count 1 --start-delay-ms 0 --output-dir .\work\game-control\shots` |

按钮白名单：`a`、`b`、`x`、`y`、`dpad-up`、`dpad-down`、`dpad-left`、`dpad-right`、`left-bumper`、`right-bumper`、`left-stick`、`right-stick`、`menu`、`view`。

## 观察-操作循环

每次最多一个短操作，然后截图验证：

```powershell
& $game connect
& $game focus
& $game press --button view --hold-ms 80
& $game screenshot --count 1 --start-delay-ms 0 --output-dir .\work\game-control\shots
# 读取写入目录的 PNG，判断地图或位置是否出现。
& $game release-all
```

发送输入前先执行 `& $game focus`：窗口失焦时手柄输入会被忽略，表现为「命令成功但游戏毫无反应」。

有些操作必须**按住**而不是点按，例如游戏里的快捷菜单（按住的期间才显示，松开即消失）、举盾、瞄准。这类操作把 `--hold-ms` 放大到 600–1500，并在按住期间截图确认；`press` 会阻塞到松开，需要「按住的同时截图」时用后台任务发送输入、前台截图。

不要在未观察截图的情况下连续移动。若当前 `windows-capture` 没有有效选中目标，`screenshot` 会报 `target_required`；先由用户通过截图工具 GUI 选择目标窗口。

## 故障处理

| 现象 | 处理 |
|---|---|
| `gamepad_unavailable` | 检查 ViGEmBus 是否已安装、服务是否可用；不要反复重试输入。 |
| `gamepad_duration_exceeded` | 缩短到最多 5000 ms；更长移动必须拆成“移动 → 截图 → 判断”的独立轮次。 |
| 游戏未响应 | 先 `release-all`；确认游戏是否接受 XInput、虚拟设备是否在系统中出现。 |
| 命令成功但游戏无反应 | 目标窗口可能不在前台。先执行 `& $game focus` 再重发；Cemu 在窗口失焦时不接收手柄输入。 |
| 截图失败 | 不再输入，检查目标窗口是否仍有效、未最小化且已由用户选中。 |
| 任意命令异常 | 立即执行 `release-all`，报告错误和最后一个已确认的截图状态。 |
