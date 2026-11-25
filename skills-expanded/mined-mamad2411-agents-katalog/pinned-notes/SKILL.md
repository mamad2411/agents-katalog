---
name: pinned-notes
description: 显式标记当前对话中需要永久保留的关键事实（必要开支、风险偏好、核心约束等），让它在 session compact/rollover 后仍存活。Agent 主动判断"哪些信息长期重要"调用，跨 session 通过 6 字符短 pin_id 引用。单 session 上限 25 条。
triggers:
  - 记下来
  - 帮我记住
  - 帮我 pin
  - 这条很重要
  - 别忘了
  - 必要开支
  - 风险偏好
  - remember
  - pin
  - unpin
scope: main
---

# Pinned Notes — 抗 Compact 失忆

## 用途与边界

Session 长时间运行后会触发 rollover/compact，LLM 自己整理摘要时**很容易丢失**用户主动陈述的关键约束（必要开支、风险偏好、不可违反的硬规则）。Pinned notes 是 agent 主动 pin 的"机械保留"机制——rollover 时这些 chunks **无视压缩边界全部带过去**，且通过 stable pin_id 在跨 session 后仍能引用。

**什么时候用**：
- 用户**明确陈述**了未来必须记住的事实（"我每月必要开支 8K"、"风险偏好稳健，不接受 20% 以上回撤"）
- 用户**强调要记住**（"这点很重要，别忘了"）
- 决策路径上的硬约束（"这个项目永远不用 Vue"、"不能在交易日提交订单前不刷新数据"）

**什么时候不用**：
- 普通对话内容（已在 chunks 历史中，不需要额外标记）
- 短期上下文（即将切换话题/任务结束就过期的信息）
- 你猜测可能重要但用户没强调

**滥用代价**：单 session 上限 25 条。超过会 hard fail（返回 pin_limit_reached），届时必须 consolidate 合并旧条目才能继续 pin。

## 工具

### `remember(content)` — 新建 pinned note

```
content: string  // 整理后的事实（用第三人称，自包含，不依赖上下文）
```

**返回成功**：
```json
{"ok": true, "pin_id": "7xK2pq", "remaining_slots": 24}
```

**返回上限错误**：
```json
{
  "ok": false,
  "error": "pin_limit_reached",
  "pinned_notes": [{"pin_id": "...", "content_preview": "...", "created_at": ...}, ...]
}
```

收到上限错误时不要重试 remember，先调 `consolidate_pinned` 合并或 `unpin` 释放。

### `consolidate_pinned(old_pin_ids, new_content)` — 合并多条

把 N 条已有 pinned 合并成 1 条新 pinned（占新 slot，net -N+1 释放）。
旧条目的 `is_pinned` 被设为 0（chunks 保留为对话历史，但不再 pinned）。

```
old_pin_ids: string[]  // 要合并的 pin_id 数组
new_content: string    // 合并后的新事实（重新整理，不简单堆叠）
```

合并后返回新的 `pin_id`（不复用旧 id）。

### `unpin(pin_id)` — 单条取消

当用户明确说"那条不要了/已过时"时使用。

```
pin_id: string
```

## Pinned content 格式

工具内部把 content 包装成 `[📌 #PINID] {content}` 写入 chunks 表。LLM 在未来 session 历史里看到这种格式时**直接当用户陈述对待**，pin_id 是稳定可引用的标识。

## 跨 session 行为

- Rollover/Fork 时所有 active pinned chunks **强制保留**，新 session 仍带 `is_pinned=1` + 同一 `pin_id`
- LLM 在新 session 看到 "[📌 #ABC123] 必要开支 8K" 即明确这是从父 session 继承的 pinned 事实
- 想 unpin 时用同一个 pin_id（不会失效）

## 设计原则提醒

Pin 是**用户陈述事实的固化**，不是 agent 总结或推论。Agent 整理 content 时要尽量保留用户原话语义，不要过度抽象或加自己的解读。
