---
name: google_meet
description: Join a Google Meet call, transcribe live captions, optionally speak in realtime, and do the followup work afterwards. Use when the user asks the agent to sit in on a meeting, take notes, summarize, respond in-call, or action items from it.
version: 0.2.0
platforms:
  - linux
  - macos
metadata:
  hermes:
    tags: [meetings, google-meet, transcription, realtime-voice]
---

# google_meet

## 适用场景

当用户说出以下任意一句话时即可使用该功能：
- “加入我的 Meet 会议，地址为 <url>”
- “为本次会议做记录”
- “总结会议内容并发送后续跟进信息”
- “旁听我的站会”
- “以机器人身份参与此次通话，并在 X 发生时发言”

## 两种模式

| 模式 | 机器人的功能 |
|---|---|
| `transcribe`（默认） | 进入会议，开启字幕功能，并提取会议文字记录。仅支持监听模式。 |
| `realtime` | 与 `transcribe` 功能相同，此外还能通过 OpenAI Realtime 在会议中发言。此时机器人会调用 `meet_say(text)` 函数，其语音将直接从通话中输出。 |

仅当用户确实希望机器人发言时才选择 `realtime` 模式。该模式需要支付实际费用（OpenAI Realtime 按音频分钟计费），并且需要在运行机器人的设备上配置虚拟音频设备。

## 两种部署位置

| 部署位置 | 适用情况 |
|---|---|
| 本地（默认） | Gateway 设备直接运行 Playwright 机器人。 |
| 远程节点（`node="<name>"`） | 机器人在另一台设备上运行，该设备需安装已登录的 Chrome 浏览器，且（对于 `realtime` 模式）还需配置音频桥接功能。当 Gateway 运行在无头 Linux 设备上，而用户的实际 Chrome 浏览器安装在 Mac 上时，此方式非常有用。 |

## 用户需一次性完成的准备事项

最简便的方法是运行内置安装程序：

```bash
hermes plugins enable google_meet
hermes meet install                 # pip deps + Chromium (transcribe only)
hermes meet install --realtime      # + pulseaudio-utils / brew blackhole+ffmpeg
hermes meet auth                    # optional; skips guest-lobby wait
hermes meet setup                   # preflight checks
```

在运行 `sudo apt-get`（Linux系统）或 `brew install`（macOS系统）之前，`hermes meet install --realtime` 会先弹出提示框。若要跳过该提示，可传递 `--yes` 参数。此操作不会更改您的macOS默认输入设置——在开始实时会议之前，您仍需在系统设置中手动选择 BlackHole 2ch。

或者也可以手动操作：
```bash
pip install playwright websockets && python -m playwright install chromium

# For realtime mode, additionally:
#   Linux:  sudo apt install pulseaudio-utils
#   macOS:  brew install blackhole-2ch ffmpeg
#           → System Settings → Sound → Input → BlackHole 2ch
#   Then set OPENAI_API_KEY or HERMES_MEET_REALTIME_KEY in ~/.hermes/.env
```

对于远程节点：
```bash
# on the user's Mac (where Chrome is signed in):
pip install playwright websockets && python -m playwright install chromium
hermes plugins enable google_meet
hermes meet node run --display-name my-mac    # persistent server
# copy the printed token

# on the gateway:
hermes meet node approve my-mac ws://<mac-ip>:18789 <token>
hermes meet node ping my-mac                   # confirm reachable
```

运行 `hermes meet setup` 以预先检查本地的必备条件。

## 工作流程

1. **加入会议** — 调用 `meet_join(url=..., mode=..., node=...)`。该方法会立即返回。
2. **自我介绍** — 不会自动获得同意。在用户正在收听的频道中说明：“有一个 Hermes Agent 机器人正在本次通话中做记录。”
3. **轮询信息** — 使用 `meet_status()` 查看会议是否仍在运行，使用 `meet_transcript(last=20)` 获取最近的文字记录。无需每次都重新读取全部文字记录。
4. **发言（仅限实时模式）** — 使用 `meet_say(text="...")` 将文本放入队列以进行语音合成。语音输出会有约 2 秒的延迟，因此请勿频繁发送语音内容。
5. **离开会议** — 完成后调用 `meet_leave()`，或是在调用 `meet_join` 时设置 `duration="30m"` 以实现自动离开。
6. **后续处理** — 完整读取 `meet_transcript()` 的内容，进行总结，然后使用常规工具发送摘要、记录问题并安排后续跟进。

