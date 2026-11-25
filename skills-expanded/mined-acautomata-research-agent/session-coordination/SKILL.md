---
name: session-coordination
description: Coordinate inter-session communication — when and why to send messages, how to structure spawned tasks. Message format lives in `send`. Use when a caller must pass a callback session key and full skill prompt to a callee, a callee must promptly report a blocker or material finding, or a task needs inter-session updates before final delivery.
---

# session-coordination - 会话协调

在 caller 与 callee 之间传递可行动信息。它只定义会话通信协议；领域任务、产出结构、wiki 写入和完成门禁仍由调用它的 skill 负责。

## 工具边界

| 目标 | 工具 | 规则 |
| --- | --- | --- |
| 创建独立工作 | `sessions_spawn` | caller 创建；self-spawn 省略 `agentId`。 |
| 回传发现或协调既有会话 | `sessions_send` | 格式细节见 `send`；只向 task 中明确给出的目标发送。 |
| 持久化领域产出 | 备好 md 经 `ingest` 写入 + inline reply | 不用 session key 或文件路径充当产物交接。 |

`timeoutSeconds: 0` 表示非阻塞投递，适合 callee 的即时回传。caller 需要在当前步骤取得回复时，才设置正的 `timeoutSeconds`。

## Caller：创建可回传的子会话

在 `sessions_spawn` 前，取得 caller 当前**可投递的非 thread-scoped** session key，并读取本次调用 skill 的**完整 prompt/正文**。若当前会话 key 以 `:thread:<id>` 结尾，改为取得对应的非 thread-scoped 父会话 key；无法取得时不得启用即时回传，改用 completion 交付。每个 callee task 都必须内联以下内容；不得只提供路径、占位符或“读取某文件”的指令：

```text
<caller_session_key>
<caller 当前可路由的 session key>
</caller_session_key>

<invoked_skill_prompt>
<本次调用 skill 的完整 prompt/正文>
</invoked_skill_prompt>

<work_item>
<具体目标、输入、约束、预期最终交付>
</work_item>

<reporting_protocol>
出现 blocker、需要 caller 决策、已验证的关键发现或会改变后续工作的结论时，立刻用 sessions_send 向 caller_session_key 发送一条简短结构化回传（格式见 `send`）。没有可行动的新信息时继续工作，不发送进度噪声。最终仍按 work_item 返回完整交付或具体失败原因。
</reporting_protocol>
```

- `caller_session_key` 仅是即时回传地址，不是领域产物、授权能力或后续流程的交接接口。
- isolated callee 不共享 caller 的会话记忆；完整 skill prompt、工作项和约束必须随 task 传入。
- caller 为每个 task 设置唯一 `label`。批量 task 全部发出后，调用一次 `sessions_yield`，通过 completion events 汇总；不轮询 `sessions_list` 或 `sessions_history`。
- 子会话不得再 spawn 子会话；当前最大深度为一层。

## Callee：及时回传可行动发现

1. 从 task 中读取 `<caller_session_key>` 与 `<invoked_skill_prompt>`，按该 prompt 和 work item 工作。获取自己当前**可路由的非 thread-scoped** session key（格式为 `agent:main:<id>`，不以 `:thread:<id>` 结尾），作为 `<message from="...">` 属性的发送方标识。
2. 出现下列任一事件时，立即发送**一条短消息**，而不是等到最终回复：
   - 输入缺失、不可读或任务无法继续；
   - caller 必须选择的方案、范围或风险；
   - 已验证且会改变后续工作方向的发现；
   - 关键阶段完成，且 caller 可以据此安排后续工作。
3. 使用 `send` predicate 定义的消息格式调用 `sessions_send`。

4. 最终 reply 仍返回完整交付或明确失败原因；需要持久化的 predicate 产出仍备好 md 经 `ingest` 写入 wiki 并内联返回内容本体。

## 回传门禁

- 只发送可行动的新信息；不发送”仍在处理””继续工作中”等低价值进度。
- 不发送 secrets、无关私人上下文或未经验证的推测。
- 不使用 `watch`，不枚举会话、不读取会话历史，也不把 session key 复制到最终交付中。
- 不向以 `:thread:<id>` 结尾的 thread-scoped session key 发送。
- 收到回传的 caller 自己决定后续工作；callee 不因回传而创建递归会话或无限来回通信。
- 若缺少 caller key、`sessions_send` 被拒绝或投递失败，继续完成可完成的工作，并在最终 reply 明确说明哪条回传未送达；不得声称已通知 caller。
- 消息格式必须遵循 `send` predicate 的要求；`sessionKey` 填 caller key（目标），`<message from="...">` 填 callee own key（发送方）。
- 当前 sandbox 关闭。若未来使用 `sandbox: "require"`，会话可见性被限制到 tree；只有 caller 位于该可见树中时才可依赖此协议。

## 完成门禁

- 每个 spawned task 都含 caller session key、完整调用 skill prompt、完整工作项和唯一 label。
- 每个可行动 blocker / decision / finding / milestone 都已即时回传，或在最终 reply 中报告未送达原因。
- 最终领域交付遵循调用 skill 的 wiki 与 inline reply 规则，未以 session key 或文件路径替代。
- caller 对每个 task 记录成功、失败或超时的唯一终态。
