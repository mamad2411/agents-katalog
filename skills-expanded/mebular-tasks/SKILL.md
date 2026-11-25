---
name: mebular-tasks
description: 通过 Mebular MCP 的任务面把活派给别的设备上的 Agent：任务树/DAG 派生、协商、进度跟踪、配额与公平准入。
whenToUse: 需要把活派给别的设备上的 Agent、跨设备协作、子任务分解、与其它 Agent 协商、看任务进度时。
---

# Mebular Tasks

任务面与记忆面**共用同一个 MCP 入口**（`mebular mcp` / HTTP `/mcp`，29 工具中的 16 个 `task_*`/`chatter_*`/`board_create`）。
任务与记忆共用同一条加密记忆通道传输，但**任务不是记忆**（见 §6）。

## 1. 何时派活（而不是自己做）

派活，当且仅当：活需要**另一台设备**上的能力/数据（如某台机器的本地文件、某 Agent 的专属工具），或需要**并行/长期**
执行而本机不适合占用。反之自己做：一次性、纯本机、无跨设备价值的工作——派活有传输与订阅成本。

判定要点：`task_targets` 里出现合适对象 → 派；没有任何对象 → 先解决订阅/发现，而不是硬发。

## 2. `task_submit` 字段语义（root 或 child）

| 字段 | 语义 |
|---|---|
| `intent` | 必填。要做什么（自然语言，写给执行方 Agent 看）。 |
| `to` | 必填。`{ device, agent }`：目标设备与目标 Agent（Agent 名来自对方目录，见 `task_targets`）。 |
| `payloadRef` | 可选。大负载的**引用**（如记忆节点 id / 文件路径），避免把负载塞进任务体。 |
| `expiresAt` | 可选。过期时间（epoch ms）；过期后不再作为有效任务推进。 |
| `causedBy` | 可选。把本任务挂到**上游事件/任务**上（因果关系可追溯）。 |
| `chain` | 可选。链上祖先列表（协助防环与审计；链长上限由预算强制）。 |
| `budget` | 可选（仅 root）。`{ maxDepth, maxChildren, maxTasks }`：子任务派生预算。 |
| `dispatch` | 可选（仅 root）。`children-ok`（默认可派生）或 `root-only`（禁止派生）。 |

示例（把「整理会议记录」派给 device-B 的 writer）：

```json
{ "intent": "把本周会议记录整理成纪要并回传要点", "to": { "device": "device-B", "agent": "writer" },
  "payloadRef": "<memory-node-id>", "budget": { "maxDepth": 2, "maxChildren": 5, "maxTasks": 20 } }
```

## 3. 跟踪进度

- `task_status`：单个任务的状态/尝试次数/最近事件。
- `task_children`：某个任务的子任务（树/DAG 展开）。
- `task_summarize`：子树摘要（快速看整体做完没）。
- `task_subscribe`：订阅事件（后续推进以事件送达，不必轮询）。
- `task_list` / `task_history`：本机视角的任务清单与历史事件。

## 4. 协作三形态与配额

1. **DAG 派生**：子任务经 `causedBy`/`chain` 挂在父任务下（受 `budget` 与链长上限约束）。
2. **协商**（`task_negotiate`）：与对端 Agent 就范围/代价/交付达成一致后再提交。
3. **轻量沟通**（`chatter_send` / `chatter_inbox`）：无需建任务的短消息。

配额与建板：`task_quota`（本机对每设备的本地记账与上限）· `task_targets`（可派对象）· `board_create`（建板 = 建域 +
双方订阅）。

## 5. 失败处理与非幂等

- `task_retry`：重试失败任务；`task_cancel`：取消。
- **`task_submit` 非幂等**：重复提交 = **新任务**（不会去重）。网络超时后重发前，先 `task_list`/`task_history`
  确认是否已受理；需要关联同一意图时用 `causedBy`/`chain` 串起来。

## 6. 与记忆面的边界

- 任务面是**树/DAG + 事件流**（`task_*` 事件）；记忆面是**类型化图**（fact/episode/skill/...）。
- 任务经**记忆通道传输**（同一加密会话），但**不是记忆**：不要把任务当成记忆去 `memory_query`，也不要把
  「派活」写进记忆节点。
- 结果交付：执行方把**结果引用**（`payloadRef`/结果事件）回传；需要长期留存的知识再显式写入记忆面。

## 7. 发现：我能派给谁

`task_targets` = **订阅任务域的对端 ∩ 对方 Agent 目录**（返回 `{ device, agent }` 列表）。没有出现的目标**不要**试着
绕道派活（不会成功，且是越权）。

## 8. 红线（自动机制，不得绕过）

- **预算递减**：子任务预算从父任务扣减，`maxTasks/maxChildren/maxDepth` 越界即被拒。
- **链长上限**：`chain` 过长会被拒（防无界递归）。
- **公平准入**：配额与本地记账由系统强制，Agent 不得伪造/复用他人配额。
- 不要试图在 `payloadRef` 里夹带凭据/密钥；身份与订阅由包层负责，任务体不是权限通道。

CLI 等价（同一 handler）：`mebular task_submit` / `fleet task_submit`（同名同参），便于脚本与非 MCP 场景。
