---
name: tool-registry-cce
description: 工具可用性追踪系统。当需要调用任何外部工具、查询工具状态、记录工具调用结果、或判断工具是否可用时，必须使用此技能。跨会话记住工具状态，避免每次盲试。
---

> 来自 [cc-enhance](https://github.com/luochang212/cc-enhance)。`-cce` 后缀表示此技能由 cc-enhance 项目安装，避免与本地同名技能冲突。

# 工具状态追踪

`~/.claude/tool-registry.json` 跨会话记住工具可用性，避免每次盲试。`references/tool-catalog.json` 是常用工具参考样本，提供 invoke 格式和 notes。安装时由 BOOT 脚本扫描本机后动态生成注册表，catalog 中未覆盖的工具也可手动添加。

## 记录格式

每个工具有一个 `history` 对象，保留最近 **1 条**调用记录：

```json
{
  "status": "available",
  "updated": "2026-05-09T18:00:00+08:00",
  "history": {"timestamp": "2026-05-09T18:00:00+08:00", "status": "available", "response_time_ms": 650, "note": "查询 'Claude Code', 3 结果"}
}
```

- `timestamp` — 调用时间
- `status` — 当时的状态（available / rate_limited / unavailable）
- `response_time_ms` — 可选，响应耗时
- `note` — 可选，简要说明

## 自动维护

**只在工具状态变化时写入注册表**：

- **首次验证成功** → 写入 `available` 记录，设置 `updated`
- **失败** → 写入 `unavailable` 记录，更新 `updated`
- **429/额度耗尽** → 记录 `rate_limited`，更新 `updated`
- **后续成功** → 不写入（状态未变，没有信息量）

工具调用失败的那一刻就自己把注册表改了，不要等用户提醒。

## 新鲜度判断

每次会话开始时读注册表。对每个工具：

- `updated` 距今 ≤ 3 天 → **信任**，直接按记录的状态决策
- `updated` 距今 3-7 天 → **信任但警惕**，首次调用时观察结果
- `updated` 距今 > 7 天或不存在 → **重新验证**，用一次轻量调用确认状态

## CLAUDE.md 注入

这是 cc-enhance 中**唯一**会写入用户 `~/.claude/CLAUDE.md` 的内容。写入时必须精确使用以下文本，以 `## 工具可用性` 为锚点：

```markdown
## 工具可用性

查询 `~/.claude/tool-registry.json` 决定工具策略：
- `updated` ≤ 3 天 → 信任，直接用
- `updated` 3-7 天 → 信任但首次调用时观察
- `updated` > 7 天或不存在 → 用轻量调用重新验证

工具调用失败时即刻更新注册表。
```

**绝不在此之外添加其他内容到用户 CLAUDE.md。**

## 环境依赖

| 依赖 | 用途 | 安装方式 | 磁盘 | 必需 |
|------|------|----------|------|------|
| 无 | — | — | — | — |
