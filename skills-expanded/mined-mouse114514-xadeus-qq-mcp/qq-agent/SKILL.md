---
name: qq-agent
description: QQ MCP bot — auto-wake on message, manage pending to prevent duplicate wakes, reply via send_message/send_image/send_voice then unlock. Use when interacting with QQ MCP, managing wake rules, or debugging QQ bot workflows.
---

# QQ MCP Agent

## 架构

```
QQ → NapCat (OneBot v11) → WebSocket(:3001) → MCP Server (Python) → opencode
                                                             ↓
                                                     wake_rules.json (持久化)
```

- NapCat 通过 WebSocket(`ws://127.0.0.1:3001`) 推送消息
- HTTP API(`http://127.0.0.1:3000`) 用于发送消息、获取群/好友列表等
- 同一个 `ContextManager` 同时处理 WebSocket 消息推送和 MCP 工具调用

---

## 唤醒系统 (Auto-Wake)

QQ 消息到达时自动激活 opencode 窗口并粘贴唤醒消息。

### 规则

- 规则通过 `add_wake_rule` 添加，持久化到 `src/qq_agent_mcp/wake_rules.json`
- 规则条件：`target_type`(group/private)，`target_id`(可选)，`keywords`(可选)
- 启动时自动从 `wake_rules.json` 加载

### ⚠️ Pending 管理

- **自动上锁：** 消息匹配规则触发唤醒时，系统自动设 `_pending = True`
- **你只需解锁：** 处理完成后调 `set_wake_pending(False)` 允许下次唤醒
- 如果 pending 保持 True 太久，用户后续消息全都不会唤醒你

### 唤醒格式

```
[MCP] {target_id} {完整消息内容}
```

**没有截断。** 消息内容原样粘贴到 opencode 输入框。你需要自行通过 `get_recent_context` 获取全量上下文。

---

## 对话流程

```
用户发消息 → WakeMonitor 检测到 → 自动上锁 → 粘贴唤醒消息 → agent 开始工作
    ↓
1. get_recent_context()                          ← 读取完整上下文
2. send_message() / send_image() / send_voice()  ← ⚠️ 用 QQ MCP 回复用户
3. set_wake_pending(False)                       ← 允许下次唤醒
    ↓
等待下一条消息

---

## MCP 工具一览

### 消息
| 工具 | 说明 |
|------|------|
| `send_message` | 发文本消息。`wait_reply=True` 会自动等待回复 |
| `send_image` | 发图片（base64） |
| `send_voice` | 发语音（base64） |
| `wait_for_reply` | 手动等待新消息（最多 300s） |

### 上下文
| 工具 | 说明 |
|------|------|
| `get_recent_context` | 查看目标最近消息 |
| `batch_get_recent_context` | 批量查看多个目标 |
| `compress_context` | 压缩消息缓存（释放内存） |
| `screenshot_chat` | 生成 QQ 风格聊天截图 |

### 唤醒管理
| 工具 | 说明 |
|------|------|
| `add_wake_rule` | 添加唤醒规则 |
| `list_wake_rules` | 列出规则 |
| `remove_wake_rule` | 删除规则 |
| `set_wake_enabled` | 启用/禁用规则 |
| `set_wake_pending` | ⚠️ 设置 pending 状态（重要！） |
| `diagnose_wake` | 查看唤醒监控状态 |
| `test_wake_activation` | 手动触发唤醒测试 |

### 其他
| 工具 | 说明 |
|------|------|
| `check_status` | 查看 QQ 连接状态 |
| `get_group_list` | 群列表 |
| `get_friend_list` | 好友列表 |

---

## 关键原则

1. **必须用 QQ MCP 回复用户。** 唤醒消息是粘贴到 opencode 的输入框，不代表你已经回复了。要调 `send_message`（或 `send_image`/`send_voice`）把结果发回 QQ。
2. **只需解锁。** pending 在唤醒时自动上锁，做完工作后调 `set_wake_pending(False)` 即可。
3. **一定要解锁。** 处理完不调 `set_wake_pending(False)`，用户后续消息全都会被吞。
3. **不要截断。** 唤醒消息是全量内容，但你应该用 `get_recent_context` 拿完整上下文，因为唤醒消息只有单条，用户可能发了多条。
4. **消息不会被吞。** pending 期间的消息会正常入 buffer，你解锁后用 `get_recent_context` 能看到全部。
5. **`send_message` 默认 `wait_reply=True`**，意为发完消息后阻塞等待用户回复。如果你不需要等，显式设 `wait_reply=False`。
6. **沉默消息不要调用工具。** 规则检测到 `[沉默]` 时 send_message 会拒绝，不要发送沉默内容到 QQ。
7. **如果发送失败，检查 target_type。** 私聊必须指定 `target_type="private"`，默认是 `"group"`。

---

## 持久化

- 唤醒规则 → `wake_rules.json`，每次增删改自动写入
- 消息缓存 → 内存（ContextManager），可调用 `compress_context` 压缩
- 重启后规则自动加载，但消息 buffer 会清空
