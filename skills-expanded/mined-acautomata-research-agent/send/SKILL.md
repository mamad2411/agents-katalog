---
name: send
description: Send a structured inter-session message via sessions_send — single source of truth for the call format, XML message wrapping, and field spec. Triggers: 发送会话消息, 回传结果, 发给上游, sessions_send, 报告 blocker.
---

# send — 会话消息发送

## Mission

作为 `sessions_send` 工具调用的唯一权威来源。定义调用签名、XML 消息包裹格式、STATUS/SUMMARY/EVIDENCE/NEXT 字段规格，以及 `sessionKey` 与 `from` 属性的角色区分。

## When to use

- 当前会话是某个 spawn 出来的子会话（callee），主任务完成或遇到 blocker，需要回传结果给 spawn 它的 caller
- 当前会话是 orchestrator，某个 `paper-batch-ingest` 子流程返回结果，需要把中间状态传给下一个 step 的 callee
- 跨 session handoff 后，新会话需要把 wiki 写入结果或决策需求回报给原会话

不要用于：决定何时发送消息（那是 `session-coordination`）、会话 spawn、会话列举/历史读取。

## 输入

| 参数 | 必需 | 类型 | 描述 |
|------|------|------|------|
| sessionKey | 是 | string | caller 的可路由 session key（发送目标），不以 `:thread:<id>` 结尾 |
| message | 是 | string | 包裹在 `<message>` XML 标签内的结构化文本 |
| timeoutSeconds | 否 | integer | 0 = 非阻塞投递；正值 = 等待回复（默认 0） |

## 消息格式

### XML 包裹

`message` 字符串必须用 `<message>` XML 标签包裹，`from` 属性填 callee 自己的 session key（标识发送方）：

```xml
<message from="<callee_session_key>">
STATUS: blocker | decision_needed | finding | milestone
SUMMARY: <一句话>
EVIDENCE: <必要证据或具体原因>
NEXT: <callee 将继续做什么，或 caller 需要做什么>
</message>
```

注意事项：STATUS / SUMMARY / EVIDENCE / NEXT 四个字段的值可能包含 `&`、`<`、`>` 等 XML 元字符。为避免 XML 解析错误，内联时手动将 `&` 替换为 `&amp;`、`<` 替换为 `&lt;`、`>` 替换为 `&gt;`。如果字段内容较复杂或含结构文本，优先使用 `<![CDATA[...]]>` 包裹该字段以避免转义遗漏。

禁止纯文本或其他格式。`from` 属性必填。

### STATUS 允许值

| 值 | 含义 |
|----|------|
| blocker | 输入缺失、不可读或任务无法继续 |
| decision_needed | 需要接收方决策方案、范围或风险 |
| finding | 已验证且会改变后续工作方向的发现 |
| milestone | 关键阶段完成，可据此安排后续工作 |

### 字段要求

| 字段 | 要求 |
|------|------|
| SUMMARY | 一句话概括 |
| EVIDENCE | 可追溯、可验证的证据或具体原因 |
| NEXT | 可行动——callee 接下来做什么，或 caller 需要做什么 |

### 关键约束

- `sessionKey` = caller 的 session key（目标会话）。
- `<message from="...">` = callee 自己的 session key（发送方）。
- 不向 `:thread:<id>` 结尾的 session key 发送。
- 不发送 secrets、无关私人上下文或未经验证的推测。
- 构造 XML 消息体时，对可变字段内容做 XML 转义（`&` → `&amp;`、`<` → `&lt;`、`>` → `&gt;`），或用 CDATA 包裹结构文本以避免 XML 解析错误。

## 执行流程

1. 取得 caller 的 session key（= `sessionKey` 参数，发送目标）和 callee 自己的 session key（= `from` 属性值，发送方标识）。
2. 按 XML 格式构造 `message`：填充 STATUS、SUMMARY、EVIDENCE、NEXT。
3. 调用 `sessions_send(sessionKey, message, timeoutSeconds)`。
4. 若投递失败，继续完成可完成的工作，在最终 reply 中说明哪条回传未送达。

## 完成门禁

- `message` 使用 `<message>` XML 包裹，`from` 属性存在且正确。
- `sessionKey` = caller key（目标），`from` = callee own key（发送方）。
- STATUS 为四个允许值之一。
- SUMMARY / EVIDENCE / NEXT 均有内容。
