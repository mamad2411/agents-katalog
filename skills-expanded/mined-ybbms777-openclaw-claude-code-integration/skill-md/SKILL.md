# compact-guardian

## 用途

防止 auto-compact 连续失败导致记忆碎片堆积。

来源：Claude Code 源码泄露中发现的 `MAX_CONSECUTIVE_AUTOCOMPACT_FAILURES = 3` 机制。
原始数据：BQ 记录显示，未加保护的系统每天全球浪费约 25 万次 API 调用。

---

## 安装方式

复制到 `~/.openclaw/workspace/skills/compact-guardian/SKILL.md`，
然后发给你的 OpenClaw：

```
帮我注册 compact-guardian skill 并确认生效，同时在 memory-lancedb-pro 的
auto-capture 钩子里接入熔断逻辑。
```

---

## 熔断逻辑说明

```
auto-compact 触发
    ↓
成功 → 重置计数器
失败 → 计数器 +1
    ↓
计数器 >= 3
    ↓
当前 session 停止触发 auto-compact
发送通知：「压缩已熔断，请手动 /compact」
    ↓
session 结束时重置计数器
```

---

## 验证方法

```bash
openclaw skills list
# 应看到：✓ ready  📦 compact-guardian
```

检查 hooks 配置里是否包含：
- `checkCompactGuardian()` — 启动时检查是否熔断
- `recordGuardianFailure()` — compact 失败时调用
- `recordGuardianSuccess()` — compact 成功时重置计数器

---

## 注意

这个 skill 解决的是**熔断**问题，不是**清理**问题。
记忆碎片的定期清理由 `memory-compaction` skill 负责。
两者配合使用效果最好。
