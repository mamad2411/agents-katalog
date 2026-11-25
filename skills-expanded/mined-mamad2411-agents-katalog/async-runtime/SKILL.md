---
name: async-runtime
description: 需要未来唤醒、后台等待、跨 channel 通知或长期订阅时的调度选择；覆盖 cron、后台 subagent、notification、channel_subscribe、wake_channel。
triggers:
  - 等到
  - 下次
  - 晚点
  - 过几分钟
  - 到时候
  - 完成后
  - 后台
  - 异步
  - 唤醒
  - cron
  - notification
  - wake_channel
  - channel_subscribe
---

# Async Runtime / Future Wakeup

任何依赖未来时点或未来事件的承诺，都必须同时安排可唤醒机制。原则：**能回来继续处理**，而不是依赖 Max 手动重启对话。

## 选择表

| 场景 | 机制 | 说明 |
|---|---|---|
| 固定时间执行一次 | `cron_add` with `at` + `owner:"session"` | 例如今晚 21:00 提醒/检查 |
| 周期性执行（守护类） | `cron_add` with `cron` / `every` | 例如每日扫描、每小时巡检，owner 默认 system |
| 会话自调度闹钟（"10 分钟后看结果"） | `cron_add` + `owner:"session"` | 随目的消亡，完成后必须主动 `cron_remove`；不进健康审计 |
| 静态提醒，无需 agent 推理 | `cron_add` payload `notification` | 直接写通知，不进 agent loop |
| 纯轮询/比对，结果结构化 | `cron_add` payload `script` | 脚本放 `data/cron-tasks/`（自编写）或 `cron-tasks/`（repo），stdout JSON 行写通知，零 token |
| 轮询发现异常后要 agent 接力判断 | `script` + stdout 打 wake 行 | gate→enrich 的 script 形态：门零 token，只在异常路径叫醒 agent；无需发布/重启。两种口味：`{"wake":{"subagent":"任务文本","model":"palette:light"}}` 派一次性隔离 agent（机械诊断/体力活，主口味，告警由脚本自己的 notification 行写出）；`{"wake":{"channel":"web:chat-x","text":"..."}}` 借宿已有 channel（需要上下文连续性或 Max 在场交互） |
| 到点后需要带上下文继续推理 | `cron_add` payload `channel-message` | 注入目标 channel，由 agent 串行处理 |
| 独立长流程，完成后回来处理 | `spawn_subagent` with `run_in_background: true` | 完成时以 framework 消息唤醒发起 channel，不轮询 |
| 长期追踪主题事件 | `channel_subscribe` + producer `notification_create` | 事件发生时按 topic fan-out |
| 跨 channel 通知另一 agent | `wake_channel` | 只传状态层指针和极短摘要；具体内容在 issue/task/memory 等 state layer |

## script 任务协议要点

- **状态文件锚定**：两个合法根目录（`cron-tasks/` 与 `data/cron-tasks/`）相对 `data/` 的几何不同，脚本内写 `../data/x.json` 只对 repo 根成立。一律读 runner 注入的 `MAXCLAW_DATA_DIR`，未注入 fail-loud。`data/cron-tasks/` 自编写脚本复制这 4 行（不要跨根 import repo 的 `cron-tasks/lib/`）：
  ```ts
  const DATA_DIR = process.env.MAXCLAW_DATA_DIR
  if (!DATA_DIR) throw new Error('MAXCLAW_DATA_DIR 未设置（直接调试：MAXCLAW_DATA_DIR=$PWD/data bun <script>）')
  const STATE_PATH = `${DATA_DIR}/my-state.json`
  ```
- **timeoutMs 上限 30min**：payload `timeoutMs` 和 wake 行 `timeoutMs` 超限直接报错，不会被静默压缩——需要更长执行时间说明任务该拆，不该硬撑。
- **`cron_run_now` 防重入**：撞上该 job 正在运行的实例会 throw「正在运行中」，等它跑完再触发。脚本的 read-modify-write 状态文件靠这把锁保护。
- 通知行与 wake 行协议全文见 `src/cron/script-runner.ts` 头注释。

## owner 归属纪律

- **会话给自己设的闹钟**（等构建、等回复、定期检查某个进行中的事）→ `owner:"session"`。它是当前任务的附属物：目的达成后**主动 `cron_remove`**，不留孤儿闹钟。
- **与会话无关的常驻任务**（巡检、订阅、提醒 Max 的长期安排）→ 默认 `owner:"system"`，进健康审计。
- 拿不准时问一句：这个任务是"我这个对话要继续处理的事"，还是"系统该一直做的事"？

## 操作纪律

- 说“稍后/完成后/到时候”之前，先决定唤醒机制并执行。
- 长期服务进程不算唤醒机制；启动 dev server 前先确认并精确清理旧进程。
- 异步任务派发后等待对应机制的通知，不轮询日志；失败通知再读完整日志。
- `notification_create` 用已有 topic；创建新 topic 前先 `topic_list` 避免重复命名。
- `wake_channel` 是门铃，不是跨频道对话；消息只放 pointer + 极短摘要。

## 最小模板

### 固定时间继续处理

1. 计算/确认 ISO 时间。
2. `cron_add({ kind: "at" }, { kind: "channel-message", text: "到点后要执行的具体任务" })`。
3. 告诉 Max 已安排什么时间、会做什么。

### 长流程后台执行

1. 任务可自包含描述且预计耗时长，`spawn_subagent({ ..., run_in_background: true })`。
2. `task` 写清楚目标、数据源、期望产出（子 agent 看不到你的对话上下文）。
3. 完成时框架自动唤醒当前 channel，不轮询；状态核对用 `check_subagents`。详见 skills/subagent/SKILL.md。

### 事件流订阅

1. `topic_list` 查已有 topic。
2. `channel_subscribe` 当前 channel。
3. producer 在事件发生时 `notification_create(topic=...)`。
