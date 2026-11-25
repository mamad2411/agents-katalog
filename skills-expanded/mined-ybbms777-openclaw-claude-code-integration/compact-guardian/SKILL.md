---
name: compact-guardian
description: 压缩熔断守护。当 memory-lancedb-pro 自动压缩（auto compaction）连续失败 3 次时，熔断机制触发，停止当前 session 的自动压缩并通过 Telegram 通知用户手动 /compact 处理。在记忆压缩失败后，激活此 skill 进行熔断检查。
---

# Compact Guardian — 压缩熔断守护

## 功能概述

在 `memory-lancedb-pro` 的 `gateway_start` 自动压缩流程中加入熔断保护：

1. **失败计数**：每次 compact 失败 → 调用 `fail` 子命令，计数器 +1
2. **熔断判定**：调用 `guardian` 子命令，count ≥ 3 → `allow: false`，触发熔断
3. **Telegram 通知**：熔断触发时自动发送通知到 Telegram
4. **计数器重置**：手动 `/compact` 成功后 → 调用 `success` 子命令 → 计数器归零

## 工作原理

```
gateway_start compact 失败
  → compact_guardian.py fail "gateway"
      → circuit_state.json sessions["gateway"].failures +1
  → if failures >= 3:
      → notify_telegram.py 发送 Telegram 通知
      → agentEndAutoCaptureHook: checkCompactGuardian() 返回 false
          → 当前 session 停止触发自动压缩
```

## 核心文件

| 文件 | 作用 |
|------|------|
| `scripts/compact_guardian.py` | 熔断状态管理器（计数/查询/重置） |
| `scripts/notify_telegram.py` | Telegram 通知发送器 |
| `~/.openclaw/workspace/skills/compact-guardian/circuit_state.json` | 熔断状态持久化文件 |

## compact_guardian.py 子命令

```bash
# 检查 session 是否被熔断（插件自动调用）
python3 scripts/compact_guardian.py guardian <session_id>
# → {"allow": false, "failures": 3, "tripped": true, "reason": "..."}

# 记录一次压缩失败
python3 scripts/compact_guardian.py fail <session_id> --reason "<错误信息>"
# → {"status": "tripped", "failures": 3, "max_failures": 3, "message": "..."}

# 记录压缩成功（重置计数器）
python3 scripts/compact_guardian.py success <session_id>
# → {"status": "reset", "failures": 0, "was_tripped": true}

# 重置 session 计数器（session 结束时自动清理）
python3 scripts/compact_guardian.py reset <session_id>
```

## 状态文件格式

`~/.openclaw/workspace/skills/compact-guardian/circuit_state.json`:

```json
{
  "sessions": {
    "gateway": {
      "failures": 2,
      "last_failure": "compact error: fragment count exceeded",
      "last_failure_at": 1743696000
    }
  }
}
```

## 熔断后修复步骤

1. 手动执行 `/compact` 修复问题
2. 成功后 `compact_guardian.py success gateway` 自动重置计数器
3. 下次 `gateway_start` 自动压缩正常进行

## 触发条件

- `config.memoryCompaction.enabled: true`（插件配置中启用自动压缩）
- compact 运行时报错（网络/LanceDB/embedding 等任何错误）
- 连续 3 次失败后熔断触发

## 依赖

- Python 3（调用 Telegram API，无需额外库）
- Telegram Bot Token（已配置在 `notify_telegram.py`）