## 工具参考

| 工具 | 参数 | 用途 |
|---|---|---|
| `meet_join` | `url`, `mode?`, `guest_name?`, `duration?`, `headed?`, `node?` | 启动机器人 |
| `meet_status` | `node?` | 查看会议是否运行及当前进度 |
| `meet_transcript` | `last?`, `node?` | 读取文字记录 |
| `meet_leave` | `node?` | 关闭机器人 |
| `meet_say` | `text`, `node?` | 在实时会议中发言 |

所有工具中的 `node?` 参数：若要操作远程机器人而非本地机器人，可传入已注册的节点名称（或使用 `"auto"` 表示仅使用单个节点）。在本地使用时可省略该参数。

## 重要限制

- 文字记录的质量取决于 Google Meet 的实时字幕功能。其效果偏向英语内容，且当有多人同时发言时会出现失真。
- 客户端模式下的机器人会停留在大厅中，直到主持人允许其加入。请提前告知用户；使用 `hermes meet auth` 可避免此问题。
- **大厅超时**：如果主持人 5 分钟内未允许机器人加入（该时间可通过 `HERMES_MEET_LOBBY_TIMEOUT` 环境变量配置），机器人将自动离开，且 `meet_status` 会返回 `leaveReason: "lobby_timeout"`。
- **每个安装位置每台设备最多只能进行一个活跃会议**。再次调用 `meet_join` 会强制结束当前的会议。
- **不支持 Windows 系统**。
- 实时模式需要虚拟音频设备。如果音频桥接设置失败，机器人将回退到文字记录模式，并在 `meet_status().error` 中标明该状态。
- 使用 `meet_say` 时，发起会议的 `meet_join` 必须设置为 `mode='realtime'` 模式。若在文字记录模式下调用此函数，将会返回明确的错误信息。
- **强行插入发言为尽力而为**。当机器人在生成语音内容时，如果有真实参会者的字幕率先出现，机器人会向 OpenAI Realtime 发送 `response.cancel` 请求。由于字幕显示需要约 500 毫秒，因此在人类打断的最初一秒左右，机器人仍会继续发言。

## 状态字典参考

`meet_status()` 会返回多种状态信息（此处仅展示部分）：

| 键值 | 含义 |
|---|---|
| `inCall` | 已通过大厅阶段。在等待主持人允许加入时为 `False`。 |
| `lobbyWaiting` | 已点击“请求加入”，正在等待主持人响应。 |
| `joinAttemptedAt` / `joinedAt` | 点击大厅入口及实际被允许加入会议的时间戳。 |
| `captioning` | 已安装字幕监听功能。 |
| `transcriptLines` / `lastCaptionAt` | 文字记录的生成进度。 |
| `realtime` / `realtimeReady` | 是否已启用实时模式/是否已连接到 WebSocket。 |
| `realtimeDevice` | 机器人正在使用的音频设备名称（例如 `hermes_meet_src`）。 |
| `audioBytesOut` / `lastAudioOutAt` | OpenAI 会话已生成的 PCM 音频数据量。 |
| `lastBargeInAt` | 最近一次发送 `response.cancel` 请求的时间戳。 |
| `leaveReason` | `duration_expired`、`lobby_timeout`、`denied`、`page_closed`，或为 `null`。 |
| `error` | 最近出现的错误信息（属于轻微错误——机器人可能仍在运行中）。 |

## 文字记录存储位置

本地：
```
$HERMES_HOME/workspace/meetings/<meeting-id>/transcript.txt
```

远程节点：转录内容存储在节点主机的磁盘上。可通过 `meet_transcript(node=...)` 命令利用 RPC 协议读取该内容。

## 安全性说明

- URL 正则限制：仅允许 `https://meet.google.com/...` 格式的地址通过验证。
- 不会扫描日历，也不会自动拨号。
- 远程节点采用承载令牌进行身份认证；这些令牌在节点上生成（长度为 32 个十六进制字符，存储于 `$HERMES_HOME/workspace/meetings/node_token.json` 文件中），需通过 `hermes meet node approve` 命令将其复制到网关。
- `meet_say` 功能发送的文本会受到 OpenAI 实时会话的限制；虽然垃圾信息过滤是机器人的责任而非用户，但仍建议不要一次性发送数百行文本。
